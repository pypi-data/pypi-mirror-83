import base64
import io
import json
import logging
from functools import wraps
from os import path

import click
import googleapiclient.discovery
from flask import Response, request

from .storage import StorageClient

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


fboxx_usr_ring_file = path.join('flowerboxx', 'rlz_usrs_ring.txt')
fboxx_pwd_ring_file = path.join('flowerboxx', 'rlz_pwds_ring.txt')

usr_ring_file = path.join('usr_ring.txt')
pwd_ring_file = path.join('pw_ring.txt')

cloud_storage = StorageClient()
cloud_storage.download_file(
    'apifiles', 'usr_ring.txt', usr_ring_file)
cloud_storage.download_file(
    'apifiles', 'pw_ring.txt', pwd_ring_file)


def check_auth(username, password, project_id):
    """This function is called to check if a username /
    password combination is valid.
    """

    usr = decrypt(project_id, 'europe-west4', 'boxx_keys', 'creds',
                  usr_ring_file)
    pwd = decrypt(project_id, 'europe-west4', 'boxx_keys', 'creds',
                  pwd_ring_file)
    return username == usr and password == pwd


def add_user(username, password, store, project_id, edit=False, debug=False):
    cloud_storage.download_file(
        'flowerboxx', 'rlz_usrs_ring.txt', fboxx_usr_ring_file)
    cloud_storage.download_file(
        'flowerboxx', 'rlz_pwds_ring.txt', fboxx_pwd_ring_file)

    usrs = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              fboxx_usr_ring_file))
    pwds = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              fboxx_pwd_ring_file))
    if debug:
        with open('dummy_creds.json') as f:
            dummy_creds = json.load(f)

        if edit and store not in dummy_creds['pwds']:
            return False
        else:
            dummy_creds['pwds'].update({store: password})
            dummy_creds['usrs'].update({store: username})
            with open('dummy_creds.json', 'w') as outfile:
                json.dump(dummy_creds, outfile)
            return True

    if edit and store not in pwds:
        return False

    pwds.update({store: password})
    usrs.update({store: username})
    encrypt(project_id, 'europe-west4', 'reeleezee',
            'creds', json.dumps(usrs), fboxx_usr_ring_file)

    encrypt(project_id, 'europe-west4', 'reeleezee',
            'creds', json.dumps(pwds), fboxx_pwd_ring_file)

    cloud_storage.upload_file(
        'flowerboxx', 'rlz_usrs_ring.txt', fboxx_usr_ring_file)
    cloud_storage.upload_file(
        'flowerboxx', 'rlz_pwds_ring.txt', fboxx_pwd_ring_file)
    return True


def remove_user(store, project_id, debug=False):
    cloud_storage.download_file(
        'flowerboxx', 'rlz_usrs_ring.txt', fboxx_usr_ring_file)
    cloud_storage.download_file(
        'flowerboxx', 'rlz_pwds_ring.txt', fboxx_pwd_ring_file)

    usrs = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              fboxx_usr_ring_file))
    pwds = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              fboxx_pwd_ring_file))
    if debug:
        with open('dummy_creds.json') as f:
            dummy_creds = json.load(f)
        import pdb
        pdb.set_trace()
        if store not in dummy_creds['pwds']:
            return False
        else:
            del dummy_creds['pwds'][store]
            del dummy_creds['usrs'][store]
            with open('dummy_creds.json', 'w') as outfile:
                json.dump(dummy_creds, outfile)
            return True

    if store not in pwds:
        return False

    del pwds[store]
    del usrs[store]
    encrypt(project_id, 'europe-west4', 'reeleezee',
            'creds', json.dumps(usrs), fboxx_usr_ring_file)

    encrypt(project_id, 'europe-west4', 'reeleezee',
            'creds', json.dumps(pwds), fboxx_pwd_ring_file)

    cloud_storage.upload_file(
        'flowerboxx', 'rlz_usrs_ring.txt', fboxx_usr_ring_file)
    cloud_storage.upload_file(
        'flowerboxx', 'rlz_pwds_ring.txt', fboxx_pwd_ring_file)
    return True


def change_id(caseid, store, project_id):
    usrs = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              'flowerboxx/rlz_usrs_ring.txt'))
    pwds = json.loads(decrypt(project_id,
                              'europe-west4',
                              'reeleezee', 'creds',
                              'flowerboxx/rlz_pwds_ring.txt'))

    pwds.update({caseid: pwds[store]})
    usrs.update({caseid: usrs[store]})

    encrypt(project_id,
            'europe-west4',
            'reeleezee', 'creds', json.dumps(usrs),
            'flowerboxx/rlz_usrs_ring.txt')

    encrypt(project_id,
            'europe-west4',
            'reeleezee', 'creds', json.dumps(pwds),
            'flowerboxx/rlz_pwds_ring.txt')


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Snippets below are from:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/kms/api-client/snippets.py


def create_key_ring(project_id, location_id, key_ring_id):
    kms_client = googleapiclient.discovery.build(
        'cloudkms', 'v1', cache_discovery=False)

    # The resource name of the location associated with the KeyRing.
    parent = 'projects/{}/locations/{}'.format(project_id, location_id)
    request = kms_client.projects().locations().keyRings().create(
        parent=parent, body={}, keyRingId=key_ring_id)
    response = request.execute()

    print('Created KeyRing {}.'.format(response['name']))


def create_crypto_key(project_id, location_id, key_ring_id, crypto_key_id):
    """Creates a CryptoKey within a KeyRing in the given location."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build(
        'cloudkms', 'v1', cache_discovery=False)

    # The resource name of the KeyRing associated with the CryptoKey.
    parent = 'projects/{}/locations/{}/keyRings/{}'.format(
        project_id, location_id, key_ring_id)

    # Create a CryptoKey for the given KeyRing.
    request = kms_client.projects().locations().keyRings().cryptoKeys().create(
        parent=parent, body={'purpose': 'ENCRYPT_DECRYPT'},
        cryptoKeyId=crypto_key_id)
    response = request.execute()

    print('Created CryptoKey {}.'.format(response['name']))


def encrypt(project_id, location_id, key_ring_id, crypto_key_id,
            plaintext, ciphertext_file_name):
    """Encrypts data from plaintext_file using the provided CryptoKey and
    saves it to ciphertext_file_name so it can only be recovered with a call to
    decrypt.
    """

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build(
        'cloudkms', 'v1', cache_discovery=False)

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)

    # Use the KMS API to encrypt the data.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.encrypt(
        name=name,
        body={'plaintext': base64.b64encode(plaintext.encode()).decode('ascii')})
    response = request.execute()
    ciphertext = base64.b64decode(response['ciphertext'].encode('ascii'))

    # Write the encrypted data to a file.
    with io.open(ciphertext_file_name, 'wb') as ciphertext_file:
        ciphertext_file.write(ciphertext)


def decrypt(project_id, location_id, key_ring_id, crypto_key_id,
            ciphertext_file_name):
    """Decrypts data from ciphertext_file_name that was previously encrypted
    using the provided CryptoKey and return the plaintext."""

    # Creates an API client for the KMS API.
    kms_client = googleapiclient.discovery.build(
        'cloudkms', 'v1', cache_discovery=False)

    # The resource name of the CryptoKey.
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)
    # Read encrypted data from the input file.
    with io.open(ciphertext_file_name, 'rb') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Use the KMS API to decrypt the data.
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.decrypt(
        name=name,
        body={'ciphertext': base64.b64encode(ciphertext).decode('ascii')})
    response = request.execute()
    plaintext = base64.b64decode(
        response['plaintext'].encode('ascii')).decode()

    return plaintext


@click.command()
@click.argument('project_id')
@click.argument('location_id')
@click.argument('key_ring_id')
@click.argument('crypto_key_id')
@click.argument('ciphertext_file_name')
@click.argument('plaintext')
def setup(project_id, location_id, key_ring_id, crypto_key_id,
          ciphertext_file_name, plaintext):
    # create_key_ring(project_id, location_id, key_ring_id)
    # create_crypto_key(project_id, location_id, key_ring_id, crypto_key_id)
    encrypt(project_id, location_id, key_ring_id, crypto_key_id,
            plaintext, ciphertext_file_name)
    result = decrypt(project_id, location_id, key_ring_id, crypto_key_id,
                     ciphertext_file_name)
    assert result == plaintext


if __name__ == '__main__':
    setup()
