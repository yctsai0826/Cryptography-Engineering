from sympy import Poly
from sympy.abc import x
import numpy as np
from pylfsr import LFSR

def string_to_binary(input_string):
    return ''.join(format(ord(char), '08b') for char in input_string)

def xor_binary_strings(a, b):
    return ''.join(str(int(bit_a) ^ int(bit_b)) for bit_a, bit_b in zip(a, b))

def binary_to_string(binary_string):
    text = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        text += chr(int(byte, 2))
    return text

def lfsr_key(state, tag):
    keystream = []
    while len(keystream) < 2368:
        keystream.append(str(state[0]))
        if state[0] == 1:
            for i in tag:
                if 0 <= 8 - i < len(state):
                    state[8 - i] = state[8 - i] ^ 1
            state = state[1:] + [1]
        else:
            state = state[1:] + [0]
    
    return ''.join(keystream)
    

plaintext = """ATNYCUWEARESTRIVINGTOBEAGREATUNIVERSITYTHATTRANSCENDSDISCIPLINARYDIVIDESTOSOLVETHEINCREASINGLYCOMPLEXPROBLEMSTHATTHEWORLDFACESWEWILLCONTINUETOBEGUIDEDBYTHEIDEATHATWECANACHIEVESOMETHINGMUCHGREATERTOGETHERTHANWECANINDIVIDUALLYAFTERALLTHATWASTHEIDEATHATLEDTOTHECREATIONOFOURUNIVERSITYINTHEFIRSTPLACE"""

fpoly = [8, 4, 3, 2]
state = [0, 0, 0, 0, 0, 0, 0, 1]
state2 = [1, 0, 0, 0, 0, 0, 0, 0]
L = LFSR(fpoly=fpoly,initstate =state2)

k = len(plaintext)*8
seq_k  = L.runKCycle(k)
key = L.arr2str(seq_k)

key2 = lfsr_key(state, fpoly)


plaintext_binary = string_to_binary(plaintext)

ciphertext_binary = xor_binary_strings(plaintext_binary, key)
ciphertext = binary_to_string(ciphertext_binary)
print("Fibonacci's LFSR ciphertext:")
print(ciphertext)
print('')

ciphertext_binary_g = xor_binary_strings(plaintext_binary, key2)
ciphertext_g = binary_to_string(ciphertext_binary_g)
print("Galois's LFSR ciphertext:")
print(ciphertext_g)
print('')

decrypted_binary = xor_binary_strings(ciphertext_binary, key)
decryptedtext = binary_to_string(decrypted_binary)
print('Decrypted text:')
print(decryptedtext)
print('')

def generate_keystream_equations(initial_state, keystream, n):
    A = []
    B = []
    
    current_state = initial_state[:]

    # Generate equations based on the length of the keystream
    t = 0
    for i in range(8, len(keystream)):
        t+=1
        equation = current_state[:]  # This copies the current state
        A.append(equation)
        tmp = [int(keystream[i])]
        B.append(tmp)

        current_state = [int(keystream[i])] + current_state[:7]
    
    return np.array(A), np.array(B)


A, B = generate_keystream_equations(state2, key, 8)


for i in range(1, 256, 2):  # There are 2^8 possible combinations for C
    # Generate a potential C matrix
    binary_numbers = format(i, '08b')
    array = [int(x) for x in str(binary_numbers)]
    potential_C = np.reshape(array, (-1, 1))

    result = ((A @ potential_C)) % 2
    if np.array_equal(result, B):
        print('')
        print("Found characteristic polynomial:")
        t = 0
        for i in range(7, -1, -1):

            if potential_C[i][0] != 0:
                if t != 0:
                    print(' + ', end = '')
                print(f'x^{i + 1}', end = '')
                t += 1
        print(' + 1\n')
        break