import binascii
import pure_pynacl as nacl
import hashlib
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend


def clamp(d):
    d[0] &= 248
    d[31] &= 127
    d[31] |= 64

def decode(recipientPrivate, senderPublic, payload):
    # Error
    if recipientPrivate is None or senderPublic is None or payload is None:
        raise ValueError('Missing argument !')
    # Processing
    binpayload = binascii.unhexlify(payload)
    payloadBuffer = binpayload[16+12:]
    # payloadBuffer = new Uint8Array(binPayload.buffer, 16 + 12)#tag + iv
    tagAndIv = binpayload[0:16+12]
    # tagAndIv = new Uint8Array(binPayload.buffer, 0, 16 + 12)
    try:
        decoded = _decode(binascii.unhexlify(recipientPrivate),binascii.unhexlify(senderPublic), payloadBuffer, tagAndIv)
        return decoded
    except Exception:
        #To return empty string rather than error throwing if authentication failed
        return ''


def _decode(recipientPrivate:bytes, senderPublic:bytes, payload:bytes, tagAndIv:bytes):
    # Error
    if recipientPrivate is None or senderPublic is None or payload is None or tagAndIv is None:
        raise ValueError('Missing argument !')
    keyPair = recipientPrivate
    encKey = deriveSharedKey(keyPair, senderPublic)
    encIv = tagAndIv[16:]
    encTag = tagAndIv[0:16]
    cipher = AES.new(encKey, AES.MODE_GCM, encIv)
    decrypted = cipher.decrypt_and_verify(payload, encTag)
    # Result
    return decrypted.decode(encoding='utf-8')

def prepareForScalarMult(sk):
    hash =hashlib.sha512()
    hash.update(sk)
    d = bytearray(hash.digest()[0:32] + bytes(32))
    clamp(d)
    return d

def deriveSharedKey(privateKey, publicKey):
    backend = default_backend()
    sharedSecret = deriveSharedSecret(privateKey, publicKey)
    info = bytes(b'catapult')
    algorithm = hashes.SHA256()
    salt = bytes(32)
    length = 32
    hkdf = HKDF(algorithm=algorithm, length=length, salt=salt, info=info,
                backend=backend)
    key = hkdf.derive(sharedSecret)
    return key
def deriveSharedSecret(privateKey, publicKey):
    d = prepareForScalarMult(privateKey)
    q = [nacl.gf(), nacl.gf(), nacl.gf(), nacl.gf()]
    p = [nacl.gf(), nacl.gf(), nacl.gf(), nacl.gf()]
    sharedSecret = bytearray(32)
    nacl.unpack(q, publicKey)
    nacl.scalarmult(p, q, d)
    nacl.pack(sharedSecret, p)

    return bytes(sharedSecret)
