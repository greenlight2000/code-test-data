import os
import argparse
import pandas as pd

from pathlib import Path
from datasets import load_from_disk


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--codes_dir_name', default='palm_codes',
                        choices=['raw_codes', 'human_1_codes', 'human_2_codes', 'human_3_codes', 'human_4_codes',
                                 'human_5_codes', 'palm_codes', 'gpt3_codes', 'gpt4_codes'],
                        type=str)
    parser.add_argument('--temp_load_name', default='palm_data',
                        choices=['raw_data', 'human_1_data', 'human_2_data', 'human_3_data', 'human_4_data',
                                 'human_5_data', 'palm_data', 'gpt3_data', 'gpt4_data'],
                        type=str)
    parser.add_argument('--filter', action='store_true', default=False)
    parser.add_argument('--temp_save_name', default='temp_data', choices=['temp_data'], type=str)
    parser.add_argument('--final_save_name', default='code_test_eval_palm.jsonl',
                        choices=['code_test_eval_human_1.jsonl', 'code_test_eval_human_2.jsonl',
                                 'code_test_eval_human_3.jsonl', 'code_test_eval_human_4.jsonl',
                                 'code_test_eval_human_5.jsonl', 'code_test_eval_palm.jsonl',
                                 'code_test_eval_gpt3.jsonl', 'code_test_eval_gpt4.jsonl'],
                        type=str)
    args = parser.parse_args()

    return args


def add_coverage(example):
    lang_cluster = example['lang_cluster']
    code_uid = example['code_uid']
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    num_hidden_unit_tests = len(hidden_unit_tests)

    # LLM failed to generate hidden unit tests
    if num_hidden_unit_tests == 0:
        print('Failed to generate hidden unit tests:', code_uid)
        example['line_coverage'] = 0.00
        example['branch_coverage'] = 0.00
    else:
        if lang_cluster == 'C':
            os.chdir(f'codes/{args.codes_dir_name}/c/{code_uid}')
            print(os.getcwd())

            try:
                coverage_data = pd.read_json('coverage.json')
                line_covered = coverage_data.loc[0, 'line_covered']
                line_total = coverage_data.loc[0, 'line_total']
                if line_total == 0:
                    line_coverage = 100.00
                else:
                    line_coverage = round(100. * line_covered / line_total, 2)
                branch_covered = coverage_data.loc[0, 'branch_covered']
                branch_total = coverage_data.loc[0, 'branch_total']
                if branch_total == 0:
                    branch_coverage = 100.00
                else:
                    branch_coverage = round(100. * branch_covered / branch_total, 2)
            except Exception as e:
                print('Error occurred while reading the JSON file:', e)
                line_coverage = 0.00
                branch_coverage = 0.00

            print(f'Line Coverage: {line_coverage}%')
            print(f'Branch Coverage: {branch_coverage}%')

            os.chdir('../../../..')
            print(os.getcwd())

            example['line_coverage'] = line_coverage
            example['branch_coverage'] = branch_coverage

        elif lang_cluster == 'C++':
            os.chdir(f'codes/{args.codes_dir_name}/cpp/{code_uid}')
            print(os.getcwd())

            try:
                coverage_data = pd.read_json('coverage.json')
                line_covered = coverage_data.loc[0, 'line_covered']
                line_total = coverage_data.loc[0, 'line_total']
                if line_total == 0:
                    line_coverage = 100.00
                else:
                    line_coverage = round(100. * line_covered / line_total, 2)
                branch_covered = coverage_data.loc[0, 'branch_covered']
                branch_total = coverage_data.loc[0, 'branch_total']
                if branch_total == 0:
                    branch_coverage = 100.00
                else:
                    branch_coverage = round(100. * branch_covered / branch_total, 2)
            except Exception as e:
                print('Error occurred while reading the JSON file:', e)
                line_coverage = 0.00
                branch_coverage = 0.00

            print(f'Line Coverage: {line_coverage}%')
            print(f'Branch Coverage: {branch_coverage}%')

            os.chdir('../../../..')
            print(os.getcwd())

            example['line_coverage'] = line_coverage
            example['branch_coverage'] = branch_coverage

        elif lang_cluster == 'Java':
            os.chdir(f'codes/{args.codes_dir_name}/java/{code_uid}')
            print(os.getcwd())

            try:
                coverage_data = pd.read_csv('coverage.csv')
                line_covered = coverage_data.loc[0, 'LINE_COVERED']
                line_missed = coverage_data.loc[0, 'LINE_MISSED']
                line_total = line_covered + line_missed
                if line_total == 0:
                    line_coverage = 100.00
                else:
                    line_coverage = round(100. * line_covered / line_total, 2)
                branch_covered = coverage_data.loc[0, 'BRANCH_COVERED']
                branch_missed = coverage_data.loc[0, 'BRANCH_MISSED']
                branch_total = branch_covered + branch_missed
                if branch_total == 0:
                    branch_coverage = 100.00
                else:
                    branch_coverage = round(100. * branch_covered / branch_total, 2)
            except Exception as e:
                print('Error occurred while reading the CSV file:', e)
                line_coverage = 0.00
                branch_coverage = 0.00

            print(f'Line Coverage: {line_coverage}%')
            print(f'Branch Coverage: {branch_coverage}%')

            os.chdir('../../../..')
            print(os.getcwd())

            example['line_coverage'] = line_coverage
            example['branch_coverage'] = branch_coverage

        elif lang_cluster == 'Python':
            os.chdir(f'codes/{args.codes_dir_name}/python/{code_uid}')
            print(os.getcwd())

            try:
                coverage_data = pd.read_json('coverage.json')
                line_covered = int(coverage_data.loc['covered_lines', 'totals'])
                line_missed = int(coverage_data.loc['missing_lines', 'totals'])
                line_total = line_covered + line_missed
                if line_total == 0:
                    line_coverage = 100.00
                else:
                    line_coverage = round(100. * line_covered / line_total, 2)
                branch_covered = int(coverage_data.loc['covered_branches', 'totals'])
                branch_missed = int(coverage_data.loc['missing_branches', 'totals'])
                branch_total = branch_covered + branch_missed
                if branch_total == 0:
                    branch_coverage = 100.00
                else:
                    branch_coverage = round(100. * branch_covered / branch_total, 2)
            except Exception as e:
                print('Error occurred while reading the JSON file:', e)
                line_coverage = 0.00
                branch_coverage = 0.00

            print(f'Line Coverage: {line_coverage}%')
            print(f'Branch Coverage: {branch_coverage}%')

            os.chdir('../../../..')
            print(os.getcwd())

            example['line_coverage'] = line_coverage
            example['branch_coverage'] = branch_coverage

    return example


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path(args.temp_load_name)
    if args.filter:
        save_path = Path(__file__).parent.parent / Path('data') / Path(args.temp_save_name)
    else:
        save_path = Path(__file__).parent.parent / Path('results') / Path(args.final_save_name)

    dataset = load_from_disk(str(load_path))
    print(dataset)

    dataset = dataset.map(add_coverage)
    print(dataset)

    if args.filter:
        dataset.save_to_disk(save_path)
    else:
        dataset.to_json(save_path, lines=True)


if __name__ == '__main__':
    args = parse_arguments()
    main()
    # python scripts/cover_codes.py
