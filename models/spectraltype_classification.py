from pathlib import Path
from astropy.io.votable import parse_single_table
import pandas as pd

script_location = Path(__file__).absolute().parent

parameters_path = str(script_location / "../tables/teff.vot")

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


# Hier wordt de te voorspellen spectraaltype gescheiden van de andere parameters.
target = parameters.copy()
target = target.map(temp_to_spectraltype).map(label_to_identifier)

# Definieer het aandeel van de trainingsset t.o.v. de validatieset.
train_frac = 0.7
train_size = int(len(parameters) * train_frac)

validation_frac = 0.85
validation_size = int(len(parameters) * validation_frac)

# Splits de trainingsset van de validatieset. Deze parameters zijn pandas Series.
parameters_train = parameters.iloc[:train_size]
parameters_validate = parameters.iloc[train_size:validation_size]
parameters_test = parameters.iloc[validation_size:]

target_train = target.iloc[:train_size]
target_validate = target.iloc[train_size:validation_size]
target_test = target.iloc[validation_size:]

import tensorflow as tf

# Converteer de pandas Series naar een TensorFlow Tensor.
parameters_train = tf.convert_to_tensor(parameters_train, dtype=tf.float32)
parameters_validate = tf.convert_to_tensor(parameters_validate, dtype=tf.float32)
parameters_test = tf.convert_to_tensor(parameters_test, dtype=tf.float32)

target_train = tf.convert_to_tensor(target_train, dtype=tf.int32)
target_validate = tf.convert_to_tensor(target_validate, dtype=tf.int32)
target_test = tf.convert_to_tensor(target_test, dtype=tf.int32)

# Initialiseer het model via een Sequential. Ook de activatiefunctie wordt hier gedefinieerd.
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32, activation='relu'),
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
history: tf.keras.callbacks.History = model.fit(parameters_train, target_train, batch_size=16, epochs=10, verbose=2)

# Test het model aan de hand van de validatieset.
model.evaluate(parameters_validate, target_validate, verbose=2)

# Zet de history om in een pandas Dataframe.
history_df = pd.DataFrame(history.history)["loss"]

# Schrijf de history naar een csv file.
csv_path = str(script_location / "results/spectraltype_regression_3.csv")

with open(csv_path, 'w') as f:
    history_df.to_csv(f)

# Test het model aan de hand van de testset.
model.evaluate(parameters_test, target_test, verbose=2)

# Sla het model op als een .keras bestand.
model.save(str(script_location / "results/spectraltype_regression_3.keras"), save_format="keras")
