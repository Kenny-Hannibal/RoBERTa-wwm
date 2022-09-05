import random
import unittest

from online.rpc.segment_client import SegmentClient

HOST = '127.0.0.1'
PORT = 8000


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = SegmentClient(host=HOST, port=PORT)
        self.samples = []
        with open('tests/data/samples.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.samples.append(line)

    def test_seg(self):
        print('test_seg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for sample in self.samples:
            data = {
                'content': sample,
                'model': _sample(['hmm', 'crf', 'dl'])
            }
            r = self.client.seg(**data)
            print(r)
        print('\n')

    def test_pos(self):
        print('test_pos~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for sample in self.samples:
            data = {
                'content': sample,
                'model': _sample(['hmm', 'crf']),
            }
            r = self.client.pos(**data)
            print(r)
        print('\n')

    def test_dict(self):
        print('test_dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        print('add word')
        data = {'word': '深度之眼', 'pos': 'nt', 'freq': 10}
        self.client.add_word(**data)

        print('delete word')
        data = {'word': '深度之眼'}
        self.client.delete_word(**data)


def _sample(values):
    return random.sample(values, 1)[0]


if __name__ == '__main__':
    unittest.main()
