from tqdm import tqdm
from pathlib import Path
from datasets import load_dataset


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path('code_test_data.json')
    codes_dir = Path(__file__).parent.parent / Path('codes')
    if not codes_dir.is_dir():
        codes_dir.mkdir(parents=True, exist_ok=True)
    python_dir = codes_dir / Path('python')
    if not python_dir.is_dir():
        python_dir.mkdir(parents=True, exist_ok=True)
    java_dir = codes_dir / Path('java')
    if not java_dir.is_dir():
        java_dir.mkdir(parents=True, exist_ok=True)

    code_test_dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(code_test_dataset)

    for example in tqdm(code_test_dataset):
        code_uid = example['code_uid']
        lang_cluster = example['lang_cluster']
        source_code = example['source_code']

        if lang_cluster == 'Python':
            file_path = python_dir / Path(f'{code_uid}.py')
        elif lang_cluster == 'Java':
            file_path = java_dir / Path(f'{code_uid}.java')

        with open(file_path, mode='w') as file:
            file.write(source_code)


if __name__ == '__main__':
    main()
