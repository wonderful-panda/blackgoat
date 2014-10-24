# coding: utf-8
from blackgoat import db
from blackgoat.models import Message
from smtpd import SMTPServer
from threading import Thread
import logging
import asyncore

class _Server(SMTPServer):
    def __init__(self, logger, localaddr, remoteaddr):
        self.logger = logger
        SMTPServer.__init__(self, localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            msg = Message.from_string(data)
            self.logger.info(' * Received: %s', msg.title)
            db.session.add(msg)
            db.session.commit()
        except:
            self.logger.error(' * Failed to process message', exc_info=True)

class FakeSMTPServer(object):
    def __init__(self, logger=None, localaddr=('0.0.0.0', 25), remoteaddr=None):
        self.localaddr = localaddr
        self.remoteaddr = remoteaddr
        self.logger = logger or logging.getLogger('blackgoat.smtpserver')

    def start(self):
        self.logger.info(' * Start SMTP Server on %s:%d', *self.localaddr)
        self.smtp = _Server(self.logger, self.localaddr, self.remoteaddr)
        self.thread = Thread(target=asyncore.loop, kwargs={'timeout':1})
        self.thread.start()

    def stop(self):
        self.smtp.close()
        self.thread.join()
        self.logger.info(' * Stop SMTP Server')

