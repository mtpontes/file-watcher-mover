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
        extensions_targets, extension_to_path = self._get_extension_config(configs)
        self.extension_config = ExtensionConfig(extensions_targets, extension_to_path)
        
        regex_targets, pattern_to_path = self._get_regex_config(configs)
        self.pattern_config = PatternConfig(regex_targets, pattern_to_path)

    def _get_extension_config(self, configs: dict) -> tuple[list[str], dict]:
        return self._get_config(configs, section="extensionConfig", map_key="extensionToPath")

    def _get_regex_config(self, configs: dict) -> tuple[list[str], dict]:
        lista, mapa = self._get_config(configs, section="regexConfig", map_key="patternToPath")
        return (lista, mapa)
    
    def _get_config(self, configs: dict, section: str, map_key: str) -> tuple[list[str], dict]:
        section_config: dict = configs.get(section)
        targets: list[str] = section_config.get("targets")
        mapping: dict = section_config.get(map_key)

        if targets is None and mapping is None:
            raise ValueError("Configuration error: some value is missing or an empty text was provided.")

        self._validate_targets(targets)
        self._validate_maps(mapping, map_key)

        return targets, mapping

    def _validate_targets(self, targets: list[str]) -> None:
        for target in targets:
            if not isinstance(target, str):
                raise ValueError(f"Invalid target: {target}. All targets must be strings.")
            if not target:
                raise ValueError("Target cannot be an empty string.")
            
    def _validate_maps(self, maps: dict, map_name: str) -> None:
        def validate(value: any, is_key: bool):
            messages: dict = {
                True: (
                    f"Invalid key within {map_name}. All keys must be text.",
                    f"Cannot have an empty string as a key."
                    ),
                False: (
                    f"Invalid value within {map_name}. All values must be text",
                    f"Cannot have an empty string as a value of a key."
                    )
            }
            
            if not isinstance(value, str):
                raise ValueError(messages.get(is_key)[0])
            if not value:
                raise ValueError(messages.get(is_key)[1])
        
        for key, path in maps.items():
            validate(key, True)
            validate(path, False)
