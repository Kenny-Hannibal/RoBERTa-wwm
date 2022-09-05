import json
import random
import unittest

import requests

HOST = '127.0.0.1'
PORT = 8000


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
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
                'model': _sample(['hmm', 'crf', 'dl']),
                'enable_offset': _sample([True, False])
            }
            print(json.dumps(data, ensure_ascii=False))
            r = requests.post('http://{}:{}/seg'.format(HOST, PORT), json=data)
            print(r.text)
            assert r.status_code == 200 and json.loads(r.text)['status'] == 'OK'
        print('\n')

    def test_pos(self):
        print('test_pos~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for sample in self.samples:
            data = {
                'content': sample,
                'model': _sample(['hmm', 'crf']),
            }
            print(json.dumps(data, ensure_ascii=False))
            r = requests.post('http://{}:{}/pos'.format(HOST, PORT), json=data)
            print(r.text)
            assert r.status_code == 200 and json.loads(r.text)['status'] == 'OK'
        print('\n')

    def test_dict(self):
        print('test_dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        print('add word')
        data = {'word': '深度之眼', 'pos': 'nt', 'freq': 50}
        r = requests.post('http://{}:{}/dict'.format(HOST, PORT), json=data)
        print(r.text)
        assert r.status_code == 200 and json.loads(r.text)['status'] == 'OK'

        print('delete word')
        data = {'word': '深度之眼'}
        r = requests.delete('http://{}:{}/dict'.format(HOST, PORT), json=data)
        print(r.text)
        assert r.status_code == 200 and json.loads(r.text)['status'] == 'OK'


def _sample(values):
    return random.sample(values, 1)[0]


if __name__ == '__main__':
    unittest.main()
