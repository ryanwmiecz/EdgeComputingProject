import sys
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import os
import shutil
import random

def key_pressed(event):
    global cur, curConf
    if event.char == 'z':
        cur = 1
    elif event.char == 'x':
        cur = 2
    elif event.char == 'c':
        cur = 3
    elif event.char == 'v':
        cur = 4
    elif event.char == 'b':
        cur = 5

def updateCars():
    global cur
    global curConf
    num = random.randint(1,3)
    if (cur == 1):
        path = "runTimeImage\\image.png"
    elif (cur ==2):
        path = "runTimeImage\\image2.png"
    elif(cur ==3):
        path = "runTimeImage\\image3.jpg"
    elif (cur ==4):
        path = "runTimeImage\\image4.png"
    elif (cur ==5):
        path = "runTimeImage\\image5.png"    

    
    results = model(path, show = False, save=True, conf = curConf, project = "runTimeImage", name = "processed", classes = 2, iou =curIou)
    names = model.names
    

    car_id = list(names)[list(names.values()).index('car')]
    a = results[0].boxes.cls.tolist().count(car_id)
    label.config(text= "Number of Cars: "+(str(a)))
    if (parkingMax == 0):
        occuPerc.config(text= "Occupancy: 0%" )
    elif(parkingMax<=int(a)):
        occuPerc.config(text= "Occupancy: 100%" )
    else:
        occuPerc.config(text= "Occupancy: " + str(int(((int(a)/parkingMax)*100)))+ "%")
    
    if (cur == 1):
        image_path = "runTimeImage\\processed\\image.jpg"
    elif cur == 2:
        image_path = "runTimeImage\\processed\\image2.jpg"
    elif cur ==3:
        image_path = "runTimeImage\\processed\\image3.jpg"
    elif cur ==4:
        image_path = "runTimeImage\\processed\\image4.jpg"
    elif cur ==5:
        image_path = "runTimeImage\\processed\\image5.jpg"
    try:
        image = Image.open(image_path)
        image = image.resize((720,480))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image = photo)
        image_label.image = photo
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        exit()
    try:
        if os.path.exists("runTimeImage\\processed"):
            shutil.rmtree("runTimeImage\\processed")
        else:
            print("not found")
    except Exception as e:
        print("Error deleting folder {e}")
    label.after(3000, updateCars)

def get_maximum():
    input = entry.get()
    global parkingMax, curCars, curConfText, curIouText
    if input != '':
        parkingMax = int(input)
    maxLabel.config(text = "Parking lot Capacity: "+input+"\nCars Detected: "+str(curCars)+"\nConfidence Level: "+ curConfText+"\nIOU Level: "+curIouText)
    frame.focus_set()
def set_curConf(int):
    global curConf, curConfText
    curConf = int
    if curConf == .6:
        curConfText = "High"
    elif curConf == .4:
        curConfText = "Medium"
    else:
        curConfText = "Low"
    get_maximum()
def set_curIOU(int):
    global curIou, curIouText
    curIou = int
    if curIou == .8:
        curIouText = "Low"
    elif curIou == .6:
        curIouText = "Medium"
    else:
        curIouText = "High"
    get_maximum()

model = YOLO('yolov8s.pt')
model.classes = [2]
root = tk.Tk()
frame = tk.Frame(root)
curConf = .4
curConfText = "Medium"
curIou = .6
curIouText = "Medium"
curCars = 0

cur = 1
label = tk.Label(root, text="Number Of Cars")
occuPerc = tk.Label(root, text= "Occupancy: ")
maxLabel = tk.Label(root, text= "Parking lot Capacity: \nCars Detected: "+str(curCars)+"\nConfidence Level: "+ curConfText+"\nIOU Level: "+curIouText)
entry = tk.Entry(root)
buttonMax = tk.Button(root, text="Set Parking Capacity", command= lambda: get_maximum())
parkingMax= 0


buttonConfFrame = tk.Frame(root)
confLabel = tk.Label(buttonConfFrame, text = "Confidence Level" )
confLabel.grid(row = 0, column=0, sticky="we")
buttonLowConf = tk.Button(buttonConfFrame, text="Low", command= lambda: set_curConf(.3))
buttonLowConf.grid(row=1, column=0, padx=5, pady=5, sticky="we")

buttonMedConf = tk.Button(buttonConfFrame, text="Medium", command= lambda: set_curConf(.4))
buttonMedConf.grid(row=1, column=1, padx=5, pady=5, sticky="we")

buttonHighConf = tk.Button(buttonConfFrame, text="High", command= lambda: set_curConf(.6))
buttonHighConf.grid(row=1, column=2, padx=5, pady=5, sticky="we")

buttonIOUFrame = tk.Frame(root)
IouLabel = tk.Label(buttonIOUFrame, text = "IOU Level" )
IouLabel.grid(row = 0, column=0, sticky="we")
buttonLowIOU = tk.Button(buttonIOUFrame, text="Low", command= lambda: set_curIOU(.8))
buttonLowIOU.grid(row=1, column=0, padx=5, pady=5, sticky="we")

buttonMedIOU = tk.Button(buttonIOUFrame, text="Medium", command= lambda: set_curIOU(.6))
buttonMedIOU.grid(row=1, column=1, padx=5, pady=5, sticky="we")

buttonHighIOU = tk.Button(buttonIOUFrame, text="High", command= lambda: set_curIOU(.4))
buttonHighIOU.grid(row=1, column=2, padx=5, pady=5, sticky="we")

image_path = "runTimeImage\\image.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
bottomLabel = tk.Label(root, text ="Z, X, C, V, B to change current image")
frame.bind("<Key>", key_pressed)
frame.focus_set()
frame.grid(row=0, column=0)
    
def init():
    maxLabel.grid(row=0, column=0)
    occuPerc.grid(row=1, column=0)
    updateCars()
    entry.grid(row=2, column=0)
    buttonMax.grid(row=3, column=0)
    buttonConfFrame.grid(row=0, column=1)
    buttonIOUFrame.grid(row=1, column=1)
    image_label.grid(row=5, column=0)
    bottomLabel.grid(row= 6, column = 0)
    root.geometry('1080x720')
    root.resizable(width=0, height=0)
    root.mainloop()

def main():
    running = True
    init()
    

if __name__ == '__main__':
    main()