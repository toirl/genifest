from typing import Dict, List

import yaml


class ManifestData:
    def __init__(self):
        self.instances: Dict[str, List[dict]] = {}

    def add_instance(self, name: str, input: List[dict]):
        self.instances[name] = input

    def get_inputs(self, name) -> List[dict]:
        return self.instances[name]


class ManifestWriter:
    """ManifestWriter will generate a Manifest file which can be used to
    compute emission data with the Impact Framework. It will generate this file
    based on a give template and provided ManifestData."""

    def __init__(self, template_path: str):
        self.template_path = template_path

    def generate(self, data: ManifestData) -> dict:
        template = load_yaml_file(self.template_path)
        for name, value in template["tree"]["children"].items():
            value["inputs"] = data.get_inputs(name)
            template["tree"]["children"][name] = value
        return template

    def write(self, path: str, data: dict):
        write_yaml_file(path, data)

    def print(self, data: dict):
        print(yaml.dump(data, sort_keys=False))


def load_yaml_file(file_path) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def write_yaml_file(file_path: str, data: dict):
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)
