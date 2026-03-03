from typing import Any
import random


class Parser:
    """Parses and validates a maze configuration file.

    Reads a plain text config file with KEY=VALUE pairs and converts
    each value to its appropriate Python type with bounds checking.
    Lines starting with '#' are treated as comments and ignored.
    """
    def _config_width(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the WIDTH key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                         Updated in place with the validated int value.

        Raises:
            SystemExit: If WIDTH is missing, not a number, or out of range.
        """
        try:
            data: str = str(config_data['WIDTH'])
            parsed: int = int(data)
            if parsed < 5:
                raise SystemExit("[Error]: WIDTH cant be lower than 5")
            if parsed > 100000:
                raise SystemExit("[Error]: WIDTH cant be higher than 100000")
            config_data['WIDTH'] = parsed
        except KeyError:
            raise SystemExit("[Error]: WIDTH is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: WIDTH key is not a valid number")

    def _config_height(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the HEIGHT key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                         Updated in place with the validated int value.

        Raises:
            SystemExit: If HEIGHT is missing, not a number, or out of range.
        """
        try:
            data: str = str(config_data['HEIGHT'])
            parsed: int = int(data)
            if parsed < 5:
                raise SystemExit("[Error]: HEIGHT cant be lower than 5")
            if parsed > 100000:
                raise SystemExit("[Error]: HEIGHT cant be higher than 100000")
            config_data['HEIGHT'] = parsed
        except KeyError:
            raise SystemExit("[Error]: HEIGHT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: HEIGHT value is not a valid number")

    def _config_entry(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the ENTRY key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                        Updated in place with a (x, y) tuple.

        Raises:
            SystemExit:If ENTRY is missing, wrongly formatted,or out of bounds.
        """
        try:
            data: str = str(config_data['ENTRY'])
            data = data.strip()
            prsd: list[str] = list(data.split(','))
            if len(prsd) != 2:
                raise SystemExit(
                    "[Error] Config file, ENTRY value wrong format"
                    )
            config_data['ENTRY'] = (int(prsd[0]), int(prsd[1]))

            width: int = int(config_data['WIDTH'])
            height: int = int(config_data['HEIGHT'])

            if int(prsd[0]) < 0 or int(prsd[0]) > width - 1:
                raise SystemExit(
                    "[Error] Config file, ENTRY value on outside of bounds"
                    )
            elif int(prsd[1]) < 0 or int(prsd[1]) > height - 1:
                raise SystemExit(
                    "[Error] Config file, ENTRY value on outside of bounds"
                    )
        except KeyError:
            raise SystemExit("[Error]: ENTRY is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: ENTRY value is not a valid number")

    def _config_exit(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the EXIT key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                         Updated in place with a (x, y) tuple.

        Raises:
            SystemExit: If EXIT is missing, wrongly formatted, out of bounds,
                        or overlaps with ENTRY.
        """
        try:
            data = config_data['EXIT']
            data = data.strip()
            data = data.split(',')
            if len(data) != 2:
                raise SystemExit(
                    "[Error] Config file, ENTRY value wrong format"
                    )
            config_data['EXIT'] = (int(data[0]), int(data[1]))

            if int(data[0]) < 0 or int(data[0]) > config_data['WIDTH'] - 1:
                raise SystemExit(
                    "[Error] Config file, EXIT value on outside of bounds"
                    )
            elif int(data[1]) < 0 or int(data[1]) > config_data['HEIGHT'] - 1:
                raise SystemExit(
                    "[Error] Config file, EXIT value on outside of bounds"
                    )

            if int(data[0]) == config_data['ENTRY'][0] and\
                    int(data[1]) == config_data['ENTRY'][1]:
                raise SystemExit(
                    "[Error] Config file, EXIT value overlaps on ENTRY"
                    )

        except KeyError:
            raise SystemExit("[Error]: EXIT is not in the config file")
        except ValueError:
            raise SystemExit("[Error]: EXIT value is not a valid number")

    def _config_output(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the OUTPUT_FILE key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                         Updated in place with the stripped filename string.

        Raises:
            SystemExit: If OUTPUT_FILE is missing or does not end with '.txt'.
        """
        try:
            data = config_data['OUTPUT_FILE']
            data = data.strip()
            config_data['OUTPUT_FILE'] = data
            if not data.endswith('.txt'):
                raise SystemExit(
                    "[Error]: OUTPUT_FILE invalid file extension (.txt)"
                    )
        except KeyError:
            raise SystemExit("[Error]: OUTPUT_FILE is not in the config file")

    def _config_seed(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the SEED key from config data.

        If SEED is not provided, a random seed is generated automatically.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                         Updated in place with the validated int seed value.

        Raises:
            SystemExit: If SEED is present but not a valid positive integer.
        """
        try:
            data: str = str(config_data['SEED'])
            data = data.strip()
            parsed: int = int(data)
            if parsed < 1:
                raise SystemExit("[Error]: SEED data wrong range >=1")
            config_data['SEED'] = parsed
        except KeyError:
            config_data['SEED'] = random.randint(1, 2**32)
        except ValueError:
            raise SystemExit("[Error]: SEED data wrong type [SEED=[int]]")

    def _config_perfect(
            self,
            config_data: dict[str, Any]
            ) -> None:
        """Parse and validate the PERFECT key from config data.

        Args:
            config_data: Dictionary of raw config key-value pairs.
                            Updated in place with a boolean value.

        Raises:
            SystemExit: If PERFECT is missing or not a valid boolean string.
        """
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

    def config(self, config_file: str = "config.txt") -> dict[
        str, Any
            ]:
        """Read and parse the maze configuration file.

        Opens the config file, strips comments, parses all KEY=VALUE
        pairs and validates each mandatory key by calling the appropriate
        private methods.

        Args:
            config_file:Path to the configuration file.Defaults to 'config.txt'

        Returns:
            Dictionary with validated and type-converted config values:
            WIDTH (int), HEIGHT (int), ENTRY (tuple), EXIT (tuple),
            PERFECT (bool), SEED (int), OUTPUT_FILE (str).

        Raises:
            SystemExit: If the file is not found or any key is invalid.
        """
        config_data: dict[str, Any] = {}
        try:
            with open(config_file, 'r') as file:

                content = file.read()
                splitted = content.strip().split('\n')
                splitted = [
                    line for line in splitted
                    if line and not line.startswith('#') and '=' in line

                ]
                for data in splitted:
                    data_split = data.split('=', 1)
                    if len(data_split) < 2:
                        raise ValueError(
                            "[Error] : Config file setup, went wrong !!"
                            )
                    config_data[data_split[0].strip()] = data_split[1]
        except FileNotFoundError:
            raise SystemExit("[Error] Config file name is not valid")

        self._config_width(config_data)
        self._config_height(config_data)
        self._config_entry(config_data)
        self._config_exit(config_data)
        self._config_perfect(config_data)
        self._config_seed(config_data)
        self._config_output(config_data)
        return config_data
