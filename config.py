import yaml


CONFIG_FILE = 'config.yaml'

def load_config(config_file=CONFIG_FILE):
    with open(config_file, 'r', encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    return config

def save_config(config, config_file=CONFIG_FILE):
    with open(config_file, 'w', encoding="utf-8") as config_file:
        yaml.dump(config, config_file, allow_unicode=True)

def get_config_value(key, config_file=CONFIG_FILE):
    config = load_config(config_file)
    return config.get(key)

def set_config_value(key, value, config_file=CONFIG_FILE):
    config = load_config(config_file)
    config[key] = value
    save_config(config, config_file)

def load_languages(config_file=CONFIG_FILE):
    config = load_config(config_file)
    lang_file = config.get("lang_file")
    with open(lang_file, 'r', encoding="utf-8") as lang_file:
        lang = yaml.safe_load(lang_file)
    return lang['languages'][config.get("lang")]

