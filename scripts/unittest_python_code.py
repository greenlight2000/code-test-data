import subprocess

from pathlib import Path
from datasets import load_dataset


def execute_command(command, input=None):
    if input is not None:
        input = input.replace('\r\n', '\n')
    outcome = subprocess.run(command, input=input, capture_output=True, text=True, timeout=20, shell=True)

    return outcome


def add_unit_test_metrics(example):
    code_uid = example['code_uid']
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    print(hidden_unit_tests)
    num_hidden_unit_tests = len(hidden_unit_tests)

    num_passed = 0
    test_command = f'python ../codes/python/{code_uid}.py'
    coverage_command = f'coverage run ../codes/python/{code_uid}.py'
    coverage_append_command = f'coverage run -a ../codes/python/{code_uid}.py'

    for index, unit_test_case in enumerate(hidden_unit_tests):
        input = unit_test_case['input']
        output = unit_test_case['output']
        # TODO:在output里面就把/n去掉
        outcome = execute_command(test_command, input)
        print(outcome)

        is_passed = True if outcome.returncode == 0 and (
                outcome.stdout in output or outcome.stdout.rstrip() in output or outcome.stdout.replace('\n',
                                                                                                        '\r\n') in output or outcome.stdout.replace(
            '\n', '\r\n').rstrip() in output) else False
        print(is_passed)
        if is_passed is True:
            num_passed += 1

        if index == 0:
            execute_command(coverage_command, input)
        else:
            execute_command(coverage_append_command, input)

    pass_rate = round(100. * num_passed / num_hidden_unit_tests, 2)
    print(f'Pass rate: {pass_rate}% [{num_passed}/{num_hidden_unit_tests}]')

    coverage_report_text_command = 'coverage report -m --precision=2'
    execute_command(coverage_report_text_command)
    coverage_report_total_command = 'coverage report --format=total --precision=2'
    outcome = execute_command(coverage_report_total_command)

    try:
        statement_coverage = float(outcome.stdout.rstrip())
    except ValueError:
        statement_coverage = 0.00

    print(f'Statement Coverage: {statement_coverage}%')

    example['pass_rate'] = pass_rate
    example['statement_coverage'] = statement_coverage

    return example


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path('code_test_data.json')

    code_test_dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(code_test_dataset)

    python_code_test_dataset = code_test_dataset.filter(lambda example: example['lang_cluster'] == 'Python')
    print(python_code_test_dataset)

    python_code_test_dataset = python_code_test_dataset.map(add_unit_test_metrics)
    print(python_code_test_dataset)

    print(python_code_test_dataset['pass_rate'])
    print(python_code_test_dataset['statement_coverage'])


if __name__ == '__main__':
    main()
