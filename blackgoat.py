from blackgoat import app, db
from flask.ext.script import Manager, Server, Option
from blackgoat.smtpserver import FakeSMTPServer

class MyServer(Server):
    smtpport = 25

    def get_options(self):
        return Server.get_options(self) + \
                (Option('--smtpport', dest='smtpport', 
                        help='port of smtp server',
                        type=int, default=self.smtpport),)

    def __call__(self, *args, **kwargs):
        db.create_all()
        kwargs = kwargs.copy()
        host = kwargs.get('host', self.host)
        smtpport = kwargs.pop('smtpport', self.smtpport)
        smtp = FakeSMTPServer(localaddr=(host, smtpport))
        smtp.start()
        Server.__call__(self, *args, **kwargs)
        smtp.stop()

manager = Manager(app)
manager.add_command('runserver', MyServer)

if __name__ == '__main__':
    manager.run()
