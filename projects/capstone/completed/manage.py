from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, APP
from models import db
# Script can be used in Heroku/Linux envs for db model
# creation
# Changed to uppercase APP as in app.py
# use:
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
