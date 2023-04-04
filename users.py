class Users:

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password
        self.poster = None

    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email

