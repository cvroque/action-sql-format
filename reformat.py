#! /usr/bin/python3

import sys
import sqlparse


def read_file(file_name):
    with open(file_name, "r") as f:
        source = f.read()
        f.close()

    return source


def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)


print("Reformatting files")
# Pretty print input files
for file in sys.argv[1:]:
    print("* " + file + ":")
    original = read_file(file)
    formatted = sqlparse.format(original, reindent=False,
                                reindent_aligned=True,
                                keyword_case='upper',
                                identifier_case='upper',
                                strip_comments=False,
                                use_space_around_operators=True,
                                indent_tabs=False,
                                indent_width=2,
                                wrap_after=120,
                                comma_first=True)

    if original == formatted:
        print("  - Unchanged")
    else:
        print("  - Changed")
        write_file(file, formatted)
