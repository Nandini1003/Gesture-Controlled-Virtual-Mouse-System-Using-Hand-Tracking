import mediapipe as mp

print("Version:", mp.__version__)
print("solutions exists:", hasattr(mp, "solutions"))
print(mp.solutions.hands)
