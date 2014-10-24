# coding: utf-8
from blackgoat import db
import sqlalchemy as sa

from email import header, utils, message_from_string
from datetime import datetime
import time

def _get_header(name, msg):
    value, charset = header.decode_header(msg[name])[0]
    if charset:
        value = value.decode(charset)
    return value

def _get_date(msg):
    datetuple = utils.parsedate(_get_header('Date', msg))
    if datetuple is None:
        return None
    else:
        return datetime.fromtimestamp(time.mktime(datetuple))

def _get_body(msg):
    if msg.is_multipart():
        try:
            item = next(x for x in msg.walk()
                          if not x.is_attachment() and 
                             x.get_content_type() == 'text/plain')
        except StopIteration:
            return ''
    else:
        item = msg 
    body = item.get_payload(decode=True)
    charset = item.get_content_charset()
    if charset:
        body = body.decode(charset)
    return body


class Message(db.Model):
    "メール"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    from_addr = sa.Column(sa.Text)
    to_addr = sa.Column(sa.Text)
    cc_addr = sa.Column(sa.Text)
    bcc_addr = sa.Column(sa.Text)
    body = sa.Column(sa.Text)
    date = sa.Column(sa.DateTime)
    raw = sa.Column(sa.Text)

    def __repr__(self):
        return "<Message id={0!r}, title={1!r}>".format(self.id, self.title)

    @classmethod
    def from_string(cls, data):
        msg = message_from_string(data)
        from_addr = _get_header('From', msg)
        to_addr = _get_header('To', msg)
        cc_addr = _get_header('Cc', msg)
        bcc_addr = _get_header('Bcc', msg)
        title = _get_header('Subject', msg)
        body = _get_body(msg)
        date = _get_date(msg)
        raw = data
        return cls(title=title, from_addr=from_addr,
                   to_addr=to_addr, cc_addr=cc_addr, bcc_addr=bcc_addr,
                   body=body, date=date, raw=data)

