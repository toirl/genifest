from datetime import UTC, datetime

import requests
import yaml


def load_yaml_file(file_path) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def write_yaml_file(file_path: str, data: dict):
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file)


def get_data(url: str, params: dict) -> dict:
    # HTTP GET-Anfrage an die Prometheus-API
    response = requests.get(url, params=params)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        data = response.json()

        # Daten verarbeiten und Zeitstempel in ISO-Format umwandeln
        for result in data["data"]["result"]:
            for value in result["values"]:
                timestamp = value[0]  # unix timestamp
                cpu_util = float(value[1])  # cpu-util as string
                iso_time = datetime.fromtimestamp(timestamp, UTC).isoformat()
                value[0] = iso_time
                value[1] = cpu_util
        return data
    else:
        print("Fehler bei der Abfrage:", response.status_code)
        return {}


def generate_manifest(template: dict, data: dict) -> dict:
    # Iterate over all configured components in the manifest
    for name, value in template["tree"]["children"].items():
        node_usage = get_node_usage(data, name)
        value["inputs"] = node_usage
        template["tree"]["children"][name] = value
    return template


def get_node_usage(data: dict, name: str) -> list[dict]:
    for node in data["data"]["result"]:
        if _get_node_name(node) == name:
            return _get_node_usage(node)
    return []


def _get_node_name(node: dict) -> str:
    return node["metric"]["instance"].split(":")[0].lower()


def _get_node_usage(node: dict) -> list[dict]:
    usage = []

    # Calculate the duration
    v1_dt = datetime.fromisoformat(node["values"][0][0])
    v2_dt = datetime.fromisoformat(node["values"][1][0])
    td = v2_dt - v1_dt
    duration = int(td.total_seconds())

    for value in node["values"]:
        timestamp = value[0]
        cpu_util = value[1]
        duration = duration

        # See minimal structure at https://if.greensoftware.foundation/users/how-to-write-manifests#inputs
        usage.append({"timestamp": timestamp, "duration": duration, "cpu/utilization": cpu_util})
    return usage


def main(path_manifest_template: str, url: str, params: dict, path_manifest_static: str):
    template = load_yaml_file(path_manifest_template)
    data = get_data(url, params)
    manifest = generate_manifest(template, data)
    print(yaml.dump(manifest))
    # write_yaml_file(path_manifest_static, manifest)
