import inspect
import logging
import os
from typing import Any

import confuse
from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from mongodb_migrations.cli import MigrationManager
from yoyo import read_migrations, get_backend
from functools import partial
from flask_restplus_data.enum import DatabaseType

logger = logging.getLogger(__name__)


class Database:
    _data_type_mapping = {
      DatabaseType.MONGODB: {
        'String': 'StringField',
        'Unicode': None,
        'Regex': 'RegExStringField',
        'Binary': 'BinaryField',
        'Boolean': 'BoolField',
        'Int': 'IntField',
        'Float': 'FloatField',
        'DateTime': 'DateTimeField',
        'Tuple': 'TupleField',
        'Geo': 'GeoField',
        'Enum': 'EnumField',
        'Json': 'AnythingField',
        'List': None,
        'Id': 'ObjectIdField',
        'Link': 'DocumentField',
      },
      DatabaseType.SQL: {
        'String': 'String',
        'Unicode': 'UnicodeText',
        'Regex': None,
        'Binary': 'Binary',
        'Boolean': 'Boolean',
        'Int': 'Integer',
        'Float': 'Float',
        'DateTime': 'DateTime',
        'Tuple': None,
        'Geo': None,
        'Enum': 'Enum',
        'Json': 'JSON',
        'List': 'ARRAY',
        'Id': None,
        'Link': 'relationship',
      },
    }
    
    def __init__(self, db_type: DatabaseType, db: Any):
        self.db = db
        for key, val in Database._data_type_mapping[db_type].items():
            if val is None:
                method = partial(Database.unsupported_field, key, db_type)
            else:
                method = getattr(db, val)
            if db_type is DatabaseType.MONGODB:
                setattr(self, key, method)
            elif db_type is DatabaseType.SQL:
                if key is 'Id':
                   method = partial(db.Column, primary_key=True)
                elif key is 'Link':
                   method = partial(Database.handle_link, db)
                else:
                    method = partial(db.Column, method, nullable=True)
                setattr(self, key, method)

    @staticmethod
    def unsupported_field(field_type: str, db_type: DatabaseType):
        raise Exception('Unsupported filed of type {} for {} database.'.format(field_type, db_type))
        
    @staticmethod
    def handle_link(db: SQLAlchemy, linked_class):
        class_stack_frame = inspect.stack()[0]
        module_stack_frame = inspect.stack()[1]
        current_class = Database.get_model_class(module_stack_frame, class_stack_frame)
        return db.relationship(linked_class.__name__, backref=db.backref(current_class.__tablename__, lazy=True))

    @staticmethod
    def get_model_class(module_stack_frame: inspect.FrameInfo, class_stack_frame: inspect.FrameInfo):
        module_name = '__main__' if module_stack_frame.function is '<module>' else module_stack_frame.function
        return __import__(module_name).__dict__[class_stack_frame.function]


class FlaskData(Database):
    def __init__(self, config_directory: str = '', app: Flask = None):
        self.config_directory = config_directory
        if app is not None:
            self.initialize(app)

    def initialize(self, app: Flask):
        os.environ[f'{app.name.upper()}DIR'] = self.config_directory
        config = confuse.Configuration(app.name, __name__)
        self.url = config['database']['url'].get(str)
        self.pool_size = config['database']['pool_size'].get(int)
        self.migration_directory = config['database']['migration_directory'].get(str)
        self.type = config['database']['type'].get(DatabaseType)
        self.app = app
        app.run = partial(self.run_app, app.run)
        db = self.initialize_database(app)
        super(FlaskData, self).__init__(self.type, db)

    def run_app(self, original_run, *args, **kargs):
        self.apply_migrations()
        original_run(*args, **kargs)

    def initialize_database(self, app: Flask) -> Any:
        db = None
        if self.type is DatabaseType.SQL:
            app.config['SQLALCHEMY_DATABASE_URI'] = self.url
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            app.config['pool_size'] = self.pool_size
            db = SQLAlchemy(app)
            setattr(self, 'Model', db.Model)
        elif self.type is DatabaseType.MONGODB:
            app.config['MONGOALCHEMY_DATABASE'] = self.url.split('/')[-1]
            app.config['MONGOALCHEMY_CONNECTION_STRING'] = self.url
            db = MongoAlchemy(app)
            setattr(self, 'Model', db.Document)
        setattr(self.Model, 'db', db)
        setattr(self.Model, 'url', self.url)
        setattr(self.Model, 'db_type', self.type)
        return db

    def apply_migrations(self):
        if not self.migration_directory:
            return

        if self.type is DatabaseType.SQL:
            try:
                backend = get_backend(self.url)
                migrations = read_migrations(self.migration_directory)
                with backend.lock():
                    backend.apply_migrations(backend.to_apply(migrations))
            except Exception as err:
                logger.error('Database migration Failed: ={}'.format(err))
        elif self.type is DatabaseType.SQL:
            manager = MigrationManager()
            manager.config.mongo_url = self.url
            manager.config.mongo_migrations_path = self.migration_directory
            manager.run()

