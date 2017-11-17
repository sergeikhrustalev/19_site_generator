from collections import defaultdict
from os.path import join, split, splitext
from urllib.parse import quote

import json


class ConfigManager:

    def __init__(self, config_dir='.', target_dir='html'):

        config_path = join(config_dir, 'config.json')

        with open(config_path) as file_handler:
            json_content = file_handler.read()

        self._config_data = json.loads(json_content)
        self._config_dir = config_dir
        self._target_dir = target_dir

    @staticmethod
    def _rename_to_html(article_source):
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
            self._rename_to_html(article_source)
        )

    @property
    def directory_list(self):

        return list(

            {
                join(
                    self._target_dir,
                    split(article['source'])[0]
                )

                for article in self._config_data['articles']
            }
        )

    @property
    def article_list(self):

        return [

            (

                article['title'],
                self._get_md_path(article['source']),
                self._get_html_path(article['source'])

            )

            for article in self._config_data['articles']

        ]

    @property
    def index_structure(self):

        article_dict = defaultdict(list)

        for article in self._config_data['articles']:

            article_dict[article['topic']].append((

                article['title'],

                quote(
                    self._rename_to_html(article['source']),
                    safe='/'
                )

            ))

        return [

            (
                topic['title'],
                article_dict[topic['slug']]
            )

            for topic in self._config_data['topics']

        ]

    @property
    def index_page(self):
        return join(self._target_dir, 'index.html')
