import glob
import os
import numpy as np
import pandas as pd
from .features import extract_feature
from .model import model_load
import keras

x, y = [], []

emotions = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

observed_emotions = ['calm', 'happy', 'fearful', 'disgust']


def predict(file_name):
    # feature = pd.DataFrame(extract_feature(file_name)).T
    feature = extract_feature(file_name)

    test_data = np.expand_dims(feature, axis=2)

    loaded_model = model_load()
    loaded_model.compile(loss=keras.losses.categorical_crossentropy,
                         optimizer=keras.optimizers.Adadelta(),
                         metrics=['accuracy'])

    pred = loaded_model.predict_classes(test_data)

    pred_proba=loaded_model.predict(test_data)*100

    if pred[0] == 0:
        print("THE RESULT OF THE AUDIO ANALYSIS IS: CALM")
    elif pred[0] == 1:
        print("THE RESULT OF THE AUDIO ANALYSIS IS: HAPPY")
    elif pred[0] == 2:
        print("THE RESULT OF THE AUDIO ANALYSIS IS: FEARFUL")
    else:
        print("THE RESULT OF THE AUDIO ANALYSIS IS: DISGUST")

    return pred_proba


def summary(file_name):
    print('The Probabilities of Emotions are as follows:')
    prediction=predict(file_name)
    prediction_proba=pd.DataFrame(prediction,columns=['Calm','Happy','Fearful','Disgust'])
    print(prediction_proba)