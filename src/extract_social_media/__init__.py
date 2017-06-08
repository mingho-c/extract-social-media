# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.1.0'


PREFIX = r'https?://(?:www\.)?'
SITES = ['twitter.com/', 'youtube.com/',
         '(?:[a-z]{2}\.)?linkedin.com/(?:company/|in/|pub/)',
         'github.com/', '(?:[a-z]{2}-[a-z]{2}\.)?facebook.com/',
         'plus\.google.com/', 'pinterest.com/', 'instagram.com/',
         'snapchat.com/', 'flipboard.com/', 'flickr.com',
         'google.com/+', 'weibo.com/', 'periscope.tv/',
         'telegram.me/', 'soundcloud.com', 'feeds.feedburner.com',
         'vimeo.com', 'slideshare.net', 'vkontakte.ru']
BETWEEN = ['user/', 'add/', 'pages/', '#!/', 'photos/',
           'u/0/']
ACCOUNT = r'[\w\+_@\.\-/%]+'
PATTERN = (
    r'%s(?:%s)(?:%s)?%s' %
    (PREFIX, '|'.join(SITES), '|'.join(BETWEEN), ACCOUNT))
SOCIAL_REX = re.compile(PATTERN, flags=re.I)


def matches_string(string):
    return SOCIAL_REX.match(string)


def find_links_tree(tree):
    """
    TODO:
    - `<fb:like href="http://www.facebook.com/elDiarioEs"`
    - `<g:plusone href="http://widgetsplus.com/"></g:plusone>`
    - <a class="reference external" href="https://twitter.com/intent/follow?screen_name=NASA">
    """
    for link in tree.xpath('//.[@href]'):
        href = link.get('href')
        if matches_string(href):
            yield href

    for script in tree.xpath('//script[not(@src)]/text()'):
        for match in SOCIAL_REX.findall(script):
            yield match

    for script in tree.xpath('//meta[contains(@name, "twitter:")]'):
        name = script.get('name')
        if name in ('twitter:site', 'twitter:creator'):
            yield script.get('content')