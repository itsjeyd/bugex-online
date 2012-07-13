'''
Created on Jul 10, 2012

an adaption of:
www.ironzebra.com/news/30/create-random-pronounceable-passwords-in-pythondjango

@author: Iliana Simova
'''
import itertools

from django.utils.crypto import get_random_string

def get_pronounceable_pass(num_syllables, num_digits, include_upper=True):
    '''Generates a pseudo random password which is easier to remember.
    
    Generates a pseudo random password which is easier to remember due to 
    being easier to pronounce. The password can contain a number of random 
    'syllables' (consonant+vowel sequences), followed by randomly generated 
    digits. By default the generated password includes capital letters. The 
    generated password does not contain letters and digits that look similar 
    (e.g. 'I','1' and 'l' or 'O' and '0'), in order to avoid confusion 
    (as in django.contrib.auth.models.make_random_password()). 
    
    num_sylables -- the number of syllables to form the password prefix
    num_digits -- the number of digits to form the password suffix
    include_upper -- when True, the password may include capital letters
    '''
    digits = '23456789'     
    
    #to avoid confusion, the generated password may not include letters and 
    #digits that look similar (e.g. 'I','1' and 'l' or 'O' and '0') 
    if include_upper:
        consonants = 'bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        vowels = 'aeiouAEU'
    else:
        consonants = 'bcdfghjkmnpqrstvwxyz'
        vowels = 'aeiou'
    
    syllables = map(''.join, itertools.product(consonants,vowels))
    
    return get_random_string(num_syllables,syllables) + \
                get_random_string(num_digits,digits)
    
    