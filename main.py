import os
from tkinter import *
import PIL
from PIL import ImageGrab
import numpy as np
from PIL import Image, ImageEnhance
import cv2
from keras.models import load_model
import warnings
warnings.filterwarnings('ignore')


def preprocessing(img):
    image=img.astype("uint8")
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image=cv2.equalizeHist(image)
    image = image/255
    return image
        
def get_className(classNo):
    if classNo==0:
        return "ZERO"
    elif classNo==1:
        return "ONE"
    elif classNo==2:
            return "TWO"
    elif classNo==3:
        return "THREE"
    elif classNo==4:
        return "FOUR"
    elif classNo==5:
        return "FIVE"
    elif classNo==6:
        return "SIX"
    elif classNo==7:
        return "SEVEN"
    elif classNo==8:
        return "EIGHT"
    elif classNo==9:
        return "NINE"


class Interface:
    def __init__(self, master):
        self.master = master
        self.res = ""
        self.pre = [None, None]
        self.bs = 8.5
        self.c = Canvas(self.master,bd=3,relief="ridge", width=300, height=282, bg='white')
        self.c.pack(side=LEFT)
        f1 = Frame(self.master, padx=5, pady=5)
        Label(f1,text="Bangla HandWriting Digit Classification",fg="black",font=("",15,"bold")).pack(pady=10)
        Label(f1,text="Draw On The Canvas Alongside",fg="black",font=("",15, "bold")).pack()
        self.pr = Label(f1,text="Prediction: None",fg="green",font=("",20,"bold"))
        self.pr.pack(pady=15)
        
        Button(f1,font=("",15),fg="white",bg="red", text="Clear Canvas", command=self.clear).pack(side=BOTTOM)

        f1.pack(side=RIGHT,fill=Y)
        self.c.bind("<Button-1>", self.putPoint)
        self.c.bind("<ButtonRelease-1>",self.getOutput)
        self.c.bind("<B1-Motion>", self.paint)
    
    def getOutput(self,e):
        x = self.master.winfo_rootx() + self.c.winfo_x()
        y = self.master.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        img = PIL.ImageGrab.grab()
        img = img.crop((x, y, x1, y1))
        #img.save("img.png")
        #imgPath="img.png"
        #img=cv2.imread(imgPath)
        img=np.asarray(img)
        img=cv2.resize(img, (32,32))
        img=preprocessing(img)
        img=img.reshape(1, 32, 32, 1)

        model=load_model('ModelBanglaDigit.h5')
        prediction= model.predict(img)
        classIndex = np.argmax(prediction,axis=1)
        self.res=str(get_className(classIndex))
        self.pr['text'] = "Prediction: " + self.res

    def clear(self):
        self.c.delete('all')

    def putPoint(self, e):
        self.c.create_oval(e.x - self.bs, e.y - self.bs, e.x + self.bs, e.y + self.bs, outline='black', fill='black')
        self.pre = [e.x, e.y]

    def paint(self, e):
        self.c.create_line(self.pre[0], self.pre[1], e.x, e.y, width=self.bs * 2, fill='black', capstyle=ROUND,
                           smooth=TRUE)

        self.pre = [e.x, e.y]


if __name__ == "__main__":
    root = Tk()
    Interface(root)
    root.title('Digit Classifier')
    root.resizable(0, 0)
    root.mainloop()