import warnings
import numpy as np
from pathlib import Path
from datasets import load_dataset


def main():
    supported_llms = ['Human', 'PaLM', 'GPT-3.5', 'GPT-4']
    supported_lang_clusters = ['C', 'C++', 'Java', 'Python']
    load_name_llms = ['code_test_eval_human.jsonl', 'code_test_eval_palm.jsonl', 'code_test_eval_gpt3.jsonl',
                      'code_test_eval_gpt4.jsonl']

    for index1, load_name_llm in enumerate(load_name_llms):
        load_path_llm = Path(__file__).parent.parent / Path('results') / Path(load_name_llm)

        dataset_llm = load_dataset('json', split='train', data_files=str(load_path_llm))
        print(dataset_llm)

        lang_cluster_dataset_llms = [
            dataset_llm.filter(lambda example: example['lang_cluster'] == lang_cluster)
            for lang_cluster in supported_lang_clusters
        ]

        print('+' + '——' * 25 + '+')
        print(supported_llms[index1] + ':')
        print('+' + '——' * 25 + '+')
        evaluation_metrics = []
        for index2 in range(len(supported_lang_clusters)):
            print('+' + '-' * 50 + '+')
            print(supported_lang_clusters[index2] + ':')
            print('+' + '-' * 50 + '+')

            lang_cluster_dataset_llm = lang_cluster_dataset_llms[index2]

            pass_rate = round(float(np.mean(lang_cluster_dataset_llm['pass_rate'])), 2)
            evaluation_metrics.append(pass_rate)
            print('average pass rate:', pass_rate)

            line_coverage = round(float(np.mean(lang_cluster_dataset_llm['line_coverage'])), 2)
            evaluation_metrics.append(line_coverage)
            print('average line coverage:', line_coverage)

            branch_coverage = round(float(np.mean(lang_cluster_dataset_llm['branch_coverage'])), 2)
            evaluation_metrics.append(branch_coverage)
            print('average branch coverage:', branch_coverage)

        print('evaluation metrics:', evaluation_metrics)
        overall_score = round(float(np.mean(evaluation_metrics)), 2)
        print('+' + '-' * 50 + '+')
        print('overall score:', overall_score)
        print('+' + '-' * 50 + '+')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    main()
