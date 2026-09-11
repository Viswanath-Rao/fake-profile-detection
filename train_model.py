import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

data = {
    'followers': [50, 120, 300, 800, 2000, 5000, 20, 80, 150, 400],
    'following': [60, 100, 200, 300, 500, 400, 300, 200, 100, 600],
    'posts': [2, 5, 20, 50, 120, 300, 1, 3, 10, 25],
    'fake':     [0, 0, 0, 0, 0, 0, 1, 1, 0, 1]
}

df = pd.DataFrame(data)

# NEW FEATURE
df['ratio'] = df['followers'] / (df['following'] + 1)

X = df[['followers', 'following', 'posts', 'ratio']]
y = df['fake']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

pickle.dump(model, open('model.pkl', 'wb'))

print("Better model trained!")