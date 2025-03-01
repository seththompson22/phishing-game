from dataclasses import dataclass

@dataclass
class Email:
    name: str
    domain: str
    subject: str
    body: str

    def full_name(self) -> str: ''' combines the name and domain '''; return f'{self.name}@{self.domain}'

