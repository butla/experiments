import hug

@hug.cli()
@hug.get('/')
def hello():
    return 'Hello world!'

