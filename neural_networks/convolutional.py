import numpy as np
import pandas as pd
import keras
import matplotlib.pyplot as plt
import os

from sudoku import Sudoku

path = os.getcwd()

df = pd.read_csv(path + "/training_data/train_sudoku1.csv", nrows=100_000, header=None, names=['quizzes', 'solutions'])

class DataGenerator(keras.utils.Sequence):
    def __init__(self, df,batch_size = 16, subset = "train", shuffle = False, info={}):
        super().__init__()
        self.df = df
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.subset = subset
        self.info = info

        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.df)/self.batch_size))
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.df))
        if self.shuffle==True:
            np.random.shuffle(self.indexes)

    def __getitem__(self,index):
        X = np.empty((self.batch_size, 9,9,1))
        y = np.empty((self.batch_size,81,1))
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        for i,f in enumerate(self.df['quizzes'].iloc[indexes]):
            f = f"{f:0>81}"
            self.info[index*self.batch_size+i]=f
            X[i,] = (np.array(list(map(int, list(f)))).reshape((9,9,1))/9)-0.5
        if self.subset == 'train':
            for i,f in enumerate(self.df['solutions'].iloc[indexes]):
                f = f"{f:0>81}"
                self.info[index*self.batch_size+i]=f
                y[i,] = np.array(list(map(int,list(f)))).reshape((81,1)) - 1
        if self.subset == 'train': return X, y
        else: return X

model = keras.models.Sequential()
model.add(keras.layers.Input(shape=(9,9,1)))
# Add convolutional layers
model.add(keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Conv2D(128, (1,1), padding='same', activation='relu'))
#flatten
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(81*9))
model.add(keras.layers.Reshape((-1, 9)))
model.add(keras.layers.Activation('softmax'))

model.compile(loss="sparse_categorical_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])

train_idx = int(len(df)*0.95)
data = df.sample(frac=1).reset_index(drop=True)
training_generator = DataGenerator(data.iloc[:train_idx], subset = "train", batch_size=256)
validation_generator = DataGenerator(data.iloc[train_idx:], subset = "train",  batch_size=256)

history = model.fit(training_generator, validation_data=validation_generator, epochs=5)

model.save('conv_model')

# plot
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history.history['loss'], label='Train')
axes[0].plot(history.history['val_loss'], label='Val')
axes[0].set_title('Loss'); axes[0].set_xlabel('Epoch'); axes[0].legend()
axes[1].plot(history.history['accuracy'], label='Train')
axes[1].plot(history.history['val_accuracy'], label='Val')
axes[1].set_title('Accuracy'); axes[1].set_xlabel('Epoch'); axes[1].legend()
plt.tight_layout()
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
