from data import schema
from data import seed

def setup():
    schema.schema()
    seed.seed()
    return None

setup()