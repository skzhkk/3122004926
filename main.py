import sys

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def main(original_file, plagiarized_file, output_file):
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
    else:
        original_file = sys.argv[1]
        plagiarized_file = sys.argv[2]
        output_file = sys.argv[3]
        main(original_file, plagiarized_file, output_file)