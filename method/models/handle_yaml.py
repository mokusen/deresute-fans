import yaml


def getSetting():
    with open('./setting.yml') as setting:
        yml = yaml.load(setting, Loader=yaml.FullLoader)
        return yml["mysql"]


def getBeforeDate():
    with open('./before_date_info.yml') as bdi:
        yml = yaml.load(bdi, Loader=yaml.FullLoader)
        return yml


def outputBeforeDate(before_date_yml):
    with open('./before_date_info.yml', 'w') as bdi:
        yaml.dump(before_date_yml, bdi, default_flow_style=False)
