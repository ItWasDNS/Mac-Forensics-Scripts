"""
    Handle directory paths for Mac Scripts
"""

import os

warning = "Directory already exists. Continuing could overwrite existing data."


def process_directory_paths():
    """ Process directory paths """
    while True:
        database = input("Enter path to database to process: ")
        if os.path.exists(database):
            break
        else:
            print("Database does not exist. Please try again.")

    while True:
        output_path = input("Enter output directory: ")
        if os.path.exists(output_path):
            print(warning)
            advance = input("Do you wish to continue (y/n): ")
            if advance.strip().lower() == 'y':
                break
        else:
            os.mkdir(output_path)
            break

    return database, output_path
