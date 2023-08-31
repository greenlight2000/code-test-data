from pathlib import Path
from collections import Counter
from datasets import load_from_disk


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path('exec_data')
    save_path = Path(__file__).parent.parent / Path('results') / Path('code_test_data_raw.jsonl')

    dataset = load_from_disk(str(load_path))
    print(dataset)

    dataset = dataset.filter(lambda example: example['all_passed'] == 1)
    dataset = dataset.remove_columns('all_passed')
    print(dataset)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    dataset.to_json(save_path, lines=True)


if __name__ == '__main__':
    main()
    # python scripts/filter_data.py
