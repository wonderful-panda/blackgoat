from blackgoat import app, db
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from blackgoat.smtpserver import FakeSMTPServer

class MyServer(Server):
    def __call__(self, *args, **kwargs):
        host = kwargs.get('host', self.host)
        smtp = FakeSMTPServer(localaddr=(host, 25))
        smtp.start()
        Server.__call__(self, *args, **kwargs)
        smtp.stop()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', MyServer)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
