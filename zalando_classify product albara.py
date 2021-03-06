# -*- coding: utf-8 -*-
"""zalando megabagus .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1miGLOgH2W30wN4FymopIA5TDVh9ZfaQ5
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

from keras.datasets import fashion_mnist
(X_train, y_train),(X_test, y_test) = fashion_mnist.load_data()

kategori = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shrit', 'Sneaker', 'Bag', 'Ankle boot']

i = random.randint(1, len(X_train))
plt.figure()
plt.imshow(X_train[i,:,:], cmap='gray')
plt.title('item ke {} . kategori = {}' .format(i, kategori[y_train[i]]))
plt.show()

nrow = 10
ncol = 10
fig, axes = plt.subplots(nrow, ncol)
axes = axes.ravel()
ntraining = len(X_train)
for i in np.arange(0, nrow*ncol):
  indexku = np.random.randint(0, ntraining)
  axes[i].imshow(X_train [indexku,:,:], cmap = 'gray')
  axes[i].set_title(int(y_train[indexku]), fontsize = 8)
  axes[i].axis('off')
plt.subplots_adjust(hspace=0.4)

X_train = X_train/225
X_test = X_test/225

from sklearn.model_selection import train_test_split
X_train, X_validate, y_train, y_validate = train_test_split(X_train,y_train,test_size=0.2,random_state=123)

X_train = X_train.reshape(X_train.shape[0], *(28,28,1))
X_test = X_test.reshape(X_test.shape[0], *(28,28,1))
X_validate = X_validate.reshape(X_validate.shape[0], *(28,28,1))

from keras.models import Sequential
from keras.layers import Conv2D , MaxPooling2D, Dense, Flatten, Dropout
from keras.optimizers import Adam

classifier = Sequential()

classifier.add(Conv2D(32,(3,3), input_shape=(28, 28, 1) , activation = 'relu'))

classifier.add(MaxPooling2D(pool_size=(2,2)))

classifier.add(Dropout(0.25))

classifier.add(Flatten())

classifier.add(Dense(activation='relu', units=32))

classifier.add(Dense(activation='sigmoid', units=10))

classifier.compile(loss='sparse_categorical_crossentropy',
                   optimizer=Adam(lr=0.001),
                   metrics=['accuracy'])

classifier.summary()

from keras.utils.vis_utils import plot_model

plot_model (classifier, to_file='ini_model_NN_saya.png',
            show_shapes = True,
            show_layer_names = False)

run_model = classifier.fit(X_train, y_train,
                           batch_size = 480,
                           epochs = 30,
                           verbose = 1,
                           validation_data = (X_validate, y_validate))

print(run_model.history.keys())

plt.plot(run_model.history['accuracy'])
plt.plot(run_model.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validate'], loc='upper left')
plt.show()

plt.plot(run_model.history['loss'])
plt.plot(run_model.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validate'], loc='upper left')
plt.show()

evaluasi = classifier.evaluate(X_test, y_test)
print('test sccuracy ={:.2f}%'.format(evaluasi[1]*100))

classifier.save('model_cnn_fashion.hds', include_optimizer=True)
print('model sudah disimpan')

"""
jika ingin menload data 

from keras models import load model
classifier = load_model('model_cnn_fashion.hds')
"""

hasil_prediksi = classifier.predict_classes(X_test)

fig, axes =plt.subplots(5,5)
axes = axes.ravel()
for i in np.arange(0,5*5):
  axes[i].imshow(X_test[i]. reshape(28,28), cmap = 'gray')
  axes[i].set_title('hasil prediksi = {}\n label asli ={}\n '.format(hasil_prediksi, y_test))
  axes[i].axis('off')

from sklearn.metrics import confusion_matrix
import pandas as pd
cm = confusion_matrix(y_test, hasil_prediksi)
cm_label = pd.DataFrame(cm, columns = np.unique(y_test), index = np.unique(y_test))
cm_label.index.name = 'asli'
cm_label.columns.name = 'prediksi'
plt.figure(figsize=(14,10))
sns.heatmap(cm_label, annot=True)

from sklearn.metrics import classification_report
jumlah_kategori = 10
nama_target = ['kategori {}' .format(i) for i in range(jumlah_kategori)]
print(classification_report(y_test, hasil_prediksi, target_names=nama_target))

