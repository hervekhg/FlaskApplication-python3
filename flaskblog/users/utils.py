import os
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

import base64
import binascii
import os

from hmac import compare_digest
from random import SystemRandom

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
    msg.body = '''To reset your password, visit the following link:
%s
If you did not make this request then simply ignore this email and no changes will be made.
''' %(url_for('users.reset_token', token=token, _external=True))
    mail.send(msg)


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

