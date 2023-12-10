import math
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
from astropy.io.votable import parse_single_table

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "../tables/age.vot")

parameters = parse_single_table(parameters_path).to_table().to_pandas()

print(parameters)

target = parameters.pop("age_flame")

train_frac = 0.7
train_size = int(len(parameters) * 0.7)

parameters_train = parameters.iloc[:train_size]
parameters_test = parameters.iloc[train_size:]

target_train = target.iloc[:train_size]
target_test = target.iloc[train_size:]

print(target)

import tensorflow as tf

parameters_train = tf.convert_to_tensor(parameters_train, dtype=tf.float32)
parameters_test = tf.convert_to_tensor(parameters_test, dtype=tf.float32)

target_train = tf.convert_to_tensor(target_train, dtype=tf.float32)
target_test = tf.convert_to_tensor(target_test, dtype=tf.float32)

print(parameters_train.get_shape())
print(target_train.get_shape())

model = tf.keras.models.Sequential([
    tf.keras.layers.Normalization(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

history: tf.keras.callbacks.History = model.fit(parameters_train, target_train, batch_size=32, epochs=30, verbose=2)

model.evaluate(parameters_test, target_test, verbose=2)

history_df = pd.DataFrame(history.history)["loss"]

csv_path = str(script_location / "../models/results/age_regression_1.csv")

with open(csv_path, 'w') as f:  # You will need 'wb' mode in Python 2.x
    history_df.to_csv(f)
