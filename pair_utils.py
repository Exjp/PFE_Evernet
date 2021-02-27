import os
import sys
from OpenSSL import crypto
import random

def CA_pair():
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 3072)

    ca_cert = crypto.X509()
    ca_cert.set_version(2)
    ca_cert.set_serial_number(random.randint(50000000,100000000))

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = "CA"

    ca_cert.add_extensions([
        crypto.X509Extension("subjectKeyIdentifier".encode('utf-8'), False, "hash".encode('utf-8'), subject=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension("authorityKeyIdentifier".encode('utf-8'), False, "keyid:always".encode('utf-8'), issuer=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension("basicConstraints".encode('utf-8'), False, "CA:TRUE".encode('utf-8')),
        crypto.X509Extension("keyUsage".encode('utf-8'), False, "keyCertSign, cRLSign".encode('utf-8')),
    ])

    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)
    ca_cert.sign(ca_key, 'sha256')

    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

    with open("ca_crt.pem", "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))

    with open("ca_key.pem", "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))

def client_pair(name):
    str_ca_cert = open("ca_crt.pem", 'rt').read()
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, str_ca_cert)

    str_ca_key = open("ca_key.pem", 'rt').read()
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, str_ca_key)

    req = crypto.X509Req()

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 3072)

    req.set_pubkey(key)
    req.sign(key, 'sha256')

    cert = crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(random.randint(50000000,100000000))

    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(ca_key, 'sha256')

    cert.add_extensions([
        crypto.X509Extension("authorityKeyIdentifier".encode('utf-8'), False, "keyid:always".encode('utf-8'), issuer=ca_cert),
        crypto.X509Extension("extendedKeyUsage".encode('utf-8'), False, "clientAuth".encode('utf-8')),
        crypto.X509Extension("keyUsage".encode('utf-8'), False, "digitalSignature".encode('utf-8')),
    ])

    cert.add_extensions([
        crypto.X509Extension("basicConstraints".encode('utf-8'), False, "CA:FALSE".encode('utf-8')),
        crypto.X509Extension("subjectKeyIdentifier".encode('utf-8'), False, "hash".encode('utf-8'), subject=cert),
    ])

    cert_name = name+"_crt.pem"
    with open(cert_name, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    key_name = name+"_key.pem"
    with open(key_name, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
