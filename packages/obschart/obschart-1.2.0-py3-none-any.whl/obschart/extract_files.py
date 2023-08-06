import io
from typing import Dict, List


def is_extractable_file(thing):
    return isinstance(thing, io.IOBase)


def extract_files(value, path=""):
    clone = None
    files: Dict[io.BufferedReader, List[str]] = dict()

    def add_file(paths, file):
        storedPaths = files.get(file, [])
        if storedPaths:
            storedPaths.extend(paths)
        else:
            files[file] = paths

    if is_extractable_file(value):
        clone = None
        add_file([path], value)
    else:
        prefix = ""
        if path:
            prefix = f"{path}."

        if isinstance(value, list):
            clone = list()
            for index, child in enumerate(value):
                child_clone, child_files = extract_files(child, f"{prefix}{index}")
                clone.append(child_clone)
                for file, paths in child_files.items():
                    add_file(paths, file)
        elif isinstance(value, dict):
            clone = dict()
            for index in value.keys():
                child = value[index]
                child_clone, child_files = extract_files(child, f"{prefix}{index}")
                clone[index] = child_clone
                for file, paths in child_files.items():
                    add_file(paths, file)
        else:
            clone = value

    return (clone, files)
