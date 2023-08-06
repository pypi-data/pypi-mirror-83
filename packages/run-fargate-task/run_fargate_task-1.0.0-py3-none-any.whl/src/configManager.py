import os,sys
from dotenv.main import dotenv_values
from ssm import SSM

def load_configs(path):
    configs = []
    try:
        if os.path.isfile(path):
            return fetch_ssm_parameters([dotenv_values(dotenv_path=path)])
        configFiles = os.listdir(path)
        for file in configFiles:
            file_path = ('{}/{}'.format(path,file))
            configs.append(dotenv_values(dotenv_path=file_path))
    except FileNotFoundError:
        print('Invalid path: {}'.format(path))
        sys.exit(0)

    return fetch_ssm_parameters(configs)

def fetch_ssm_parameters(configs):
    print("FETCHING PARAMETERS FROM SSM")
    for config in configs:
        ssm = SSM(config["AWS_PROFILE"])
        ssm_keys = list(filter(lambda k: k.startswith(config["PARAMETER_STORE_PREFIX"]),config.keys()))
        for key in ssm_keys:
            config[key.replace(config["PARAMETER_STORE_PREFIX"],"")] = ssm.get_parameter(config[key])
            del config[key]
    return configs
