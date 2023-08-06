import sys

from unify_package.replace_custom_color_with_unify import replace_custom_color_with_unify
from unify_package.replace_hardcode_color_with_unify import replace_hardcode_color_with_unify
from unify_package.replace_neutral_to_unify_new import replace_neutral_with_unify


def replace_color(project_path, module_path):
    module_path = project_path + module_path
    count = 0
    count = count + replace_neutral_with_unify(module_path)
    count = count + replace_custom_color_with_unify(module_path)
    count = count + replace_hardcode_color_with_unify(module_path)
    print(module_path + ": " + str(count) + " file changes")


if __name__ == "__main__":
    replace_color(sys.argv[1], sys.argv[2])