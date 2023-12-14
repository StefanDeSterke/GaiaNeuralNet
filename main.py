from pathlib import Path
from astropy.io.votable import parse_single_table
import pandas as pd

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "tables/teff.vot")

parameters = parse_single_table(parameters_path).to_table().to_pandas()

print(parameters)

labels = ["CSTAR", "M", "K", "G", "F", "A", "B", "O"]


def label_to_identifier(label: str) -> int:
    return labels.index(label)


def temp_to_spectraltype(temp: float) -> str:
    if temp < 2400:
        return labels[0]
    elif temp < 3700:
        return labels[1]
    elif temp < 5200:
        return labels[2]
    elif temp < 6000:
        return labels[3]
    elif temp < 7500:
        return labels[4]
    elif temp < 10000:
        return labels[5]
    elif temp < 30000:
        return labels[6]
    else:
        return labels[7]


target = parameters.copy()
target = target.map(temp_to_spectraltype).map(label_to_identifier)

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

target_train = tf.convert_to_tensor(target_train, dtype=tf.int32)
target_validate = tf.convert_to_tensor(target_validate, dtype=tf.int32)
target_test = tf.convert_to_tensor(target_test, dtype=tf.int32)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

history: tf.keras.callbacks.History = model.fit(parameters_train, target_train, batch_size=16, epochs=10, verbose=2)

model.evaluate(parameters_validate, target_validate, verbose=2)

history_df = pd.DataFrame(history.history)["loss"]

csv_path = str(script_location / "models/results/spectraltype_regression_3.csv")

with open(csv_path, 'w') as f:
    history_df.to_csv(f)

model.evaluate(parameters_test, target_test, verbose=2)

model.save(str(script_location / "models/results/spectraltype_regression_3.keras"), save_format="keras")

print(model.predict([6000]))
