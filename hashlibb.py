import hashlib
import sqlite3
def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_pw_hash(password,hash):
    if make_pw_hash(password) == hash:
        return True
    else:
        return False


sqlite3.connect('')