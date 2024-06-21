import json
import math

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for value in [round(0.0 + i * 0.1, 1) for i in range(6)]:
    probabilities = []
    for x in range(0, len(letters)):
        probabilities.append(math.exp(value * x))

    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]

    # Sauvegarde des probabilités dans un fichier JSON
    with open(f'probabilities_letter_{value}.json', 'w') as f:
        json.dump(probabilities, f)

    print(f"Probabilités pour value={value} sauvegardées avec succès.")

