from OpenSSL import crypto


def create_cert(cert_dir, days=365):
    # 创建一个RSA密钥
    private_key = crypto.PKey()
    private_key.generate_key(crypto.TYPE_RSA, 2048)

    # 创建一个自签名证书
    cert = crypto.X509()
    cert.get_subject().CN = "My Cert"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(days * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(private_key)
    cert.sign(private_key, 'sha256')

    # 保存证书和密钥
    with open(f"{cert_dir}/server.pem", "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(f"{cert_dir}/server.key", "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))


create_cert("ssl")