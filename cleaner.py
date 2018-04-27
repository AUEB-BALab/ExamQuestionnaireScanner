import os

def clean_directory(directory):
    print("## Cleaning directory {}".format(directory), flush=True)
    # delete images
    for file in os.listdir(directory):
        if file != ".gitignore":
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


directories = ["questionnaire_images",
                "formscanner_csv",
                "scan_to_csv"]

for direc in directories:
    clean_directory(direc)