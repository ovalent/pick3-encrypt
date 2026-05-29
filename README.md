Pick3 File Encryptor
====================

A secure, batch file encryption and decryption tool built with Python and [Marimo](https://marimo.io/).

This project uses modern cryptographic standards (AES-GCM and PBKDF2HMAC) to protect your files. It features a custom .enc file format that dynamically stores the cryptographic parameters (Salt, Nonce, and Iteration count) alongside the encrypted data, ensuring future-proof decryption even if iteration standards change over time.

🌟 Features
-----------

*   **Strong Cryptography:** Uses 256-bit **AES-GCM** for authenticated encryption, ensuring both the confidentiality and integrity of your files.
    
*   **Secure Key Derivation:** Uses **PBKDF2HMAC (SHA256)** with a high, dynamic iteration count (defaulted to 1,000,000) to protect against offline brute-force attacks.
    
*   **Dynamic Iteration Storage:** Saves the exact PBKDF2 iteration count directly into the file header. This allows you to increase the iteration count for future encryptions without breaking the ability to decrypt older files.
    
*   **Batch Processing:** Easily encrypt or decrypt entire directories of files at once.
    
*   **Marimo Integration:** Built as a reactive Marimo app, allowing for interactive execution and easy visual modification.
    

📦 Custom .enc File Structure
-----------------------------

When a file is encrypted, it is saved with a .enc extension using the following custom byte structure:

Content
| Offset | Size | Content | Description |
|---|---|---|---|
| 0x00 | 16 bytes | **Salt** | Randomly generated salt for PBKDF2 key derivation. |
| 0x10 | 12 bytes | **Nonce** | Randomly generated initialization vector for AES-GCM. |
| 0x1C | 4 bytes | **Iterations** | Big-endian integer representing the PBKDF2 iteration count. |
| 0x20 | Variable | **Ciphertext** | The actual AES-GCM encrypted file data and authentication tag. |


🚀 Getting Started
------------------

### Prerequisites

You need Python 3.7+ and the following libraries installed:

```
pip install cryptography marimo
```

### Configuration

Before running the script, open Encryptor.py and update the input and output folder paths in the execution cells to match your local environment:

```python
input_folder = r"C:\path\to\your\input\folder"  
output_folder = r"C:\path\to\your\output\folder"
```

### Usage

Since this is built as a Marimo app, you can run it interactively in your browser:

```
marimo edit Encryptor.py
```

Alternatively, you can run it directly as a standard Python script:

```
python Encryptor.py
```

1.  **To Encrypt:** The script will prompt you for a master password, read all files in your input\_folder, and save the .enc versions to your output\_folder.
    
2.  **To Decrypt:** The script will prompt you for the master password, read the .enc files, extract the dynamic iteration count and parameters, and restore the original files.
    

⚠️ Security Notes
-----------------

*   **Master Password:** The security of your files relies entirely on the strength of your master password. Use a long, strong passphrase (e.g., 16-20 random characters or a Diceware passphrase).
    
*   **Key Loss:** There is no "forgot password" feature. If you lose your master password, your encrypted files cannot be recovered.
    
*   **Authentication:** Because the script uses AES-GCM, any unauthorized modification to the encrypted .enc files will result in an InvalidTag error during decryption, protecting you from tampered files.