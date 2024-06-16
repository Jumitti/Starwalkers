import json
import math


letters = ["*", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                   'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

probabilities = []
for x in range(0, len(letters)):
    probabilities.append(math.exp(0.4 * x))

total = sum(probabilities)
probabilities = [p / total for p in probabilities]

# Sauvegarde des probabilités dans un fichier JSON
with open('starwalkers/probabilities_letter_player.json', 'w') as f:
    json.dump(probabilities, f)

print("Probabilités sauvegardées avec succès.")