from bottle import route, run, static_file
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

    def as_js_dict(self) -> str:
        return f'"{self.subject}": "{self.body.replace('"', '\\"')}"'

    def as_html(self) -> str:
        preview = self.body
        for punc in ('.', '!', '?'):
            if punc in preview: preview = preview[0:preview.index(punc)]
        return f"""
<div class="email">
    <div class="email-buttons">
        <button class="archive-button">Archive</button>
        <button class="delete-button">Delete</button>
    </div>
    <div class="email-content">
        <div class="email-sender">{self.name} | {self.address}</div>
        <div class="email-subject">{self.subject}</div>
        <div class="email-preview">{preview}...</div>
    </div>
</div>"""

class Game:
    day: int = 1
    emails: list[Email] = [
        Email('Waluigi', 'waluigi@nintendo.com', 'I wanna wah with you', 'Let\'s go wahing in park on tuesday!', {'fakeperson'}, True),
        Email('Wario', 'wario@nintendo.com', 'She WAH', 'Now I\'m gonna wah with you, you have no choice in the matter.', {'fakeperson'}, True),
        # Email('Twilight Sparkle', 'tsparkle@mylittlepony.gov', 'Friendship', 'THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY <a href="givememoney.gov">donate today</a>THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY ', {'fakeperson'}, True),
    ]
    
    @classmethod 
    def new_day(cls) -> None:
        '''Every day a day passes, the day increases by one'''
        day += 1

    @classmethod
    def generate_emails(cls) -> None:
        ''' Fills the emails list with random emails '''
        cls.emails.clear()
        cls.emails.append(cls.make_email()) # force phishing
        for _ in range(cls.day - 1): cls.emails.append(cls.make_email())
        shuffle(cls.emails)
    
    @classmethod
    def make_email(cls) -> Email:
        ''' Generates an email using Gemini and returns an Email object. '''
        # check if returned email should be hardcoded or generated
        if not randint(0, 99):
            return rchoice([  # random email
                Email('Waluigi', 'waluigi@nintendo.com', 'I wanna wah with you', 'Let\'s go wahing in park on tuesday!', {'fakeperson'}, True),
                Email('Wario', 'wario@nintendo.com', 'I wanna wah with you', 'Let\'s go wahing in park on tuesday!', {'fakeperson'}, True),
                Email('Twilight Sparkle', 'tsparkle@mylittlepony.gov', 'Friendship', 'THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY <a href="givememoney.gov">donate today</a>', {'fakeperson'}, True),
                ## Add more emails
            ])

        # Call the Gemini function to generate an email
        user_name = "John Smith"  # Replace with dynamic data if needed
        acceptable_emails = ["support@company.com", "hr@company.com"]  # Replace with your list
        model_name = "gemini-1.5-flash"  # Replace with your model name

        raw_response = generate_email_with_gemini(user_name, acceptable_emails, model_name)

        # Step 1: Remove the Markdown code block markers (if present)
        cleaned_response = raw_response.strip("```json\n").rstrip("```").strip()

        # Step 2: Parse the cleaned JSON
        try:
            email_data_list = json.loads(cleaned_response)  # This is a list of dictionaries
            print("Parsed JSON:", email_data_list)

            # Select the first email from the list
            email_data = email_data_list[0]  # Select the first dictionary
        except (json.JSONDecodeError, IndexError) as e:
            print("Failed to parse JSON or select email:", e)
            print("Raw Response:", raw_response)
            raise e  # Re-raise the exception to stop further execution

        # Create an instance of the Email class
        email = Email(
            name=email_data["name"],
            address=email_data["address"],
            subject=email_data["subject"],
            body=email_data["body"],
            flags=email_data["checks"],
            is_phish=email_data["is_phish"]
        )
        print("Generated Email:", email)
        print("Parsed JSON:", email_data_list)  # Print the parsed JSON data
        return email

    @classmethod
    def new_address(cls) -> Email: ''' Gemini creates a random address.'''


@route('/img/<filename>')
def server_static(filename) -> str:
     ''' Get images '''
     return static_file(filename, root='images/')


@route('/')
def index() -> str:
    ''' Loading page '''
    with open('htmlpages/login.html') as file: page = ''.join(file.readlines())
    return page


@route('/inbox')
def inbox():
    with open('htmlpages/inbox.txt') as template: page = ''.join(template.readlines())
    page = page.replace('EMAILSEMAILSEMAILSEMAILS', ''.join(e.as_html() for e in Game.emails))
    page = page.replace('EMAILDICTEMAILDICTEMAILDICT', ',\n\t\t\t'.join(e.as_js_dict() for e in Game.emails))
    return page


@route('/browser')
def browser():
    with open('htmlpages/browser.txt') as template: page = ''.join(template.readlines())
    return page


@route('/info')
def info():
    with open('htmlpages/info.txt') as template: page = ''.join(template.readlines())
    return page



# Generate emails for the game
# Game.generate_emails()

# Run the server
run(host='localhost', port=8080, debug=True)