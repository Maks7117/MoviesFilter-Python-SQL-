from pandas import read_csv, read_parquet


class CommandFactory(object):
    def __init__(self, args):
        self.args = args

    def create(self):
        action = self.args.action

        if action == 'output_parquet':
            return CsvToParquetCommand(self.args.input_file, self.args.output_file)

        elif action == 'output_csv':
            return ParquetToCsvCommand(self.args.input_file, self.args.output_file)

        elif action == 'schema':
            return ParquetToSchemaCommand(self.args.input_file)
        else:
            raise ValueError('%s action is not supported' % action)


class Command(object):
    def execute(self):
        raise NotImplementedError("Implement this method!")


class CsvToParquetCommand(Command):
    def __init__(self, csv_file, parquet_file):
        self.csv_file = csv_file
        self.parquet_file = parquet_file

    def execute(self):
        df = read_csv(self.csv_file)
        df.to_parquet(self.parquet_file)


class ParquetToCsvCommand(Command):
    def __init__(self, parquet_file, csv_file):
        self.parquet_file = parquet_file
        self.csv_file = csv_file

    def execute(self):
        df = read_csv(self.parquet_file)
        df.to_parquet(self.csv_file)


class ParquetToSchemaCommand(Command):
    def __init__(self, parquet_file):
        self.parquet_file = parquet_file

    def execute(self):
        schema = read_parquet(self.parquet_file)
        print(schema.info())



