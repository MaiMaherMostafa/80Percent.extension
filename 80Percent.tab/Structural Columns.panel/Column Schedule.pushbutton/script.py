# -*- coding: utf-8 -*-

import os, System
from System import Array, Byte
from System.Security.Cryptography import Aes, HMACSHA256, Rfc2898DeriveBytes

CMD_DIR  = os.path.dirname(__file__)
ENC_FILE = os.path.join(CMD_DIR, "engine_secure.aes")

def to_net_bytes(py_iterable):
    arr = Array.CreateInstance(Byte, len(py_iterable))
    for i, v in enumerate(py_iterable):
        arr[i] = int(v) & 0xFF
    return arr

def to_py_bytes(net_array):
    return bytearray(net_array if net_array is not None else [])

_s1 = [0x7A,0x11,0x5E,0x29,0x34,0x6D,0x21,0x41]
_s2 = [0x01,0x5C,0x68,0x3F,0x44,0x7B,0x07,0x10]
_s3 = [0x3D,0x52,0x09,0x6A,0x55,0x23,0x0C,0x48]

def _mam():
    mask = 0x63
    out = []
    for chunk in (_s1, _s2, _s3):
        for v in chunk:
            out.append((int(v) ^ mask) & 0xFF)
    return to_net_bytes(out)

_sami_x = [0xA2,0x91,0xC5,0xBB,0xDE,0xE7,0xF1,0x8C,
           0xD9,0xEE,0xA7,0xC2,0x9D,0xF4,0xB8,0xD5]

def _sami():
    mk = 0x5A
    return to_net_bytes([(int(b) ^ mk) & 0xFF for b in _sami_x])

_ITER = 100000

def _derive_key():
    sec = _mam()
    slt = _sami()
    pb  = Rfc2898DeriveBytes(sec, slt, _ITER)
    return pb.GetBytes(32)

def _mac(msg_net_array, key_net_array):
    h = HMACSHA256(key_net_array)
    h.TransformFinalBlock(msg_net_array, 0, len(msg_net_array))
    return bytearray(h.Hash)

def _dec(path):
    raw = bytearray(open(path, "rb").read())
    if not raw:
        raise Exception("Encrypted engine is empty.")

    magic = raw[0:4]             
    sl_py = raw[4:20]
    iv_py = raw[20:36]
    ct_py = raw[36:-32]
    mac_py= raw[-32:]

    key = _derive_key()

    hdr_py = raw[0:-32]
    mac2_py = _mac(to_net_bytes(hdr_py), key)
    if bytes(mac2_py) != bytes(mac_py):
        raise Exception("Engine integrity failure.")

    aes = Aes.Create()
    aes.Mode    = System.Security.Cryptography.CipherMode.CBC
    aes.Padding = System.Security.Cryptography.PaddingMode.PKCS7
    aes.Key     = key
    aes.IV      = to_net_bytes(iv_py)

    clear_net = aes.CreateDecryptor().TransformFinalBlock(
        to_net_bytes(ct_py), 0, len(ct_py)
    )
    text = bytes(to_py_bytes(clear_net)).decode("utf-8")

    for i in range(len(clear_net)): clear_net[i] = 0
    for i in range(len(ct_py)):     ct_py[i]     = 0
    for i in range(len(raw)):       raw[i]       = 0

    return text

code = _dec(ENC_FILE)
exec(compile(code, "<engine>", "exec"), globals(), globals())
del code
