import pickle

x = pickle.load(open("sequence.pkl", "rb"))

print("\n".join(x))
