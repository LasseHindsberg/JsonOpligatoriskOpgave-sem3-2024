import json
from socket import *

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print("Connected to server, please write your operation")


def json_communication():
    """
    Sends JSON data to the server and receives the response.

    This function prompts the user for an operation, sends it to the server as JSON,
    receives the server's response, and prints it out. Then it prompts the user for
    a set of numbers, sends it to the server as JSON, receives the response, and
    prints it out.

    Args:
        None

    Returns:
        None
    """
    clientData = input()
    clientData = {"operation": clientData}
    clientSocket.send(json.dumps(clientData).encode())
    serverResponse = clientSocket.recv(1024).decode()
    serverResponse = json.loads(serverResponse)
    # prints out the response from the server
    print(serverResponse["response"])
    # gets our "new" data from the user input
    clientData = input()
    clientData = {"numbers": clientData}

    clientSocket.send(json.dumps(clientData).encode())
    serverResponse = clientSocket.recv(1024).decode()
    serverResponse = json.loads(serverResponse)
    # prints out the response from the server
    print(serverResponse["response"])
    

def send_server_request():
    """
    Sends a request to the server.

    This function calls the `json_communication` function and then closes the client socket.

    Args:
        None

    Returns:
        None
    """
    json_communication()
    clientSocket.close()

def main():
    """
    Main function of the client.

    This function calls the `send_server_request` function.

    Args:
        None

    Returns:
        None
    """
    send_server_request()


__name__ == "__main__" and main()