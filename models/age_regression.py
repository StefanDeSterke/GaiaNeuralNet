import math
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
from astropy.io.votable import parse_single_table

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "../tables/age.vot")

# Laad de parameters in als een pandas Dataframe.
parameters = parse_single_table(parameters_path).to_table().to_pandas()

# Print de huidige parameters om te kijken of het klopt.
print(parameters)

# Hier wordt de te voorspellen leeftijd gescheiden van de andere parameters.
target = parameters.pop("age_flame")

# Definieer het aandeel van de trainingsset t.o.v. de validatieset.
train_frac = 0.7
train_size = int(len(parameters) * 0.7)

# Splits de trainingsset van de validatieset. Deze parameters zijn pandas Series.
parameters_train = parameters.iloc[:train_size]
parameters_test = parameters.iloc[train_size:]

target_train = target.iloc[:train_size]
target_test = target.iloc[train_size:]

import tensorflow as tf

# Converteer de pandas Series naar een TensorFlow Tensor.
parameters_train = tf.convert_to_tensor(parameters_train, dtype=tf.float32)
parameters_test = tf.convert_to_tensor(parameters_test, dtype=tf.float32)

target_train = tf.convert_to_tensor(target_train, dtype=tf.float32)
target_test = tf.convert_to_tensor(target_test, dtype=tf.float32)

# Initialiseer het model via een Sequential. Ook de activatiefunctie wordt hier gedefinieerd.
model = tf.keras.models.Sequential([
    tf.keras.layers.Normalization(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compileer het model met een specifieke learning rate en de gemiddelde kwadratische afwijking als loss functie.
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

# Train het model en sla het trainingsproces op als een History datatype.
history: tf.keras.callbacks.History = model.fit(parameters_train, target_train, batch_size=32, epochs=30, verbose=2)

# Test het model aan de hand van de validatieset.
model.evaluate(parameters_test, target_test, verbose=2)

# Zet de history om in een pandas Dataframe.
history_df = pd.DataFrame(history.history)["loss"]

# Schrijf de history naar een csv file.
csv_path = str(script_location / "../models/results/age_regression_1.csv")

with open(csv_path, 'w') as f:  # You will need 'wb' mode in Python 2.x
    history_df.to_csv(f)
