import matplotlib.pyplot as plt

from pathlib import Path
from collections import Counter
from datasets import load_dataset


def main():
    load_path = Path(__file__).parent.parent / Path('results') / Path('code_test_eval_human.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(dataset)

    aaa = dataset.filter(
        lambda example: example['pass_rate'] == 100 and example['line_coverage'] == 100 and example[
            'branch_coverage'] == 100
    )
    print(aaa)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    pass_rates = dataset['pass_rate']
    line_coverages = dataset['line_coverage']
    branch_coverages = dataset['branch_coverage']
    print(pass_rates)
    print(line_coverages)
    print(branch_coverages)

    ax = plt.subplot(projection='3d')
    ax.scatter(line_coverages, branch_coverages, pass_rates, c='r', marker='o', alpha=0.5)
    ax.set_xlim(0.00, 100.0)
    ax.set_ylim(0.00, 100.0)
    ax.set_zlim(0.00, 100.0)
    ax.set_title('Unit Test Metrics 3D')
    ax.set_xlabel('Line coverage (%)')
    ax.set_ylabel('Branch coverage (%)')
    ax.set_zlabel('Pass rate (%)')

    plt.show()


if __name__ == '__main__':
    main()
    # python scripts/plot_data.py
