import json
import math

digits = list(range(10000))
probabilities_number = []
for x in digits:
    probability = math.exp(-0.0005 * x)
    probabilities_number.append(probability)

total_probability = sum(probabilities_number)
probabilities_number = [p / total_probability for p in probabilities_number]

# Sauvegarde des probabilités dans un fichier JSON
with open('probabilities_number.json', 'w') as f:
    json.dump(probabilities_number, f)

print("Probabilités sauvegardées avec succès.")
