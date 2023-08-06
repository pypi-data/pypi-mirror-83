import unittest
from bi_lstm_crf.app import WordsTagger


class MyTestCase(unittest.TestCase):
    # def test_empty(self):
    #     tags = WordsTagger.tokens_from_tags(["abcde"], [["O", "O", "O", "O", "O"]], begin_tags="BS");
    #     self.assertEqual(tags, [[]])

    def test_1(self):
        tags = WordsTagger.tokens_from_tags(["abcde"], [["O", "B-ME", "I-ME", "O", "S-YOU"]], begin_tags="BS");
        self.assertEqual(tags, [[("bc", "ME"), ("e", "YOU")]])

    def test_start(self):
        tags = WordsTagger.tokens_from_tags(["abcde"], [["B-ME", "I-ME", "O", "S-YOU", "S-YOU"]], begin_tags="BS");
        self.assertEqual(tags, [[("ab", "ME"), ("d", "YOU"), ("e", "YOU")]])

    def test_whole(self):
        tags = WordsTagger.tokens_from_tags(["abcde"], [["B-ME", "I-ME", "I", "I-YOU", "I-YOU"]], begin_tags="BS");
        self.assertEqual(tags, [[("abcde", "ME")]])


if __name__ == '__main__':
    unittest.main()
