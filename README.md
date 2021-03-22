# Evernet - Serveur central et PKI
Evernet -Everywhere, Anonymous, Secure and Efficient Image Sharing Network

## Installation

### Setup
Check the version of Python 3 that is installed in the system by typing: 
```shell
$ sudo apt-get -y upgrade
$ python3 -V
```
To manage software packages for Python and download all the required lib
```shell
$ sudo apt-get install -y python3-pip
```
Download required lib
```shell
$ pip3 install jpysocket rsaUtils lxml pyOpenSSL bcrypt pcrytodome
```
To launch the server
```shell
$ python3 server.py
```

To launch the test server with the debug client
```shell
$ python3 server.py test
$ python3 client.py
```

## Auteurs

**Boisseau Martin**
- Github : [@MartinBoisseau](https://github.com/MartinBoisseau)

**Chardon Jeremy**
- Github : [@JeremyChardon](https://github.com/JeremyChardon)

**Larigue Ghislain**
- Github : [@GhislainLartigue](https://github.com/GhislainLartigue) 

**Nadal Clément**
- Github : [@Clement](https://github.com/Mr-Clem)

**Portes Narrieu Alex**
- Github : [@Alex Portes Narrieu](https://github.com/apnarrieu)

**Pourtier Jacques**
- Github : [@Exjp](https://github.com/Exjp)

