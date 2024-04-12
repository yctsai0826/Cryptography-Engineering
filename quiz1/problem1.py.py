# Given the text provided by the user, let's write a Python program to calculate the frequencies of the letters in the ciphertext.

ciphertext = """
C UYGHARMZ IUWMPRWIR GAIR YVRMP MBHMZWMPUM C VMMXWPE YV PYR VCZ ZMGYQMD VZYG CXCZG YP CPCXKTWPE CPD MBHXYZM RNM VXYYD YV CDQCPUMD OPYSXMDEM SNWUN MCUN
KMCZ LZWPEI SWRN WR
"""

# Remove spaces and newlines
ciphertext_clean = ciphertext.replace(" ", "").replace("\n", "")

# Calculate frequency of each letter in the ciphertext
frequency = {}
for letter in ciphertext_clean:
    if letter in frequency:
        frequency[letter] += 1
    else:
        frequency[letter] = 1

# Sort the frequency dictionary by value in descending order
sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

print(sorted_frequency)


