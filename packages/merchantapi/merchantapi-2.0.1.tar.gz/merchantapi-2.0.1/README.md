# Miva Merchant API SDK for Python (3.x)

This python library wraps the Miva Merchant JSON API introduced in 
Miva Merchant 9.12. It allows you to quickly integrate your python
applications with a Miva Merchant store to fetch, create, and update
store data.

For api documentation visit [https://docs.miva.com/json-api](https://docs.miva.com/json-api).

# Requirements

- Miva Merchant 10.00+
- Python 3.x

**For Miva Merchant 9.x, use the 1.x release**

# Installation via pip

To install the SDK simply add it to your project with pip:

    pip install merchantapi
    
*Note: On some operating systems the `pip` program may be named `pip3`*

# Adding as a dependency in your packages

You can also add it to your project's `requirements.txt` file:

    merchantapi>=2.0.1
    
Then install

    pip install -r requirements.txt
    
*Note: On some operating systems the `pip` program may be named `pip3`*

# Getting Started

For usage see the examples provided in the `examples/` directory. 

#  SSH Private Key Authentication

## Compatible Private Key Formats

- OpenSSH PEM
- PKCS#1 PEM
- PKCS#8 PEM

When specifying the key to use within the `SSHClient` or `SSHPrivateKeyAuthenticator`, specify the full path to your private key file.

## Create PKCS#1 from OpenSSH private key format

If your private key is in OpenSSH format (starts with `-----BEGIN OPENSSH PRIVATE KEY-----`) then you will need to convert it.

Create a copy of your key preserving permissions:

    cp -p /path/to/private/key/id_rsa /path/to/private/key/id_rsa.pem

Convert in place to the proper format:

    ssh-keygen -p -m PEM -f /path/to/private/key/id_rsa.pem

## Create PKCS#8 PEM from PKCS#1 PEM private key format

Converting the key with encryption:

     openssl pkcs8 -in /path/to/private_key.pem -topk8 -out /path/to/private_key.pkcs8.pem

Converting the key without encryption:

     openssl pkcs8 -in /path/to/private_key.pem -topk8 -nocrypt -out /path/to/private_key.pkcs8.pem

# SSH Agent Authentication

## Compatible Public Key Formats

Your public key must be in the OpenSSH Public Key format. The default public key format is usually the correct type if you generated your key using `ssh-keygen`.

See https://tools.ietf.org/html/rfc4253#section-6.6 for format.

A quick way to get the correct format if you have the key associated with your local SSH agent is to run the command `ssh-add -L` and copying the corresponding key.

# License

This library is licensed under the `Miva SDK License Agreement`.

See the `LICENSE` file for more information.
