import os
import glob

# clean the temporary storage
def clean_temp_storage(folder_path: str):
    for file_path in glob.glob(os.path.join(folder_path, "*")):
        os.remove(file_path)