import sys
from simhash import Simhash


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def calculate_similarity(original_text, plagiarized_text):
    original_hash = Simhash(original_text)
    #使用 Simhash 算法计算原始文本的哈希值，结果存储在original_hash中
    plagiarized_hash = Simhash(plagiarized_text)
    #使用 Simhash 算法计算抄袭文本的哈希值，结果存储在plagiarized_hash中
    distance = original_hash.distance(plagiarized_hash)
    #计算两个哈希值之间的海明距离
    similarity = 1 - distance / 64
    #通过海明距离换算成相似度（Simhash为64位）
    return similarity


def write_file(output_file, similarity):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("{:.2f}".format(similarity))


def main(original_file, plagiarized_file, output_file):
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)

    similarity = calculate_similarity(original_text, plagiarized_text) #计算两个文本的相似度
    print(similarity)#输出文本相似度
    write_file(output_file, similarity)#写入文件


if __name__ == "__main__":
    if len(sys.argv) != 4:#参数数量错误
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
    else:
        original_file = sys.argv[1]#原始文本
        plagiarized_file = sys.argv[2]#抄袭文本
        output_file = sys.argv[3]#输出文本
        main(original_file, plagiarized_file, output_file)