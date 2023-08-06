import functools
import inspect
import json
import logging
from typing import Type
from string import Template
from sqlalchemy import create_engine, exists, text
from sqlalchemy import orm

from flask_restplus_data.enum import DatabaseType

logger = logging.getLogger(__name__)


class Query:
    def __init__(self, query_str: str):
        self.query_str = query_str

    def __call__(self, function):
        @functools.wraps(function)
        def execute(*args, **kwargs):
            func_param_names = inspect.getfullargspec(function)[0][1:]
            # Find method params not specified as kwargs. They are in args
            missing_kwarg = list(filter(lambda arg: arg not in kwargs.keys(), func_param_names))
            positional_args = args[1:]
            merged_kwarg = dict(zip(missing_kwarg, positional_args))
            kwargs.update(merged_kwarg)
            if len(positional_args) == 0:
                positional_args = list(kwargs.values())
            # Convert list to enumerated dict
            positional_args = {str(i): positional_args[i] for i in range(0, len(positional_args))}
            if args[0].model_class.db_type is DatabaseType.SQL:
                session = args[0].session
                query_object = session.query(args[0].model_class) \
                    .from_statement(text(self.query_str)) \
                    .params(kwargs) \
                    .params(positional_args)
                if self.query_str.upper().startswith('SELECT'):
                    result = query_object.all()
                else:
                    result = session.execute(query_object.statement).rowcount
                return result
            elif args[0].model_class.db_type is DatabaseType.MONGODB:
                query_str = Template(self.query_str).safe_substitute(kwargs)
                query_str = Template(query_str).safe_substitute(positional_args)
                result = args[0].model_class.query.filter(json.loads(query_str))
                return result
        return execute


T = Type['T']


def create_new_sql_repo_class(repo_class: type):
    class NewRepository(repo_class):
        def __init__(self, model_class: T, *args, **kwargs):
            super(NewRepository, self).__init__(*args, **kwargs)
            self.model_class = model_class
            primary_keys = self.model_class._sa_class_manager.mapper.primary_key
            self.primary_keys = primary_keys

        def __enter__(self):
            self.session = orm.sessionmaker(self.model_class.db.engine)()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                self.session.flush()
                self.session.expunge_all()
                self.session.commit()
            except Exception as _:
                self.session.rollback()
                raise
            finally:
                self.session.close()

        def save(self, instance: object):
            self.session.add(instance)

        def update(self, instance: object) -> T:
            result = self.session.merge(instance)

            return result

        def find_one(self, *object_ids: object) -> T:
            query_obj = self.session.query(self.model_class)
            for index, object_id in enumerate(object_ids):
                query_obj = query_obj.filter(self.primary_keys[index] == object_id)
            result = query_obj.one_or_none()
            return result

        def exists(self, *object_ids: object) -> bool:
            exist = exists()
            for index, object_id in enumerate(object_ids):
                exist = exist.where(self.primary_keys[index] == object_id)
            result = self.session.query(exist).scalar()
            return result

        def delete(self, *object_ids: object) -> int:
            query_obj = self.session.query(self.model_class)
            for index, object_id in enumerate(object_ids):
                query_obj = query_obj.filter(self.primary_keys[index] == object_id)
            result = query_obj.delete(synchronize_session='fetch')
            return result
    return NewRepository


def create_new_mongodb_repo_class(repo_class: type):
    class NewRepository(repo_class):
        def __init__(self, model_class: T, *args, **kwargs):
            super(NewRepository, self).__init__(*args, **kwargs)
            self.model_class = model_class

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return

        def save(self, instance: object):
            instance.save()

        def update(self, instance: object) -> T:
            self.save(instance)

        def find_one(self, object_id: object) -> T:
            return self.model_class.query.get(object_id)

        def exists(self, object_id: object) -> bool:
            return self.find_one(object_id) is not None

        def delete(self, object_id: object) -> int:
            result = self.find_one(object_id)
            result.remove()
            return result
    return NewRepository


class FlaskDataRepository:
    def __init__(self, repo_class: type):
        self.repo_class = repo_class

    def __call__(self, model_class, *args, **kwargs):
        if model_class.db_type is DatabaseType.SQL:
            return create_new_sql_repo_class(self.repo_class)(model_class, *args, **kwargs)
        elif model_class.db_type is DatabaseType.MONGODB:
            return create_new_mongodb_repo_class(self.repo_class)(model_class, *args, **kwargs)
