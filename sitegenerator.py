from jinja2 import Environment, FileSystemLoader
from confman import ConfigManager


def generate_index_page(filepath, structure):

    environment = Environment(loader=FileSystemLoader('.'))

    template = environment.get_template('templates/index.html')

    with open(filepath, 'w') as file_handler:

        file_handler.write(
            template.render(index_structure=structure)
        )


def generate_article_page(title, md_filepath, html_filepath):

    environment = Environment(loader=FileSystemLoader('.'))

    template = environment.get_template('templates/article.html')

    with open(html_filepath, 'w') as file_handler:
        
        file_handler.write(
            template.render(title=title)
        )


if __name__ == '__main__':

    config_manager = ConfigManager()

    structure = config_manager.index_structure
    filepath = config_manager.index_page

    generate_index_page(filepath, structure)

    for title, md_filepath, html_filepath in config_manager.article_list:
        generate_article_page(title, md_filepath, html_filepath)






