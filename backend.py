import cryptography
from cryptography.fernet import Fernet
import os

def key_exists():
  """Checks if the key file 'secret.key' exists."""
  return os.path.exists('secret.key')

def generate_key():
  """Generates a key and saves it to 'secret.key'."""
  key = Fernet.generate_key()
  with open('secret.key', 'wb') as key_file:
    key_file.write(key)
  return key

def load_key():
  """Loads the encryption key from 'secret.key' if it exists."""
  if key_exists():
    with open('secret.key', 'rb') as key_file:
      return key_file.read()
  else:
    print("Key not found. Generating a new key...")
    key = generate_key()
    return key

def decrypt_file(filename):
  """Decrypts the specified file using the loaded key."""
  key = load_key()
  if not key:
    return

  try:
    with open(filename, 'rb') as encrypted_file:
      encrypted_data = encrypted_file.read()
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return

  fernet = Fernet(key)
  try:
    decrypted_data = fernet.decrypt(encrypted_data)
  except cryptography.fernet.InvalidToken:  # Use InvalidToken here
    print("Error: Invalid key. The file might be corrupted or encrypted with a different key.")
    return

  return decrypted_data.decode('utf-8')  # Decode bytes to string


def encrypt_file(filename, data):
  """Encrypts the provided data and saves it to the specified file."""
  key = load_key()
  if not key:
    return

  fernet = Fernet(key)
  encrypted_data = fernet.encrypt(data.encode('utf-8'))  # Encode string to bytes

  with open(filename, 'wb') as encrypted_file:
    encrypted_file.write(encrypted_data)

def promptUser():
  """Prompts the user for data to append to the file."""
  data = input("Enter data to append: ")
  return data

def create_accounts_file():
  """Creates the 'accounts.txt' file if it doesn't exist."""
  if not os.path.exists('accounts.txt'):
    with open('accounts.txt', 'w') as file:
      pass  # Create an empty file


def main():
  filename = "accounts.txt"
  create_accounts_file()  # Call before decryption

  decrypted_data = decrypt_file(filename)

  if decrypted_data:
    # Append user input to decrypted data
    decrypted_data += "\n" + promptUser()
    encrypt_file(filename, decrypted_data)
  else:
    print("Failed to decrypt or open file. Exiting...")

if __name__ == "__main__":
  main()
