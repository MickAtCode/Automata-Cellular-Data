import hashlib
import numpy as np
import matplotlib as mtpl
import secrets
import os

def initialize_ca(key, size):
    seed = os.urandom(4)
    
    # Convert the hexadecimal seed to an integer
    int_seed = int.from_bytes(seed,byteorder='big')
    
    # Seed the random number generator with the derived integer seed
    np.random.seed(int_seed % (2**32))  # Ensure seed fits within a 32-bit integer
    
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