from setuptools import setup

setup(name='SlackBot',
      version='1.0',
      description='Slackbot for personal use',
      author='Piotr Ciastko',
      author_email='ciaasteczkowy@gmail.com',
      install_requires=['Flask>=0.10.1', 'requests[security]', 'Flask-Slack', 'APScheduler', 'SQLAlchemy', 'psycopg2']
     )
