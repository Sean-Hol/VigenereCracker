import sys
import string
import re
import math 

# Name: Sean Holschier z5308039
# Assignment: Programming for Security Assignment 1
# Description: A python script for decoding a text file encrypted with a Vigenere cipher, with no given key. 
#   Utilises a modified version of the Kasiski examination method where rather than a repetition of a keyword is searched for, we look for any single letter matches for any shift amount. Then the greatest common denominator is considered the key length.
#   Once the key length is determined, english unigram frequency analysis is used to break the caesar cipher for each letter of the key.

#Utilises shifting and looking for patterns of letters match to find the key length.
def solveKeyLen(alphastring):
    shiftAmounts = []
    matches = []
    #shifts the string and looks for matches
    for i in range(5, 100):
        count = 0
        for j in range(len(alphastring) - i):
            if alphastring[j] == alphastring[j+i]:
                count = count + 1
        shiftAmounts.append(i)
        matches.append(count)
    #get largest value
    large1 = max(matches)
    large1Index = matches.index(large1)
    large1Offset = shiftAmounts[large1Index]
    shiftAmounts.pop(large1Index)
    matches.pop(large1Index)
    #get second largest value
    large2 = max(matches)
    large2Index = matches.index(large2)
    large2Offset = shiftAmounts[large2Index]
    shiftAmounts.pop(large2Index)
    matches.pop(large2Index)
    #get third largest value
    large3 = max(matches)
    large3Index = matches.index(large3)
    large3Offset = shiftAmounts[large3Index]
    shiftAmounts.pop(large3Index)
    matches.pop(large3Index)
    #get fourth largest value
    large4 = max(matches)
    large4Index = matches.index(large4)
    large4Offset = shiftAmounts[large4Index]
    shiftAmounts.pop(large4Index)
    matches.pop(large4Index)
    #Gets the greatest common denominator of the 4 largest match offset
    keysize = math.gcd(large1Offset, large2Offset, large3Offset, large4Offset)
    print("Keysize determined to be: " + str(keysize))
    return keysize

#returns entropies of each possible caesar shift per key letter
def getEntropies(letters):
    standardFreq = {
		 'a' : 0.08167, 'b' : 0.01492, 'c' : 0.02782, 'd' : 0.04253, 'e' : 0.12702, 'f' : 0.02228, 'g' : 0.02015, 'h' : 0.06094, 'i' : 0.06966, 'j' : 0.00153, 'k' : 0.00772, 'l' : 0.04025, 'm' : 0.02406,
		'n' : 0.06749, 'o' : 0.07507, 'p' : 0.01929, 'q' : 0.00095, 'r' : 0.05987, 's' : 0.06327, 't' : 0.09056, 'u' : 0.02758, 'v' : 0.00978, 'w' : 0.02360, 'x' : 0.00150, 'y' : 0.01974, 'z' : 0.00074}
    entropies = []
    for i in range(26):
        sum = 0
        for c in letters:
            l = alphabet[((alphabet.index(c) - i)+ 26)% 26]
            sum += math.log(standardFreq[l])
        entropy = ((-sum / math.log(2)) / len(letters))
        entropies.append(entropy)
    return (alphabet[entropies.index(min(entropies))])

#Once key is known, this method will return the decoded text
def decrypt(string, key):
    counter = 0
    newString = ""
    for i in range(len(string)):
        if string[i].isalpha():
            if string[i].isupper():
                newString += (alphabet[(alphabet.index(string[i].lower())-alphabet.index(key[counter]) + 26) %26]).upper()
            else:
                newString += (alphabet[(alphabet.index(string[i])-alphabet.index(key[counter]) + 26) %26])
            counter+=1
            counter = counter % len(key)
        else:
            newString+= string[i]
    return newString


#start of operations, imports text file and extracts string
fullstring = ""
alphabet = list(string.ascii_lowercase)
try:
    filepath = sys.argv[1]
except Exception as err:
    print("Input error. Command should look like:\npython VigenereCracker.py InputFilepath\nRefer to README for usage instructions")
    quit()
with open(filepath, 'r',encoding="utf8") as f:
    fullstring = f.read()
#alphastring is used for cracking the key, fullstring is used for decoding
alphastring = re.sub('[^a-zA-Z]+', '', fullstring)
alphastring = alphastring.lower()
#checks to ensure that there is actually string to decode
if alphastring == "":
    print("No decodable text detected in file")
    quit()
keySize = solveKeyLen(alphastring)
print("Now moving to solve key of length " + str(keySize))
#split into columns based on keySize
c = 0
stringCols = [] 
for i in range(keySize):
    stringCols.append([])
while c < len(alphastring):
    stringCols[c % keySize].append(alphastring[c])
    c +=1
#adds the letter with the lowest entropy to the key
key=""
for i in range(len(stringCols)):
    key = key+ getEntropies(stringCols[i])
print("Key determined to be: " + key)
print("Decrypting with key: " + key)
#string is decoded with key once acquired
decodedString = decrypt(fullstring, key)
print("Decoded message")
print(decodedString)
