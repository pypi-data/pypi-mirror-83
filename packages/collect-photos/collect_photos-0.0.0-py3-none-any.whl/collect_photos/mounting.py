import os
import string
from os import listdir
from os.path import isfile, join


class Mounting:
    files = []
    path: string

    def __init__(self, path: string):
        if path != ".":
            if path[len(path) - 1] != "/":
                self.working_directory = path + "/"
            else:
                self.working_directory = path
        else:
            self.working_directory = ""
        self.path = path

    def list_files_in_directory(self, path=None):
        # Set Path
        if path is None:
            path = self.path
        # Recursive Go through Sub Directories
        list_result = []
        for directory, sub_directory, files in os.walk(path):
            list_result = list_result + [(directory[len(self.path):] + "/" + item) for item in files]
        # Reformat File Name
        list_result = [(item[1:] if item[0] == '/' else item) for item in list_result]
        return list_result
