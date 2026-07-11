import numpy as np

embeddings = {
    "fever":     np.array([0.9, 0.0, 0.3]),
    "pain":      np.array([0.8, 0.1, 0.4]),
    "discharge": np.array([0.5, 0.5, 0.1]),
    "billing":   np.array([0.0, 0.9, 0.1]),
    "admit":     np.array([0.2, 0.8, 0.2]),
    "cough":     np.array([0.8, 0.5, 0.3 ])
    # TODO 1: Add a 'cough' vector that sits close to 'fever' and far from 'billing'.
}

def cosine_similarity(word1, word2):
    vec1, vec2 = embeddings[word1], embeddings[word2]
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(f"cough vs fever:   {cosine_similarity('cough', 'fever'):.4f}")
print(f"cough vs billing: {cosine_similarity('cough', 'billing'):.4f}")

# TODO 2: Print cosine_similarity('cough', 'fever') and cosine_similarity('cough', 'billing').
# TODO 3: Confirm the fever score is meaningfully higher than the billing score.