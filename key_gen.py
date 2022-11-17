from simplecrypt import encrypt, decrypt
import random
import string
from db import save_key, select_key

passkey = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50))
try:
    #save_key(passkey)
    print (passkey)
    print("Clave guardada correctamente")
except:
    print("Error al guardad clave")


#print(select_key())
#str1 = 'I am okay'
#cipher = encrypt(str(passkey), str1)
#print(cipher)
#print(decrypt(passkey, cipher).decode())
