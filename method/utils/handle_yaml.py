import yaml


def get_yaml(target_path):
    with open(target_path, encoding='utf-8') as target:
        yml = yaml.load(target, Loader=yaml.FullLoader)
        return yml


def output_yaml(target_path, yaml_data):
    with open(target_path, 'w') as bdi:
        yaml.dump(yaml_data, bdi, default_flow_style=False)
