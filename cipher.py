# Run from same working directory with: `python3 cipher.py`

# Install `cryptography` with: `pip3 install cryptography`

import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

bold = '\033[1m'
underline = '\033[4m'
end = '\033[0m'


def keyGen():
    print('\nFiles will be encrypted using a public key and can only be')
    print('decrypted using the relevant private key')

    print('\nYou should share your public key with people who should be')
    print('able to encrypt files for you to receive')

    print(bold + '\nDO NOT SHARE YOUR PRIVATE KEY')

    print('\n**WARNING**: THIS WILL OVERWRITE PRE-EXISTING KEYS IN THE')
    print('CURRENT WORKING DIRECTORY' + end)

    response = input('\nDo you understand [Y/n]: ').lower()
    if response != 'y':
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )
    public_key = private_key.public_key()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
        )

    with open('private_key.pem', 'wb') as f:
        f.write(pem)

    print('\nPrivate key saved to: ' + bold + 'private_key.pem' + end)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    with open('public_key.pem', 'wb') as f:
        f.write(pem)

    print('\nPublic key saved to: ' + bold + 'public_key.pem' + end + '\n')


def encrypt(file):
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    f = open(file, 'rb')
    message = f.read()
    f.close()

    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    writeFile = file.replace('.txt', '.encrypted')

    f = open(writeFile, 'wb')
    f.write(encrypted)
    f.close()

    print('\nEncrypted file saved as: ' + bold + writeFile + end + '\n')


def decrypt(file):
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    f = open(file, 'rb')
    message = f.read()
    f.close()

    decrypted = private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    writeFile = file.replace('.encrypted', '.txt')

    f = open(writeFile, 'wb')
    f.write(decrypted)
    f.close()

    print('\nDecrypted file saved as: ' + bold + writeFile + end + '\n')


def selectionMenu():
    print('\nWelcome to the file encrypter/decrypter')
    print('You will need a public and private key')
    print('These are necessary for encryption and decryption\n')

    print(underline + 'Options:' + end)
    print(bold + '[1] ' + end + 'Encryption')
    print(bold + '[2] ' + end + 'Decryption')
    print(bold + '[3] ' + end + 'Key generation')

    response = int(input('\nChoose an option (1-3): '))
    if response == 1:
        file = input('\nInput name of .txt file to encrypt: ')
        if file.split('.')[-1] != 'txt':
            print('File type not supported, choose a .txt file')
            selectionMenu()
        encrypt(file)
    elif response == 2:
        file = input('\nInput name of file to decrypt: ')
        if file.split('.')[-1] != 'encrypted':
            print('File type not supported, choose a .encrypted file')
            selectionMenu()
        decrypt(file)
    elif response == 3:
        keyGen()
    else:
        print('Invalid choice, select an option 1-3')
        selectionMenu()


selectionMenu()
