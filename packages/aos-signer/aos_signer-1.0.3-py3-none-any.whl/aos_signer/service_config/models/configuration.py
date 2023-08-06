from .config_chapter import ConfigChapter


class Configuration(ConfigChapter):

    @staticmethod
    def from_yaml(input_dict):
        p = Configuration()
        ConfigChapter.validate(input_dict, validation_file='configuration_schema.json')
        return p
