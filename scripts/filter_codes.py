import random
import argparse

from tqdm import tqdm
from pathlib import Path
from collections import Counter
from datasets import load_from_disk, concatenate_datasets


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample_seed', default=1, choices=[1, 2, 3, 4, 5], type=int)
    args = parser.parse_args()

    return args


def update_hidden_unit_tests(example):
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    random.shuffle(hidden_unit_tests)
    example['hidden_unit_tests'] = str(random.sample(hidden_unit_tests, num_hidden_unit_tests))
    print(example['hidden_unit_tests'])
    example['num_hidden_unit_tests'] = num_hidden_unit_tests

    return example


def main():
    supported_lang_clusters = ['C', 'C++', 'Java', 'Python']
    over_tokens_limit_code_uids = ['24ec0baf29c51e9778eb26a30520d019', 'f006d77bad35b82bc0416f8d13ce55b2']
    load_path = Path(__file__).parent.parent / Path('data') / Path('temp_data')
    save_path_1 = Path(__file__).parent.parent / Path('results') / Path(
        f'code_test_data_human_{args.sample_seed}.jsonl')
    save_path_2 = Path(__file__).parent.parent / Path('results') / Path('code_test_data.jsonl')

    dataset = load_from_disk(str(load_path))
    print(dataset)

    # find duplicate problems for each language
    c_unique_src_uids = set()
    cpp_unique_src_uids = set()
    java_unique_src_uids = set()
    python_unique_src_uids = set()
    for example in tqdm(dataset):
        lang_cluster = example['lang_cluster']
        src_uid = example['src_uid']
        if lang_cluster == 'C':
            if src_uid in c_unique_src_uids:
                print('C duplicate problem src uid:', src_uid)
            else:
                c_unique_src_uids.add(src_uid)
        elif lang_cluster == 'C++':
            if src_uid in cpp_unique_src_uids:
                print('C++ duplicate problem src uid:', src_uid)
            else:
                cpp_unique_src_uids.add(src_uid)
        elif lang_cluster == 'Java':
            if src_uid in java_unique_src_uids:
                print('Java duplicate problem src uid:', src_uid)
            else:
                java_unique_src_uids.add(src_uid)
        elif lang_cluster == 'Python':
            if src_uid in python_unique_src_uids:
                print('Python duplicate problem src uid:', src_uid)
            else:
                python_unique_src_uids.add(src_uid)
        else:
            print('Language cluster not found.')
    print(len(c_unique_src_uids))
    print(len(cpp_unique_src_uids))
    print(len(java_unique_src_uids))
    print(len(python_unique_src_uids))

    dataset = concatenate_datasets(
        [
            dataset.filter(
                lambda example:
                example['num_hidden_unit_tests'] >= num_hidden_unit_tests and
                example['difficulty'] is not None and
                'megabytes' in example['prob_desc_memory_limit'] and
                'second' in example['prob_desc_time_limit'] and
                example['code_uid'] not in over_tokens_limit_code_uids and
                example['pass_rate'] == 100 and
                example['line_coverage'] == 100 and
                example['branch_coverage'] == 100 and
                example['lang_cluster'] == lang_cluster
            ).shuffle(seed).select(range(num_per_lang_cluster))
            for lang_cluster in supported_lang_clusters
        ]
    )
    print(dataset)

    dataset = dataset.remove_columns('src_uid')
    dataset = dataset.remove_columns('pass_rate')
    dataset = dataset.remove_columns('line_coverage')
    dataset = dataset.remove_columns('branch_coverage')
    dataset.cleanup_cache_files()  # for multiple random selections
    dataset = dataset.map(update_hidden_unit_tests)
    print(dataset)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    dataset.to_json(save_path_1, lines=True)

    dataset = dataset.remove_columns('hidden_unit_tests')
    print(dataset)

    dataset.to_json(save_path_2, lines=True)


if __name__ == '__main__':
    args = parse_arguments()
    seed = 42
    random.seed(args.sample_seed)
    num_hidden_unit_tests = 5
    num_per_lang_cluster = 100
    main()
    # python scripts/filter_codes.py
