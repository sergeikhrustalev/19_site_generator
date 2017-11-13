import os

from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from confman import ConfigManager


def create_directories(directory_list):

    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)


def convert_from_markdown(md_filepath):

    with open(md_filepath) as file_handler:
        md_content = file_handler.read()

    return markdown(md_content, extensions=['codehilite'])


def generate_index_page(index_page, index_structure):

    environment = Environment(loader=FileSystemLoader('.'))

    template = environment.get_template('templates/index.html')

    with open(index_page, 'w') as file_handler:

        file_handler.write(
            template.render(index_structure=index_structure)
        )


def generate_article_page(title, md_filepath, html_filepath):

    environment = Environment(loader=FileSystemLoader('.'))

    template = environment.get_template('templates/article.html')

    html_content = convert_from_markdown(md_filepath)

    with open(html_filepath, 'w') as file_handler:

        file_handler.write(
            template.render(title=title, html_content=html_content)
        )


def generate_site(path_to_configdir, path_to_targetdir):

    manager = ConfigManager(
        config_dir=path_to_configdir,
        target_dir=path_to_targetdir
    )

    create_directories(manager.directory_list)

    generate_index_page(
       manager.index_page,
       manager.index_structure
    )

    for title, md_filepath, html_filepath in manager.article_list:
        generate_article_page(title, md_filepath, html_filepath)


if __name__ == '__main__':

    generate_site('.', 'htmldir')
