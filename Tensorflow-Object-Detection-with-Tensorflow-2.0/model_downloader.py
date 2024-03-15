import wget
model_link = "http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz"
wget.download(model_link)
import tarfile
tar = tarfile.open('faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz')
tar.extractall('.')
tar.close()