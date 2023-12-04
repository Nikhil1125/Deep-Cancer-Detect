import cv2
from keras.models import load_model
from PIL import Image
import numpy as np

model=load_model("myModel.keras")

image = cv2.imread("uploads/father.jpg")

img = Image.fromarray(image)
img = img.resize((64,64))

img = np.array(img)

img = img/255.0

input_img = np.expand_dims(img, axis=0)


result = model.predict(input_img)
threshold =0.5

predicted_class = 1 if result[0][0]> threshold else 0

sureity = int(result[0][0]*100)

if predicted_class==1:
    print(" 'There is tumor present in the MRI picture "+ str(sureity) +" % sureity' " )

else:
    print(" 'There is tumor not present in the MRI picture' ")
