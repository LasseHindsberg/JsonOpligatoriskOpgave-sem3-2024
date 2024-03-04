import json
from socket import *
from random import randint
from threading import Thread

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready to listen')

def random(connectionSocket, data):
    """
    Generates a random number between two given numbers and sends the response back to the client.

    Args:
        connectionSocket (socket): The socket connection to the client.
        data (dict): The data received from the client, containing the two numbers.

    Returns:
        None
    """
    try:
        # Split the numbers received from the client
        number1, number2 = data["numbers"].split()
        # Convert the numbers to integers
        number1 = int(number1)
        number2 = int(number2)

        # Generate a random number between the two given numbers
        if number1 > number2:
            connectionSocket.send(json.dumps({"response": randint(number2, number1)}).encode())
            return
        connectionSocket.send(json.dumps({"response": randint(number1,number2)}).encode())
        return
    except ValueError:
        # Send an error response if the input is invalid
        connectionSocket.send(json.dumps({"error": "Invalid Input"}).encode())
        return

def add(connectionSocket, data):
    """
    Adds two numbers and sends the response back to the client.

    Args:
        connectionSocket (socket): The socket connection to the client.
        data (dict): The data received from the client, containing the two numbers.

    Returns:
        None
    """
    try:
        # Split the numbers received from the client
        number1, number2 = data["numbers"].split()
        # Convert the numbers to integers
        number1 = int(number1)
        number2 = int(number2)
        # Add the two numbers and send the response back to the client
        connectionSocket.send(json.dumps({"response": number1 + number2}).encode())
        return
    except ValueError:
        # Send an error response if the input is invalid
        connectionSocket.send(json.dumps({"error": "Invalid Input"}).encode())
        return

def subtract(connectionSocket, data):
    """
    Subtracts two numbers and sends the response back to the client.

    Args:
        connectionSocket (socket): The socket connection to the client.
        data (dict): The data received from the client, containing the two numbers.

    Returns:
        None
    """
    try:
        # Split the numbers received from the client
        number1, number2 = data["numbers"].split()
        # Convert the numbers to integers
        number1 = int(number1)
        number2 = int(number2)
        # If number 2 is of greater value than number 1, then we will subtract number 1 from number 2
        if number2 > number1:
            connectionSocket.send(json.dumps({"response": number2 - number1}).encode())
            return
        # Likewise, if number 1 is of greater value, we will subtract its value from number 2
        connectionSocket.send(json.dumps({"response": number1 - number2}).encode())
        return
    except ValueError:
        # Send an error response if the input is invalid
        connectionSocket.send(json.dumps({"error": "Invalid Input"}).encode())
        return
    
def protocol_error(connectionSocket):
    """
    Sends an error response to the client indicating an invalid protocol.

    Args:
        connectionSocket (socket): The socket connection to the client.

    Returns:
        None
    """
    connectionSocket.send(json.dumps({"error": "Invalid Protocol"}).encode())
    return

def handle_protocol(connectionSocket):
    """
    Handles the protocol for a client connection.

    Args:
        connectionSocket (socket): The socket connection to the client.

    Returns:
        None
    """
    # Receive the operation from the client
    operation = connectionSocket.recv(1024).decode()
    operation = json.loads(operation)
    
    # Send a response to prompt the client to input numbers
    connectionSocket.send(json.dumps({"response": "input your Numbers"}).encode())
    
    # Receive the data (numbers) from the client
    data = connectionSocket.recv(1024).decode()
    data = json.loads(data)
    
    # Perform the corresponding operation based on the received operation
    match operation["operation"].lower():
        case "random":
            random(connectionSocket, data)
        case "add":
            add(connectionSocket, data)
        case "subtract":
            subtract(connectionSocket, data)
        case _:
            protocol_error(connectionSocket)

def handle_client(connectionSocket, addr):
    """
    Handles a client connection.

    Args:
        connectionSocket (socket): The socket connection to the client.
        addr (tuple): The address of the client.

    Returns:
        None
    """
    print(addr[0])
    handle_protocol(connectionSocket)
    connectionSocket.close()

def start_server():
    """
    Starts the server and listens for client connections.

    Returns:
        None
    """
    while True:
        connectionSocket, addr = serverSocket.accept()
        t = Thread(target=handle_client, args=(connectionSocket, addr))
        t.start()

def main():
    """
    Main function to start the server.

    Returns:
        None
    """
    start_server()

if __name__ == "__main__":
    main()