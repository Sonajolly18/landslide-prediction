import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the original dataset
df = pd.read_csv('encoded_data.csv')
# Split the dataset into features (X) and target variable (y)
X = df.drop('Type_of_sl', axis=1)
y = df['Type_of_sl']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train model
rf_model.fit(X_train, y_train)

# Evaluate the model
predictions = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy}")

# Save the model
joblib.dump(rf_model, 'rf_model.pkl')

