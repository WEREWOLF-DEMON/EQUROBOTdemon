import glob
import importlib
from os.path import basename, dirname, isfile

def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    all_modules = [
        (basename(f)[:-3], f)  # Return both the module name and file path
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    return all_modules

ALL_MODULES = sorted(__list_all_modules())

# Import modules and display their file paths
for module_name, file_path in ALL_MODULES:
    print(f"Importing module: {module_name} from file: {file_path}")
    importlib.import_module("EQUROBOT.modules." + module_name)

__all__ = [module_name for module_name, _ in ALL_MODULES] + ["ALL_MODULES"]
