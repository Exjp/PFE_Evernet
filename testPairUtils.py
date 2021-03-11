from pairUtils import *
import time

test_counter = 0

try:
    CA_pair()
    print("---Successfully generated CA pair---")
    test_counter+=1
except:
    print("---Unable to generate CA pair---")

try:
    client_pair("test")
    print("---Successfully generated client pair---")
    test_counter+=1
except:
    print("---Unable to generate client pair---")

time.sleep(1)

if (verify_certificate("test_crt.pem", ["ca_crt.pem"]) == True):
    print("---Test failed: the function returned True while the certificate was not in the trusted list---")
else:
    print("---Successfully returned False when the certificate was not in the trusted list---")
    test_counter+=1

if (verify_certificate("test_crt.pem", ["ca_crt.pem","test_crt.pem"]) == True):
    print("---Successfully returned True when the certificate was in the trusted list---")
    test_counter+=1
else:
    print("---Test failed: the function returned False while the certificate was in the trusted list---")


print("---Test passed: [" + str(test_counter) + "/4]---")
