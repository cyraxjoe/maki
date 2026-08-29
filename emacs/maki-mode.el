;;; maki-mode.el --- Emacs client for the Maki blog engine -*- lexical-binding: t; -*-

;; Author: Joel Rivera <rivera@joel.mx>
;; Keywords: comm, outlines
;; Package-Requires: ((emacs "29.1"))

;;; Commentary:

;; Editing client for the Maki blogging engine (blog.joel.mx).
;; It talks to the JSON API of the running maki server (digest auth):
;;
;;   (add-to-list 'load-path "/path/to/maki/emacs")
;;   (require 'maki-mode)
;;   (setq maki-host "http://127.0.0.1:8080")
;;   M-x maki-mode
;;
;; Key bindings: C-c f fetch post, C-c n new post; inside a post buffer
;; C-c l set language (new posts), C-c v toggle visibility.  Saving the
;; buffer posts the changes to the server.
;;
;; Historical note: this used to ship with a patched copy of url-auth.el
;; because the digest auth of old Emacsen did not interoperate with
;; CherryPy.  Emacs >= 29 works out of the box, so the patch is gone.

;;; Code:

(require 'url)
(require 'json)
(require 'maki-url-auth)

(defconst maki-mode-version "0.2"
  "Version of `maki-mode'.")

(defgroup maki nil
  "Maki blog engine major mode."
  :group 'comm)

(defcustom maki-host "http://127.0.0.1:8080"
  "Base host url."
  :type 'string
  :group 'maki)

(defcustom maki-debug nil
  "Set to not nil to show debugging messages."
  :type 'boolean
  :group 'maki)

(defcustom maki-post-uri "/posts/"
  "URI to fetch the post content."
  :type 'string
  :group 'maki)

(defcustom maki-banner
  (mapconcat 'identity
             '(
               "    ,;'O@';,    ,;'O@';,    ,;'O@';,  "
               "   |',_@H_,'|  |',_@H_,'|  |',_@H_,'| "
               "   |        |  |        |  |        | "
               "    '.____.'    '.____.'    '.____.'  "
               "        ___  ___        _     _       "
               "        |  \\/  |       | |   (_)      "
               "        | .  . |  __ _ | | __ _       "
               "        | |\\/| | / _` || |/ /| |      "
               "        | |  | || (_| ||   < | |      "
               "        \\_|  |_/ \\__,_||_|\\_\\|_|      "
               "                                      "
               "               Welcome                ") "\n")
  "Text to be displayed at the begining of the maki-mode."
  :type 'string
  :group 'maki)

(defcustom maki-user nil
  "User to be used in the maki server.  If nil ask the user."
  :type '(choice (const :tag "Ask" nil) string)
  :group 'maki)

(defcustom maki-passwd nil
  "Password to be used in the maki server.  If nil ask user."
  :type '(choice (const :tag "Ask" nil) string)
  :group 'maki)

(defcustom maki-def-lang "en"
  "Default language to the new posts."
  :type 'string
  :group 'maki)

(defcustom maki-autolist nil
  "List the content when the mode is invoked."
  :type 'boolean
  :group 'maki)

(defcustom maki-mode-hook nil
  "Hook called by `maki-mode'.  Use this to customize."
  :type 'hook
  :group 'maki)

;; keybinding
(defvar maki-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map "\C-c\ f" 'maki-get-post)
    (define-key map "\C-c\ n" 'maki-new-post)
    map)
  "Local key map to the maki mode.")

(defvar maki-post-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map "\C-c\ l" 'maki-post-set-lang)
    (define-key map "\C-c\ v" 'maki-post-visib-toggle)
    map)
  "Local keymap to the maki-post minor mode.")
;; end of keybinding

(defvar-local maki-post-hash nil
  "Post data (a hash table) of the current post buffer.")

(defvar-local maki-curr-post nil
  "Id of the post being fetched from the main maki buffer.")

;; utilities
(defun maki-chomp (str)
  "Chomp leading and tailing whitespace from STR."
  (while (string-match "\\`\n+\\|^\\s-+\\|\\s-+$\\|\n+\\'"
                       str)
    (setq str (replace-match "" t t str)))
  str)

(defun maki-json-headers ()
  '(("Content-Type" . "application/json; charset=UTF-8")
    ("Accept" . "application/json")))
;;

;; url functions

(defun maki-post-public-url (slug)
  (concat maki-host maki-post-uri slug))

(defun maki-post-url (pid)
  "Return the appropiate URL of the post depending where the
PID is an id, url or slug."
  (let ((baseurl (concat maki-host maki-post-uri)))
    (cond
     ((string-match ".*/posts/\\(.*\\)$" pid) ;; url
      (let ((slug (match-string 1 pid)))
        (concat baseurl slug "?by=slug")))
     ((string-match "^[0-9]+$" pid) (concat baseurl pid)) ;; id
     (t (let ((slug pid)) ;; if is not and id or a url, then is a slug;
          (concat baseurl slug "?by=slug"))))))

(defun maki-post-list-url (&optional category public)
  (let ((pl-url (concat maki-host maki-post-uri))
        (qse ())
        (qs ""))
    (when category (push (cons "category" category) qse))
    (when (and (not (null public)) (numberp public))
      (push (cons "public" (number-to-string public)) qse))
    (if qse (progn
              (dolist (key-val qse)
                (setq qs (concat qs (format "%s=%s&" (car key-val) (cdr key-val)))))
              (setq qs (substring qs 0 (- (length qs) 1))) ;; remove last &
              (concat pl-url "?" qs))
      pl-url)))

(defun maki-post-add-url ()
  (concat maki-host maki-post-uri "add/"))

(defun maki-post-update-url (pid)
  (concat maki-host maki-post-uri "update/" (number-to-string pid)))

(defun maki-visibility-url ()
  (concat maki-host maki-post-uri "visibility"))

;;

(defmacro maki-req-callback (_skey succ-expr _ekey err-expr)
  "Handle an `url-retrieve' callback.
The `:success' and `:error' keywords at the call site are just
place-holders; SUCC-EXPR runs with the parsed JSON bound to
`response', ERR-EXPR runs on request errors.  Both can use the
`status' argument of the enclosing callback."
  `(if (or (null status) (not (plist-get status :error)))
       (let ((response (maki-get-json-response)))
         (if maki-debug (message "%s" response))
         ,succ-expr)
     ,err-expr
     (if maki-debug ;; show the full http response.
         (message "Response buffer: %s"
                  (buffer-substring (point-min) (point-max))))))

(defmacro maki-make-new-posth ()
  `(let ((posth (make-hash-table :test 'equal)))
     (puthash "public" nil posth)
     (puthash "lang" maki-def-lang posth)
     posth))

(defmacro maki-post-id () '(gethash "id" maki-post-hash))
(defmacro maki-post-lang () '(gethash "lang" maki-post-hash))
(defmacro maki-post-is-new () '(null (gethash "id" maki-post-hash)))
(defmacro maki-post-visib () '(gethash "public" maki-post-hash))
(defmacro maki-req-resp (status) `(car (reverse (cadr ,status))))
(defmacro maki-valid-lang? (lang)
  `(and (not (string= ,lang "es"))
        (not (string= ,lang "en"))))

(defun maki-get-post-list (&optional category public)
  (interactive)
  (let ((plist-url (maki-post-list-url category public))
        (cbuffer (current-buffer))
        (url-request-extra-headers (maki-json-headers)))
    (url-retrieve plist-url 'maki-show-post-list `(,cbuffer))))

(defun maki-show-post-list (status mainbuff)
  (let ((json-false nil)
        (json-array-type 'list))
    (ignore json-false json-array-type)
    (maki-req-callback
     :success
     (with-current-buffer mainbuff
       (setq buffer-read-only nil)
       (let* ((postlist response))
         (insert "\n\n\n")
         (insert (propertize "Post list:" 'face 'bold))
         (dolist (post postlist)
           (insert "\n\n")
           (maki-list-insert-post post)))
       (setq buffer-read-only t))
     :error
     (message "Unable to show post list: %s"
              (or (plist-get status :error)
                  (plist-get status :redirect)
                  status)))))

(defun maki-util-open-link (link)
  (lambda (_btn) (browse-url link)))

(defun maki-list-insert-post (post)
  "Insert one post element in a list for the main buffer."
  (let* ((title (propertize (gethash "title" post) 'face 'bold-italic))
         (abstract (propertize (gethash "abstract" post) 'face 'italic))
         (url (maki-post-public-url (gethash "slug" post))))
    (insert (format "  %s %s\n" (propertize "*" 'face 'bold-italic) title))
    (insert (format "    %s\n" abstract))
    (insert "    ")
    (insert-button "[View] " 'action (maki-util-open-link url))
    (insert-button " [Edit]" 'action (lambda (_btn) (maki-get-post url)))))

;;;###autoload
(defun maki-get-post (pid)
  "Fetch the JSON post with the id, url or slug PID from the maki blog."
  (interactive "sPost id|url|slug: ")
  (let ((url-request-extra-headers (maki-json-headers)))
    (if maki-debug
        (message "Fetching '%s' " (maki-post-url pid)))
    (url-retrieve (maki-post-url pid) 'maki-post-show)))

(defun maki-post-save ()
  "Save the changes to the blog post.  Do not ask for confirmation."
  (interactive)
  (let* ((post (make-hash-table))
         (update-url nil))
    (save-excursion
      (puthash "title" (maki-get-current-title) post)
      (puthash "abstract" (maki-get-current-abstract) post)
      (puthash "tags" (maki-get-current-tags) post)
      (puthash "content" (maki-get-current-content) post)
      (puthash "category" (maki-get-current-category) post)
      (puthash "format" "rst" post))
    (if maki-debug
        (message "Posting post hash = %s\njson = %s "
                 post (json-encode post)))
    (if (maki-post-is-new)
        (progn
          (setq update-url (maki-post-add-url))
          (puthash "lang" (maki-post-lang) post))
      (setq update-url (maki-post-update-url (maki-post-id))))

    (let ((cbuffer (current-buffer))
          (url-request-method "POST")
          (url-request-extra-headers (maki-json-headers))
          (url-request-data (json-encode post)))
      (url-retrieve update-url 'maki-post-confirm-save
                    (list cbuffer)))))

(defun maki-post-confirm-save (status postbuff)
  "Check the response of the server and inform the results."
  (ignore status)
  (maki-req-callback
   :success
   (let ((json-false nil)
         (json-object-type 'hash-table))
     (ignore json-false json-object-type)
     (with-current-buffer postbuff
       (if (maki-post-is-new)
           (let ((posthash (json-read-from-string
                            (gethash "message" response))))
             (setq maki-post-hash posthash)
             (rename-buffer (maki-get-buffname))))
       (message "Post successfully saved")
       (set-buffer-modified-p nil)))
   :error
   (let ((stcode (maki-req-resp status)))
     (if (equal stcode 418) ;; is a teapot
         (message "You are not allowed, the server is a teapot >.<'")
       (message "Unable to save post [%s]" stcode)))))

(defun maki-post-ask-save ()
  "Save the changes to the blog post, but confirm first."
  (interactive)
  (if (buffer-modified-p)
      (if (equal "y" (read-string "Do you want to save the changes? (y/n): "))
          (maki-post-save))
    (message "The blog post has not been modified.")))

(defun maki-post-setup (buffname postc)
  (progn
    (switch-to-buffer buffname)
    (maki-draw-post postc)
    (goto-char (point-min))
    (set-visited-file-name buffname)
    (set-buffer-modified-p nil) ;; to remove the **
    (progn ;; maki-post-mode minor mode changes
      (rst-mode)
      (maki-post-mode)
      (maki-set-post-mode)
      (setq maki-post-hash postc))))

(defun maki-post-show (status)
  (ignore status)
  (let ((json-false nil)
        (json-object-type 'hash-table))
    (ignore json-false json-object-type)
    (maki-req-callback
     :success (let* ((postc response)
                     (buffname (maki-get-buffname postc)))
                (if (get-buffer buffname)
                    (if (equal (read-string
                                "The post is already loaded. Reload? (y/n): ") "y")
                        (kill-buffer buffname))
                  (generate-new-buffer buffname))
                (maki-post-setup buffname postc))
     :error (message "Unable to fetch post"))))

;;;###autoload
(defun maki-new-post ()
  "Set a new buffer with the default template."
  (interactive)
  (let* ((newpost (maki-make-new-posth))
         (buffname (maki-get-buffname newpost)))
    (maki-post-setup buffname newpost)))

(defun maki-get-json-response ()
  "Parse the JSON body of the response in the current buffer.
This is meant to be used in the `url-retrieve' callbacks."
  (let ((json-object-type 'hash-table)
        cnt)
    (goto-char (point-max))
    (setq cnt (thing-at-point 'line))
    (if maki-debug
        (message "JSON Response content \n\n%s\n\n\n\n----\n-" cnt))
    (json-read-from-string cnt)))

;;  Functions to format the fetched post from the server.

(defun maki-draw-rst-title (title)
  (progn
    (dotimes (_ (length title))
      (insert "="))
    (insert "\n")))

(defun maki-draw-post-title (title)
  (progn
    (insert (format "%s\n" title))
    (maki-draw-rst-title title)))

(defun maki-draw-post-simple-section (name content)
  (insert (format ".. %s\n%s\n" name content)))

(defun maki-draw-post-abstract (abstract)
  (maki-draw-post-simple-section "Abstract" abstract))

(defun maki-draw-post-category (category)
  (maki-draw-post-simple-section "Category" category))

(defun maki-draw-post-content (content)
  (maki-draw-post-simple-section "Content" content))

(defun maki-draw-post-tags (tags)
  (progn
    (insert ".. Tags\n")
    (dotimes (pos (length tags))
      (let ((tag (elt tags pos)))
        (insert (format " - %s\n" tag))))))

(defun maki-draw-post (postc)
  "Draw the post in the new buffer, POSTC could be an empty hash."
  (let ((title (gethash "title" postc "New Post Title"))
        (abstract (gethash "abstract" postc ""))
        (content (gethash "content" postc ""))
        (tags (gethash "tags" postc nil))
        (category (gethash "category" postc "")))
    (maki-draw-post-title title)
    (maki-draw-post-abstract abstract)
    (maki-draw-post-category category)
    (maki-draw-post-tags tags)
    (maki-draw-post-content content)))

;; End of "drawing" functions.

;; Functions to fetch the current data of the post buffer.

(defun maki-get-current-title ()
  (progn
    (goto-char 1)
    (maki-chomp (thing-at-point 'line))))

(defun maki-get-range-from (mytag nexttag)
  (let (start stop)
    (goto-char 1)
    (setq start (1+ (re-search-forward (format "^%s$" mytag) nil t))
          stop (re-search-forward (format "^%s$" nexttag) nil t))
    (buffer-substring start (- stop (length nexttag)))))

(defun maki-get-current-abstract ()
  (let ((abstract ".. Abstract")
        (category ".. Category"))
    (maki-chomp (maki-get-range-from abstract category))))

(defun maki-get-current-tags ()
  (let ((tags ".. Tags")
        (content ".. Content")
        (tag-cnt nil))
    (setq tag-cnt (maki-get-range-from tags content))
    (split-string (replace-regexp-in-string ".*- " "" tag-cnt))))

(defun maki-get-current-content ()
  (let (start end)
    (goto-char 1)
    (setq start (1+ (re-search-forward "^.. Content$" nil t))
          end (1- (point-max)))
    (buffer-substring start end)))

(defun maki-get-current-category ()
  (let ((category ".. Category")
        (tags ".. Tags"))
    (maki-chomp (maki-get-range-from category tags))))

(defun maki-post-set-visibility (visib)
  (let* ((json-false nil)
         (url-request-method "POST")
         (url-request-extra-headers (maki-json-headers))
         (url-request-data (json-encode `((id . ,(gethash "id" maki-post-hash))
                                          (public . ,visib)))))
    (ignore json-false)
    (if maki-debug
        (message "Setting the visibility with data: %s"
                 url-request-data))
    (url-retrieve (maki-visibility-url)
                  'maki-post-visib-check `(,visib ,(current-buffer)))))

(defun maki-post-visib-toggle ()
  (interactive)
  (let ((status (not (maki-post-visib))))
    (if (maki-post-is-new) ;; if is new set the value in the local hash.
        (message "You can't change the visibility of a new post.")
      (maki-post-set-visibility status))))

(defun maki-post-visib-check (status visib prebuff)
  (ignore status)
  (maki-req-callback
   :success (with-current-buffer prebuff
              (ignore response)
              (puthash "public" visib maki-post-hash)
              (rename-buffer (maki-get-buffname)))
   :error (message "Unable to change visibility")))

(defun maki-auth-get-user (&optional refresh)
  (progn
    (if refresh (setq maki-user nil))
    (if (null maki-user)
        (setq maki-user (read-string "User: ")))
    maki-user))

(defun maki-auth-get-passwd (&optional refresh)
  "Get the user password, if is not defined use password-cache ask and return.
With REFRESH forget the cached one first."
  (progn
    (when refresh
      (setq maki-passwd nil)
      (password-cache-remove "maki"))
    (if (null maki-passwd)
        (let ((passwd (password-read "Password: " "maki")))
          (password-cache-add "maki" passwd)
          passwd)
      maki-passwd)))
;;

(defun maki-get-buffname (&optional posthash)
  "Get the appropiate name of the maki post buffer from POSTHASH.
If POSTHASH is nil, then use `maki-post-hash'.
`maki-post-hash' will not exists if this is not a `maki-post-mode' buffer."
  (let* ((post (if (null posthash) maki-post-hash posthash))
         (slug (gethash "slug" post "new"))
         (id (gethash "id" post "*new*"))
         (lang (gethash "lang" post maki-def-lang))
         (is-public (gethash "public" post nil))
         (public-msg (if is-public "PUBLIC" "PRIVATE")))
    (format "%s [%s] {%s} -%s-" slug id lang public-msg)))

(defun maki-set-post-mode ()
  "Setup the environment in the maki-post minor mode."
  (progn
    ;; Overwrite the default save process, with a hardcoded "t"
    ;; to always stop the chain of hooks.
    (make-local-variable 'write-file-functions)
    (setq write-file-functions
          (list (lambda ()
                  "Catch the save execution to save the changes"
                  (progn (maki-post-ask-save) t))))))

(defun maki-post-set-lang (lang)
  "Set the language of the post to LANG."
  (interactive "sLang code (es/en): ")
  (if (maki-post-is-new)
      (if (maki-valid-lang? lang)
          (message "Invalid language %s" lang)
        (puthash "lang" lang maki-post-hash)
        (message (maki-get-buffname maki-post-hash))
        (rename-buffer (maki-get-buffname) t)
        (message "Language changed to %s" lang))
    (message "You can't change the laguage when the post already exists.")))

;;;###autoload
(defun maki-mode ()
  "Major mode to edit the maki blog."
  (interactive)
  (let ((main-buff "*Maki*"))
    (switch-to-buffer main-buff)
    (insert (propertize maki-banner 'face 'bold))
    (kill-all-local-variables)
    (setq maki-curr-post nil
          major-mode 'maki-mode
          mode-name "Maki"
          buffer-read-only t)
    (use-local-map maki-mode-map)
    (run-mode-hooks 'maki-mode-hook)
    (if maki-autolist
        (maki-get-post-list))))

(define-minor-mode maki-post-mode
  "Set the minor mode for the post edition.
With no argument, this command toggles the mode.
Non-null prefix argument turns on the mode.
Null prefix argument turns off the mode."
  :init-value nil
  :lighter " maki-post"
  :keymap maki-post-mode-map)

(provide 'maki-mode)

;;; maki-mode.el ends here
