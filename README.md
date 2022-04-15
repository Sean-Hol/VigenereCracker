# VigenereCracker

## Description:
    A python script for decoding a text file encrypted with a Vigenere cipher, with no given key. Utilises a modified version of the Kasiski examination method where rather than a repetition of a keyword is searched for, we look for any single letter matches for any shift amount. Then the greatest common denominator is considered the key length. Once the key length is determined, english unigram frequency analysis is used to break the caesar cipher for each letter of the key.

## Design decisions:
    I found that the single character version of Kasiski's method was fairly effective, so I implemented this, which would have a better processing speed over the 3 letter phrases that is originally used in this method. However, this may not be as effective with larger keys, and as we only shift by up to 100 characters, larger keys may not be as well detected. When testing, I tested with key lengths of up to 20 characters, all of which we actually returned. The use of the entropy analysis equation that I found through some research could be used to return a decimal value on how much a collection of letters vary from standard English unigram frequencies, from which the lowest value can be taken as the correct number of shifts. Testing showed that this method was very effective.

## How to use:
    The command to call this script should look like this:
        python VigenereCracker.py InputFilepath

    InputFilepath = This should be the filepath of a textfile containing Vigenere cipher encrypted text.

    The length of the key, the key itself and the decoded text should all be printed onto the terminal once calculated.

## Example test:
    test.txt contains the full lyrics to "The Duck Song" encoded with the key "fishandchips"

###    Input:
        python .\VigenereCracker.py .\test.txt

###    Terminal output:
        Keysize determined to be: 12
        Now moving to solve key of length 12
        Key determined to be: fishandchips
        Decrypting with key: fishandchips
        Decoded message
        A duck walked up to a lemonade stand
        And he said to the man runnin' the stand
        ....REST OF DECODED LYRICS....
