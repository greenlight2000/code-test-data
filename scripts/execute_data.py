from pathlib import Path
from datasets import load_from_disk

from api_comm import APICommunication, ExtendedUnittest


def get_runtimes():
    api = APICommunication()
    response = api.get_runtimes()

    return response


def search_runtime(runtime_name):
    runtimes = get_runtimes()
    result = {
        'compile_cmd': None,
        'compile_flags': None,
        'execute_cmd': None,
        'execute_flags': None,
        'has_sanitizer': None,
        'is_compiled': None,
        'runtime_name': None,
        'timelimit_factor': None
    }
    for runtime in runtimes:
        if runtime['runtime_name'] == runtime_name:
            result = runtime
            break

    return result


def execute_code(language, source_code, unittests, compile_cmd, compile_flags, execute_cmd, execute_flags):
    api = APICommunication()
    response = api.execute_code(
        language=language,
        source_code=source_code,
        unittests=unittests,
        compiler_program_name=compile_cmd,
        compiler_flags=compile_flags,
        interpreter_cmd=execute_cmd,
        interpreter_flags=execute_flags
    )
    print(response)

    exec_outcomes = []
    results = []
    response_datas = response[0]

    if isinstance(response_datas, list):
        for response_data in response_datas:
            exec_outcomes.append(response_data['exec_outcome'])
            results.append(response_data['result'])
    else:
        exec_outcomes.append('UNKNOWN_ERROR')
        results.append('')

    return exec_outcomes, results


def add_execute(example):
    language = example['lang']
    source_code = example['source_code']
    hidden_unit_tests = eval(example['hidden_unit_tests'])

    runtime = search_runtime(language)
    compile_cmd = runtime['compile_cmd']
    compile_flags = runtime['compile_flags']
    execute_cmd = runtime['execute_cmd']
    execute_flags = runtime['execute_flags']

    unittests = []
    for unit_test_case in hidden_unit_tests:
        unittests.append(
            ExtendedUnittest(
                input=unit_test_case['input'],
                output=unit_test_case['output']
            ).json()
        )

    exec_outcomes, results = execute_code(language, source_code, unittests, compile_cmd, compile_flags, execute_cmd,
                                          execute_flags)
    print(exec_outcomes)
    print(results)

    if all(exec_outcome == 'PASSED' for exec_outcome in exec_outcomes):
        example['all_passed'] = 1
    else:
        example['all_passed'] = 0

    # Python 3 compiler has some bugs
    if language == 'Python 3':
        example['all_passed'] = 1

    return example


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path('lang_code_translation')
    save_path = Path(__file__).parent.parent / Path('data') / Path('exec_code_translation')

    dataset = load_from_disk(str(load_path))
    print(dataset)

    dataset = dataset.map(add_execute)
    print(dataset)

    dataset.save_to_disk(save_path)


if __name__ == '__main__':
    main()
