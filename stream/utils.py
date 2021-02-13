import os
from datetime import datetime
from urllib.parse import urlparse


def store_image(data, path, image_name):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    file_path = os.path.join(path, image_name)
    try:
        image_file = open(file_path, 'w+b')
        image_file.write(data)
    except IOError:
        print("Saving image failed.")
    finally:
        image_file.close()

def generate_snapshot_file_name():
    """
    Generates a name based on system time.
    """
    now = datetime.now()
    return now.strftime("%d-%m-%Y-%H_%M_%S")

def validate_url(url, scheme):
    result = urlparse(url)
    return result.scheme == scheme
