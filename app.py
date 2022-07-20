from tkinter import mainloop
from keras.models import load_model
from flask import Flask, jsonify,request,render_template
import sys
import cv2 as cv
if sys.version_info[0] == 3:
    import tkinter as tk
    from tkinter import *
    import tkinter  as tk
else:
    import Tkinter as tk
    from Tkinter import *

import win32gui
from PIL import ImageGrab, Image
import numpy as np
app = Flask(__name__)

__model = None
__number = None


@app.route("/")
def index():
    global __model
    __model = load_model('mnist.h5')
    return render_template("app.html")

@app.route("/get_response",methods=['GET'])
def get_response():
    global __model
    global __number
    class App(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            # screen_width = self.winfo_screenwidth()
            # screen_height = self.winfo_screenheight()
            # app_width = 500
            # app_height = 500
            # x = (screen_width / 2) - (app_width / 2)
            # y = (screen_height / 2) - (app_height / 2)
            # tk.Tk.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
            self.x = self.y = 0
            # Creating elements
            self.canvas = tk.Canvas(self, width=300, height=250, bg = "black", cursor="arrow")
            self.canvas.pack()
            self.canvas.old_coords = None
            self.label = tk.Label(self, text="Analyzing..", font=("Helvetica", 48))
            self.classify_btn = tk.Button(self, text = "Search", command =  self.classify_handwriting) 
            self.button_clear = tk.Button(self, text = "Dlt", command = self.clear_all)
            # Grid structure
            self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
            self.label.grid(row=0, column=1,pady=2, padx=2)
            self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
            self.button_clear.grid(row=1, column=0, pady=2)
            self.canvas.bind("<ButtonPress-1>", self.draw_lines)
            self.canvas.bind("<B1-Motion>", self.draw_lines)
            self.canvas.bind("<ButtonRelease-1>", self.draw_lines)
        
        def clear_all(self):
            self.canvas.delete("all")
        def classify_handwriting(self):
            Hd = self.canvas.winfo_id() # to fetch the handle of the canvas
            rect = win32gui.GetWindowRect(Hd) # to fetch the edges of the canvas
            im = ImageGrab.grab(rect)
            print("**************",rect)
            digit, acc = predict_digit(im)
            __number = digit
            self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
        def draw_lines(slf, event):
            slf.x = event.x
            slf.y = event.y
            r=8
            slf.canvas.create_oval(slf.x-r, slf.y-r, slf.x + r, slf.y + r, width=20,fill="white",outline="white")
    app = App()
    mainloop()
    return str(__number)

def predict_digit(img1):
    global __model
    img = img1.resize((28,28))
    img = img.convert('L') 
    img = np.array(img)
    # im = Image.fromarray(img)
    # im.save("saved.png")
    img = img.reshape(1,28,28,1)
    img = img/255.0
    res = __model.predict([img])[0]
    digit = np.argmax(res), max(res)
    print(digit)
    print(res)
    return digit


if __name__ =="__main__":
    # load_artifacts()
    app.run()