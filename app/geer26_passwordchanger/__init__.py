"""
TODOS:
1. import living fernet objects
2. create passwordlist
3. create temp fernet objects and choose randomly
4. change in daabase with new password
5. make full db save with new password
6. overwrite existing app fernet objects
7. overwrite dotenv secrets
"""

from random import SystemRandom


def generate_rnd(N=32):

    chars = ''
    for i in range(33,127):
        chars += chr(i)

    # Generates N lenght random text and returns it
    return ''.join(
        SystemRandom().choice(chars) for _ in
        range(N))


class Passwordchanger:

    def __init__(self, **kwargs):
        self. oldfernets = None
        self.password_list = None
        self.password_length = None
        self.secrets = None
        self.new_secrets = None
        return


    def init_app(self, **kwargs):

        if 'password_length' in kwargs:
            self.password_length = int(kwargs.get('password_length'))
        else:
            self.password_length = 32

        if 'password_list' in kwargs:
            self.password_list = kwargs.get('password_list')
        else:
            self.password_list = self.generate_passwords(iterates=1000)

        if 'secrets' in kwargs:
            self.secrets = kwargs.get('secrets')
        else:
            self.secrets = []

        if 'new_secrets' in kwargs:
            self.new_secrets = kwargs.get('new_secrets')
        else:
            self.new_secrets = []
            #TODO fill this according to the secrets length

        return 0

    def generate_passwords(self, **kwargs):
        if 'iterates' in kwargs:
            iterates = int(kwargs.get('iterates'))
        else: iterates = 1000
        pwlist = []

        for i in range(iterates):
            pwlist.append(generate_rnd(N=32))

        return pwlist

