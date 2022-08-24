from flask import Flask
from flaskext.mysql import MySQL
from app import SSHTunnelForwarder
# config.py you can put this file anywhere in the project
class Config(object):
    DEBUG = False
    TESTING = False
    tunnel = SSHTunnelForwarder(('47.250.49.41', 22), ssh_password="123456Aa!", ssh_username="root",
                            remote_bind_address=("127.0.0.1", 3306))
    tunnel.start()


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = '123456Aa!'
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_DB = 'test'  # can be any

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = '123456Aa!'
    MYSQL_DATABASE_HOST = '127.0.0.1' # eg to amazone db :- yourdbname.xxxxxxxxxx.us-east-2.rds.amazonaws.com
    MYSQL_DATABASE_DB = 'test'

    DEBUG = False