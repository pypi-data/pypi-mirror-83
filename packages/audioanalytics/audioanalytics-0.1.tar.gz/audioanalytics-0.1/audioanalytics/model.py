import keras
import pkgutil
import json
import importlib.resources
import h5py

def model_load():
    json_file = pkgutil.get_data("audioanalytics", "model_85.json")
    loaded_model_json = json.dumps(json.loads(json_file.decode('utf-8')))
    loaded_model = keras.models.model_from_json(loaded_model_json)
    with importlib.resources.path("audioanalytics", "model_85.h5") as p:
        h5_path = p

    loaded_model.load_weights(h5_path)

    return loaded_model
