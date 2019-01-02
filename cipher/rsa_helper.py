#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2019/1/1'
# @description: 


import codecs
import rsa
import pickle


class RSAHelper(object):
    def __init__(self):
        pass

    def gene_ras_key_to_file(self, pub_file='public.pem', priv_file='private.pem', nbits=1024):
        # 生成密钥
        (pubkey, privkey) = rsa.newkeys(nbits=nbits)

        # 保存密钥
        with codecs.open(pub_file, 'w+', 'utf-8') as f:
            # print(type(pubkey.save_pkcs1()))
            f.write(pubkey.save_pkcs1())
        with codecs.open(priv_file, 'w+', 'utf-8') as f:
            f.write(privkey.save_pkcs1())

    def load_pub_key(self, pub_file='public.pem'):
        with codecs.open(pub_file, 'r+', 'utf-8') as f:
            pub_key = rsa.PublicKey.load_pkcs1(f.read().encode('utf-8'))
            return pub_key

    def load_priv_key(self, priv_file='private.pem'):
        with codecs.open(priv_file, 'r+', 'utf-8') as f:
            priv_key = rsa.PrivateKey.load_pkcs1(f.read().encode('utf-8'))
            return priv_key

    # RSA非对称加密内容长度有限制，1024位key的最多只能加密127位数据，否则就会报错
    # TODO 文件分段加密
    def encrypt_file_to_dump(self, src_file, dst_file, pub_file='public.pem'):
        pub_key = self.load_pub_key(pub_file=pub_file)
        with codecs.open(src_file, 'rb', 'utf-8') as scr_fp:
            all_uni = scr_fp.read()
            crypto = rsa.encrypt(all_uni.encode('utf-8'), pub_key)
        with open(dst_file, 'wb') as dst_fp:
            pickle.dump(crypto, dst_fp)

    def decrypt_dump_to_file(self, src_file, dst_file, priv_file='private.pem'):
        priv_key = self.load_priv_key(priv_file=priv_file)
        with open(src_file, 'rb') as scr_fp:
            crypto = pickle.load(scr_fp)
        with codecs.open(dst_file, 'wb', 'utf-8') as dst_fp:
            # utf-8
            all_str = rsa.decrypt(crypto, priv_key)
            dst_fp.write(all_str)


if __name__ == "__main__":
    pass
    rsa_helper = RSAHelper()
    # rsa_helper.gene_ras_key_to_file(nbits=10240)

    # pub_key = rsa_helper.load_pub_key()
    # print(pub_key)
    # print(type(pub_key))

    # priv_key = rsa_helper.load_priv_key()
    # print(priv_key)
    # print(type(priv_key))

    in_file = r''
    out_file = r''
    rsa_helper.encrypt_file_to_dump(in_file, out_file)

    # in_file = r''
    # out_file = r''
    # rsa_helper.decrypt_dump_to_file(in_file, out_file)
