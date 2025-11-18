from roboflow import Roboflow
import os
from dotenv import load_dotenv

load_dotenv()

Roboflow_api_key = os.getenv("ROBOFLOW_API_KEY")

rf = Roboflow(api_key=Roboflow_api_key)

#1
# project = rf.workspace("azat1").project("intelligentvision")
# version = project.version(7)
# dataset = version.download("yolov11")

#2
# project = rf.workspace("material-identification").project("garbage-classification-3")
# version = project.version(2)
# dataset = version.download("yolov11")

                