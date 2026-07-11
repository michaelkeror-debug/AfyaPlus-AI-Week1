import numpy as np

def emergency_tokeniser(text):
    text = text.lower().replace("!", " ! ").replace("?", "").replace(".", "")
    

    tokens = np.array(text.split())

    return tokens


samples = ["Help!!!", "I cannot breathe!", "My chest hurts."]
for s in samples:
    print(s, "->", emergency_tokeniser(s))
