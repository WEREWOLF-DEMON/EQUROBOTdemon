import glob
from os.path import dirname, isfile, join

def __list_all_modules():
    work_dir = dirname(__file__)
    # Use glob with recursive=True to fetch all .py files in subdirectories
    mod_paths = glob.glob(join(work_dir, "**", "*.py"), recursive=True)

    all_modules = [
        # Correctly format the module name by replacing slashes with dots for import
        ((f.replace(work_dir, "")).replace("\\", ".").replace("/", "."))[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    # Remove the leading dot from module names (in case it's at the top-level)
    all_modules = [mod.lstrip('.') for mod in all_modules]

    return all_modules

# Generate the sorted list of all modules
ALL_MODULES = sorted(__list_all_modules())

# Update __all__ to include all the module names and ALL_MODULES itself
__all__ = ALL_MODULES + ["ALL_MODULES"]
