SortStream
Grant Holtes 2020
A GUI Document Classification Tool

Sortstream allows non-technical users to train and distribute AI document sorting models.

GUI Usage

from sortstream import document_classifier_gui
document_classifier_gui() opens a user interface.

Usual Usage

from sortstream import document_classifier
sorter = document_classifier()
sorter.fit(data_folder = "/PATH/TO/ROOT/DATA/FOLDER")
sorter.predict()

Operation

SortStream uses a directory based approch to labelling training data and outputting predictions.

The training dataset is orgaised as a root folder containing folders for each class or type of document. Each of these subfolders should contain the training examples for each class.

When predict is called, sortstream will gather input documents from a folder and attempt to move them into the approporate class subfolder. These class prediction subfolders are in the 'predictions' folder.

Fit - How to Build a Model:

In order to sort documents, the system needs to learn how to identify the category of each document. To do this, the user needs to provide a number of examples of each type of document the system would be expected to sort. 

1) Find a few examples of each category (between 10 and 100 is a good sample size)
2) For each category, make a folder that contains all of the examples. The name of this folder will be the name of the category.
3) Put all of these category example folders in a folder named data which is in the same file location as the program.
4) Open the program and click build model or fit() The program will learn from the examples in the data folder, and build a model. This model is saved alongside the program file. Do not change the folder name of the saved model. 

Each time build model or fit()is used, a new model is created. If multiple models are present in the folder, the program will use the first one it finds.

Predict - Classifying Documents:

1) Place the documents that need to be classified into input_files_to_be_sorted folder. This folder can either be created manually or will be automatically created the first time you press the predict button or call the predict() method.
2) Open the program, use the slider to select a confidence value (see Confidence), and click predict or call the predict()method.

The files will be sorted from the input_files_to_be_sorted folder into subfolders in the predictions folder.  Each subfolder contains the documents that belong to a specific category. 

If the system is not confident in a result, it will move the file to a specific subfolder named NotClassified in the predictions folder. These need to be sorted manually. 

Each time predict is used, a log file is saved to the logs folder. This CSV file lists every file classified and includes confidence levels for all categories alongside other logs. 

Sharing Models:

The model files, which are named SortStreammodelXXXXX can be shared between users, and will be used if in the same folder as the SortStream.py program file. 

Each time build model is used, a new model is created. If multiple models are present in the folder, the program will use the first one it finds.

Confidence: 

When classifying documents, the user can select the desired confidence level. This is the probability that the classification made by the program is correct, based on the data that the model was trained on. 

The below heuristic can be used:

High confidence:
It is highly unlikely that the program will classify a document incorrectly. However, it is likely that only a few documents will be classified, with the remaining requiring manual sorting.

Low confidence:
It is more likely that the program will classify a document incorrectly, but very few documents will require manual sorting.

Ultimately the best confidence level to use will change based on the use case, so it is worth inspecting the logs files to see what confidence levels the program is producing on your data. 
It is also worth considering the cost of misclassification relative to the cost of manually sorting documents when choosing the confidence level. 

