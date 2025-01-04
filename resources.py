import os
def save_to_csv_file(total_text, file_path):
    csv_file_path = file_path
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, "w", encoding="utf-8") as file:
        file.write(total_text)
    print(csv_file_path)


def read_text_file(file_path):
    # Specify the path to your text file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content