import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/shodan_results.csv")

# Simulate labels (1 = exposed camera, 0 = benign)
df['label'] = df['data'].apply(lambda x: 1 if "webcam" in x.lower() or "surveillance" in x.lower() else 0)

# Vectorize banner data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['data'])
y = df['label']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict and flag
predictions = model.predict(X_test)
print("Model trained. Accuracy:", model.score(X_test, y_test))

# Visualize the distribution of flagged devices
plt.hist(df['label'], bins=2, edgecolor='black')
plt.title("Exposed vs Benign Devices")
plt.xlabel("Device Type (0 = Benign, 1 = Exposed)")
plt.ylabel("Count")
plt.xticks([0, 1])
plt.grid(True)
plt.show()
