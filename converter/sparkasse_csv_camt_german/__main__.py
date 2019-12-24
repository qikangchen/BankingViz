import argparse

from .converter import Sparkasse_csv_camt_german


def main():
    """
    Application to convert Sparkasse csv file to agreed csv file to be read by the visualizer.

    For more information use -h for help.

    :return:
    """

    # read parameters
    parser = argparse.ArgumentParser(description='Converting from Sparkasse csv file to agreed .csv file')

    parser.add_argument('--source', help='<Required> File source', required=True)
    parser.add_argument('--destination', help='<Required> Destination where the agreed .csv file will be saved.',
                        required=True)
    args = parser.parse_args()

    conv = Sparkasse_csv_camt_german(args.source, args.destination)
    print(conv.convert())

if __name__ == '__main__':
    main()
