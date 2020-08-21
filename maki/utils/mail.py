import smtplib
from email.message import Message

import maki
from maki.utils import log
from maki.utils import in_development


def get_admin_addresses():
    config = maki.CONFIG("email")
    return config["admin"], config["sender"]


def get_smtp_config(inputconf):
    def req_keys(conf):
        try:
            for k in ("user", "passwd", "host"):
                if not conf[k].strip():  # invalid empty param.
                    return False
        except KeyError:
            return False
        else:  # all keys, and non-empty.
            return True

    if inputconf is not None and req_keys(inputconf):
        return inputconf
    else:
        try:
            config = maki.CONFIG("email")
            host = config["host"]
            user = config["user"]
            passwd = config["passwd"]
        except KeyError:
            return None
        else:
            # simple validation just to verify any empty field.
            if not host.strip() or not user.strip() or not passwd.strip():
                return None
            else:
                return {
                    "host": host,
                    "user": user,
                    "passwd": passwd,
                    "port": config.get("port", 587),
                }


def send(from_, to, subject, content, smtpconf=None):
    """
    Send and email, return True/False on Succes/Failure,
    depending on the configuration, any other
    possible error from the SMTP server will raise an Error.
    """
    smtpconf = get_smtp_config(smtpconf)
    log("Sending email", "EMAIL")
    log(
        "From: %s\n"
        "To: %s\n"
        "Subject: %s\n"
        "Content: %s\n\n" % (from_, to, subject, content),
        "EMAIL",
    )
    msg = Message()
    msg["From"] = from_
    msg["To"] = to
    msg["Subject"] = subject
    msg["Content-Type"] = "text/html"
    msg.set_payload(content)
    msg.set_charset("utf-8")
    # DEBUG
    # log(msg.as_string())
    if smtpconf is None:
        log(
            "Missing required parameters [host, user, passwd]"
            " please, make sure that you have the right configuration"
            " in the main config file. Unable to send email.",
            "ERROR",
        )
    if in_development():
        return True
    else:
        if smtpconf is None:
            return False
        else:  # Finally send!
            connection = smtplib.SMTP(smtpconf["host"], smtpconf["port"])
            connection.starttls()
            connection.login(smtpconf["user"], smtpconf["passwd"])
            connection.send_message(msg)
            connection.quit()
            return True
