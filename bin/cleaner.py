import logging
import os

def clean_directory(directory):
    logging.info("Cleaning directory: {} ...".format(os.path.abspath(directory)))
    # delete images
    counter = 0
    for file in os.listdir(directory):
        if file != ".gitignore":
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    counter += 1
            except Exception as e:
                print(e)
    logging.info("Deleted {} files.".format(counter))


directories = ["tmp"]

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    for direc in directories:
        clean_directory(direc)