import yaml
from flexitex.flexiast.structure import NodeRule


class Config:
    def __init__(self, path="config.yml"):
        with open(path, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.input_file = config.get("input")
        if not self.input_file:
            raise ValueError("Missing 'input' field in config.yml")

        output = config.get("output", {})
        self.output_folder = output.get("folder", "")
        self.output_main_file = output.get("main_file", "main.tex")

        self.structure_rules = [NodeRule(**rule) for rule in config.get("structure", []) or []]
