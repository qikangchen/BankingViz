import argparse

from .Bankingviz import Bankingviz


def main():
    '''
    Main application for generating visual reports.

    For more information use -h for help.

    :return:
    '''
    parser = argparse.ArgumentParser(description='BankingViz: A visual report generator for banking information')

    parser.add_argument('-c ', '--converter',
                        help='<Required> Choose a converter from this list [sparkasse_csv_camt_german]',
                        required=True)
    parser.add_argument('-s', '--sources', nargs='+', help='<Required> Source files', required=True)
    parser.add_argument('-p', '--project_name', help='<Required> Files will be generated in data/project_name',
                        required=True)
    args = parser.parse_args()

    bv = Bankingviz()
    bv.generate(args.converter, args.sources, args.project_name)

if __name__ == '__main__':
    main()
