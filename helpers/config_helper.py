import json

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = json.load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)

# Create a global configuration instance
config = Config('./assets/config.json')
