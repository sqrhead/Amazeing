from typing import Union, Optional
import random

# [TODO] Bounds check on entry/exit
# This class will manage the reading from the config file
class Parser:

    def _config_width(self, config_data: dict) -> None:
        try:
            data = config_data['WIDTH']
            data = int(data)
            if data < 5:
                raise SystemExit("[Error]: WIDTH cant be lower than 5")
            if data > 100000:
                raise SystemExit("[Error]: WIDTH cant be higher than 100000")
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
            if data > 100000:
                raise SystemExit("[Error]: HEIGHT cant be higher than 100000")
            config_data['HEIGHT'] = data
        except KeyError:
            raise SystemExit("[Error]: HEIGHT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: HEIGHT value is not a valid number")

    def _config_entry(self, config_data: dict) -> None:
        try:
            data = config_data['ENTRY']
            data = data.strip()
            data = data.split(',')
            if len(data) != 2:
                raise SystemExit("[Error] Config file, ENTRY value wrong format")
            config_data['ENTRY'] = (int(data[0]), int(data[1]))

            if int(data[0]) < 0 or int(data[0]) > config_data['WIDTH'] -1:
                raise SystemExit("[Error] Config file, ENTRY value on outside of bounds")
            elif int(data[1]) < 0 or int(data[1]) > config_data['HEIGHT'] -1:
                raise SystemExit("[Error] Config file, ENTRY value on outside of bounds")
        except KeyError:
            raise SystemExit("[Error]: ENTRY is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: ENTRY value is not a valid number")

    def _config_exit(self, config_data: dict) -> None:
        try:
            data = config_data['EXIT']
            data = data.strip()
            data = data.split(',')
            if len(data) != 2:
                raise SystemExit("[Error] Config file, ENTRY value wrong format")
            config_data['EXIT'] = (int(data[0]), int(data[1]))

            if int(data[0]) < 0 or int(data[0]) > config_data['WIDTH'] -1:
                raise SystemExit("[Error] Config file, EXIT value on outside of bounds")
            elif int(data[1]) < 0 or int(data[1]) > config_data['HEIGHT'] -1:
                raise SystemExit("[Error] Config file, EXIT value on outside of bounds")

            if int(data[0]) == config_data['ENTRY'][0] and\
                int(data[1]) == config_data['ENTRY'][1]:
                raise SystemExit("[Error] Config file, EXIT value overlaps on ENTRY")

        except KeyError:
            raise SystemExit("[Error]: EXIT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: EXIT value is not a valid number")

    def _config_output(self, config_data: dict) -> None:
        try:
            data = config_data['OUTPUT_FILE']
            data = data.strip()
            if not data.endswith('.txt'):
                raise SystemExit("[Error]: OUTPUT_FILE invalid file extension (.txt)")
        except KeyError:
            raise SystemExit("[Error]: OUTPUT_FILE is not in the config file")

    def _config_seed(self, config_data: dict) -> None:
        try:
            data = config_data['SEED']
            data = data.strip()
            data = int(data)
            if data < 1:
                raise SystemExit("[Error]: SEED data wrong range >=1")
            config_data['SEED'] = data
        except KeyError:
            config_data['SEED'] = random.randint(1, 2**32)
        except ValueError:
            raise SystemExit("[Error]: SEED data wrong type [SEED=[int]]")

    def _config_perfect(self, config_data: dict) -> None:
        try:
            data = config_data['PERFECT']
            data = data.strip()
            lower = data.lower()
            if lower == 'true':
                config_data['PERFECT'] = True
            elif lower == 'false':
                config_data['PERFECT'] = False
            else:
                raise SystemExit("[Error]: PERFECT value is not a valid bool")
        except KeyError:
            raise SystemExit("[Error]: PERFECT key is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: PERFECT key is not a valid bool")

    def config(self, config_file: Optional[str] = "config.txt") -> dict[str,Union[str, bool, int, list]]:
        config_data: dict = {}
        # We open the file asked in the subject
        try:
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
                    data_split = data.split('=', 1)
                    if len(data_split) < 2:
                        raise ValueError("[Error] : Config file setup, went wrong !!")
                    config_data[data_split[0].strip()] = data_split[1]
        except FileNotFoundError :
            raise SystemExit("[Error] Config file name is not valid")

        # Here we use a series of functions
        # They convert the data to the right type
        # Remember everything read until now is a string
        self._config_width(config_data)
        self._config_height(config_data)
        self._config_entry(config_data)
        self._config_exit(config_data)
        self._config_perfect(config_data)
        self._config_seed(config_data)
        self._config_output(config_data)
        return config_data

if __name__ == '__main__':
    parser: Parser = Parser()
    config_data = parser.config()
    print(f"{config_data}")