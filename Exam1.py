 # ----------------------------
# # Task 1
# Create an xor based encryption that changes the key like the following for every byte: new_key = last_key * key_multiplier + key_increment.
# We have one byte sized key and encrypt the first byte of the plain message with the key.
# The second byte is encrypted by key * key_multiplier + key_increment.
# The third byte is encrypted by second_byte_key * key_multiplier + key_increment.
# And so on.
def encrypt_with_one_byte_prg(plaintext, key, key_multiplier, key_increment):
    '''
    >>> encrypt_with_one_byte_prg('Hello',12,210,43)
    'DfÍQZ'
    >>> encrypt_with_one_byte_prg('Cryptography',99,120,93)
    ' ·ÌEAZRGTE]L'
    >>> encrypt_with_one_byte_prg(encrypt_with_one_byte_prg('Hello',123,12,24),123,12,24)
    'Hello'
    >>> encrypt_with_one_byte_prg(encrypt_with_one_byte_prg('Cryptography',10,44,55),10,44,55)
    'Cryptography'
    '''
    cipher = ''

    for i in plaintext:
        cipher += chr(ord(i) ^ key)
        key = (key * key_multiplier + key_increment) % 256

    return cipher

# ----------------------------
# # Task 2.
# Create a base64_to_hex() function using the base64 library.
import base64


def base64_to_hex(base):
    '''
    >>> base64_to_hex('q80=')
    'abcd'
    >>> base64_to_hex('7u7//6qq')
    'eeeeffffaaaa'
    >>> base64_to_hex('EjRWeJq83g==')
    '123456789abcde'
    >>> base64_to_hex('Ee6qVczd')
    '11eeaa55ccdd'
    '''
    return base64.b64decode(base).hex()


# ----------------------------
# # Task 3.
# Create a function that swaps the first 4 bit with the second 4 bit in a byte.
def swap_lower_and_upper_bits(input):
    '''
    >>> swap_lower_and_upper_bits(0)
    0
    >>> swap_lower_and_upper_bits(1)
    16
    >>> swap_lower_and_upper_bits(2)
    32
    >>> swap_lower_and_upper_bits(8)
    128
    >>> bin(swap_lower_and_upper_bits(0b1111))
    '0b11110000'
    >>> bin(swap_lower_and_upper_bits(0b10011010))
    '0b10101001'
    '''
    bin_input = bin(input)
    bin_input = bin_input[2:].zfill(8)
    swap = bin_input[4:] + bin_input[:4]
    return int(swap, 2)


# ----------------------------
# # Task 4.
# Create a scoring function that returns the number of most used English letters in a given string
def score_text(most_used_letters, text):
    '''
    >>> most_used_letters = 'etaoin'
    >>> score_text(most_used_letters,'cryptography')
    3
    >>> score_text(most_used_letters,'team building')
    6
    >>> score_text(most_used_letters,'eeeoooii')
    8
    '''
    count = 0
    for x in text:
        if x in most_used_letters:
            count += 1
    return count

# ----------------------------
# # Task 5.
# Modify 'decrypt_single_byte_xor' function from week3, so that it applies the scoring function instead of count_simple_text_chars on
# the decrypted_messages and returns the decrypted message with the highest score and score as well.
# Return tuple like you can see the second point here: https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/

from week3 import hex2string, encrypt_single_byte_xor
# import from previous submissions

def decrypt_single_byte_xor(cipher):
    '''
    >>> decrypt_single_byte_xor('48692120596f75206861766520666f756e64206d652120746865206c6f6e6765722074686520746578742074686520656173696572')
    ('Hi! You have found me! the longer the text the easier', 23)
    >>> decrypt_single_byte_xor('370c430106430c11430d0c1743170c4301064f43170b0217430a1043170b064312160610170a0c0d')
    ('To be or not to be, that is the question', 20)
    >>> decrypt_single_byte_xor('37060f0f430e0643020d07432a43050c110406174d43370602000b430e0643020d07432a4311060e060e0106114d432a0d150c0f1506430e0643020d07432a430f0602110d4d')
    ('Tell me and I forget. Teach me and I remember. Involve me and I learn.', 24)
    '''
    most_used_letters = 'etaoin'
    # Run a maximum search on the results
    best = None
    best_score = None
    for key in range(256):
        hex_key = hex(key)[2:]
        decrypted_message = hex2string(encrypt_single_byte_xor(cipher, hex_key))
        score = score_text(most_used_letters, decrypted_message)
        if best_score is None or best_score < score:
            best = decrypted_message
            best_score = score
    return best, best_score


# ----------------------------
# # Task 6.
# There are 50 Base64 strings in the array below.
# One of them contains a message (English text) encrypted with single-byte XOR.
# You have to retrieve the original message.
# Finally put everything together, and apply decrypt_single_byte_xor on each of the decoded hex strings, and return the one with the highest score. and the result must be readable English text
base64_encoded_ciphers = [
    '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'
]


def find_correct_row_in_base64_encoded(base64_encoded_ciphers):
    '''
    >>> find_correct_row_in_base64_encoded(base64_encoded_ciphers)
    'Cryptography is the practice and study of techniques for secure communication in the presence of third parties called adversaries'
    '''
    max = 0
    for i in base64_encoded_ciphers:
        mes, score = decrypt_single_byte_xor(base64_to_hex(i))
        if max < score:
            max = score
            bestmes = mes
    return bestmes
