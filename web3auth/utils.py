import sha3
import json
import symbolhkdf
import time
import datetime
import base64
import hashlib
from eth_utils import is_hex_address
from django import forms
from django.utils.translation import gettext_lazy as _
from ethereum.utils import ecrecover_to_pub

###########テスト用，要削除
server_secret = "0000000000000000000000000000000000000000000000000000000000000000"
pub = "3B6A27BCCEB6A42D62A3A8D02A6F0D73653215771DE243A63AC048A18B59DA29"
owner = "TCHBDENCLKEBILBPWP3JPB2XNY64OE7PYHHE32I"
deadline = 60 * 60 * 24 * 1000


def recover_to_addr(token, payload):
    sender_publickey = payload[:64]
    encrypted_message = payload[64:]
    decode = json.loads(symbolhkdf.decode(server_secret, sender_publickey, encrypted_message))#復号
    print(decode)
    iat = decode["iat"]
    signer = decode["signerAddress"]
    verifier = decode["verifierAddress"]
    if verifier != owner:
        raise ValueError("Invalid verifier")
    if time.time()*1000 - int(iat) + deadline < 0:
        raise ValueError("iat expired")
    return signer


def validate_xym_address(value):# サインアップ時のアドレス検証
    if not len(value) == 39:
        raise forms.ValidationError(
            _('%(value)s is not a valid Symbol address'),
            params={'value': value},
        )
    decode = base64.b32decode(value+"=")
    checksum = decode[21:]
    hasher = hashlib.sha3_256()
    calculate_chk = hasher.update(decode[:21])
    calculate_chk = hasher.digest()[:len(checksum)]
    print("decode:",decode,"chk:",checksum,"calc:",calculate_chk)
    if checksum != calculate_chk:
        raise forms.ValidationError(
            _('%(value)s is not a valid Symbol address'),
            params={'value': value},
        )

