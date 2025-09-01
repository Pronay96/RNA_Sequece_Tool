from sys import argv
import os

def copy_file_content(source_path, destination_path):
    with open(source_path, 'r', encoding='utf-8') as src:
        lines_to_write = []

        content = src.read()

        blocks = content.strip().split('\n\n')

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                lines_to_write.append(f"{lines[0].strip()} -> {lines[2].strip()}")

    with open(destination_path, 'w', encoding='utf-8') as dest:
        dest.write('\n'.join(lines_to_write))


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python script_name.py <source_file> <destination_file>")
    source_path = os.path.abspath(argv[1])
    destination_path = os.path.abspath(argv[2])
    copy_file_content(source_path, destination_path)
