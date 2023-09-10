import argparse
import matplotlib.pyplot as plt

from pathlib import Path
from datasets import load_dataset


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', default='PaLM', choices=['Human', 'PaLM', 'GPT-3.5', 'GPT-4'], type=str)
    parser.add_argument('--data_load_name', default='code_test_eval_palm.jsonl',
                        choices=['code_test_eval_human.jsonl', 'code_test_eval_palm.jsonl',
                                 'code_test_eval_gpt3.jsonl', 'code_test_eval_gpt4.jsonl'], type=str)
    parser.add_argument('--figure_save_name', default='code_test_eval_palm.png',
                        choices=['code_test_eval_human.png', 'code_test_eval_palm.png', 'code_test_eval_gpt3.png',
                                 'code_test_eval_gpt4.png'],
                        type=str)
    args = parser.parse_args()

    return args


def main():
    load_path = Path(__file__).parent.parent / Path('results') / Path(args.data_load_name)
    save_path = Path(__file__).parent.parent / Path('results') / Path(args.figure_save_name)

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(dataset)

    pass_rates = dataset['pass_rate']
    print('pass rates:', pass_rates)
    line_coverages = dataset['line_coverage']
    print('line coverages:', line_coverages)
    branch_coverages = dataset['branch_coverage']
    print('branch coverages:', branch_coverages)

    fig = plt.figure(figsize=(8, 6))
    ax = plt.subplot(projection='3d')
    ax.scatter(line_coverages, branch_coverages, pass_rates, c='r', marker='o', alpha=0.5)
    ax.set_xlim(0.00, 100.0)
    ax.set_ylim(0.00, 100.0)
    ax.set_zlim(0.00, 100.0)
    ax.set_title(f'Code Test Evaluation Metrics ({args.model_name})')
    ax.set_xlabel('Line coverage (%)')
    ax.set_ylabel('Branch coverage (%)')
    ax.set_zlabel('Pass rate (%)')
    plt.tight_layout()
    plt.show()
    fig.savefig(save_path)


if __name__ == '__main__':
    args = parse_arguments()
    main()
    # python scripts/plot_data.py
