import marimo

__generated_with = "0.23.8"
app = marimo.App(width="columns")


@app.cell
def _():
    import os
    import sys
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive a 256-bit AES key from a password and salt using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # 32 bytes = 256 bits
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def encrypt_file(input_filepath, output_filepath, password):
        print(f"Encrypting '{input_filepath}'...")

        # 1. Read the raw original data
        with open(input_filepath, 'rb') as f:
            data = f.read()

        # 2. Generate random cryptographic parameters
        salt = os.urandom(16)  # 16 bytes for PBKDF2 salt
        nonce = os.urandom(12) # 12 bytes for GCM nonce/IV

        # 3. Derive the secure key
        key = derive_key(password, salt)

        # 4. Encrypt the data
        aesgcm = AESGCM(key)
        encrypted_data = aesgcm.encrypt(nonce, data, None)

        # 5. Write the custom package: [Salt (16)] + [Nonce (12)] + [Encrypted Data]
        with open(output_filepath, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(encrypted_data)

        print(f"Success! Saved as '{output_filepath}'\n")

    return encrypt_file, os, sys


@app.cell
def _(encrypt_file, os, sys):
    # Example usage for your Proof of Concept
    input_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test" # Replace with a real folder path
    output_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-encrypted" # Replace with your desired output folder path

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Please ensure the directory '{input_folder}' exists.")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    pwd = input("Enter master password to ENCRYPT: ")

    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)

        # Skip directories and already encrypted files
        if os.path.isfile(input_file) and not filename.endswith('.enc'):
            output_file = os.path.join(output_folder, f"{filename}.enc")
            encrypt_file(input_file, output_file, pwd)
    return


if __name__ == "__main__":
    app.run()
