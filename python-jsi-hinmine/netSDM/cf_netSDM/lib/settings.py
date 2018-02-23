from rdflib import Namespace
import os


HEDWIG = Namespace('http://kt.ijs.si/hedwig#')
W3C = Namespace('http://www.w3.org/')

# Pre-defined assets path
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
EXAMPLE_SCHEMA = os.path.join(ASSETS_DIR, 'builtin.n3')
