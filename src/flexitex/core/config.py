import os
import yaml
from flexitex.flexiast.structure import NodeRule


class Config:
    def __init__(self, path="config.yml"):
        with open(path, encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        input = config.get("input", {})
        self.input_folder = input.get("folder", "")
        self.input_main_file = input.get("main_file", "main.tex")

        output = config.get("output", {})
        self.output_folder = output.get("folder", "")
        self.output_main_file = output.get("main_file", "main.tex")
        self.output_figure_folder = output.get("figure_folder", "figs")

        self.structure_rules = [NodeRule(**rule)
                                for rule in config.get("structure", []) or []]

    def override(self, input_folder=None, input_main=None,
                 output_folder=None, output_main=None, figure_folder=None):
        if input_folder:
            self.input_folder = input_folder
        if input_main:
            self.input_main_file = input_main
        if output_folder:
            self.output_folder = output_folder
        if output_main:
            self.output_main_file = output_main
        if figure_folder:
            self.output_figure_folder = figure_folder

    def validate(self):
        errors = []

        if not self.input_folder:
            errors.append("Missing input folder.")
        if not self.input_main_file:
            errors.append("Missing input main file.")
        if not self.output_folder:
            errors.append("Missing output folder.")
        if not self.output_main_file:
            errors.append("Missing output main file.")
        if not self.output_figure_folder:
            errors.append("Missing output figure folder.")

        if not isinstance(self.structure_rules, list):
            errors.append("structure_rules must be a list.")
        elif not all(isinstance(rule, NodeRule) for rule in self.structure_rules):
            errors.append("All structure_rules must be instances of NodeRule.")

        if self.input_folder:
            if not os.path.isdir(self.input_folder):
                errors.append(
                    f"Input folder does not exist: {self.input_folder}")
            elif self.input_main_file:
                input_main_path = os.path.join(
                    self.input_folder, self.input_main_file)
                if not os.path.isfile(input_main_path):
                    errors.append(
                        f"Input main file does not exist: {input_main_path}")

        if errors:
            raise ValueError("Invalid configuration:\n" + "\n".join(errors))
