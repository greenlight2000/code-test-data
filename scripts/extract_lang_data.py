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
    supported_langs = ['Python', 'Java']
    save_path = Path(__file__).parent.parent / Path('data') / Path('code_test_data.json')

    ct_dataset = datasets.load_dataset('NTU-NLP-sg/xCodeEval', 'code_translation', split='validation')
    print(ct_dataset)

    ct_dataset = ct_dataset.remove_columns('file_name')
    ct_dataset = ct_dataset.map(add_length)
    ct_dataset = ct_dataset.map(add_num_hidden_unit_tests)
    print(ct_dataset)

    lang_counts = Counter(ct_dataset['lang_cluster'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_ct_dataset = concatenate_datasets(
        [
            ct_dataset.filter(lambda example: example['lang_cluster'] == lang).sort(
                ['num_hidden_unit_tests', 'difficulty', 'length'], reverse=True).select(range(10)) for lang in
            supported_langs
        ]
    )
    print(lang_ct_dataset)

    lang_counts = Counter(lang_ct_dataset['lang_cluster'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_ct_dataset.to_json(save_path, lines=False)


if __name__ == '__main__':
    main()
