import argparse

import pandas as pd

from .visualizer import Visualizer


def main():
    """
    Application for visualizing the banking data. A agreed csv file need to be provided.

    For more information use -h for help.

    :return:
    """

    # read parameters
    parser = argparse.ArgumentParser(description='Generating stats from your agreed .csv file')

    parser.add_argument('--source', help='<Required> Location of the agreed .csv file', required=True)
    parser.add_argument('--dest_dir', help='<Required> Directory where the files will be generated', required=True)
    args = parser.parse_args()

    # load data
    df = pd.read_csv(args.source)

    # generate reports
    viz = Visualizer(df, args.dest_dir)
    viz.generate_spending_bins_amount()
    viz.generate_spending_bins_weekdays()
    viz.generate_spending_timeline()
    viz.generate_earning_bins_amount()
    viz.generate_earning_bins_weekdays()
    viz.generate_earning_timeline()


if __name__ == '__main__':
    main()
