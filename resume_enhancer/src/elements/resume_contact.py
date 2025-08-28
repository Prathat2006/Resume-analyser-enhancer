
class Contact:
    def __init__(self):
        self.email = ''
        self.phone = ''
        self.location = ''
        self.linkedIn = ''
        self.github = ''
    ...
        
    def set_email(self, email : str) -> None:
        self.email = email
        
    def set_phone(self, phone : str) -> None:
        self.phone = phone
        
    def set_location(self, location : str) -> None:
        self.location = location

    def set_linkedIn(self, linkedIn : str) -> None:
        self.linkedIn = linkedIn

    def set_github(self, github : str) -> None:
        self.github = github