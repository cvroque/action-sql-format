#! /usr/bin/python3
import sys
import sqlparse
import chardet

def read_file(file_name):
    # Use chardet to detect the encoding
    with open(file_name, "rb") as f:
        result = chardet.detect(f.read())
    
    detected_encoding = result['encoding']

    with open(file_name, "r", encoding=detected_encoding) as f:
        source = f.read()

    return source

def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)


print("Reformatting files")
# Pretty print input files
for file in sys.argv[1:]:
    print("* " + file + ":")
    original = read_file(file)
    
    # Temporary replacement 
    original = original.replace('@@ FETCH_STATUS', '__AT_AT_FETCH_STATUS__')
    original = original.replace('@@FETCH_STATUS', '__AT_AT_FETCH_STATUS__')
    original = original.replace('*/', '__COMMENT_END__')
    
    formatted = sqlparse.format(original, reindent=False,
                                reindent_aligned=True,
                                keyword_case='upper',
                                identifier_case='upper',
                                strip_comments=False,  # Keep comments
                                use_space_around_operators=True,
                                indent_tabs=False,
                                indent_width=2,
                                wrap_after=120,
                                reindent_aligned_blocks=[('UNION ALL', ['SELECT'])],
                                comma_first=True)
    
    # Restore after formatting
    formatted = formatted.replace('__AT_AT_FETCH_STATUS__', '@@FETCH_STATUS')
    formatted = formatted.replace('__COMMENT_END__', '*/')


    if original == formatted:
        print("  - Unchanged")
    else:
        print("  - Changed")
        write_file(file, formatted)
