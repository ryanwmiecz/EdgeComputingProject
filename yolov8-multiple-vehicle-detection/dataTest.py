from ultralytics import YOLO
import pandas as pd
import os
# Download latest version
if __name__ == "__main__":
    repo_path = os.path.dirname(os.getcwd())
    print(repo_path)
    # Add the path to the utils folder to the system path
    path = ('dataSet\\car_dataset-master\\data.yaml')

    model = YOLO('yolov8s.pt')
    #model.classes = [2]

    results = model('image.png', show = False, save=True)
    #validation_results = model.val(data=path , classes =  [0], save_json = True, imgsz=640, batch=1, conf=0.4, device="cpu")
    #model.train(data=path, single_cls = True, imgsz=640, save=True, batch=16)
    #print(validation_results.box.map)