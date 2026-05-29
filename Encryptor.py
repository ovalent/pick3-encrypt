import marimo

__generated_with = "0.23.8"
app = marimo.App(width="columns")


@app.cell
def _(InvalidTag):
    import os
    import sys
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    def derive_key(password: str, salt: bytes, iterations: int) -> bytes:
        """Derive a 256-bit AES key from a password and salt using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # 32 bytes = 256 bits
            salt=salt,
            iterations=iterations,
        )
        return kdf.derive(password.encode())

    def encrypt_file(input_filepath, output_filepath, password, iterations=600000):
        print(f"Encrypting '{input_filepath}'...")

        # 1. Read the raw original data
        with open(input_filepath, 'rb') as f:
            data = f.read()    

        # 2 Generate random cryptographic parameters
        salt = os.urandom(16)  # 16 bytes for PBKDF2 salt
        nonce = os.urandom(12) # 12 bytes for GCM nonce/IV

        # 2.1 Convert the iteration integer into 4 bytes (big-endian format)
        iter_bytes = iterations.to_bytes(4, byteorder='big')

        # 3. Derive the secure key
        key = derive_key(password, salt, iterations)

        # 4. Encrypt the data
        aesgcm = AESGCM(key)
        encrypted_data = aesgcm.encrypt(nonce, data, None)

        # 5. Write the custom package: [Salt (16)] + [Nonce (12)] + [Encrypted Data]
        with open(output_filepath, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(iter_bytes)
            f.write(encrypted_data)

        print(f"Success! Saved as '{output_filepath}'\n")

    def decrypt_file(input_filepath, output_filepath, password):
        print(f"Attempting to decrypt '{input_filepath}'...")

        # 1. Read the encrypted package
        with open(input_filepath, 'rb') as f:
            file_data = f.read()

        # 2. Extract the parameters based on our exact byte sizes
        salt = file_data[:16]
        nonce = file_data[16:28]
        iter_bytes = file_data[28:32]
        encrypted_data = file_data[32:]

        iterations = int.from_bytes(iter_bytes, byteorder='big')
        print(f"Decrypting '{input_filepath}' (Found iterations: {iterations})...")

        # 3. Derive the key using the extracted salt
        key = derive_key(password, salt, iterations)

        # 4. Initialize the cipher and decrypt
        aesgcm = AESGCM(key)
        try:
            # If the password is wrong, or the file was modified, this will throw an InvalidTag error
            decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)

            # 5. Save the restored file
            with open(output_filepath, 'wb') as f:
                f.write(decrypted_data)

            print(f"Success! Restored file saved as '{output_filepath}'\n")

        except InvalidTag:
            print("ERROR: Decryption failed! Incorrect password or corrupted file.\n")

    return decrypt_file, encrypt_file, os, sys


@app.cell
def _(encrypt_file, os, sys):
    ###############################################
    # ENCRYPT FILES
    ###############################################

    # Example usage for your Proof of Concept
    input_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test" # Replace with a real folder path
    output_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-encrypted" # Replace with your desired output folder path

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Please ensure the directory '{input_folder}' exists.")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    pwd = input("Enter master password to ENCRYPT: ")

    current_iteration_target = 1000000

    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)

        # Skip directories and already encrypted files
        if os.path.isfile(input_file) and not filename.endswith('.enc'):
            output_file = os.path.join(output_folder, f"{filename}.enc")
            encrypt_file(input_file, output_file, pwd, iterations=current_iteration_target)
    return


@app.cell
def _(decrypt_file, os, sys):
    ###############################################
    # DECRYPT FILES
    ###############################################

    # Example usage for your Proof of Concept
    _input_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-encrypted"
    _output_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-decrypted"

    if not os.path.exists(_input_folder):
        print(f"Could not find '{_input_folder}'. Run the encryptor script first.")
        sys.exit(1)

    os.makedirs(_output_folder, exist_ok=True)

    _pwd = input("Enter master password to DECRYPT: ")

    for _filename in os.listdir(_input_folder):
        _input_file = os.path.join(_input_folder, _filename)
        if os.path.isfile(_input_file) and _filename.endswith(".enc"):
            _output_filename = _filename[:-4]  # Remove the .enc extension
            _output_file = os.path.join(_output_folder, _output_filename)
            decrypt_file(_input_file,_output_file, _pwd)
    return


if __name__ == "__main__":
    app.run()
