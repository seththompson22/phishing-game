from bottle import route, run, static_file
from random import shuffle
from dataclasses import dataclass
from gemini import generate_email_with_gemini
from random import randint as rint, choice as rchoice, sample as rsample
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
        return '"SUB": "BODY"'\
            .replace('SUB', self.subject)\
            .replace('BODY', self.body\
                .replace('"', '\\"')\
                .replace('\n', '<br/>')
            ) 

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
    day: int = 0
    valid_emails: dict[str, tuple[str]] = {
        'Wells Fargo': ('alerts@wellsfargo.com',),
        'Carl Weezer': ('weezing@carl.com', 'carl@wheezer.org'),
        'Amazon Orders': ('order-update@amazon.com', 'shipment@amazon.com'),
        'LinkedIn Notifications': ('notifications-noreply@linkedin.com',),
        'GitHub Updates': ('noreply@github.com',),
        'Netflix Account': ('noreply@netflix.com', 'account@netflix.com'),
        'Spotify Listeners': ('noreply@spotify.com',),
        'Google Account': ('no-reply@accounts.google.com', 'security-alert@accounts.google.com'),
        'Apple ID': ('appleid@id.apple.com',),
        'Microsoft Account': ('account-security-noreply@accountprotection.microsoft.com',),
        'Facebook Notifications': ('notification@facebookmail.com',),
        'Twitter (X) Updates': ('noreply@mail.x.com',),
        'Instagram Updates': ('mail@instagram.com',),
        'Paypal Transactions': ('service@paypal.com', 'transaction@paypal.com'),
        'Ebay Purchases': ('ebay@ebay.com',),
        'Zoom Meetings': ('no-reply@zoom.us',),
        'Slack Notifications': ('feedback@slack.com', 'notifications@slack.com'),
        'Handshake Notifications': ('notifications@joinhandshake.com',),
        'LinkedIn Messages': ('messages-noreply@linkedin.com',),
        'Walmart Grocery': ('no-reply@walmartgrocery.com', 'orders@walmartgrocery.com'),
        'Kroger Grocery': ('noreply@kroger.com', 'myaccount@kroger.com'),
        'Aldi Grocery': ('noreply@aldi.us', 'feedback@aldi.us'),
        'Target Grocery': ('targetgrocery@target.com', 'order@target.com'),
        'Instacart': ('noreply@instacart.com', 'support@instacart.com'),
        'Whole Foods Market': ('orders@wholefoodsmarket.com', 'noreply@wholefoodsmarket.com'),
        'Trader Joe\'s': ('noreply@traderjoes.com',), #Trader Joe's is known to have very little email presence.
        'Local Grocery Store': ('orders@localgrocerystore.com', 'info@localgrocerystore.com') #Replace with a real local store
    }
    emails: list[Email] = [
        Email('Waluigi', 'waluigi@nintendo.com', 'I wanna wah with you', 'Let\'s go wahing/n in park on tuesday!', {'fakeperson'}, True),
        Email('Wario', 'wario@nintendo.com', 'She WAH', 'Now I\'m gonna wah with you, you have no choice in the matter.', {'fakeperson'}, True),
        Email('Carl Wheezer', 'carl@wheezer.ne', 'Excuse me', 'Can i have that croissant', {'fakeperson'}, True)
        # Email('Twilight Sparkle', 'tsparkle@mylittlepony.gov', 'Friendship', 'THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY <a href="givememoney.gov">donate today</a>THE POWER OF FRIENDSHIP COMPELS YOU TO GIVE ME MONEY ', {'fakeperson'}, True),
    ]

    @classmethod
    def generate_emails(cls) -> None:
        ''' Fills the emails list with random emails '''
        cls.emails.append(Email('Dev Team', 'supercoolawesomepeople.gov', 'Helpful info', "Hello! Welcome to Phish Mail, the digital post office that tests your email expertise that increases in difficulty as time passes. The game is simple, read your inbox and determine if each email is fake or fact. Click an email, read it, and click the archive button if it’s real, or delete it if they’re phishing. Click the website tab to view any link that you find in an email and utilize the info tab to find confirmed information about the companies that may be trying to contact you to see if they’re legit or not. Climb your way through the days, confirming that you are the ultimate anti phisher. Happy reading! <br/><br/>Dev team", {}, False))
        cls.emails.extend(cls.make_email_batch(cls.day))  # Generate a batch of emails
        shuffle(cls.emails)
    
    @classmethod
    def next_day(cls) -> None:
        ''' Increases the day by 1 every time Next Day is clicked'''
        cls.day += 1

    @classmethod
    def make_email_batch(cls, number_of_emails: int) -> list[Email]:
        """Generates a batch of Email objects.

        Args:
            number_of_emails (int): The number of emails to generate.

        Returns:
            list[Email]: A list of Email objects.
        """

        todays_email_keys = cls.get_todays_valid_email_keys(cls.day)
        todays_valid_emails = [email for key in todays_email_keys for email in cls.valid_emails[key]]
        print(todays_valid_emails)

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
                "John Smith", todays_valid_emails, "gemini-2.0-flash-lite", number_of_emails
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
    def spoofify_address(cls, email: Email) -> Email: 
        ''' Gemini creates a random spoofed address.'''

        parts = email.split('@')
        if len(parts) != 2:
            return email  # Return original if invalid format

        local_part, domain = parts

        # Common spoofing techniques:
        methods = [
            lambda lp, d: f"{lp}.{rint(1, 100)}@{d}",  # Add a dot and random number
            lambda lp, d: f"{lp[1] if len(lp) > 1 else lp}{rchoice(['-', '_'])}update@{d}", # Add a - or _ followed by a word like update.
            lambda lp, d: f"{lp}{rchoice(['.', '_', '-'])}{rchoice(['verify', 'alert', 'info'])}@{d}", # Add a separator and a common word
            lambda lp, d: f"{lp}{rint(10, 99)}@{d}",  # Add a few digits
            lambda lp, d: f"{lp.replace('o', '0').replace('l', '1')}@{d}",  # Common character replacements
            lambda lp, d: f"{''.join(rsample(lp, len(lp)))}@{d}" if len(lp)>3 else f"{lp}@{d}", #Scramble the local part.
            lambda lp, d: f"{lp}{rchoice(['.net', '.org', '.co'])}@{d.replace('.com', '')}{rchoice(['.net', '.org', '.co'])}", # Change TLDs
            lambda lp, d: f"{lp}@{d.replace('.com', '.co')}" # change .com to .co
        ]

        method = rchoice(methods)
        spoofed_email = method(local_part, domain)

        return spoofed_email
    
    @classmethod
    def get_todays_valid_email_keys(cls, number_of_emails: int) -> list[str]:
        ''' Returns a list of [str, tuple(str)] for the day '''
        # Get a random sample of valid emails
        valid_emails = [email for email in cls.valid_emails.keys()]
        print(valid_emails)
        todays_email_keys = rsample(valid_emails, number_of_emails)
        print(todays_email_keys)
        return todays_email_keys

    


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
    page = page.replace('ISPHISHISPHISHISPHISH', ',\n\t\t\t'.join(f'"{e.subject}": true' if e.is_phish else f'"{e.subject}": false' for e in Game.emails))
    page = page.replace('DAYDAYDAYDAY', str(Game.day))
    return page

@route('/browser')
def browser():
    with open('htmlpages/browser.txt') as template: page = ''.join(template.readlines())
    page = page.replace('DAYDAYDAYDAY', str(Game.day))
    return page


@route('/info')
def info():
    with open('htmlpages/info.txt') as template: page = ''.join(template.readlines())
    page = page.replace('DAYDAYDAYDAY', str(Game.day))
    return page

@route('/nextday')
def nextday():
    Game.next_day()
    Game.generate_emails()
    return inbox()


# Generate emails for the game
Game.generate_emails()

# Run the server
run(host='localhost', port=8080, debug=True)