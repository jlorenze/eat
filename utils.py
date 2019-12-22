import sys
import pdb
import os

def load_recipe(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    recipe = {}
    # Title
    recipe["title"] = lines[0].strip()

    # Yield
    i = 1
    while 'yield' not in lines[i].lower():
        i += 1
    yield_val =  lines[i].split(':')[-1].strip().lower()
    if yield_val == '':
        recipe["yield"] = []
    else:
        recipe["yield"] = yield_val

    # Time
    i = 1
    while 'time' not in lines[i].lower():
        i += 1
    time = lines[i].split(':')[-1].strip().lower()
    if time == '':
        recipe["time"] = []
    else:
        recipe["time"] = time

    # Keywords
    i = 1
    while 'keywords' not in lines[i].lower() or 'keyword' not in lines[i].lower():
        i += 1
    keywords = lines[i].split(':')[1].split(',')
    if len(keywords) == 1 and keywords[0] == '\n':
        recipe["tags"] = []
    else:
        recipe["tags"] = [keyword.strip().lower() for keyword in keywords]

    # Recommended sides
    i = 1
    while 'recommended' not in lines[i].lower() or 'sides' not in lines[i].lower():
        i += 1
    sides = lines[i].split(':')[1].split(',')
    if len(sides) == 1 and sides[0] == '\n':
        recipe["pairs"] = []
    else:
        recipe["pairs"] = [side.strip().lower() for side in sides]

    # Ingredients
    i = 1
    while 'ingredients' not in lines[i].lower():
        i += 1

    ingredients = []
    i += 1
    while lines[i].lower() != '\n':
        ingredients.append(lines[i].strip())
        i += 1
    recipe["ingredients"] = ingredients

    # Instructions
    i = 1
    while 'make' not in lines[i].lower():
        i += 1

    make = []
    i += 1
    while i < len(lines) and lines[i].lower() != '\n':
        make_item = '.'.join(lines[i].strip().strip('.').split('.')[1:])
        make.append(make_item.strip(' '))
        i += 1
    recipe["make"] = make

    return recipe


def write_recipe_md(recipe, rec_dir):
    name = ''.join([recipe["title"].replace(' ', '-'), '.md'])
    filename = os.path.join(rec_dir, name)

    print('Generating recipe {}'.format(name))

    # Start writing file
    with open(filename, 'w') as file:
        file.write('---\n')
        file.write('layout: recipe\n')

        if not recipe["yield"]:
            file.write('yield: {}\n'.format(''))
        else:
            file.write('yield: {}\n'.format(recipe["yield"]))

        if not recipe["time"]:
            file.write('time: {}\n'.format(''))
        else:    
            file.write('time: {}\n'.format(recipe["time"]))

        if recipe["tags"]:
            file.write('tags:\n')
            for tag in recipe["tags"]:
                file.write('- {}\n'.format(tag))

        if recipe["pairs"]:
            file.write('pair:\n')
            for pair in recipe["pairs"]:
                file.write('- {}\n'.format(pair))

        if recipe["ingredients"]:
            file.write('ingredients:\n')
            for item in recipe["ingredients"]:
                file.write('- {}\n'.format(item))

        if recipe["make"]:
            file.write('directions:\n')
            for instr in recipe["make"]:
                file.write('- {}\n'.format(instr))

        file.write('---\n')


def write_category_md(tag, cat_dir, img_dir):
    name = ''.join([tag, '.md'])
    filename = os.path.join(cat_dir, name)

    print('Generating category {}'.format(name))

    # Check if image exists
    pngimg_filename = os.path.join(img_dir, ''.join([tag,'.png']))
    jpgimg_filename = os.path.join(img_dir, ''.join([tag,'.jpg']))
    if os.path.exists(pngimg_filename):
        imgname = ''.join([tag,'.png'])
        needed = []
    elif os.path.exists(jpgimg_filename):
        imgname = ''.join([tag,'.jpg'])
        needed = []
    else:
        imgname = 'default.jpg'
        needed = tag

    # Start writing file
    with open(filename, 'w') as file:
        file.write('---\n')
        file.write('title: {}\n'.format(tag.title()))
        file.write('layout: default\n')

        if needed:
            file.write('img: \n')
        else:
            file.write('img: {}\n'.format(imgname))
        file.write('thumbnail: {}\n'.format(imgname))
        file.write('---\n')

    return needed

