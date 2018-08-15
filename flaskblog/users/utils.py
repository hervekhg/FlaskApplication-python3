import os
from PIL import Image
from flask import url_for, current_app, render_template
from flask_mail import Message
from flaskblog import mail, create_app

import base64
import binascii
import os

from hmac import compare_digest
from random import SystemRandom

from threading import Thread

_sysrand = SystemRandom()

randbits = _sysrand.getrandbits
choice = _sysrand.choice

def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user,emailsender):
    token = user.get_reset_token()
    msg = Message('237story - Password Reset Request',
                  sender=emailsender,
                  recipients=[user.email])
#     msg.body = '''To reset your password, visit the following link:
# %s
# If you did not make this request then simply ignore this email and no changes will be made.
# ''' %(url_for('users.reset_token', token=token, _external=True))
    msg.html = render_template('emails/reset_password.html', token=token, user=user)
    mail.send(msg)



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_newpostnotif_email(username,users,post,emailsender):
    app = create_app()
    for recipient_user in users:
        #username = current_user.username
        msg = Message('237story [New Story] - ' + post.title,
                      sender=emailsender,
                      recipients=[recipient_user.email]) 
    #     msg.body = '''Hello,
    # %s has published a new Story.
    # You could read it now : %s
    # ''' %(username, url_for('posts.post', post_id=post.id, slug=post.slug, _external=True))
        msg.html = render_template('emails/post_email_notif.html',
                                   post=post, username=username, user=recipient_user)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        #mail.send(msg)



def token_hex(nbytes=None):
    """Return a random text string, in hexadecimal.
    The string has *nbytes* random bytes, each byte converted to two
    hex digits.  If *nbytes* is ``None`` or not supplied, a reasonable
    default is used.
    >>> token_hex(16)  #doctest:+SKIP
    'f9bf78b9a18ce6d46a0cd2b0b86df9da'
    """
    return binascii.hexlify(token_bytes(nbytes)).decode('ascii')

def token_bytes(nbytes=None):
    """Return a random byte string containing *nbytes* bytes.
    If *nbytes* is ``None`` or not supplied, a reasonable
    default is used.
    >>> token_bytes(16)  #doctest:+SKIP
    b'\\xebr\\x17D*t\\xae\\xd4\\xe3S\\xb6\\xe2\\xebP1\\x8b'
    """
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    return os.urandom(nbytes)

