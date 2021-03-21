from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as cipher_algorithm
from OpenSSL import crypto
import base64
import xmlManager


def encrypt_with_pem(data, pseudo):
    """Encrypt data using a certificate file named <pseudo>_crt.pem

    Args:
        data (bytes) : data to be encrypt
        pseudo (string) : pseudo of the message recipient
    Returns:
        string : data encrypted and encoded in base64
    """
    certPath = pseudo+"_crt.pem"
    str_cert = open(certPath, 'rt').read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, str_cert)
    pKey = cert.get_pubkey()
    pKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pKey)
    public = RSA.importKey(pKeyString)

    cipher = cipher_algorithm.new(public)
    cipher_text = cipher.encrypt(data)#.encode())
    signed = base64.b64encode(cipher_text)

    return signed

def encrypt(data, pseudo):
    """Encrypt data using a certificate from the database.

    Args:
        data (bytes) : data to be encrypt
        pseudo (string) : pseudo of the message recipient
    Returns:
        string : data encrypted and encoded in base64
    """
    str_cert = xmlManager.getKeyFromAlias(pseudo)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, str_cert)
    pKey = cert.get_pubkey()
    pKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pKey)
    public = RSA.importKey(pKeyString)

    cipher = cipher_algorithm.new(public)
    cipher_text = cipher.encrypt(data)
    signed = base64.b64encode(cipher_text)

    return signed

def decrypt(cipherText):
    """Decrypt a cyphertext using CA private key (only for CA).

    Args:
        cipherText (string) : string to be decrypt
    Returns:
        bytes : string decrypted
    """
    keyPath = "ca_key.pem"
    with open(keyPath,'rb') as fk:
    	priv = fk.read()
    	fk.close()
    privat = RSA.importKey(priv)

    cipher = base64.b64decode(cipherText)
    pr = cipher_algorithm.new(privat)
    x = pr.decrypt(cipher, "error")

    return x

def decrypt_with_file(cipherText, pseudo):
    """Decrypt a cyphertext using a private key file named <pseudo>_key.pem.

    Args:
        cipherText (string) : string to be decrypt
        pseudo (string): pseudo of the message recipient
    Returns:
        bytes : string decrypted
    """
    keyPath = pseudo+"_key.pem"
    with open(keyPath,'rb') as fk:
    	priv = fk.read()
    	fk.close()
    privat = RSA.importKey(priv)

    cipher = base64.b64decode(cipherText)
    pr = cipher_algorithm.new(privat)
    x = pr.decrypt(cipher, "error")
    #print(x)
    #x = x.decode('utf-8')

    return x
