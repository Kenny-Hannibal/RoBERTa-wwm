import json
import random
import sys

data_file = '../data/samples.txt'


def _read_samples(sample_file):
    samples = []
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            samples.append(line)
    return samples


def gen_json(txt_len):
    samples = _read_samples(data_file)

    # 不断更新content，直到长度达到text_len
    content = random.sample(samples, 1)[0]
    while len(content) < txt_len:
        content += random.sample(samples, 1)[0]
    content = content[:txt_len]

    data = {
        "content": content,
        "model": "crf",
    }

    with open('request.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    text_len = int(sys.argv[1])
    gen_json(text_len)
