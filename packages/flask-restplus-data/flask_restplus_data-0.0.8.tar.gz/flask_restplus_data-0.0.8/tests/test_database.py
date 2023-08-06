import os
import unittest
from unittest.mock import MagicMock

from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from mongoalchemy.session import Session
from flask_restplus_data.database import FlaskData
from flask_restplus_data.enum import DatabaseType
from tests.resources.test_migrations import postgres_migrations, mongodb_migrations


class Test_FlaskData(unittest.TestCase):
    def setUp(self):
        self.mongo_app = Flask('mongodbapp')
        self.postgres_app = Flask('postgresapp')
        self.fake_migration = MagicMock()
        self.postgres_app.run = MagicMock()
        self.mongo_app.run = MagicMock()
        Session.connect = MagicMock()
        FlaskData.apply_migrations = self.fake_migration
        self.postgres_flask_data = FlaskData(os.path.dirname(postgres_migrations.__file__), self.postgres_app)
        self.mongodb_flask_data = FlaskData(os.path.dirname(mongodb_migrations.__file__), self.mongo_app)

    def test_postgres_config(self):
        self.assertEqual('postgres://test', self.postgres_flask_data.url)
        self.assertEqual(20, self.postgres_flask_data.pool_size)
        self.assertIn('postgres_migrations', self.postgres_flask_data.migration_directory)
        self.assertEqual(DatabaseType.SQL, self.postgres_flask_data.type)
        self.assertIsInstance(self.postgres_flask_data.db, SQLAlchemy)
        self.assertEqual(self.postgres_flask_data.app, self.postgres_app)
        self.assertEqual(self.postgres_flask_data.Model, self.postgres_flask_data.db.Model)
        self.assertEqual('postgres://test', self.postgres_app.config['SQLALCHEMY_DATABASE_URI'])
        self.assertEqual(20, self.postgres_app.config['pool_size'])

    def test_postgres_migration_call(self):
        self.postgres_app.run()
        self.fake_migration.assert_called_once()

    def test_mongodb_config(self):
        self.assertEqual('mongodb://test', self.mongodb_flask_data.url)
        self.assertEqual(20, self.mongodb_flask_data.pool_size)
        self.assertIn('mongodb_migrations', self.mongodb_flask_data.migration_directory)
        self.assertEqual(DatabaseType.MONGODB, self.mongodb_flask_data.type)
        self.assertIsInstance(self.mongodb_flask_data.db, MongoAlchemy)
        self.assertEqual(self.mongodb_flask_data.app, self.mongo_app)
        self.assertEqual(self.mongodb_flask_data.Model, self.mongodb_flask_data.db.Document)
        self.assertEqual('mongodb://test', self.mongo_app.config['MONGOALCHEMY_CONNECTION_STRING'])

    def test_mongodb_migration_call(self):
        self.mongo_app.run()
        self.fake_migration.assert_called_once()

class Test_FlaskDataModel(unittest.TestCase):
    @staticmethod
    def create_model(flask_data: FlaskData):
        class Model(flask_data.Model):
            id = flask_data.Id()
            title = flask_data.String()
            # author = self.postgres_flask_data.Link(Author)
            year = flask_data.Int()
        return Model

    def setUp(self):
        self.mongo_app = Flask('mongodbapp')
        self.postgres_app = Flask('postgresapp')
        Session.connect = MagicMock()
        self.postgres_flask_data = FlaskData( os.path.dirname(postgres_migrations.__file__), self.postgres_app)
        self.mongodb_flask_data = FlaskData(os.path.dirname(mongodb_migrations.__file__), self.mongo_app)

        self.PostgresModel = self.create_model(self.postgres_flask_data)
        self.MongoModel = Test_FlaskDataModel.create_model(self.mongodb_flask_data)

    def test_postgres_model(self):
        self.assertEqual('model', self.PostgresModel.__tablename__)
        self.assertIsNotNone(self.PostgresModel._sa_class_manager)

    def test_mongodb_model(self):
        self.assertIsNotNone(self.MongoModel.mongo_id)
        self.assertEqual(self.MongoModel, self.MongoModel.query.type)
