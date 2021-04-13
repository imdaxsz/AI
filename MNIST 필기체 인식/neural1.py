import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
import time
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

class MyCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        if time.time() - self.start_time > 300:
            self.model.stop_training = True

mnist = tf.keras.datasets.mnist
(x_train, y_train_origin), (x_test, y_test_origin) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0           # 0과 1 사이의 값으로 변환

nb_classes = 10
y_train = keras.utils.to_categorical(y_train_origin, num_classes = nb_classes)       # one-hot encoding
y_test = keras.utils.to_categorical(y_test_origin, num_classes = nb_classes)       # one-hot encoding

model = keras.Sequential()
model.add(Flatten(input_shape=(28, 28)))
model.add(Dense(128, activation = 'sigmoid'))
model.add(Dense(10, activation = 'softmax'))

model.compile(optimizer = keras.optimizers.SGD(learning_rate = 0.01), loss = 'mse', metrics = ['categorical_accuracy'])
hist = model.fit(x_train, y_train, epochs=300, batch_size=100, validation_data=(x_test, y_test), callbacks=[MyCallback()])
model.evaluate(x_test, y_test)


print(hist.history["val_categorical_accuracy"])
print(">>> 최대값 :", max(hist.history["val_categorical_accuracy"]))

#image = Image.new("1", (200, 200), (255))      # "1" : 1bit pixel - balck and white
image = Image.new("L", (200, 200), (255))       # "L" : 8bit pixel - black and white (gray)
image_width, image_height = image.size
draw = ImageDraw.Draw(image)

window = tk.Tk()
window.geometry("%sx%s" % (image_width, image_height))
window.update()
canvas = tk.Canvas(window)
canvas.pack(expand = 1, fill = tk.BOTH)

tk_image = ImageTk.PhotoImage(image)
canvas.create_image(image_width / 2, image_height / 2, image = tk_image, tags = "image1")

def Resize(event):
    canvas.delete("image1")
    canvas.create_image(canvas.winfo_width() / 2, canvas.winfo_height() / 2, image=tk_image, tags="image1")

canvas.bind("<Configure>", Resize)

def SetStartPosition(event):
    global x, y
    x = event.x
    y = event.y

def DrawLine(event):
    global tk_image, x, y
    canvas.delete("image1")
    draw.line([(x, y), (event.x, event.y)], fill = None, width = 10)
    x = event.x
    y = event.y
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(canvas.winfo_width() / 2, canvas.winfo_height() / 2, image = tk_image, tags = "image1")

def GetPixelInfo(event):
    data = []
    image2 = image.resize((28, 28))
    for i in range(28):
        data.append([])
        for j in range(28):
            color = image2.getpixel((i, j))
            data[i].append(color)
    print(data)

    x_1 = np.array(data)
    x_1 = x_1 / 255.0
    x_1 = x_1.reshape((-1, 28, 28))
    y_1 = model.predict(x_1)
    print(y_1)
    y_label = tf.argmax(y_1, axis=1)
    print(y_label.numpy())

    return np.array(data)

canvas.bind("<Button-1>", SetStartPosition)
canvas.bind("<B1-Motion>", DrawLine)
canvas.bind("<Button-3>", GetPixelInfo)
window.mainloop()
