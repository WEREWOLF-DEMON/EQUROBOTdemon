import glob
from os.path import dirname, isfile, join

def __list_all_modules():
    work_dir = dirname(__file__)
    # Use join for cross-platform compatibility
    mod_paths = glob.glob(join(work_dir, "**", "*.py"), recursive=True)

    all_modules = [
        ((f.replace(work_dir, "").replace("\\", ".").replace("/", "."))[:-3])
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    # Clean up the leading dot if the module is directly in the work_dir
    all_modules = [mod.lstrip('.') for mod in all_modules]

    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
