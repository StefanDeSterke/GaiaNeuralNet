import math
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
from astropy.io.votable import parse_single_table

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "../tables/dist.vot")

parameters = parse_single_table(parameters_path).to_table().to_pandas()

parameters.insert(column="parallax", value=parameters.pop("__").map(lambda x: 1 / x), loc=3)

print(parameters)

parameters.pop("parallax")

target = parameters.pop("distance_gspphot").map(lambda x: math.log10(x))

train_frac = 0.7
train_size = int(len(parameters) * train_frac)

validation_frac = 0.85
validation_size = int(len(parameters) * validation_frac)

parameters_train = parameters.iloc[:train_size]
parameters_validate = parameters.iloc[train_size:validation_size]
parameters_test = parameters.iloc[validation_size:]

target_train = target.iloc[:train_size]
target_validate = target.iloc[train_size:validation_size]
target_test = target.iloc[validation_size:]

import tensorflow as tf

parameters_train = tf.convert_to_tensor(parameters_train, dtype=tf.float32)
parameters_validate = tf.convert_to_tensor(parameters_validate, dtype=tf.float32)
parameters_test = tf.convert_to_tensor(parameters_test, dtype=tf.float32)

target_train = tf.convert_to_tensor(target_train, dtype=tf.float32)
target_validate = tf.convert_to_tensor(target_validate, dtype=tf.float32)
target_test = tf.convert_to_tensor(target_test, dtype=tf.float32)

model = tf.keras.models.Sequential([
    tf.keras.layers.Normalization(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

history: tf.keras.callbacks.History = model.fit(parameters_train, target_train, batch_size=32, epochs=10, verbose=2)

model.evaluate(parameters_validate, target_validate, verbose=2)

history_df = pd.DataFrame(history.history)["loss"]

csv_path = str(script_location / "results/distance_regression_3.csv")

with open(csv_path, 'w') as f:  # You will need 'wb' mode in Python 2.x
    history_df.to_csv(f)

model.save(str(script_location / "results/distance_regression_3.keras"), save_format="keras")

model.evaluate(parameters_test, target_test, verbose=2)

'''
sumSquaredError = 0

for i in range(0, len(parameters_test)):
    params_datapoint = parameters_test[i]
    target_datapoint = target_test[i]

    params_predict = model.predict(params_datapoint, verbose=0)

    error = math.pow(10, params_predict[0][0]) - math.pow(10, tf.get_static_value(target_datapoint))

    error /= math.pow(10, tf.get_static_value(target_datapoint))

    sumSquaredError += error * error

    print(f"Predicted: {math.pow(10, params_predict[0][0])}")
    print(f"Real: {math.pow(10, tf.get_static_value(target_datapoint))}")
    print(error)
    print(sumSquaredError / (i + 1))

print(sumSquaredError / len(parameters_test))
'''