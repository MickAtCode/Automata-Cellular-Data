import numpy as np
import encryptor_XOR as d
import sys
import os

def main(encrypted_file, key, permutation_file, output_file):
    # Read the encrypted data from the file
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    # Read the permutation data
    with open(permutation_file, 'rb') as f:
        permutation = np.frombuffer(f.read(), dtype=np.int32)

    # Decrypt the data using the decryption function
    decrypted_data = d.decrypt(encrypted_data, key, rule=30, steps=100, permutation=permutation)

    # Split the file extension from the decrypted data
    file_extension, file_data = decrypted_data.split(b'||', 1)
    file_extension = file_extension.decode()

    # If no output file is provided, use the default naming convention
    if not output_file:
        output_file = os.path.splitext(encrypted_file)[0] + file_extension

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(file_data)

    print(f"Data decrypted and saved to {output_file}")

if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) not in [4, 5]:
        print("Usage: python decrypt_file.py <encrypted_file> <key> <permutation_file> [output_file]")
    else:
        encrypted_file = sys.argv[1]
        key = sys.argv[2]
        permutation_file = sys.argv[3]
        # If an output file is provided, use it; otherwise, set it to None
        output_file = sys.argv[4] if len(sys.argv) == 5 else None
        main(encrypted_file, key, permutation_file, output_file)