from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.0.8'
author = 'nucklehead'
github_url = f'https://github.com/{author}/flask-restplus-data'

setup(name='flask_restplus_data',
      version=version,
      description='Library inspired by Spring Data to perform Operations on datastores',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      url=github_url,
      download_url=f'{github_url}/tarball/{version}',
      author=author,
      author_email='pierevans@gmail.com',
      keywords=[
          'datastore', 'sql', 'nosql', 'postgres', 'mysql', 'sqlite', 'obdc', 'oracle database', 'mongodb', 'orm',
          'flask'
          , 'flask_restplus', 'rest', 'restplus'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Framework :: Flask',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      packages=find_packages(exclude=['test']),
      install_requires=[
          'confuse==1.0.0',
          'psycopg2-binary==2.8.6',
          'flask-sqlalchemy==2.4.1',
          'Flask-MongoAlchemy==0.7.2',
          'yoyo-migrations==6.1.0',
          'mongodb-migrations==0.7.0',
      ])

