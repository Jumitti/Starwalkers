import json
import math

digits = list(range(10000))
for value in [round(-0.0004 + i * 0.0001, 4) for i in range(6)]:
    probabilities_number = []
    for x in digits:
        probability = math.exp(value * x)
        probabilities_number.append(probability)

    total_probability = sum(probabilities_number)
    probabilities_number = [p / total_probability for p in probabilities_number]

    # Sauvegarde des probabilités dans un fichier JSON
    with open(f'probabilities_number_{value}.json', 'w') as f:
        json.dump(probabilities_number, f)

    print("Probabilités sauvegardées avec succès.")
