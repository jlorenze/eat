import utils
import os
import pdb

if __name__ == '__main__':
    # Gather directory names
    root_path = os.path.dirname(os.path.realpath(__file__))
    load_path = os.path.join(root_path, "recipes")
    recipes_path = os.path.join(root_path, "docs/_recipes")
    categories_path = os.path.join(root_path, "docs/_categories")
    img_path = os.path.join(root_path, "docs/img/categories")

    # Empty current files, we will rebuild all
    all_recipes = os.listdir(recipes_path)
    all_categories = os.listdir(categories_path)
    print('Removing all recipes and categories.')
    for recipe in all_recipes:
        os.remove(os.path.join(recipes_path, recipe))

    for cat in all_categories:
        os.remove(os.path.join(categories_path, cat))

    # Find all recipe files in the recipes directory
    load_paths = []
    for file in os.listdir(load_path):
        if file.endswith(".txt"):
            load_paths.append(os.path.join(load_path, file))
        else:
            print('Skipping file {}'.format(file))

    tags = []
    # Load each recipe
    for path in load_paths:
        recipe = utils.load_recipe(path)
        utils.write_recipe_md(recipe, recipes_path)

        # Add new categories to array
        for tag in recipe["tags"]:
            if tag not in tags:
                tags.append(tag)

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

    