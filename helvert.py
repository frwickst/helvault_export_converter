#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path
from typing import List

from formatters import supported_formatters


class Helvert:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Helvault Export Converter")
        subparsers = self.parser.add_subparsers(
            dest="command", metavar="<command>", required=True
        )

        export_parser = subparsers.add_parser("export", help="Export Helvault file")

        export_parser.add_argument("-f", "--format", dest="format")

        export_parser.add_argument("-i", "--in-file", dest="in_file")

        export_parser.add_argument("-o", "--out-file", dest="out_file")

        export_parser.add_argument("-r", "--replace", dest="replace", action='store_true')

    def run_command(self) -> None:
        args = vars(self.parser.parse_args())
        command = args.pop("command")

        # use dispatch pattern to invoke method with same name
        getattr(self, command)(**args)

    def help(self) -> None:
        self.parser.print_help()

    def export(self, in_file: str, out_file: str, format: str, replace: bool):
        formatter = supported_formatters.get(format, None)
        if not formatter:
            print(f"Error: Format {format} is not supported")
            sys.exit(-1)
        formatter = formatter()

        if not in_file or not out_file:
            print("Error: Both an in file and out file needs to be specified")
            sys.exit(-1)

        in_file_path = Path(in_file)
        out_file_path = Path(out_file)

        if not in_file_path.exists():
            raise FileNotFoundError(f"File {in_file_path.absolute()} does not exist")

        if out_file_path.exists():
            if not replace:
                raise FileExistsError(
                    f"File {out_file_path.absolute()} exists and -r/--replace was not set"
                )
            out_file_path.unlink()

        out_rows = []
        with in_file_path.open() as i_f:
            in_reader = csv.reader(i_f, delimiter=',', quotechar='"')
            headers = in_reader.__next__()
            headers_list = formatter.format_headers(headers)

            valid_headers = self.get_valid_row(headers_list, headers_list)
            out_rows.append(valid_headers)

            for row in in_reader:
                valid_row = self.get_valid_row(row, headers_list)
                dict_row = dict(zip(valid_headers, valid_row))
                out_rows.append(formatter.format_row(dict_row))

        with out_file_path.open(mode="w") as o_f:
            out_writer = csv.writer(o_f, delimiter=",", quotechar='"')
            for row in out_rows:
                out_writer.writerow(row)

    def get_valid_row(self, row: List[str], headers: List[str]):
        removable_value_indices = [i for i, value in enumerate(headers) if value is None]
        new_row = [i for j, i in enumerate(row) if j not in removable_value_indices]
        return new_row


if __name__ == "__main__":
    do = Helvert()
    do.run_command()
