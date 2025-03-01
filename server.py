from bottle import route, run
from emails import Email
from random import shuffle
from dataclasses import dataclass

@dataclass
class Email:
    name: str
    domain: str
    subject: str
    body: str

class Game:
    day: int = 1
    emails: list[Email] = []
    times_phished: int = 0

    @classmethod
    def generate_emails(cls) -> None:
        ''' Fills the emails list with random emails '''
        cls.emails.clear()
        for _ in range(cls.day): cls.emails.append(cls.make_email())
        shuffle(cls.emails)
    
    @classmethod
    def make_email(cls) -> Email: ''' Placeholder for function to return an email. '''


@route('/')
def index() -> str: return hello('homeslice@phishmail.com')

@route('/hello/<name>')
def hello(name):
    return f'Hello {name}!'

run(host='localhost', port=8080, debug=True)