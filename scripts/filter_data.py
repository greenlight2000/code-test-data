from pathlib import Path
from collections import Counter
from datasets import load_from_disk, concatenate_datasets


def main():
    supported_lang_clusters = ['Python', 'Java', 'C', 'C++']
    supported_langs = ['Python 3', 'Java 8', 'GNU C', 'GNU C++']
    load_path = Path(__file__).parent.parent / Path('data') / Path('exec_code_translation')
    save_path = Path(__file__).parent.parent / Path('results') / Path('code_test_data.jsonl')

    dataset = load_from_disk(str(load_path))
    print(dataset)

    filter_dataset = concatenate_datasets(
        [
            dataset.filter(lambda example: example['lang'] == lang and example['all_passed'] == 1).sort(
                ['num_hidden_unit_tests', 'difficulty', 'length'], reverse=True).select(range(100)) for lang in
            supported_langs
        ]
    )
    filter_dataset = filter_dataset.remove_columns('all_passed')
    print(filter_dataset)

    lang_cluster_counts = Counter(filter_dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    lang_counts = Counter(filter_dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    filter_dataset.to_json(save_path, lines=True)


if __name__ == '__main__':
    main()
