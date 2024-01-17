import argparse
import sys
import io
def count_bytes(file):
    return len(file.read())

def count_lines(file):
    return sum(1 for _ in file)

def count_words(file):
    return sum(len(line.split()) for line in file)

def count_characters(file):
    return sum(len(line) for line in file)

def main():
    parser = argparse.ArgumentParser(description='Word counter tool')
    parser.add_argument('-c', action='store_true', help='Count bytes')
    parser.add_argument('-l', action='store_true', help='Count lines')
    parser.add_argument('-w', action='store_true', help='Count words')
    parser.add_argument('-m', action='store_true', help='Count characters')
    parser.add_argument('filename', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, help='Input file (default: standard input)')

    args = parser.parse_args()

    if not (args.c or args.l or args.w or args.m):
        args.c = args.l = args.w = True

    if args.c:
        file = args.filename
        if isinstance(file, io.BufferedReader):
            file.seek(0)  # Rewind the file to the beginning
        print(f"Bytes: {count_bytes(file)}")

    if args.l:
        file = args.filename
        if isinstance(file, io.BufferedReader):
            file.seek(0)  # Rewind the file to the beginning
        print(f"Lines: {count_lines(file)}")

    if args.w:
        file = args.filename
        if isinstance(file, io.BufferedReader):
            file.seek(0)  # Rewind the file to the beginning
        print(f"Words: {count_words(file)}")

    if args.m:
        file = args.filename
        if isinstance(file, io.BufferedReader):
            file.seek(0)  # Rewind the file to the beginning
        print(f"Characters: {count_characters(file)}")

if __name__ == '__main__':
    main()
