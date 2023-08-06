from . import generate_task, paragraph_parser, process_translation
from deep_translator import GoogleTranslator
import pickle
import click
import os
from typing import Dict


@click.group()
def translate_group():
    pass


@click.group()
def update_group():
    pass


@translate_group.command()
@click.option('--input-file', help='input file path')
@click.option('--patch-file', help='output patch file path')
@click.option('--dict-file', help='dictionary file path')
@click.option('--lang-in', default='english', help='source language')
@click.option('--lang-out', help='destination language')
def translate(input_file, patch_file, dict_file, lang_in, lang_out):
    if input_file is None or not os.path.isfile(input_file):
        print("ERROR: input file does not exist")
        return
    with open(input_file, 'r') as f:
        input_txt = f.read()
    dictionary: Dict[str, str] = dict()
    if dict_file is not None and os.path.isfile(dict_file):
        dictionary = pickle.load(open(dict_file, "rb"))
    task = generate_task(input_txt,
                         lambda piece: GoogleTranslator(lang_in, lang_out).translate(piece),
                         dictionary,
                         paragraph_parser)
    if patch_file is None:
        print(task)
    else:
        with open(patch_file, 'w') as f:
            f.write(task)


@update_group.command()
@click.option('--patch-file', help="patch file")
@click.option('--dict-file', help="dictionary file path")
def update(patch_file, dict_file):
    if patch_file is None or not os.path.isfile(patch_file):
        print("ERROR: patch file does not exist")
        return
    dictionary = dict()
    if dict_file is not None and os.path.isfile(dict_file):
        dictionary = pickle.load(open(dict_file, "rb"))
    with open(patch_file, 'r') as f:
        translation = f.read()
    process_translation(translation, dictionary)
    pickle.dump(dictionary, open(dict_file, "wb"))


cli = click.CommandCollection(sources=[translate_group, update_group])


if __name__ == '__main__':
    cli()
