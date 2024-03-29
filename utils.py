import sys
import pdb
import os
import yaml

def load_recipe(filename):
    """ Loads the recipe txt file and parses it, outputs a dictionary
    with all of the components of the recipe. Future work would
    be to actually switch from using txt files to using YAML files """
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
    methods = []
    method_tags = []
    i += 1
    while i < len(lines) and lines[i].lower() != '\n':
        # Split string to look for method tags in <>
        first_split = lines[i].strip().split('<')

        # Parse out the actual line instruction
        make_item = '.'.join(first_split[0].strip().strip('.').split('.')[1:])
        make.append(make_item.strip(' '))

        # Now look for method tags
        if len(first_split) > 1:
            tags = first_split[1].strip('>').split(',')
            tags = [tag.strip() for tag in tags]
            methods.append(tags)
            for tag in tags:
                if tag not in method_tags:
                    method_tags.append(tag) # running list of tags in recipe
        else:
            methods.append([]) # otherwise no tags

        i += 1
    recipe["make"] = make
    recipe["methods"] = methods
    recipe["method_tags"] = method_tags

    # Notes
    i = 1
    has_notes = True
    while 'notes' not in lines[i].lower() or 'note' not in lines[i].lower():
        i += 1
        if i >= len(lines):
            has_notes = False
            break

    notes = []
    if has_notes:
        i += 1
        while i < len(lines) and lines[i].lower() != '\n':
            note = '.'.join(lines[i].strip().strip('.').split('.')[1:])
            notes.append(note.strip(' '))
            i += 1
            
    recipe["notes"] = notes

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

            # Also write methods
            file.write('methods:\n')
            for method in recipe["methods"]:
                file.write('- {}\n'.format(method))

        if recipe["notes"]:
            file.write('notes:\n')
            for note in recipe["notes"]:
                file.write('- {}\n'.format(note))

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


def load_method(filename):
    """ Using YAML file format to make things a lot easier. """
    with open(filename) as file:
        method = yaml.load(file, Loader=yaml.FullLoader)
    return method


def write_method_md(method, method_dir, img_dir):
    name = ''.join([method['tag'], '.md'])
    filename = os.path.join(method_dir, name)

    print('Generating method {}'.format(name))

    # Start writing file
    with open(filename, 'w') as file:
        file.write('---\n')
        file.write('title: {}\n'.format(method['title']))
        file.write('tag: {}\n'.format(method['tag']))
        file.write('layout: method\n')
        if "steps" in method.keys():
            file.write('steps:\n')
            for line in method["steps"]:
                file.write('- {}\n'.format(line))
        else:
            print('Method {} has no steps.'.format(method['title']))

        if "notes" in method.keys():
            file.write('notes:\n')
            for line in method["notes"]:
                file.write('- {}\n'.format(line))
        file.write('---\n')
