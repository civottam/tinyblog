import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from tinyblog import models
from tinyblog import create_app


env = os.environ.get('BLOG_ENV', 'dev')
app = create_app('tinyblog.config.{}Config'.format(env.capitalize()))
manager = Manager(app)
migrate = Migrate(app, models.db)

# Create a new commands: server
# This command will be run the Flask development_env server
#manager.add_command("server", Server('192.168.7.157'), port=8089)
manager.add_command("server", Server('127.0.0.1'))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app, 
        db=models.db, 
        User=models.User, 
        Post=models.Post, 
        Comment=models.Comment,
        Tag=models.Tag,
        Server=Server
        )


if __name__ == '__main__':
    manager.run()