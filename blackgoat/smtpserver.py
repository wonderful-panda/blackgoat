# coding: utf-8
from blackgoat import db
from blackgoat.models import Message
from smtpd import SMTPServer
from threading import Thread
import asyncore

class _FakeSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            msg = Message.from_string(data)
            db.session.add(msg)
            db.session.commit()
        except Exception as e:
            # TODO: logging
            print('[error({0})] {1}'.format(e.__class__.__name__, e))

class FakeSMTPServer(object):
    def __init__(self, localaddr=('0.0.0.0', 25), remoteaddr=None):
        self.localaddr = localaddr
        self.remoteaddr = remoteaddr

    def start(self):
        self.smtpserver = _FakeSMTPServer(self.localaddr, self.remoteaddr)
        self.thread = Thread(target=asyncore.loop, kwargs={'timeout':1})
        self.thread.start()

    def stop(self):
        self.smtpserver.close()
        self.thread.join()


