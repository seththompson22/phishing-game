from bottle import route, run
from random import shuffle
from dataclasses import dataclass
from gemini import generate_email_with_gemini
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
        if '.' in preview: preview = preview[0:preview.index('.')]
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
        for _ in range(cls.day - 1): cls.emails.append(cls.make_email())
        shuffle(cls.emails)
    
    @classmethod
    def make_email(cls) -> Email: 
        ''' Generates an email using Gemini and returns an Email object. '''
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
        return email
    
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
    return page.replace('EMAILSEMAILSEMAILSEMAILS', ''.join(e.as_html() for e in Game.emails))


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