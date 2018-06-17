#IDC Classification Trainer
mvNCCompile model/DevCloudIDC.pb -in=input -on=InceptionV3/Predictions/Softmax -o model/idc.graph
python3.5 Classifier.py Inception
python3.5 Classifier.py Facenet
