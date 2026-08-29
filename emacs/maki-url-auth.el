;;; maki-url-auth.el --- Fix digest auth HA2 caching in url-auth -*- lexical-binding: t; -*-

;; Author: Joel Rivera <rivera@joel.mx>

;;; Commentary:

;; Emacs' url-auth.el caches the digest HA2 hash inside the credentials
;; key when the key is first created (see `url-digest-auth-create-key').
;; HA2 is md5("METHOD:URI"), so it is only valid for the exact request
;; that created the key: any later request with a different method or
;; path (e.g. a POST to /posts/update/1 after a GET of /posts/1) sends a
;; stale digest and gets rejected with 401.
;;
;; This is the modern, minimal replacement for the full patched copy of
;; url-auth.el that this project carried since the Emacs 24 days: advise
;; `url-digest-auth-build-response' to recompute HA2 from the actual
;; request method and URI, leaving everything else (qop, auth-source,
;; caching of HA1) to stock url-auth.

;;; Code:

(require 'url-auth)
(require 'url-vars)

(defun maki-url-auth--fresh-ha2 (orig key url realm attrs)
  "Call ORIG with KEY's HA2 recomputed for the current request.
URL, REALM and ATTRS are passed through untouched."
  (let ((fixed
         (and key
              (list (nth 0 key)
                    (nth 1 key)
                    (nth 2 key)
                    ;; The 401 retry runs in the url-http connection
                    ;; buffer, where the method is only in the
                    ;; buffer-local `url-http-method'.
                    (url-digest-auth-make-ha2
                     (or url-request-method
                         (bound-and-true-p url-http-method)
                         "GET")
                     (url-filename (if (stringp url)
                                       (url-generic-parse-url url)
                                     url)))))))
    (funcall orig fixed url realm attrs)))

(advice-add 'url-digest-auth-build-response
            :around #'maki-url-auth--fresh-ha2)

(provide 'maki-url-auth)

;;; maki-url-auth.el ends here
