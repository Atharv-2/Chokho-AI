from roboflow import Roboflow
rf = Roboflow(api_key="WlbcOGXr69ltE40RtlYZ")
project = rf.workspace("azat1").project("intelligentvision")
version = project.version(7)
dataset = version.download("yolov11")
                