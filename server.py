from bottle import route, run
from random import shuffle
from dataclasses import dataclass

@dataclass
class Email:
    name: str
    address: str
    subject: str
    body: str
    flags: dict[str, str]
    is_phish: bool

    def as_html(self) -> str:
        preview = self.body
        if '.' in preview: preview = preview[0:preview.index(':')]
        return """
<a href="https://example.com/email/2" class="email">
    <div class="email-buttons">
        <button class="archive-button">Archive</button>
        <button class="delete-button">Delete</button>
    </div>
    <div class="email-content">
        <div class="email-sender">{self.address}</div>
        <div class="email-subject">{self.subject}</div>
        <div class="email-preview">{preview}</div>
    </div>
</a>"""

class Game:
    day: int = 1
    emails: list[Email] = []
    times_phished: int = 0

    @classmethod
    def generate_emails(cls) -> None:
        ''' Fills the emails list with random emails '''
        cls.emails.clear()

        for _ in range(cls.day - 1): cls.emails.append(cls.make_email())
        shuffle(cls.emails)
    
    @classmethod
    def make_email(cls) -> Email: ''' Placeholder for function to return an email. '''

    @classmethod
    def new_address(cls) -> Email: ''' Gemini creates a random address.'''



class Pages:
    @staticmethod
    def emails() -> str:
        with open('htmlpages/emails.txt') as template:
            page = ''.join(template.readlines())
        page.replace('{{{{{{{{EMAILS}}}}}}}}', ''.join(e.as_html() for e in Game.emails))
        return page


@route('/')
def index() -> str: return hello('homeslice@phishmail.com')

@route('/hello/<name>')
def hello(name):
    return f'Hello {name}!'

run(host='localhost', port=8080, debug=True)