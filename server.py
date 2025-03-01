from bottle import route, run, template

@route('/')
def index() -> str: return hello('homeslice@phishmail.com')

@route('/hello/<name>')
def hello(name):
    return template(f'<b>Hello {name}</b>!')

run(host='localhost', port=8888, debug=True)