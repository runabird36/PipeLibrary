
import os, json, yaml
import pandas as pd
def read_json(_json_file_path):
    try:
        if os.path.exists(_json_file_path) is False:
            return None
        json_info = open(_json_file_path, 'r').read()
    except:
        return None
    return json.loads(json_info)


def load_yaml_file(yaml_path):
    try:
        with open(yaml_path) as f:
            load_yml = yaml.safe_load(f)
        return load_yml
    except Exception as e:
        print(str(e))
        return

def dump_to_yaml(info, yaml_path):
    try:
        with open(yaml_path, "w") as f:
            yaml.dump(info, f)
    except Exception as e:
        print(str(e))
    return



def parq_to_pandas(input_path :str) -> str:
    return pd.read_parquet(input_path, engine="pyarrow")


