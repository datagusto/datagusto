import os
from cryptography.fernet import Fernet
import streamlit as st

def load_or_generate_key():
    key_filename = "zzz_encryption_key.key"
    # Check if the key file exists
    if not os.path.exists(key_filename):
        # Generate a new key if the file does not exist
        key = Fernet.generate_key()
        # Save the key to a file
        with open(key_filename, "wb") as key_file:
            key_file.write(key)
    else:
        # Load the key from the file
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
    return key

def get_key():
    # Check if the key is already loaded in session_state
    if 'encryption_key' not in st.session_state:
        # Load or generate the key and store it in session_state
        st.session_state.encryption_key = load_or_generate_key()
    return st.session_state.encryption_key

def encrypt_string(plain_text):
    """Encrypts a string."""
    key = get_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plain_text.encode())
    return cipher_text.decode()  # Return as string for easier handling

def decrypt_string(cipher_text):
    """Decrypts a string."""
    key = get_key()
    cipher_suite = Fernet(key)
    try:
        plain_text = cipher_suite.decrypt(cipher_text.encode()).decode()
        return plain_text
    except Exception as e:
        print(f"Error decrypting string: {e}")
        return None

# encrypted_string = encrypt_string("Hello, World!")
# decrypted_string = decrypt_string(encrypted_string)
# st.write(decrypted_string)
