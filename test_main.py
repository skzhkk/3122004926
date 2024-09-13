import unittest
from main import SimHash, read_file, calculate_similarity, write_file, main


class TestSimHash(unittest.TestCase):

    def setUp(self):
        # 创建 SimHash 实例
        self.simhash_instance = SimHash()

    def test_empty_string(self):
        # 测试空字符串的情况 期望返回 '00'
        self.assertEqual(self.simhash_instance.simHash(""), '00')
        self.assertEqual(self.simhash_instance.string_hash(""), 0)

    def test_single_word(self):
        # 测试单个单词的哈希值 期望返回特定的二进制字符串
        self.assertEqual(self.simhash_instance.simHash("hello"),
                         '0000101110101010100110000011110110110100011101101001011111111101')

    def test_identical_strings(self):
        # 测试两个相同字符串的哈希值 期望汉明距离为 0
        hash1 = self.simhash_instance.simHash("This is a test.")
        hash2 = self.simhash_instance.simHash("This is a test.")
        self.assertEqual(self.simhash_instance.getDistance(hash1, hash2), 0)

    def test_different_strings(self):
        # 测试两个不同字符串的哈希值 期望汉明距离大于 0
        hash1 = self.simhash_instance.simHash("This is a test.")
        hash2 = self.simhash_instance.simHash("This is another test.")
        distance = self.simhash_instance.getDistance(hash1, hash2)
        self.assertGreater(distance, 0)

    def test_hamming_distance(self):
        # 测试汉明距离的计算 期望返回整数
        hash1 = self.simhash_instance.simHash("hello world")
        hash2 = self.simhash_instance.simHash("hello there")
        distance = self.simhash_instance.getDistance(hash1, hash2)
        self.assertIsInstance(distance, int)

    def test_similarity(self):
        # 测试相同文本的相似度 期望返回 1.0
        original_text = "This is a simple test."
        plagiarized_text = "This is a simple test."
        similarity = calculate_similarity(original_text, plagiarized_text)
        self.assertAlmostEqual(similarity, 1.0)

    def test_two_empty_similarity(self):
        # 测试两个空文本的相似度 期望返回 1.0
        original_text = ""
        plagiarized_text = ""
        similarity = calculate_similarity(original_text, plagiarized_text)
        self.assertAlmostEqual(similarity, 1.0)

    def test_one_empty_similarity(self):
        # 测试两个空文本的相似度 期望返回 1.0
        original_text = "a"
        plagiarized_text = ""
        similarity = calculate_similarity(original_text, plagiarized_text)
        self.assertAlmostEqual(similarity, 0)

    def test_similarity_different_texts(self):
        # 测试不同文本的相似度 期望返回小于 1.0
        original_text = "This is a simple test."
        plagiarized_text = "This is a completely different text."
        similarity = calculate_similarity(original_text, plagiarized_text)
        self.assertLess(similarity, 1.0)

    def test_file_reading(self):
        # 测试文件读取功能 确保读取的内容与写入的内容一致
        with open("test_file.txt", "w", encoding='utf-8') as f:
            f.write("This is a test file.")
        content = read_file("test_file.txt")
        self.assertEqual(content, "This is a test file.")

    def test_file_writing(self):
        # 测试文件写入功能 确保写入的相似度格式正确
        output_file = "output.txt"
        calculate_similarity("This is a test.", "This is a test.")  # 计算相似度
        write_file(output_file, 1.0)  # 写入相似度
        with open(output_file, "r", encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "1.00")

    def test_invalid_file(self):
        # 测试读取不存在的文件 期望抛出 FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            read_file("non_existent_file.txt")


    def test_write_to_non_existent_path(self):
        # 测试写入不存在的路径，期望抛出 FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            write_file("non_existent_directory/output.txt", 0.95)

    def test_main_function_write_file_call(self):
        # 准备测试数据
        original_text = "This is the original text."
        plagiarized_text = "This is the plagiarized text."
        original_file = "original.txt"
        plagiarized_file = "plagiarized.txt"
        output_file = "output.txt"

        # 写入原始文本和抄袭文本到临时文件
        with open(original_file, 'w', encoding='utf-8') as f:
            f.write(original_text)
        with open(plagiarized_file, 'w', encoding='utf-8') as f:
            f.write(plagiarized_text)

        # 调用被测试的main函数
        main(original_file, plagiarized_file, output_file)

        # 读取输出文件内容
        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()

        # 断言write_file函数正确写入了相似度到输出文件
        self.assertGreater(output_content, "0.5")

if __name__ == '__main__':
    unittest.main()