from bottle import route, run
from random import shuffle
from dataclasses import dataclass
from gemini import generate_email_with_gemini
from random import randint, choice as rchoice
import json

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
        for punc in ('.', '!', '?'):
            if punc in preview: preview = preview[0:preview.index(punc)]
        return f"""
<a href="https://example.com/email/2" class="email">
    <div class="email-buttons">
        <button class="archive-button">Archive</button>
        <button class="delete-button">Delete</button>
    </div>
    <div class="email-content">
        <div class="email-sender">{self.name} | {self.address}</div>
        <div class="email-subject">{self.subject}</div>
        <div class="email-preview">{preview}...</div>
    </div>
</a>"""

class Game:
    day: int = 1
    emails: list[Email] = [Email('waluigi', 'waluigi@nintendo.com', 'free waluigi games', 'WAH. WAH WAH WAH WAH WAH WAH WAH WAH WAH. WAHWFAWFAWOFAORNWAORNONAWROAWJEDNAWON', {}, True)]
    times_phished: int = 0

    @classmethod
    def generate_emails(cls) -> None:
        ''' Fills the emails list with random emails '''
        cls.emails.clear()
        cls.make_email_batch(cls.day - 1)  # Generate a batch of emails
        shuffle(cls.emails)
    
    @classmethod
    def make_email_batch(cls, number_of_emails: int) -> list[Email]:
        """Generates a batch of Email objects.

        Args:
            number_of_emails (int): The number of emails to generate.

        Returns:
            list[Email]: A list of Email objects.
        """

        emails = []
        fallback_email = Email(
            name="IT Support",
            address="support@company.com",
            subject="Password Reset Required",
            body="Dear user, please reset your password using this link: reset-password.com",
            flags={"grammar": "high", "spelling": "high", "time": "any", "links": "suspicious"},
            is_phish=True
        )

        try:
            raw_response = generate_email_with_gemini(
                "John Smith", ["support@company.com", "hr@company.com"], "gemini-2.0-flash-lite", number_of_emails
            )

            if raw_response:
                # Attempt to parse and create Email objects
                try:
                    lines = raw_response.strip().split('\n')
                    for line in lines:
                        parts = line.split('|')
                        if len(parts) == 9:
                            try:
                                email = Email(
                                    name=parts[0],
                                    address=parts[1],
                                    subject=parts[2],
                                    body=parts[3],
                                    flags={
                                        "grammar": parts[4],
                                        "spelling": parts[5],
                                        "time": parts[6],
                                        "links": parts[7]
                                    },
                                    is_phish=parts[8].lower() == 'true'
                                )
                                emails.append(email)
                            except Exception as e:
                                print(f"Error parsing line: {line}, error: {e}")

                except (json.JSONDecodeError, IndexError, KeyError) as e:
                    print("Failed to parse JSON or create Email object:", e)
                    print("Raw Response:", raw_response)
                    # Add fallback email if any parsing or creation error occurs
                    emails.append(fallback_email)
            else:
                print("API returned an empty response. Using fallback email.")
                emails.append(fallback_email)

        except Exception as e:
            print("Error generating emails:", e)
            # Add fallback email if any other error occurs
            emails.append(fallback_email)

        return emails

    @classmethod
    def new_address(cls) -> Email: ''' Gemini creates a random address.'''


@route('/')
def index() -> str:
    ''' Loading page '''
    with open('htmlpages/login.html') as file: page = ''.join(file.readlines())
    return page


@route('/inbox')
def inbox():
    with open('htmlpages/inbox.txt') as template: page = ''.join(template.readlines())
    return page.replace('EMAILSEMAILSEMAILSEMAILSEMAILSEMAILSEMAILSEMAILSEMAILS', ''.join(e.as_html() for e in Game.emails))


@route('/browser')
def browser():
    with open('htmlpages/browser.txt') as template: page = ''.join(template.readlines())
    return page


@route('/info')
def info():
    with open('htmlpages/info.txt') as template: page = ''.join(template.readlines())
    return page



# Generate emails for the game
Game.generate_emails()

# Run the server
run(host='localhost', port=8080, debug=True)