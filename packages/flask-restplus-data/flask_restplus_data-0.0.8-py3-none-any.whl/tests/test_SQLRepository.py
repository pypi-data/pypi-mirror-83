import os
import unittest
from unittest.mock import MagicMock

from flask import Flask
from mongoalchemy.session import Session
from sqlalchemy.dialects import postgresql

from flask_restplus_data.FlaskDataRepository import Query
from flask_restplus_data.FlaskDataRepository import FlaskDataRepository
from sqlalchemy import orm

from flask_restplus_data.database import FlaskData
from tests.resources.test_migrations import mongodb_migrations, postgres_migrations

mongo_app = Flask('mongodbapp')
postgres_app = Flask('postgresapp')
Session.connect = MagicMock()
postgres_flask_data = FlaskData(os.path.dirname(postgres_migrations.__file__), postgres_app)
mongodb_flask_data = FlaskData(os.path.dirname(mongodb_migrations.__file__), mongo_app)


class PostgresModel(postgres_flask_data.Model):
    id = postgres_flask_data.Id()
    title = postgres_flask_data.String()
    year = postgres_flask_data.Int()


class MongoModel(mongodb_flask_data.Model):
    id = mongodb_flask_data.Id()
    title = mongodb_flask_data.String()
    year = mongodb_flask_data.Int()


@FlaskDataRepository
class TestFlaskDataRepository:
    @Query('SELECT * FROM postrgre_model WHERE id = :object_id')
    def test_get_sql(self, object_id: str):
        pass

    @Query('DELETE FROM postrgre_model WHERE id = :object_id')
    def test_delete_sql(self, object_id: str):
        pass

    @Query('SELECT * FROM postrgre_model WHERE id = :0')
    def test_get_positional_sql(self, object_id: str):
        pass

    @Query('DELETE FROM postrgre_model WHERE id = :0')
    def test_delete_positional_sql(self, object_id: str):
        pass

    @Query('{"id": "$object_id"}')
    def test_get_mongodb(self, object_id: str):
        pass

    # What to do
    @Query('{"id": "$object_id"}')
    def test_delete_mongodb(self, object_id: str):
        pass

    @Query('{"id": "$0"}')
    def test_get_positional_mongodb(self, object_id: str):
        pass

    @Query('{"id": "0"}')
    def test_delete_positional_mongodb(self, object_id: str):
        pass


class TestPostgresRepository(unittest.TestCase):
    def setUp(self):
        self.odl_sessionmaker = orm.sessionmaker

    def tearDown(self):
        orm.sessionmaker = self.odl_sessionmaker

    def test_custom_query_args(self):
        def check_params(**kwarg): self.assertEqual(kwarg['object_id'], 'id')

        def check_model(model): self.assertEqual(model, PostgresModel)

        mock_query = MagicMock()
        mock_query.from_statement().params = MagicMock(wraps=check_params, return_value=MagicMock())
        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.query = MagicMock(wraps=check_model, return_value=mock_query)
            repo.test_get_sql('id')

    def test_custom_query_kwarg(self):
        def check_params(**kwarg): self.assertEqual(kwarg['object_id'], 'id')

        def check_model(model): self.assertEqual(model, PostgresModel)

        mock_query = MagicMock()
        mock_query.from_statement().params = MagicMock(wraps=check_params, return_value=MagicMock())
        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.query = MagicMock(wraps=check_model, return_value=mock_query)
            repo.test_get_sql(object_id='id')

    def test_delete_custom_query_args(self):
        def check_statement(sql):
            self.assertEqual(str(sql.compile(dialect=postgresql.dialect())) % sql.compile().params,
                             'DELETE FROM postgre_model WHERE object_id = id')

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.execute = MagicMock(wraps=check_statement, return_value=MagicMock())
            repo.test_delete_sql('id')

    def test_delete_custom_query_kwarg(self):
        def check_statement(sql):
            self.assertEqual(str(sql.compile(dialect=postgresql.dialect())) % sql.compile().params,
                             'DELETE FROM postgre_model WHERE object_id = id')

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.execute = MagicMock(wraps=check_statement, return_value=MagicMock())
            repo.test_delete_sql(object_id='id')

    def test_delete_custom_query_positional_args(self):
        def check_statement(sql):
            self.assertEqual(str(sql.compile(dialect=postgresql.dialect())) % sql.compile().params,
                             'DELETE FROM postgre_model WHERE object_id = id')

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.execute = MagicMock(wraps=check_statement, return_value=MagicMock())
            repo.test_delete_positional_sql('id')

    def test_delete_custom_query_positional_kwarg(self):
        def check_statement(sql):
            self.assertEqual(str(sql.compile(dialect=postgresql.dialect())) % sql.compile().params,
                             'DELETE FROM postgre_model WHERE object_id = id')

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.session.execute = MagicMock(wraps=check_statement, return_value=MagicMock())
            repo.test_delete_positional_sql(object_id='id')

    def test_generic_methods_save(self):
        fake_session = MagicMock()
        fake_sessionmaker = MagicMock(return_value=fake_session)
        orm.sessionmaker = MagicMock(return_value=fake_sessionmaker)

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.save({})
            fake_session.add.assert_called_once()
        fake_session.commit.assert_called_once()

    def test_generic_methods_update(self):
        fake_session = MagicMock()
        fake_sessionmaker = MagicMock(return_value=fake_session)
        orm.sessionmaker = MagicMock(return_value=fake_sessionmaker)

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.update({})
            fake_session.merge.assert_called_once()
        fake_session.commit.assert_called_once()

    def test_generic_methods_find_one(self):
        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        fake_session = MagicMock()
        fake_session.query = MagicMock(return_value=mock_query)
        fake_sessionmaker = MagicMock(return_value=fake_session)
        orm.sessionmaker = MagicMock(return_value=fake_sessionmaker)

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.find_one('1')
            fake_session.query.assert_called_once()
            self.assertEqual(1, mock_query.filter.call_count)
            mock_query.one_or_none.assert_called_once()
        fake_session.commit.assert_called_once()

    def test_generic_methods_exists(self):
        fake_session = MagicMock()
        fake_sessionmaker = MagicMock(return_value=fake_session)
        orm.sessionmaker = MagicMock(return_value=fake_sessionmaker)

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.exists('1')
            fake_session.query.assert_called_once()
        fake_session.commit.assert_called_once()

    def test_generic_methods_delete(self):
        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        fake_session = MagicMock()
        fake_session.query = MagicMock(return_value=mock_query)
        fake_sessionmaker = MagicMock(return_value=fake_session)
        orm.sessionmaker = MagicMock(return_value=fake_sessionmaker)

        with TestFlaskDataRepository(PostgresModel) as repo:
            repo.delete(['1'])
            mock_query.delete.assert_called_once()
            self.assertEqual(1, mock_query.filter.call_count)
        fake_session.commit.assert_called_once()

