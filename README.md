<a name="teDHI"></a>
# Step 1: Installation
1. Make sure you run this program in Windows system.
2. Install GCC: [mingw-w64](https://sourceforge.net/projects/mingw-w64/files/mingw-w64/mingw-w64-release/)
3. Install Java 8: [java8](https://www.oracle.com/java/technologies/downloads/#java8-windows)
4. Install Python 3: [python3](https://www.python.org/downloads/windows/)
5. Install Docker: [docker](https://docs.docker.com/desktop/install/windows-install/)
6. Clone ExecEval project: `git clone [https://github.com/ntunlp/ExecEval.git](https://github.com/ntunlp/ExecEval.git)`
7. Enter ExecEval project directory: `cd ExecEval`
8. Build Docker image: `docker build . -t exec-eval:1.0`
9. Run Docker image: `docker run -it -p 5000:5000 -e NUM_WORKERS=5 exec-eval:1.0`
10. Clone the project: `git clone [https://github.com/Haitianboom/code-test-data.git](https://github.com/Haitianboom/code-test-data.git)`
11. Enter the project directory: `cd code-test-data`
12. Install the requirements: `pip install -r requirements.txt`
<a name="YrAD1"></a>
# Step 2: Run

1. Extract data that supports four programming language (C, C++, Java and Python) from raw data and add two features (`length` and `num_hidden_unit_tests`) for each extracted data: `python scripts/process_data.py`
2. Execute source codes with all hidden unit test cases, count execution results and add feature `all_passed` for each raw extracted data: `python scripts/execute_data.py`
3. Filter out raw extracted data that does not pass all hidden unit test cases: `python scripts/filter_data.py`
4. Save source codes from raw filtered data: `python scripts/save_codes.py --code_test_data_name code_test_data_raw.jsonl --codes_dir_name raw_codes`
5. Test source codes with all hidden unit test cases, generate files containing coverage, count pass rate and add feature `pass_rate` for each raw filtered data : `python scripts/test_codes.py --code_test_data_name code_test_data_raw.jsonl --codes_dir_name raw_codes --temp_save_name raw_data`
6. Read files containing coverage, count line coverage and branch coverage, add two features (`line_coverage` and `branch_coverage`) for each raw temp data: `python scripts/cover_codes.py --codes_dir_name raw_codes --temp_load_name raw_data --filter --temp_save_name temp_data`
7. Filter out raw temp data with pass rate, line coverage or branch coverage less than 100%: `python scripts/filter_codes.py`
8. Repeat step 4 to 6 to test LLM data.
<a name="fshsa"></a>
# Structure
<a name="sWMbk"></a>
## codes
This directory stores the code files.
<a name="KWs4A"></a>
## data
This directory stores the temp datasets.
<a name="ojcaT"></a>
## jars
This directory stores the JaCoCo dependency jars.
<a name="ZHKWO"></a>
## results
This directory stores the final results.
<a name="XioaF"></a>
## scripts
This directory stores the script source code.
<a name="JGiER"></a>
# Reference

1. [https://github.com/ntunlp/xCodeEval](https://github.com/ntunlp/xCodeEval)
2. [https://github.com/ntunlp/ExecEval](https://github.com/ntunlp/ExecEval)
3. [https://huggingface.co/datasets/NTU-NLP-sg/xCodeEval](https://huggingface.co/datasets/NTU-NLP-sg/xCodeEval)
4. [https://arxiv.org/abs/2303.03004](https://arxiv.org/abs/2303.03004)
5. [https://github.com/ZJU-ACES-ISE/ChatUniTest](https://github.com/ZJU-ACES-ISE/ChatUniTest)
6. [https://arxiv.org/abs/2305.04764](https://arxiv.org/abs/2305.04764)
7. [https://gcovr.com/en/stable/](https://gcovr.com/en/stable/)
8. [https://coverage.readthedocs.io/en/7.3.0/](https://coverage.readthedocs.io/en/7.3.0/)
9. [https://www.eclemma.org/jacoco/trunk/doc/agent.html](https://www.eclemma.org/jacoco/trunk/doc/agent.html)
10. [https://www.eclemma.org/jacoco/trunk/doc/cli.html](https://www.eclemma.org/jacoco/trunk/doc/cli.html)
11. [https://blog.51cto.com/u_13280061/3083744](https://blog.51cto.com/u_13280061/3083744)
12. [https://codeantenna.com/a/2BsM2BlZQc](https://codeantenna.com/a/2BsM2BlZQc)
13. [https://www.nerd.vision/post/jacoco-coverage-of-util-classes](https://www.nerd.vision/post/jacoco-coverage-of-util-classes)
14. [https://www.ibm.com/docs/en/developer-for-zos/14.2?topic=coverage-frequently-asked-questions-about-java-code](https://www.ibm.com/docs/en/developer-for-zos/14.2?topic=coverage-frequently-asked-questions-about-java-code)
15. [https://www.cnblogs.com/robothy/p/11997759.html](https://www.cnblogs.com/robothy/p/11997759.html)
16. [https://lihuia.com/jacoco%EF%BC%9A%E4%BB%A3%E7%A0%81%E8%A6%86%E7%9B%96%E7%8E%87%E6%B5%8B%E8%AF%95/](https://lihuia.com/jacoco%EF%BC%9A%E4%BB%A3%E7%A0%81%E8%A6%86%E7%9B%96%E7%8E%87%E6%B5%8B%E8%AF%95/)
