import io
import datasets

from pathlib import Path
from collections import Counter
from datasets import concatenate_datasets


def count_length(code):
    length = 0
    text_stream = io.TextIOWrapper(io.BytesIO(code.encode()), encoding='utf-8')
    for _ in text_stream:
        length += 1

    return length


def add_length(example):
    example['length'] = count_length(example['source_code'])

    return example


def add_num_hidden_unit_tests(example):
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    example['num_hidden_unit_tests'] = len(hidden_unit_tests)

    return example


def main():
    supported_lang_clusters = ['Python', 'Java', 'C', 'C++']
    supported_langs = ['Python 3', 'Java 8', 'GNU C', 'GNU C++']
    save_path = Path(__file__).parent.parent / Path('data') / Path('lang_code_translation')

    dataset = datasets.load_dataset('NTU-NLP-sg/xCodeEval', 'code_translation',
                                    split='validation')  # +validation_small+test
    print(dataset)

    dataset = concatenate_datasets(
        [dataset.filter(lambda example: example['lang'] == lang) for lang in supported_langs]
    )
    print(dataset)

    dataset = dataset.remove_columns('file_name')
    dataset = dataset.map(add_length)
    dataset = dataset.map(add_num_hidden_unit_tests)
    print(dataset)

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    dataset.save_to_disk(save_path)


if __name__ == '__main__':
    main()
