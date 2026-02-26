# WIDTH Maze width (number of cells) WIDTH=20
# HEIGHT Maze height HEIGHT=15
# ENTRY Entry coordinates (x,y) ENTRY=0,0
# EXIT Exit coordinates (x,y) EXIT=19,14
# OUTPUT_FILE Output filename OUTPUT_FILE=maze.txt
# PERFECT


from typing import Union, Optional

# This class will manage the reading from the config file
class Parser:
    def __init__(self):
        ...

    def _config_width(self, config_data: dict) -> None:
        try:
            data = config_data['WIDTH']
            data = int(data)
            if data < 5:
                raise SystemExit("[Error]: WIDTH cant be lower than 5")
            config_data['WIDTH'] = data
        except KeyError:
            raise SystemExit("[Error]: WIDTH is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: WIDTH key is not a valid number")

    def _config_height(self, config_data: dict) -> None:
        try:
            data = config_data['HEIGHT']
            data = int(data)
            if data < 5:
                raise SystemExit("[Error]: HEIGHT cant be lower than 5")
            config_data['HEIGHT'] = data
        except KeyError:
            raise SystemExit("[Error]: HEIGHT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: HEIGHT key is not a valid number\nSetting HEIGHT to Default")

    def _config_entry(self, config_data: dict) -> None:
        try:
            data = config_data['ENTRY']
            data = data.strip()
            data = data.split(',')
            config_data['ENTRY'] = (int(data[0]), int(data[1]))
        except KeyError:
            raise SystemExit("[Error]: ENTRY is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: ENTRY key is not a valid number")

    def _config_exit(self, config_data: dict) -> None:
        try:
            data = config_data['EXIT']
            data = data.strip()
            data = data.split(',')
            config_data['EXIT'] = (int(data[0]), int(data[1]))
        except KeyError:
            raise SystemExit("[Error]: EXIT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: EXIT key is not a valid number")

    def _config_output(self, config_data: dict) -> None:
        ...

    def _config_seed(self, config_data: dict) -> None:
        try:
            data = config_data['SEED']
            data = data.strip()
            data = int(data)
            if data < 1:
                raise SystemExit("[Error]: SEED data wrong range >=1")
            config_data['SEED'] = data
        except KeyError:
            raise SystemExit("[Error]: SEED is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: SEED data wrong type [SEED=[int]]")

    def _config_perfect(self, config_data: dict) -> None:
        try:
            data = config_data['PERFECT']
            data = data.strip()
            if data == 'True':
                config_data['PERFECT'] = True
            elif data == 'False':
                config_data['PERFECT'] = False
            else:
                raise SystemError("[Error]: PERFECT key is not a valid bool")
        except ValueError:
            raise SystemExit("[Error]: PERFECT key is not a valid bool")

    def config(self, config_file: Optional[str] = "config.txt") -> dict[str,Union[str, bool, int, list]]:
        config_data: dict = {}
        # We open the file asked in the subject
        with open(config_file, "r") as file:

            # Then we read it and split on '\n' char
            content = file.read()
            splitted = content.strip().split('\n')
            splitted = [
                line for line in splitted
                if line and not line.startswith('#') and '=' in line

            ]
            # After removing the comments and possible useless data
            # We go and take the data we need from the config file
            for data in splitted:
                data_split = data.split('=')
                if len(data_split) < 2:
                    raise ValueError("[Error] : Config file not well set upped")
                config_data[data_split[0]] = data_split[1]

        # Here we use a series of functions
        # They convert the data to the right type
        # Remember everything read until now is a string
        self._config_width(config_data)
        self._config_height(config_data)
        self._config_entry(config_data)
        self._config_exit(config_data)
        self._config_perfect(config_data)
        self._config_seed(config_data)
        return config_data

if __name__ == '__main__':
    parser: Parser = Parser()
    config_data = parser.config()
    print(f"{config_data}")