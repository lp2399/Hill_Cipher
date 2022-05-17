import math
import numpy as np
import re
import random
from sympy import Matrix 

def text_to_numerical_val_list(input_text):
    regex = re.compile('[^a-zA-Z]')
    input_text = regex.sub('', input_text)
    input_text = re.sub(r"\s+", "", input_text, flags=re.UNICODE)
    input_text = input_text.lower()
    text_char_to_numerical_value_list = []
    for character in input_text:
        numerical_value = ord(character) - 97
        text_char_to_numerical_value_list.append(numerical_value)
    return text_char_to_numerical_value_list    

def create_matrix(n, v):
    matrix = []
    for i in range(n):
        row_list = []
        for j in range(n):
            row_list.append(v[n * i + j])
        matrix.append(row_list)
    return matrix   

def sublists(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def is_square(M):
    square_matrix = False
    for i in M:
        if(len(M)==len(i)):
            square_matrix = True
    return square_matrix

def modular_inverse_matrix(M,n):
    determinant = int(np.linalg.det(M))
    try:
      modular_inverse = pow(determinant, -1, n)
    except :
        print("Matrix is not invertible for the given modulus")
    try:
      inverse_matrix = np.linalg.inv(M)    
    except :
        print("Matrix is not invertible")
    A = Matrix(M)
    A = A.inv_mod(n)
    return A

def encipher(plaintext,key): 
    plaintext_numerical_val_list= text_to_numerical_val_list(plaintext)
    if(type(key)==str):
        key_numerical_val_list = text_to_numerical_val_list(key)
        n = int(math.sqrt(len(key)))
        if(len(key)/n!=float(n)):
            return "Key length must be a perfect square"
        enciphering_matrix = create_matrix(n, key_numerical_val_list)    
    key_numerical_val_list = key 
    if(is_square(key_numerical_val_list)!=True):
        return "Key must be a perfect square"      
    if(is_square(key_numerical_val_list)):
        n = len(key)     
        enciphering_matrix = key
    flag_is_divisible = False
    if(len(plaintext_numerical_val_list)%n!=0):
        while flag_is_divisible==False:
            r = random.randint(0, 25)
            plaintext_numerical_val_list.append(r)
            if(len(plaintext_numerical_val_list)%n==0):
                flag_is_divisible = True
    vector_list = list(sublists(plaintext_numerical_val_list, n))  
    multiplied_values = []  
    for i in vector_list:
        multiplied_values.append(np.matmul(i,enciphering_matrix))
    enciphered_list = [] 
    for i in multiplied_values:
        for j in i:
            enciphered_list.append(chr(((j)% 26)+97))   
    cipher_text = ''.join(str(char) for char in enciphered_list)
    return "Cipher text:  "+cipher_text.upper()

def decipher(ciphertext,key): 
    ciphertext_numerical_val_list= text_to_numerical_val_list(ciphertext)
    if(type(key)==str):
        key_numerical_val_list = text_to_numerical_val_list(key)
        n = int(math.sqrt(len(key)))
        if(len(key)/n!=float(n)):
            return "Key length must be a perfect square"
        enciphering_matrix = create_matrix(n, key_numerical_val_list)    
    key_numerical_val_list = key 
    if(is_square(key_numerical_val_list)!=True):
        return "Key must be a perfect square"      
    if(is_square(key_numerical_val_list)):
        n = len(key)     
        enciphering_matrix = key
    vector_list = list(sublists(ciphertext_numerical_val_list, n))  
    mod_inverse_matrix = modular_inverse_matrix(enciphering_matrix,26)
    multiplied_values = []  
    for i in vector_list:
        multiplied_values.append(np.matmul(i,mod_inverse_matrix))
    deciphered_list = []     
    for i in multiplied_values:
        for j in i:
            deciphered_list.append(chr(((j)% 26)+97))   
    plain_text = ''.join(str(char) for char in deciphered_list)    
    return "Plain text: "+plain_text.lower()

print(encipher("jack and jill went up the hill",[[1,2,3,4],[4,3,2,1],[11,2,4,6],[2,9,6,4]]))
print(decipher("ZIRKZWOPJJOPTFAPUHFHADRQ",[[1,2,3,4],[4,3,2,1],[11,2,4,6],[2,9,6,4]]))
