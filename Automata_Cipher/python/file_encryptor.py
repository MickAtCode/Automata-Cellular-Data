import os
import encryptor_XOR as e
import numpy as np
import sys

def main(input_file, key, output_file):
    file_extension = os.path.splitext(input_file)[1].encode()  # Get file extension
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Prepend file extension to the data
    data_with_extension = file_extension + b'||' + data

    encrypted_data, permutation = e.encrypt(data_with_extension, key, rule=30, steps=100)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    # Save the permutation used
    perm_file = output_file + ".perm"
    with open(perm_file, 'wb') as f:
        f.write(np.array(permutation, dtype=np.int32).tobytes())

    print(f"File encrypted and saved as {output_file}")
    print(f"Permutation saved as {perm_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encrypt_file.py <input_file> <key> <output_file>")
    else:
        input_file = sys.argv[1]
        key = sys.argv[2]
        output_file = sys.argv[3]
        main(input_file, key, output_file)
