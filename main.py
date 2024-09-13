import sys
import jieba
import jieba.analyse
import numpy as np
import re


class SimHash(object):
    def simHash(self, content):
        # 清洗文本
        content = re.sub(r'[^\w\s]', '', content)  # 去除标点符号
        content = ' '.join(content.split())  # 去除多余空格
        stop_words = {'的', '了', '在', '是', '有', '和', '不', '这', '也', '人', '说', '要', '就', '但', '可以', '还',
                      '你', '我', '他', '它'}  # 停用词
        content = ' '.join([word for word in content.split() if word not in stop_words])

        # 对输入内容进行分词
        seg = jieba.cut(content)
        # jieba基于TF-IDF提取前10个关键词 用|连接成一个字符串 返回一个包含元组（关键词，权重）的列表
        keyWords = jieba.analyse.extract_tags("|".join(seg), topK=10, withWeight=True)

        keyList = []  # 用于存储每个关键词的加权哈希值
        for feature, weight in keyWords:
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
            keyList.append(temp)  # 当前关键词的加权值列表 temp 添加到 keyList 中
        listSum = np.sum(np.array(keyList), axis=0)  # keyList 转换为 NumPy 数组按行求和，得到每一位的总和
        if not keyList:
            return '00'
        simhash = ''
        for i in listSum:
            if i > 0:
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash  # 返回 simhash 值

    def string_hash(self, source):
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

    def getDistance(self, hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:  # 如果两个哈希字符串在当前位相同，则继续；否则，汉明距离加 1
                continue
            else:
                length += 1

        return length  # 返回汉明距离


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def calculate_similarity(original_text, plagiarized_text):
    # 创建 SimHash 类的实例
    simhash_instance = SimHash()
    # 计算两个文本的哈希值
    hash1 = simhash_instance.simHash(original_text)
    hash2 = simhash_instance.simHash(plagiarized_text)

    # 输出哈希值
    print("文本1的哈希值:", hash1)
    print("文本2的哈希值:", hash2)

    # 计算汉明距离
    distance = simhash_instance.getDistance(hash1, hash2)

    # 输出汉明距离
    print("汉明距离:", distance)
    # 计算两个哈希值之间的海明距离
    similarity = 1 - distance / 64
    # 通过海明距离换算成相似度（Simhash为64位）
    return similarity


def write_file(output_file, similarity):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("{:.2f}".format(similarity))


def main(original_file, plagiarized_file, output_file):
    original_text = read_file(original_file)
    plagiarized_text = read_file(plagiarized_file)

    similarity = calculate_similarity(original_text, plagiarized_text)  # 计算两个文本的相似度
    print(similarity)  # 输出文本相似度
    write_file(output_file, similarity)  # 写入文件


if __name__ == "__main__":
    if len(sys.argv) != 4:  # 参数数量错误
        print("Usage: python main.py [original_file] [plagiarized_file] [output_file]")
    else:
        original_file = sys.argv[1]  # 原始文本
        plagiarized_file = sys.argv[2]  # 抄袭文本
        output_file = sys.argv[3]  # 输出文本
        main(original_file, plagiarized_file, output_file)
