#encoding: utf-8
import os

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'flask_learn'
USERNAME = 'root'
PASSWORD = 'kirisame'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

#邮箱配置信息
MAIL_SERVER ="smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME ="3114785283@qq.com"
MAIL_PASSWORD ="wgpwybxthxdudeig"
MAIL_DEFAULT_SENDER ="3114785283@qq.com"

SECRET_KEY = os.urandom(24)

SECRET_KE = "fafadgrawewga"