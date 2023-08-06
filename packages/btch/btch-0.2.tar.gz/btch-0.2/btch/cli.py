from argparse import ArgumentParser
from logging import getLogger, StreamHandler, DEBUG
from .logger import logger
from json import dumps
from .fns import jobs, dump
from csv import reader

JOB_CMD = "job"
CSV_CMD = "csv"
DUMP_CMD = "dump"
PURGE_CMD = "purge"

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action = "store_true")
subparsers = parser.add_subparsers(dest = "which")
subparsers.required = True

job_parser = subparsers.add_parser(JOB_CMD)
dump_parser = subparsers.add_parser(DUMP_CMD)
csv_parser = subparsers.add_parser(CSV_CMD)
csv_parser.add_argument("file")

def run():
    # Parse the CLI arguments.
    args, unknown_args = parser.parse_known_args()

    # Enable logging if the verbose arg is used.
    if args.verbose:
        root_logger = getLogger()
        root_logger.addHandler(StreamHandler())
        logger.setLevel(DEBUG)

    # Submit a job to AWS batch.
    if args.which == JOB_CMD:
        output = dict(group_id = jobs([("master", unknown_args)]))
        print(dumps(output, indent = 4))
    elif args.which == CSV_CMD:
        commands = list()
        with open(args.file) as f:
            for row in reader(f):
                commands.append((row[0], row[1:]))
        output = dict(group_id = jobs(commands))
        print(dumps(output, indent = 4))
    elif args.which == DUMP_CMD:
        print(dumps(dump(), indent = 4))

if __name__ == "__main__":
    run()