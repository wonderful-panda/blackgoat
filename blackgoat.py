# coding: utf-8
from flask.ext.script import Manager, Server, Option
from blackgoat import setup
import os
import sys
import logging
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
    if hasattr(sys, 'frozen'):
        script = sys.executable
        basedir = os.path.dirname(os.path.abspath(sys.executable))
        template_dir = os.path.join(basedir, 'templates')
        static_dir = os.path.join(basedir, 'static')
    else:
        basedir = os.path.dirname(os.path.abspath(__file__))
        template_dir = static_dir = None
    os.chdir(basedir)
    
    configfile = os.path.join(basedir, 'config.yaml')
    if os.path.exists(configfile):
        config = yaml.load(open(configfile).read())

        logging.config.dictConfig(config['logging'])
        appconfig = config.get('flask')
    else:
        appconfig = None

    app, db = setup(basedir, appconfig, template_dir, static_dir)
    db.create_all()

    manager = Manager(app)
    manager.add_command('runserver', MyServer)
    manager.run()

