from pathlib import Path
from collections import Counter
from datasets import load_dataset


def main():
    # TODO：回来重复五次，整理代码，得到一个平均值，处理五个json文件得到一个baseline，继续调优prompt，然后处理返回的json数据
    
    load_path_human = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human.jsonl')
    load_path_palm = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_palm.jsonl')

    dataset_human = load_dataset('json', split='train', data_files=str(load_path_human))
    print(dataset_human)

    dataset_human = dataset_human.filter(
        lambda example: example['pass_rate'] == 100 and example['line_coverage'] == 100 and example[
            'branch_coverage'] == 100
    )
    print(dataset_human)

    lang_counts = Counter(dataset_human['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset_human['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')


if __name__ == '__main__':
    main()
