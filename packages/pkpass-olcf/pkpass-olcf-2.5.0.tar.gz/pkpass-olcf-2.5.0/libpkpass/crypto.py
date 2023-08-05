#!/usr/bin/env python3
"""This Module handles the crypto functions i.e. encryption and decryption"""
import base64
import tempfile
import os
import hashlib
import shutil
from subprocess import Popen, PIPE, STDOUT, DEVNULL
from pem import parse_file
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from libpkpass.util import color_prepare
from libpkpass.errors import EncryptionError, DecryptionError, SignatureCreationError, X509CertificateError

    ##############################################################################
def handle_python_strings(string):
    """handles py2/3 incompatiblities"""
    ##############################################################################
    if not isinstance(string, bytes):
        string = string.encode("UTF-8")
    return string

    ##############################################################################
def pk_encrypt_string(plaintext_string, certificate):
    """ Encrypt and return a base 64 encoded string for the provided identity"""
    ##############################################################################

    plaintext_derived_key = Fernet.generate_key()
    if isinstance(certificate, bytes):
        with tempfile.NamedTemporaryFile(delete=False) as fname:
            fname.write(certificate)
            cert_file_path = fname.name
    else:
        cert_file_path = certificate['certificate_path']
    command = ['openssl', 'rsautl', '-inkey', cert_file_path, '-certin', '-encrypt', '-pkcs']
    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, _ = proc.communicate(input=plaintext_derived_key)
    if isinstance(certificate, bytes):
        os.unlink(fname.name)

    if proc.returncode != 0:
        raise EncryptionError("Error encrypting derived key: %s" % stdout)
    ciphertext_derived_key = stdout

    fern = Fernet(plaintext_derived_key)
    encrypted_string = fern.encrypt(handle_python_strings(plaintext_string))

    return (encrypted_string, base64.urlsafe_b64encode(handle_python_strings(ciphertext_derived_key)))

    ##############################################################################
def get_card_info():
    ##############################################################################
    command = ['pkcs11-tool', '-L']
    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, _ = proc.communicate()
    return (handle_python_strings(stdout).split(b'Slot'), stdout)

    ##############################################################################
def print_card_info(card_slot, identity, verbosity, color, theme_map):
    """Inform the user what card is selected"""
    ##############################################################################
    if 'key_path' not in identity:
        out_list, stdout = get_card_info()
        if verbosity > 1:
            print_all_slots(stdout, color, theme_map)
        for out in out_list[1:]:
            stripped = out.decode("UTF-8").strip()
            if int(stripped[0]) == int(card_slot):
                verbosity = verbosity + 1 if verbosity < 2 else 2
                stripped = ("\n").join(stripped.split('\n')[:verbosity])
                stripped = "Using Slot" + stripped
                print("%s" % (color_prepare(stripped, "info", color, theme_map)))

    ##############################################################################
def print_all_slots(slot_info, color, theme_map):
    """Print all slots and cards available"""
    ##############################################################################
    columns = int(shutil.get_terminal_size().columns) // 4
    print(color_prepare("#" * columns, "debug", color, theme_map))
    print(handle_python_strings(slot_info).decode("UTF-8").strip())
    print(color_prepare("#" * columns, "debug", color, theme_map))

    ##############################################################################
def pk_decrypt_string(ciphertext_string, ciphertext_derived_key, identity, passphrase, card_slot=None):
    """ Decrypt a base64 encoded string for the provided identity"""
    ##############################################################################
    ciphertext_derived_key = handle_python_strings(ciphertext_derived_key)
    if 'key_path' in identity:
        command = ['openssl', 'rsautl', '-inkey', identity['key_path'], '-decrypt', '-pkcs']
        proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout, _ = proc.communicate(
            input=base64.urlsafe_b64decode(ciphertext_derived_key))
        plaintext_derived_key = stdout
    else:
        # We've got to use pkcs15-crypt for PIV cards, and it only supports pin on
        # command line (insecure) or via stdin.  So, we have to put ciphertext into
        # a file for pkcs15-crypt to read.  YUCK!
        with tempfile.NamedTemporaryFile(delete=False) as fname:
            fname.write(base64.urlsafe_b64decode(ciphertext_derived_key))
        command = ['pkcs15-crypt', '--decipher', '--raw', '--pkcs', '--input', fname.name]
        if card_slot is not None:
            command.extend(['--reader', str(card_slot)])
        command.extend(['--pin', '-'])
        proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate(input=passphrase.encode('UTF-8'))
        os.unlink(fname.name)
        try:
            plaintext_derived_key = stdout
        except IndexError:
            raise DecryptionError(stdout)

    if proc.returncode != 0:
        raise DecryptionError(stdout)

    fern = Fernet(plaintext_derived_key)

    plaintext_string = fern.decrypt(handle_python_strings(ciphertext_string))
    return plaintext_string.decode("UTF-8")

    ##############################################################################
def pk_sign_string(string, identity, passphrase, card_slot=None):
    """ Compute the hash of string and create a digital signature """
    ##############################################################################
    stringhash = hashlib.sha256(string.encode("UTF-8")).hexdigest()
    if 'key_path' in identity:
        command = ['openssl', 'rsautl', '-sign', '-inkey', identity['key_path']]
        proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout, _ = proc.communicate(input=stringhash.encode('UTF-8'))
        signature = base64.urlsafe_b64encode(handle_python_strings(stdout))
    else:
        # We've got to use pkcs15-crypt for PIV cards, and it only supports pin on
        # command line (insecure) or via stdin.  So, we have to put signature text
        # into a file for pkcs15-crypt to read.  YUCK!
        with tempfile.NamedTemporaryFile(delete=False) as fname:
            fname.write(stringhash.encode('UTF-8'))
        out = tempfile.NamedTemporaryFile(delete=False)
        command = ['pkcs15-crypt', '--sign', '-i', fname.name, '-o', out.name, '--pkcs1', '--raw']
        if card_slot is not None:
            command.extend(['--reader', str(card_slot)])
        command.extend(['--pin', '-'])
        proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout, _ = proc.communicate(input=passphrase.encode('UTF-8'))
        out.close()

        with open(out.name, 'rb') as sigfile:
            signature = base64.urlsafe_b64encode(handle_python_strings(sigfile.read()))

        os.unlink(fname.name)
        os.unlink(out.name)

    if proc.returncode != 0:
        raise SignatureCreationError(stdout)

    return signature

    ##############################################################################
def pk_verify_signature(string, signature, identity):
    """ Compute the hash of string and verify the digital signature """
    ##############################################################################
    stringhash = hashlib.sha256(string.encode("UTF-8")).hexdigest()
    for cert in parse_file(identity['certificate_path']):
        with tempfile.NamedTemporaryFile(delete=False) as fname:
            fname.write(cert.as_bytes())
        command = ['openssl', 'rsautl', '-inkey', fname.name, '-certin', '-verify']
        proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout, _ = proc.communicate(input=base64.urlsafe_b64decode(handle_python_strings(signature)))
        os.unlink(fname.name)
        if stdout.decode("UTF-8") == stringhash:
            return True

    return stdout.decode("UTF-8") == stringhash

    ##############################################################################
def pk_verify_chain(certificate, cabundle):
    """ Verify the publickey trust chain against a CA Bundle and return True if valid"""
    ##############################################################################
    command = ['openssl', 'verify', '-CAfile', cabundle]
    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, _ = proc.communicate(input=certificate)

    return stdout.decode("UTF-8").rstrip() == "stdin: OK"

    ##############################################################################
def get_cert_fingerprint(cert):
    """ Return the modulus of the x509 certificate of the identity """
    ##############################################################################
    # SHA1 Fingerprint=F9:9D:71:54:55:BE:99:24:6A:5E:E0:BB:48:F9:63:AE:A2:05:54:98
    return get_cert_element(cert, 'fingerprint').split('=')[1]

    ##############################################################################
def get_cert_subject(cert):
    """ Return the subject DN of the x509 certificate of the identity """
    ##############################################################################
    # subject= /C=US/O=Entrust/OU=Certification Authorities/OU=Entrust Managed Services SSP CA
    return ' '.join(get_cert_element(cert, 'subject').split(' ')[1:])

    ##############################################################################
def get_cert_issuer(cert):
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    # issuer= /C=US/O=Entrust/OU=Certification Authorities/OU=Entrust Managed Services SSP CA
    return ' '.join(get_cert_element(cert, 'issuer').split(' ')[1:])

    ##############################################################################
def get_cert_enddate(cert):
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_cert_element(cert, 'enddate').split('=')[1]

    ##############################################################################
def get_cert_issuerhash(cert):
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_cert_element(cert, 'issuer_hash')

    ##############################################################################
def get_cert_subjecthash(cert):
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_cert_element(cert, 'subject_hash')

    ##############################################################################
def get_cert_element(cert, element):
    """ Return an arbitrary element of an x509 certificate """
    ##############################################################################
    command = ['openssl', 'x509', '-noout', ("-%s" % element)]
    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, _ = proc.communicate(input=cert)
    if proc.returncode != 0:
        raise X509CertificateError(stdout)

    try:
        return stdout.decode("UTF-8").rstrip()
    except IndexError:
        raise X509CertificateError(stdout)

    ##############################################################################
def get_card_element(element):
    """Return an arbitrary element of a pcks15 capable device"""
    ##############################################################################
    command = ['pkcs15-tool', '--read-certificate', '1']
    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, _ = proc.communicate()
    if stdout.decode('utf-8').strip().lower() == 'no smart card readers found.':
        raise X509CertificateError('Smartcard not detected')
    return get_cert_element(stdout, element)

    ##############################################################################
def get_card_fingerprint():
    """ Return the modulus of the x509 certificate of the identity """
    ##############################################################################
    # SHA1 Fingerprint=F9:9D:71:54:55:BE:99:24:6A:5E:E0:BB:48:F9:63:AE:A2:05:54:98
    return get_card_element('fingerprint').split('=')[1]

    ##############################################################################
def get_card_subject():
    """ Return the subject DN of the x509 certificate of the identity """
    ##############################################################################
    # subject= /C=US/O=Entrust/OU=Certification Authorities/OU=Entrust Managed Services SSP CA
    return ' '.join(get_card_element('subject').split(' ')[1:])

    ##############################################################################
def get_card_issuer():
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    # issuer= /C=US/O=Entrust/OU=Certification Authorities/OU=Entrust Managed Services SSP CA
    return ' '.join(get_card_element('issuer').split(' ')[1:])

    ##############################################################################
def get_card_startdate():
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_card_element('startdate').split('=')[1]

    ##############################################################################
def get_card_enddate():
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_card_element('enddate').split('=')[1]

    ##############################################################################
def get_card_issuerhash():
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_card_element('issuer_hash')

    ##############################################################################
def get_card_subjecthash():
    """ Return the issuer DN of the x509 certificate of the identity """
    ##############################################################################
    return get_card_element('subject_hash')

    ##############################################################################
def sk_encrypt_string(plaintext_string, key):
    """ Symmetrically Encrypt and return a base 64 encoded string using the provided secret"""
    ##############################################################################
    fern = Fernet(hash_password(key))
    encrypted_string = fern.encrypt(plaintext_string.encode('UTF-8'))
    return base64.urlsafe_b64encode(handle_python_strings(encrypted_string))

    ##############################################################################
def sk_decrypt_string(ciphertext_string, key):
    """ Symmetrically Decrypt a base64 encoded string using the provided key"""
    ##############################################################################
    fern = Fernet(hash_password(key))
    ciphertext_string = handle_python_strings(ciphertext_string)
    try:
        plaintext_string = fern.decrypt(base64.urlsafe_b64decode(handle_python_strings(ciphertext_string)))
        return plaintext_string.decode("UTF-8")
    except InvalidToken:
        # handle some legacy stuff from NCCS
        try:
            plaintext_string = fern.decrypt(ciphertext_string)
            return plaintext_string.decode("UTF-8")
        except InvalidToken:
            raise DecryptionError("Incorrect Password")

    ##############################################################################
def hash_password(password):
    """Hash people's password"""
    ##############################################################################
    password = handle_python_strings("%s" % password)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"salt",
                     iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(handle_python_strings(kdf.derive(password)))
