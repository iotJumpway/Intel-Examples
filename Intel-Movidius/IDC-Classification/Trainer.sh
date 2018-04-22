#IDC Classification Trainer
pip3 install -r requirements.txt
python3.5 Trainer.py DataSort
python3.5 Trainer.py Train
mvNCCompile model/IDC.pb -in=input -on=InceptionV3/Predictions/Softmax -o igraph
python3.5 Eval.py
python3.5 Classifier.py InceptionTest
