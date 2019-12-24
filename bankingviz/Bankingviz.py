import os

import pandas as pd

import config
from converter.sparkasse_csv_camt_german.converter import Sparkasse_csv_camt_german
from visualizer.visualizer import Visualizer


class Bankingviz:

    def generate(self, converter: str, sources: list, project_name: str) -> None:
        # create dir if not existing
        destination_dir = os.path.join(config.DATA_DIR, project_name)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # select converter
        if converter == "sparkasse_csv_camt_german":
            conv = Sparkasse_csv_camt_german(sources[0], os.path.join(destination_dir, config.CONVERTED_CSV))
        else:
            raise AttributeError("Converter " + converter + " does not exist")

        # convert to agreed csv file format
        csv_converted = conv.convert()
        print("Converted .csv file is located ", csv_converted)

        # read agreed csv file
        df = pd.read_csv(csv_converted)

        # generate reports
        viz = Visualizer(df, destination_dir)
        viz.generate_spending_bins_amount()
        viz.generate_spending_bins_weekdays()
        viz.generate_spending_timeline()
        viz.generate_earning_bins_amount()
        viz.generate_earning_bins_weekdays()
        viz.generate_earning_timeline()
