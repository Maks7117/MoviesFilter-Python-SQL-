import argparse
from command import CommandFactory


def parse_args():
    parser = argparse.ArgumentParser(description='csv to parquet',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input_file', type=str, help='Input dir for csv', required=False)
    parser.add_argument('-o', '--output_file', type=str, help='Output dir for parquet', required=False)
    parser.add_argument('-a', '--action', help='What to do with file? output_parquet, output_csv, schema \n' +
                        'default = output_parquet',
                        default='output_parquet')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    CommandFactory(args) \
        .create() \
        .execute()
