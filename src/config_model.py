from dataclasses import dataclass


@dataclass
class PatternConfig:
    targets: list[str]
    pattern_to_path: dict


@dataclass
class ExtensionConfig:
    targets: list[str]
    extension_to_path: dict


@dataclass
class ConfigModel:
    extension_config: ExtensionConfig
    pattern_config: PatternConfig

    def __init__(self, configs: dict):
        extension_config_data = configs["extensionConfig"]
        self.extension_config = ExtensionConfig(
            targets=extension_config_data["targets"], extension_to_path=extension_config_data["extensionToPath"],
        )

        regex_config_data = configs["regexConfig"]
        self.pattern_config = PatternConfig(
            targets=regex_config_data["targets"], pattern_to_path=regex_config_data["patternToPath"],
        )
