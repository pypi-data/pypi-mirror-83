import keras
import pkgutil  # dependency covered as part of setuptools?
import json
# import importlib.resources
import setuptools
import pkg_resources


def model_load():
    json_file = pkgutil.get_data("audioanalytics", "model_85.json")
    loaded_model_json = json.dumps(json.loads(json_file.decode('utf-8')))

    loaded_model = keras.models.model_from_json(loaded_model_json)

    h5_path = pkg_resources.resource_filename("audioanalytics", "model_85.h5")

    loaded_model.load_weights(h5_path)


    return loaded_model

