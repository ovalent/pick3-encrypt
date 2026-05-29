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
    from cryptography.exceptions import InvalidTag

    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive the exact same 256-bit AES key using the saved salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def decrypt_file(input_filepath, output_filepath, password):
        print(f"Attempting to decrypt '{input_filepath}'...")

        # 1. Read the encrypted package
        with open(input_filepath, 'rb') as f:
            file_data = f.read()

        # 2. Extract the parameters based on our exact byte sizes
        salt = file_data[:16]
        nonce = file_data[16:28]
        encrypted_data = file_data[28:]

        # 3. Derive the key using the extracted salt
        key = derive_key(password, salt)

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

    return decrypt_file, os, sys


@app.cell
def _(decrypt_file, os, sys):
    # Example usage for your Proof of Concept
    input_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-encrypted"
    output_folder = r"C:\Users\ovale\Documents\10_git\pick3-encrypt\media-test-decrypted"

    if not os.path.exists(input_folder):
        print(f"Could not find '{input_folder}'. Run the encryptor script first.")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)

    pwd = input("Enter master password to DECRYPT: ")

    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        if os.path.isfile(input_file) and filename.endswith(".enc"):
            output_filename = filename[:-4]  # Remove the .enc extension
            output_file = os.path.join(output_folder, output_filename)
            decrypt_file(input_file, output_file, pwd)
    return


if __name__ == "__main__":
    app.run()
