import unittest

from segment.word_tokenizer.word_graph import WordGraph, Node


class TestGraph(unittest.TestCase):

    def test_graph(self):
        graph = WordGraph()
        graph.insert_start_word(WordGraph.NODE_S)  # 0
        graph.insert_start_word(Node('我', 1, 'core_dict'))  # 1
        graph.insert_start_word(Node('喜', 2, 'core_dict'))  # 2
        graph.insert_start_word(Node('喜欢', 4, 'model_word_dict'))  # 3
        graph.insert_start_word(Node('欢', 1, 'core_dict'))  # 4

        graph.insert_end_words([1])
        graph.insert_end_words([2, 3])
        graph.insert_end_words([4])
        graph.insert_end_words([5])
        graph.insert_end_words([5])

        route = graph.calculate()

        print(graph)
        print(route)
        assert route[0][0] == 5  # 确保最优路径权重为5


if __name__ == '__main__':
    unittest.main()
