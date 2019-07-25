#!/usr/bin/env python3

from flask import Flask 
from model.orm import ORM
from data.schema import DBPATH

ORM.dbpath = DBPATH

app = Flask(__name__)

from . import routes

