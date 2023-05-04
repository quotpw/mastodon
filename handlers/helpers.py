import datetime
import os
import random
import re


def set_console_title(title):
    """
    Set the title of the console window.

    Parameters:
        title (str): The new title for the console window.
    """
    if os.name == "nt":
        # For Windows
        os.system("title " + title)
    else:
        # For other platforms, such as Linux or macOS
        print("\033]0;" + title + "\a", end="", flush=True)


def default_input(value, default_value):
    result = input(value + f" [{default_value}]: ")
    if result == "":
        return default_value
    return type(default_value)(result)


def create_save_path(name):
    time_now = datetime.datetime.now()
    return f"results/{name}/{time_now.year}-{time_now.month}-{time_now.day}_{time_now.hour}-{time_now.minute}-{time_now.second}/"


def append_to_file(save_path, file_name, data):
    # create dir tree if not exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(save_path + file_name, "a") as file:
        file.write(data + "\n")


def get_png_files_as_bytes(dir_path):
    """
    Get all PNG files in the specified directory and return them as a list of bytes arrays.

    Parameters:
        dir_path (str): The path of the directory to search for PNG files.

    Returns:
        list: A list of bytes arrays, where each bytes array represents the contents of a PNG file.
    """
    png_files = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".png"):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, "rb") as f:
                png_files.append(f.read())
    return png_files


def randomize_text(text):
    """
    Randomize the text in spintax format.

    Parameters:
        text (str): The text in spintax format to be randomized.

    Returns:
        str: The randomized text.
    """

    def replace(match):
        options = match.group(1).split("|")
        return random.choice(options)

    pattern = re.compile(r"\{([^{}]*)\}")
    while pattern.search(text):
        text = pattern.sub(replace, text)
    return text
