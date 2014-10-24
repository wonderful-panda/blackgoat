# coding: utf-8
from flask.ext.script import Manager, Server, Option
from blackgoat import app, db, setup_app
import os
import sys
import logging
import urllib
import logging.config
import yaml

class MyServer(Server):
    """
    SMTPサーバを別スレッドで起動しつつ、HTTPサーバを起動する
    """
    smtpport = 25

    def get_options(self):
        return Server.get_options(self) + \
                    (Option('--smtpport', dest='smtpport', 
                            type=int, default=self.smtpport),
                     )

    def __call__(self, *args, **kwargs):
        from blackgoat.smtpserver import FakeSMTPServer
        kwargs = kwargs.copy()
        host = kwargs['host']
        smtpport = kwargs.pop('smtpport')
        smtp = FakeSMTPServer(logger=logging.getLogger('blackgoat.smtp'), 
                              localaddr=(host, smtpport))
        smtp.start()
        Server.__call__(self, *args, **kwargs)
        smtp.stop()

if __name__ == '__main__':
    script = sys.executable if hasattr(sys, 'frozen') else __file__
    basedir = os.path.dirname(os.path.abspath(script))
    os.chdir(basedir)

    database_uri = 'sqlite:' + \
                   urllib.pathname2url(os.path.join(basedir, 'blackgoat.db'))
    setup_app(database_uri)
    
    configfile = os.path.join(basedir, 'config.yaml')
    if os.path.exists(configfile):
        config = yaml.load(open(configfile).read())

        logging.config.dictConfig(config['logging'])
        appconfig = config.get('flask')
        if appconfig:
            app.config.update(appconfig)

    db.create_all()

    manager = Manager(app)
    manager.add_command('runserver', MyServer)
    manager.run()

