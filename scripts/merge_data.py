from pathlib import Path
from datasets import load_dataset


def main():
    load_path = Path(__file__).parent.parent / Path('results') / Path('code_test_data.jsonl')
    load_path_1 = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human_1.jsonl')
    load_path_2 = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human_2.jsonl')
    load_path_3 = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human_3.jsonl')
    load_path_4 = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human_4.jsonl')
    load_path_5 = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human_5.jsonl')
    save_path = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(dataset)

    dataset_1 = load_dataset('json', split='train', data_files=str(load_path_1))
    print(dataset_1)

    dataset_2 = load_dataset('json', split='train', data_files=str(load_path_2))
    print(dataset_2)

    dataset_3 = load_dataset('json', split='train', data_files=str(load_path_3))
    print(dataset_3)

    dataset_4 = load_dataset('json', split='train', data_files=str(load_path_4))
    print(dataset_4)

    dataset_5 = load_dataset('json', split='train', data_files=str(load_path_5))
    print(dataset_5)

    pass_rates = [
        round((dataset_1[index]['pass_rate'] + dataset_2[index]['pass_rate'] + dataset_3[index]['pass_rate'] +
               dataset_4[index]['pass_rate'] + dataset_5[index]['pass_rate']) / 5, 2)
        for index in range(len(dataset))
    ]
    print(pass_rates)
    print(len(pass_rates))

    line_coverages = [
        round((dataset_1[index]['line_coverage'] + dataset_2[index]['line_coverage'] + dataset_3[index]['line_coverage']
               + dataset_4[index]['line_coverage'] + dataset_5[index]['line_coverage']) / 5, 2)
        for index in range(len(dataset))
    ]
    print(line_coverages)
    print(len(line_coverages))

    branch_coverages = [
        round((dataset_1[index]['branch_coverage'] + dataset_2[index]['branch_coverage'] + dataset_3[index][
            'branch_coverage'] + dataset_4[index]['branch_coverage'] + dataset_5[index]['branch_coverage']) / 5, 2)
        for index in range(len(dataset))
    ]
    print(branch_coverages)
    print(len(branch_coverages))

    dataset = dataset.add_column('pass_rate', pass_rates)
    dataset = dataset.add_column('line_coverage', line_coverages)
    dataset = dataset.add_column('branch_coverage', branch_coverages)
    print(dataset)

    dataset.to_json(save_path, lines=True)


if __name__ == '__main__':
    main()
    # python scripts/merge_data.py
