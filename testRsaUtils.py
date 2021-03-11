from rsaUtils import *

st = "This is a text to test our encrytion and decrytion functions!"
print(st)

test_counter = 0

enc_str = encrypt(st, 'test_crt.pem')
if(st != enc_str):
    print("Encrypted text:")
    print(enc_str)
    print("---Encryption worked well---")
    test_counter+=1
else:
    print("---Encryption did not work, encrypted text and original are the same---")

dec_str = decrypt(enc_str, 'test_key.pem')

if(st == dec_str):
    print("Decrypted text:")
    print(dec_str)
    print("---Decryption worked well---")
    test_counter+=1
else:
    print("---Decryption did not work, decrypted text and original are not the same---")


print("---Test passed: " + str(test_counter) + "/2---")
