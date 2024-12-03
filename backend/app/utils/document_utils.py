import os
import glob

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# save the .md file
def save_md_file(markdown_content: str):
    with open(f"{OUTPUT_DIR}/output.md", "w") as file:
        file.write(markdown_content)

# clean the temporary storage
def clean_temp_storage(folder_path: str):
    for file_path in glob.glob(os.path.join(folder_path, "*")):
        os.remove(file_path)