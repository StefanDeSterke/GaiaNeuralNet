from pathlib import Path
from astropy.io.votable import parse_single_table

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "tables/teff.vot")

parameters = parse_single_table(parameters_path).to_table().to_pandas()

print(parameters)

# Definieer de verschillende labels.
labels = ["CSTAR", "M", "K", "G", "F", "A", "B", "O"]


# Zet een label om naar zijn id.
def label_to_identifier(label: str) -> int:
    return labels.index(label)


# Zet een temperatuur om in zijn bijbehorende label.
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

print(target)

import tensorflow as tf

parameters = tf.convert_to_tensor(parameters, dtype=tf.float32)
target = tf.convert_to_tensor(target, dtype=tf.int8)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(1, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics='MeanSquaredError'
)

model.fit(parameters, target, batch_size=32, epochs=10, verbose=2)
