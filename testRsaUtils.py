from rsaUtils import *

#Testing with pem file
st = "This is a text to test our encrytion and decrytion functions!"
print(st)

test_counter = 0

enc_str = encrypt_with_pem(st.encode(), "ca")
if(st != enc_str):
    print("Encrypted text:")
    print(enc_str)
    print("---Encryption worked well---")
    test_counter+=1
else:
    print("---Encryption did not work, encrypted text and original are the same---")

dec_str = decrypt(enc_str).decode('utf-8')
if(st == dec_str):
    print("Decrypted text:")
    print(dec_str)
    print("---Decryption worked well---")
    test_counter+=1
else:
    print("---Decryption did not work, decrypted text and original are not the same---")

print("")
print("Now testing with database")
print("")

#Testing with database
xmlManager.init()
xmlManager.removeUserFromName("test")
xmlManager.addUser("test", "test", "0987654321", open("ca_crt.pem", 'rt').read())

st = "This is a text to test our encrytion and decrytion functions!"
print(st)

enc_str = encrypt(st.encode(), "test")
if(st != enc_str):
    print("Encrypted text:")
    print(enc_str)
    print("---Encryption worked well---")
    test_counter+=1
else:
    print("---Encryption did not work, encrypted text and original are the same---")

dec_str = decrypt(enc_str).decode('utf-8')

if(st == dec_str):
    print("Decrypted text:")
    print(dec_str)
    print("---Decryption worked well---")
    test_counter+=1
else:
    print("---Decryption did not work, decrypted text and original are not the same---")

print("---Test passed: " + str(test_counter) + "/4---")
