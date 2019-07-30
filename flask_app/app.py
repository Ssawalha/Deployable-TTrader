#!/usr/bin/env python3

from flask import Flask 
from model.orm import ORM
from data.schema import DBPATH

ORM.dbpath = DBPATH

app = Flask(__name__)

from . import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0')
