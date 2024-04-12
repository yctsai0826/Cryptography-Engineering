import numpy as np
import itertools

# Define the ciphertext and remove spaces
ciphertext = "UONCSVAIHGEPAAHIGIRLBIECSTECSWPNITETIENOIEEFDOWECXTRSRXSTTARTLODYFSOVNEOECOHENIODAARQNAELAFSGNOPTE".replace(
    " ", "")

# Count the total number of characters
total_characters = len(ciphertext)

# Estimate the total number of vowels (approx 40% of total characters)
total_vowels = total_characters * 0.4

# Define the vowels
vowels = "AEIOU"

# Count the actual number of vowels in the ciphertext
actual_vowel_count = sum(1 for char in ciphertext if char in vowels)

# Possible dimensions of the rectangle (factors of the total number of characters)
dimensions = [(i, total_characters // i) for i in range(1, total_characters + 1) if total_characters % i == 0]

# Define a function to calculate the number of vowels in each row for given dimensions
rows = []
for i in range(14):
    r = ""
    for j in range(7):
        r += ciphertext[i + j * 14]
    rows.append(r)
matrix = rows


def calculate_vowels_per_row(ciphertext, row_length, vowels, x, y):
    rows = []
    for i in range(x):
        r = ""
        for j in range(y):
            r += ciphertext[i + j * x]
        rows.append(r)

    vowel_counts = [sum(1 for char in row if char in vowels) for row in rows]
    return vowel_counts


for x, y in dimensions:
    difference = 0
    vc = calculate_vowels_per_row(ciphertext, y, vowels, x, y)
    for i in vc:
        difference += abs((y * 0.4) - i)
    difference /= x
    print(f"({x}, {y}) average difference: {difference}")

best_dimension = [14, 7]
train_data = 'withmalicetowardnonewithcharityforallwithfirmnessintherightasgodgivesustoseetherightletusstriveontofinishtheworkweareintobindupthenationswoundstocareforhimwhoshallhavebornethebattleandforhiswidowandhisorphantodoallwhichmayachieveandcherishajustandlastingpeaceamongourselvesandwithallnationsgreeceannouncedyesterdaytheagragreementwithtrukeyendthecyprusthatthegreekandturkishcontingentswhicharetoparticipateinthetripartiteheadquartersshallcompriserespectivelygreekofficersnoncommissionedofficersandmenandturkishofficersnoncommissionedofficersandmenthepresidentandvicepresidentoftherepublicofcyprusactinginagreementmayrequestthegreekandturkishgovernmentstoincreaseorreducethegreekandturkishcontingentsitisagreedthatthesitesofthecantonmentsforthegreekandturkishcontingentsparticipatinginthetripartiteheadquarterstheirjuridicalstatusfacilitiesandexemptionsinrespectofcustomsandtaxesaswellasotherimmunitiesandprivilegesandanyothermilitaryandtechnicalquestionsconcerningtheorganizationandoperationoftheheadquartersmentionedaboveshallbedeterminedbyaspecialconventionwhichshallcomeintoforcenotlaterthanthetreatyofalliance'

# Train Markov chain model
# Initialize: The matrix is of size 26x26x26 to account for the probability of a letter based on the preceding two letters
transition_matrix = np.zeros((26, 26, 26))


# Function to convert character to matrix index
def char2index(char):
    return ord(char.lower()) - ord('a')


# Build the transition matrix based on the probabilities in text2
for i in range(0, len(train_data) - 2):
    if train_data[i].isalpha() and train_data[i + 1].isalpha() and train_data[i + 2].isalpha():
        index1 = char2index(train_data[i])
        index2 = char2index(train_data[i + 1])
        index3 = char2index(train_data[i + 2])
        transition_matrix[index1, index2, index3] += 1

# Normalize the transition matrix to get probabilities
transition_matrix += 1e-6
transition_matrix = transition_matrix / transition_matrix.sum(axis=2, keepdims=True)

def score_sequence(sequence, transition_matrix):
    score = 0
    for i in range(len(sequence) - 2):
        if sequence[i].isalpha() and sequence[i + 1].isalpha() and sequence[i + 2].isalpha():
            index1 = char2index(sequence[i])
            index2 = char2index(sequence[i + 1])
            index3 = char2index(sequence[i + 2])
            score += np.log(transition_matrix[index1, index2, index3])
    return score

# Hold the best score and the corresponding permutation
best_score = float('-inf')
best_permutation = None
best_sequence = None
# Generate all permutations of indexes 0 to 6
permutations = list(itertools.permutations(range(0, 7)))

# Iterate over each permutation
for perm in permutations:
    # Apply the same permutation to all rows
    permuted_matrix = [''.join([row[i] for i in perm]) for row in matrix]
    # Flatten the matrix into a single sequence
    sequence = ''.join(permuted_matrix)
    # Score the sequence
    score = score_sequence(sequence, transition_matrix)
    # Update best score and permutation if this is the best so far
    if score > best_score:
        best_score = score
        best_permutation = perm
        best_sequence = sequence


# Output the results
print("Decrypted text:", best_sequence)
