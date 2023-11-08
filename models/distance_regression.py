import math
from pathlib import Path

import pandas as pd
from astropy.io.votable import parse_single_table

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "../tables/dist.vot")

parameters = parse_single_table(parameters_path).to_table().to_pandas()

parameters.insert(column="parallax", value=parameters.pop("__").map(lambda x: 1 / x), loc=3)

print(parameters)

# parameters.pop("phot_g_mean_mag")
# parameters.pop("bc_flame")
# parameters.pop("lum_flame")
# parameters.pop("parallax")


target = parameters.pop("distance_gspphot").map(lambda x: math.log10(x))

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
    tf.keras.layers.Dense(32, activation='sigmoid'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

model.fit(parameters_train, target_train, batch_size=32, epochs=60, verbose=2)

model.evaluate(parameters_test, target_test, verbose=2)
