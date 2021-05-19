# simple-e2ee-cmd-chat

The purpose of the project is to develop a program which allows 2 users to communicate with one another in a secure manner through the use of End-to-End Encrypted (E2EE) Communications.

## Features

- Base Chat Sender/Listener
- RSA Key Generation & Exchange
- Digital Signing & Verification
- Message Encryption & Decryption
- Message Padding

## Program Flow
![Program Flow](Flow.png)

## Program Architecture
![Architecture](Architecture.png)

## Limitations

- Message length due to the nature of RSA & socket being binded to 4096 bits
- No Error Handling

## Requirements

- [Python 3.6](https://www.python.org/downloads/release/python-360/)

- pycryptodome
```sh
pip install pycryptodome
```

- Python Socket
```sh
pip install socket
```

## Usage - Server

1. Run the program server.py via cmd
```sh
python server.py
```
2. Key in the port number to start the session
3. Now wait for connections

## Usage - Client

1. Run the program client.py via cmd
```sh
python client.py
```
2. Key in Server's IP address and port number
3. Viola!
