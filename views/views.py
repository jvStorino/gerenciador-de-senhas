import string, secrets, hashlib, base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class Hasher:
    RANDOM_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def _get_random_str(cls, length=25):
        rand_str = ''
        for i in range(length):
            rand_str += secrets.choice(cls.RANDOM_CHARS)
        return rand_str
    
    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_str()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        _file = 'key.key'
        while Path(cls.KEY_DIR / _file).exists():
            _file = f'key{cls._get_random_str(length=5)}.key'

        with open(cls.KEY_DIR / _file, 'wb') as arq:
            arq.write(key)

        return cls.KEY_DIR / _file
    
    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return 'Token inválido'
