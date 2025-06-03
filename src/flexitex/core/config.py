import yaml
from flexitex.flexiast.structure import NodeRule


class Config:
    def __init__(self, path="config.yml"):
        with open(path, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        input = config.get("input", {})
        self.input_folder = input.get("folder", "")
        self.input_main_file = input.get("main_file", "main.tex")
        
        output = config.get("output", {})
        self.output_folder = output.get("folder", "")
        self.output_main_file = output.get("main_file", "main.tex")
        self.output_figure_folder = output.get("figure_folder", "figs")

        self.structure_rules = [NodeRule(**rule) for rule in config.get("structure", []) or []]
