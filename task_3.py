import os


DIR_NAME = 'sorted'
RESULT_FILE_NAME = 'result.txt'


def merge_files_in_directory(dir_path: str, result_file_name: str) -> None:
    for parent_path, _, files in os.walk(dir_path):
        print(f"Dir name: {parent_path}")
        print(f"Files for merge: {files}")
        files_content = []
        for file_name in files:
            file_path = os.path.join(parent_path, file_name)
            with open(file_path, encoding='utf-8') as file:
                content = list(map(lambda l: l.strip(' \n'), file.readlines()))
                files_content.append((len(content), file_name, content))

        files_content.sort()
        with open(result_file_name, 'w', encoding='utf-8') as new_file:
            for item in files_content:
                lines_num, file_name, content = item[0], item[1], item[2]
                new_file.write(file_name + '\n')
                new_file.write(str(lines_num) + '\n')
                for line in content:
                    new_file.write(line + '\n')
        print(f'Files successfully merged into "{result_file_name}".')


merge_files_in_directory(DIR_NAME, RESULT_FILE_NAME)
