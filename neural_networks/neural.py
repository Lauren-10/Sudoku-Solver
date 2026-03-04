import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt


# baseline sample code to load data, encode it, build a simple model, train, and plot results.
# only using 10k samples for now (only using one training set for now)
df = pd.read_csv("/Users/brennahenry/Sudoku-Solver/training_data/train_sudoku1.csv", nrows=10_000, header=None, names=['quizzes', 'solutions'])
quizzes   = df['quizzes'].values
solutions = df['solutions'].values

# one hot encode the board: 9x9x9 with 1-9, and 0 is empty
def encode_board(s):
    board = np.array([int(c) for c in s]).reshape(9, 9)
    one_hot = np.zeros((9, 9, 9), dtype=np.float32)
    for r in range(9):
        for c in range(9):
            if board[r, c] != 0:
                one_hot[r, c, board[r, c] - 1] = 1.0
    return one_hot

X = np.array([encode_board(str(q).zfill(81)) for q in quizzes])
y = np.array([[int(c) - 1 for c in str(s).zfill(81)] for s in solutions], dtype=np.int32)

# build simple model
inputs  = keras.Input(shape=(9, 9, 9))
x       = layers.Flatten()(inputs)
x       = layers.Dense(512, activation='relu')(x)
x       = layers.Dense(81 * 9)(x)
outputs = layers.Reshape((81, 9))(x)
model   = keras.Model(inputs, outputs)

model.compile(
    optimizer='adam',
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

# train
history = model.fit(X, y, epochs=5, batch_size=256, validation_split=0.1, verbose=1)

# plot
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history.history['loss'], label='Train')
axes[0].plot(history.history['val_loss'], label='Val')
axes[0].set_title('Loss'); axes[0].set_xlabel('Epoch'); axes[0].legend()
axes[1].plot(history.history['accuracy'], label='Train')
axes[1].plot(history.history['val_accuracy'], label='Val')
axes[1].set_title('Accuracy'); axes[1].set_xlabel('Epoch'); axes[1].legend()
plt.tight_layout()
plt.savefig("10k_samples.png")
plt.show()

final_train_acc = history.history['accuracy'][-1]
final_val_acc   = history.history['val_accuracy'][-1]
final_train_loss = history.history['loss'][-1]
final_val_loss   = history.history['val_loss'][-1]


# print training accuracy and loss
print(f"Final Training Accuracy  : {final_train_acc:.4f}")
print(f"Final Validation Accuracy: {final_val_acc:.4f}")
print(f"Final Training Loss      : {final_train_loss:.4f}")
print(f"Final Validation Loss    : {final_val_loss:.4f}")



# -- After training small model, increase sample size to 10k-300k ---

sample_sizes = [10_000, 50_000, 100_000, 300_000]
results = []

for n in sample_sizes:
    print(f"\nTraining with {n:,} samples")
    df_n = pd.read_csv("/Users/brennahenry/Sudoku-Solver/training_data/train_sudoku1.csv", 
                       nrows=n, header=None, names=['quizzes', 'solutions'])
    X_n = np.array([encode_board(str(q).zfill(81)) for q in df_n['quizzes'].values])
    y_n = np.array([[int(c) - 1 for c in str(s).zfill(81)] for s in df_n['solutions'].values], dtype=np.int32)
    
    # new model for each sample size
    model_n = keras.Model(inputs, outputs)
    model_n.compile(optimizer='adam',
                    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
    h = model_n.fit(X_n, y_n, epochs=5, batch_size=256, validation_split=0.1, verbose=0)
    results.append({
        'samples': n,
        'val_accuracy': h.history['val_accuracy'][-1],
        'val_loss': h.history['val_loss'][-1]
    })
    print(f"  Val accuracy: {h.history['val_accuracy'][-1]:.4f}")

# plot accuracy vs sample size to see how it scales
plt.figure(figsize=(7, 4))
plt.plot([r['samples'] for r in results], [r['val_accuracy'] for r in results], marker='o')
plt.title('Accuracy vs Training Set Size')
plt.xlabel('Number of Training Samples')
plt.ylabel('Accuracy')
plt.tight_layout()
plt.savefig("accuracy_vs_samples_300k.png")
plt.show()


# print results in a table format
print("\n Results Summary")
for r in results:
    print(f"Samples: {r['samples']:>7,} | Val Accuracy: {r['val_accuracy']:.4f} | Val Loss: {r['val_loss']:.4f}")
    