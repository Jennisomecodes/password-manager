import os, json, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag

VAULT_FILE = "vault.enc"

def b64e(b): return base64.b64encode(b).decode()
def b64d(s): return base64.b64decode(s)

def derive_key(master, salt):
    return Scrypt(salt=salt, length=32, n=2**15, r=8, p=1).derive(master.encode())

def save_vault(data, master):
    salt, nonce = os.urandom(16), os.urandom(12)
    key = derive_key(master, salt)
    ct = AESGCM(key).encrypt(nonce, json.dumps(data).encode(), None)
    with open(VAULT_FILE, "w") as f:
        json.dump({"salt": b64e(salt), "nonce": b64e(nonce), "ct": b64e(ct)}, f)

def load_vault(master):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE) as f:
        blob = json.load(f)
    key = derive_key(master, b64d(blob["salt"]))
    try:
        pt = AESGCM(key).decrypt(b64d(blob["nonce"]), b64d(blob["ct"]), None)
    except InvalidTag:
        raise ValueError("Wrong master password or vault was tampered with.")
    return json.loads(pt)
