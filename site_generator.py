import os
import sys
import argparse


from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from config_manager import ConfigManager


def create_directories(directory_list):

    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)


def convert_from_markdown(mdpath):

    with open(mdpath) as file_handler:
        mdcontent = file_handler.read()

    return markdown(mdcontent, extensions=['codehilite'])


def generate_index_page(index_page, index_structure):

    environment = Environment(loader=FileSystemLoader('templates'))

    template = environment.get_template('index.html')

    with open(index_page, 'w') as file_handler:

        file_handler.write(
            template.render(index_structure=index_structure)
        )


def generate_article_page(title, mdpath, htmlpath):

    environment = Environment(loader=FileSystemLoader('templates'))

    template = environment.get_template('article.html')

    html_content = convert_from_markdown(mdpath)

    with open(htmlpath, 'w') as file_handler:

        file_handler.write(
            template.render(title=title, html_content=html_content)
        )


def generate_site(config_dir, target_dir):

    manager = ConfigManager(
        config_dir=config_dir,
        target_dir=target_dir
    )

    create_directories(manager.directory_list)

    generate_index_page(
       manager.index_page,
       manager.index_structure
    )

    for title, mdpath, htmlpath in manager.article_list:
        generate_article_page(title, mdpath, htmlpath)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='site generator')

    parser.add_argument('--config_dir')
    parser.add_argument('--target_dir')

    args = parser.parse_args()

    if not all((args.config_dir, args.target_dir)):

        print(
            'Syntax: sitegenerator.py',
            '--config_dir <path to config>',
            '--target_dir <path to html>'
        )
        sys.exit()

    generate_site(args.config_dir, args.target_dir)
