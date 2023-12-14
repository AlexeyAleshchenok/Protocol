"""
author: Alexey Aleshchenok
date: 2023-12-05
List of server's function:
* dir_cmd - returns the contents of a specific folder,
* delete_cmd - deletes a specific file from a folder,
* copy_cmd - tries to copy one file to another and return success/fail,
* execute_cmd - executes passed program and return success/fail,
* take_screenshot_cmd - takes screenshot and return it,
* exit_cmd - breaks the connection with the client
"""
import os
import shutil
import subprocess
import pyscreenshot


def dir_cmd(request):
    """gets path to the file and returns data from it """
    try:
        request = request.decode()
        directory = os.listdir(r'' + request)
        return '\n'.join(directory).encode()
    except FileNotFoundError as err:
        return f'File not found: {err}'.encode()


def delete_cmd(request):
    """gets path to the file and deletes it"""
    try:
        file_to_delete = request.decode()
        os.remove(r'' + file_to_delete)
        return "File was successfully deleted".encode()
    except FileNotFoundError as err:
        return f'File not found: {err}'.encode()


def copy_cmd(request):
    """gets line with two paths to files separated by comma and copy data from first to second"""
    try:
        files = request.decode().split(',')
        shutil.copy(files[0], files[1])
        return f"{files[0]} was copied successfully to {files[1]}".encode()
    except FileNotFoundError as err:
        return f'File not found: {err}'.encode()


def execute_cmd(request):
    """gets name of the program and try to execute it"""
    try:
        program = request.decode()
        subprocess.call(program)
        return f'{program} was executed successfully'.encode()
    except FileNotFoundError as err:
        return f'File not found: {err}'.encode()


def take_screenshot_cmd():
    """takes screenshot, saves it to 'screenshot.jpg' and returns it as bytes"""
    screenshot_path = 'screenshot.jpg'
    image = pyscreenshot.grab()
    image.save(screenshot_path)
    try:
        with open(screenshot_path, 'rb') as screen:
            screenshot_data = screen.read()
    except os.error as err:
        return f'File {screenshot_path} not found: {err}'.encode()
    return screenshot_data


def exit_cmd():
    """returns 'Bye' message"""
    return 'Bye'.encode()
