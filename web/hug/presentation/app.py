import hug

@hug.get('/')
def hello():
    return 'Hello world!'

