import utils
import os
import pdb

if __name__ == '__main__':
    # Gather directory names
    root_path = os.path.dirname(os.path.realpath(__file__))
    recipe_load_path = os.path.join(root_path, "recipes")
    method_load_path = os.path.join(root_path, "methods")
    recipes_path = os.path.join(root_path, "docs/_recipes")
    categories_path = os.path.join(root_path, "docs/_categories")
    methods_path = os.path.join(root_path, "docs/_methods")
    img_path = os.path.join(root_path, "docs/img/categories")

    # Empty current files, we will rebuild all
    all_recipes = os.listdir(recipes_path)
    all_categories = os.listdir(categories_path)
    all_methods = os.listdir(methods_path)
    print('Removing all recipes, categories, and methods.')
    for recipe in all_recipes:
        os.remove(os.path.join(recipes_path, recipe))

    for cat in all_categories:
        os.remove(os.path.join(categories_path, cat))

    for method in all_methods:
        os.remove(os.path.join(methods_path, method))

    # Find all recipe files in the recipes directory
    recipe_load_paths = []
    for file in os.listdir(recipe_load_path):
        if file.endswith(".txt"):
            recipe_load_paths.append(os.path.join(recipe_load_path, file))
        else:
            print('Skipping file {}'.format(file))

    tags = []
    methods = []
    # Load each recipe
    for path in recipe_load_paths:
        recipe = utils.load_recipe(path)
        utils.write_recipe_md(recipe, recipes_path)

        # Add new categories to array
        for tag in recipe["tags"]:
            if tag not in tags:
                if tag != '':
                    tags.append(tag)
                # elif tag == '' and 'default' not in tags:
                #     tags.append('default')

        # Add new methods to array
        for tag in recipe["method_tags"]:
            if tag not in methods:
                methods.append(tag)
                

    # Create category file for each tag
    needed = []
    for tag in tags:
        need = utils.write_category_md(tag, categories_path, img_path)
        if need:
            needed.append(need)

    if needed:
        print('\nNeed the following category images:')
        for need in needed:
            print('{}.(jpg/png)'.format(need))


    # Create method file for each method
    method_load_paths = []
    for file in os.listdir(method_load_path):
        if file.endswith(".yml"):
            method_load_paths.append(os.path.join(method_load_path, file))
        else:
            print('Skipping file {}'.format(file))

    # Load each method
    for path in method_load_paths:
        method = utils.load_method(path)
        utils.write_method_md(method, methods_path, img_path)


    