import os
from dotenv import load_dotenv



basedir = os.path.abspath(os.path.dirname(__file__))
# print(os.path.join(basedir,'.env'))
load_dotenv(os.path.join(basedir,'.env'))


class Config(object):
    pass