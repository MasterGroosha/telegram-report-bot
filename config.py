from configparser import ConfigParser

# Global config object
cfg = None


def check_config_file(filename: str) -> bool:
    required_structure = {
        "bot": ["token"]
    }

    global cfg
    cfg = ConfigParser()
    cfg.read(filename)
    if len(cfg.sections()) == 0:
        print("Config file missing or empty")
        return False
    for section in required_structure.keys():
        if section not in cfg.sections():
            print(f'Missing section "{section}" in config file')
            return False
        for option in required_structure[section]:
            if option not in cfg[section]:
                print(f'Missing option "{option}" in section "{section}" of config file')
                return False
    return True


if __name__ == '__main__':
    check_config_file("config.ini")
