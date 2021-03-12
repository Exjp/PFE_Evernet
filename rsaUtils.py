from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as cipher_algorithm
from OpenSSL import crypto
import base64
import xmlManager

def encrypt_with_pem(data, pseudo):
    certPath = pseudo+"_crt.pem"
    str_cert = open(certPath, 'rt').read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, str_cert)
    pKey = cert.get_pubkey()
    pKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pKey)
    public = RSA.importKey(pKeyString)

    cipher = cipher_algorithm.new(public)
    cipher_text = cipher.encrypt((data).encode())
    signed = base64.b64encode(cipher_text)

    return signed

def encrypt(data, pseudo):
    str_cert = xmlManager.getKeyFromAlias(pseudo)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, str_cert)
    pKey = cert.get_pubkey()
    pKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pKey)
    public = RSA.importKey(pKeyString)

    cipher = cipher_algorithm.new(public)
    cipher_text = cipher.encrypt((data).encode())
    signed = base64.b64encode(cipher_text)

    return signed

def decrypt(cipherText):
    keyPath = "ca_key.pem"
    with open(keyPath,'rb') as fk:
    	priv = fk.read()
    	fk.close()
    privat = RSA.importKey(priv)

    cipher = base64.b64decode(cipherText)
    pr = cipher_algorithm.new(privat)
    x = pr.decrypt(cipher, "error")
    x = x.decode('utf-8')

    return x

def decrypt_with_file(cipherText, pseudo):
    keyPath = pseudo+"_key.pem"
    with open(keyPath,'rb') as fk:
    	priv = fk.read()
    	fk.close()
    privat = RSA.importKey(priv)

    cipher = base64.b64decode(cipherText)
    pr = cipher_algorithm.new(privat)
    x = pr.decrypt(cipher, "error")
    print(x)
    x = x.decode('utf-8')

    return x
