from os.path import join, splitext
import json


class ConfigManager:

    def __init__(self, config_dir='.', target_dir='html'):

        config_path = join(config_dir, 'config.json')
        
        with open(config_path) as file_handler:
            json_content = file_handler.read()

        self._config_data = json.loads(json_content)
        self._config_dir = config_dir
        self._target_dir = target_dir

    def _rename_md_to_html(self, article_source):
        return '{}{}'.format(splitext(article_source)[0], '.html')

    def _get_md_path(self, article_source):

        return join(
            self._config_dir,
            'articles',
            article_source
        )

    def _get_html_path(self, article_source):

        return join(
        self._target_dir,
        self._rename_md_to_html(article_source)
        )

    @property
    def article_list(self):

        article_list = []

        for article in self._config_data['articles']:

            article_list.append((
                article['title'],
                self._get_md_path(article['source']),
                self._get_html_path(article['source'])
            ))

        return article_list

    @property
    def index_structure(self):

        slug_dict = dict()

        for topic in self._config_data['topics']:
            slug_dict[topic['slug']] = topic['title'], []

        for article in self._config_data['articles']:

            article_topic = article['topic']

            slug_dict[article_topic][1].append((
                article['title'],
                self._rename_md_to_html(article['source'])
            ))

        structure = []

        for topic in self._config_data['topics']:
            structure.append(slug_dict[topic['slug']])

        return structure

    @property
    def index_page(self):
        return join(self._target_dir, 'index.html')
