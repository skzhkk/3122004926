import sys
import jieba
import jieba.analyse
import numpy as np
import re
import concurrent.futures


class SimHash(object):
    def simhash(self, content):
        # 清洗文本
        content = re.sub(r'[^\w\s]', '', content)  # 去除标点符号
        content = ' '.join(content.split())  # 去除多余空格
        stop_words = {'的', '了', '在', '是', '有', '和', '不', '这', '也', '人', '说', '要', '就', '但', '可以', '还',
                      '你', '我', '他', '它'}  # 停用词
        content = ' '.join([word for word in content.split() if word not in stop_words])

        # 对输入内容进行分词
        seg = list(jieba.cut(content))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(jieba.analyse.extract_tags, "|".join(seg), topK=10, withWeight=True)
            key_words = future.result()

        key_list = []  # 用于存储每个关键词的加权哈希值
        for feature, weight in key_words:
            # print('weight: {}'.format(weight))
            # 将关键词转换为二进制字符串（哈希值）
            binstr = self.string_hash(feature)
            # print('feature: %s , string_hash %s' % (feature, binstr))
            temp = []  # 用于存储当前关键词的加权值

            for c in binstr:
                if c == '1':
                    temp.append(weight)
                else:
                    temp.append(-weight)
            key_list.append(temp)  # 当前关键词的加权值列表 temp 添加到 key_list 中
        list_sum = np.sum(np.array(key_list), axis=0)  # key_list 转换为 NumPy 数组按行求和，得到每一位的总和
        if not key_list:
            return '00'
        simhash = ''
        for i in list_sum:
            if i > 0:
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash  # 返回 simhash 值

    @staticmethod
    def string_hash(source):
        if source == "":  # 空字符串返回0
            return 0
        else:
            x = ord(source[0]) << 7  # 第一个字符的 ASCII 值左移 7 位
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2  # 避免返回-1
            x = bin(x).replace('0b', '').zfill(64)[-64:]  # 转换为二进制字符串，去掉前缀 '0b'，并填充至 64 位
            return str(x)  # 返回哈希值字符串

    @staticmethod
    def get_distance(hash_str1, hash_str2):
        length = 0
        for index, char in enumerate(hash_str1):
            if char == hash_str2[index]:  # 如果两个哈希字符串在当前位相同，则继续；否则，汉明距离加 1
                continue
            else:
                length += 1

        return length  # 返回汉明距离


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"错误: 文件 '{file_path}' 未找到。")
    except PermissionError:
        raise PermissionError(f"错误: 没有权限读取文件 '{file_path}'。")
    except Exception as e:
        raise Exception(f"发生了一个错误: {e}")


def calculate_similarity(original_text, plagiarized_text):
    # 创建 SimHash 类的实例
    simhash_instance = SimHash()
    # 计算两个文本的哈希值
    hash1 = simhash_instance.simhash(original_text)
    hash2 = simhash_instance.simhash(plagiarized_text)

    # 输出哈希值
    print("文本1的哈希值:", hash1)
    print("文本2的哈希值:", hash2)

    # 计算汉明距离
    distance = SimHash.get_distance(hash1, hash2)

    # 输出汉明距离
    print("汉明距离:", distance)

    if not original_text and plagiarized_text or original_text and not plagiarized_text:
        return 0.0

    # 计算两个哈希值之间的汉明距离
    similarity = 1 - distance / 64
    # 通过海明距离换算成相似度（Simhash为64位）
    return similarity


def write_file(file_path, similarity):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("{:.2f}".format(similarity))
    except PermissionError:
        raise PermissionError(f"没有权限写入文件: {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"文件路径不存在: {file_path}")
    except Exception as e:
        raise Exception(f"写入文件时发生错误: {e}")


def main(original_file_main, plagiarized_file_main, output_file_main):
    original_text = read_file(original_file_main)
    plagiarized_text = read_file(plagiarized_file_main)

    similarity = calculate_similarity(original_text, plagiarized_text)  # 计算两个文本的相似度
    print(similarity)  # 输出文本相似度
    write_file(output_file_main, similarity)  # 写入文件


if __name__ == "__main__":
    if len(sys.argv) != 4:  # 参数数量错误
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
    else:
        original_file = sys.argv[1]  # 原始文本
        plagiarized_file = sys.argv[2]  # 抄袭文本
        output_file = sys.argv[3]  # 输出文本
        main(original_file, plagiarized_file, output_file)
