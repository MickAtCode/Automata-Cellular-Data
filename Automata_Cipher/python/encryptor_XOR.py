import hashlib
import numpy as np
import time

# Cellular automata functions
def initialize_ca(key, size):
    # Use a hash of the key to create a deterministic seed
    seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)
    
    # Seed the random number generator with the derived integer seed
    np.random.seed(seed)
    
    # Generate the initial state using the seeded random number generator
    initial_state = np.random.randint(0, 2, size, dtype=np.uint8)
    return initial_state

def evolve_ca(state, rule, steps):
    # Convert the rule number to its binary representation (as an 8-bit string)
    rule_bin = f"{rule:08b}"
    
    # Create a dictionary to map neighborhood patterns to their corresponding rule output
    rule_dict = {f"{i:03b}": int(rule_bin[7-i]) for i in range(8)}
    
    # Get the length of the state
    n = len(state)
    
    # Evolve the state for the specified number of steps
    for _ in range(steps):
        new_state = state.copy()
        
        # Update each cell based on its neighborhood
        for i in range(n):
            left = state[(i-1) % n]  
            center = state[i]        
            right = state[(i+1) % n] 
            neighborhood = f"{left}{center}{right}"
            
            # Update the cell state based on the rule
            new_state[i] = rule_dict[neighborhood]
        
        # Set the current state to the new state
        state = new_state
    
    return state

# P-box functions
def pbox(data, permutation):
    # Convert data to a binary string
    binary_data = ''.join(f'{byte:08b}' for byte in data)
    
    # Pad binary_data to ensure it fits exactly into permutation size
    binary_data = binary_data.ljust(len(permutation), '0')
    
    # Apply the permutation to the binary string
    permuted_data = ''.join(binary_data[i] for i in permutation)
    
    # Convert the permuted binary string back to bytes
    permuted_bytes = int(permuted_data, 2).to_bytes((len(permuted_data) + 7) // 8, byteorder='big')
    return permuted_bytes

def inverse_pbox(data, permutation):
    # Convert data to a binary string
    binary_data = ''.join(f'{byte:08b}' for byte in data)
    
    # Apply the inverse of the permutation
    inverse_permutation = np.argsort(permutation)
    permuted_data = ''.join(binary_data[i] for i in inverse_permutation)
    
    # Convert the permuted binary string back to bytes
    permuted_bytes = int(permuted_data, 2).to_bytes((len(permuted_data) + 7) // 8, byteorder='big')
    return permuted_bytes

# Encryption and decryption functions
def encrypt(data, key, rule, steps):
    # Ensure the data is a numpy array of uint8
    data = np.frombuffer(data, dtype=np.uint8)
    
    # Initialize the CA with the given key
    size = len(data)
    state = initialize_ca(key, size)
    
    # Evolve the CA
    evolved_state = evolve_ca(state, rule, steps)
    
    # Perform encryption (XOR with evolved state)
    encrypted_data = np.bitwise_xor(data, evolved_state)
    
    # Apply the P-box
    bit_length = len(encrypted_data) * 8
    permutation = np.random.permutation(bit_length)  # Example permutation
    encrypted_data = pbox(encrypted_data, permutation)
    
    return encrypted_data, permutation

def decrypt(encrypted_data, key, rule, steps, permutation):
    # Reverse the P-box permutation
    permuted_data = inverse_pbox(encrypted_data, permutation)
    
    # Ensure the data is a numpy array of uint8
    permuted_data = np.frombuffer(permuted_data, dtype=np.uint8)
    
    # Initialize the CA with the given key
    size = len(permuted_data)
    state = initialize_ca(key, size)
    
    # Evolve the CA
    evolved_state = evolve_ca(state, rule, steps)
    
    # Perform decryption (XOR with evolved state)
    decrypted_data = np.bitwise_xor(permuted_data, evolved_state)
    
    return decrypted_data.tobytes()

# Example usage
#key = "hello key"
#data = b"Attack helicopter"

# Encrypt the data
# st = time.time_ns()
# encrypted_data, permutation = encrypt(data, key, rule=30, steps=100)
# et = time.time_ns()
# print("Encrypted data:", encrypted_data)
# print("Encryption Time:", (et - st))

# Decrypt the data
# decrypted_data = decrypt(encrypted_data, key, rule=30, steps=100, permutation=permutation)
# print("Decrypted data:", decrypted_data)
