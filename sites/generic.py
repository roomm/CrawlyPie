import importlib

import requests
from lxml import html, etree
import yaml
import os
from multiprocessing.dummy import Pool as ThreadPool
import core.xpath_custom_functions as xpath_functions


class GenericSite:
    def __init__(self, module, entity, debug):
        self._items = []
        self._link_items = []
        self._config = None
        self._debug = debug
        self.entity_name = entity
        self.module_name = "entities." + module
        self.init_xpath()

    def echo_results(self):
        for recipe in self._items:
            print recipe

    @staticmethod
    def init_xpath():
        ns = etree.FunctionNamespace(None)
        for helper_func in dir(xpath_functions):
            func_prefix = 'xpath_func_'
            if helper_func.startswith(func_prefix):
                ns[helper_func[len(func_prefix):]] = getattr(xpath_functions,
                                                             helper_func)  # function's name is without the prefix

    @staticmethod
    def get_html(url, hedaers=None):
        if not hedaers:
            hedaers = {}
        page = requests.get(url, headers=hedaers)
        page.encoding = 'UTF-8'
        return html.fromstring(page.text)

    @staticmethod
    def post_html(url, data, headers=None):
        r = requests.post(url, data=data, headers=headers)
        r.encoding = "UTF-8"
        return r.text

    def set_config(self, config):
        path = os.getcwd() + os.sep + "yaml" + os.sep + config
        # path = os.getcwd() + os.sep + "../yaml" + os.sep + config
        with open(path, 'r') as f:
            self._config = yaml.load(f)

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def set_entity_attr(entity, field, value):
        typ = type(getattr(entity, field))
        if typ is str:
            if type(value) is list:
                setattr(entity, field, value[0])
            else:
                setattr(entity, field, value)
        else:
            setattr(entity, field, value)

    def _go_get_pages(self, pages_range):

        if self._debug:
            for page in pages_range:
                self._get_pages(page)
        else:
            pool = ThreadPool(10)
            pool.map(self._get_pages, pages_range)

    def _get_pages(self, page):
        url = self._config["core"]["site"] + self._config["core"]["paginationUrl"]
        raw_html = self.get_html(url.format(str(page)))
        self._link_items += self._get_items_from_page(raw_html)

    def _get_items_from_page(self, raw_html):
        items_found = []
        xpath = self._config["pagination"]["item"]["xpath"]
        # site = self._config["core"]["site"]
        for flat in raw_html.xpath(xpath):
            items_found.append(flat)

        return items_found

    def _parse_items(self):
        if self._debug:
            for item in self._link_items:
                self._parse_item(item)
        else:
            pool = ThreadPool(20)
            pool.map(self._parse_item, self._link_items)

    def _parse_item(self, url):
        html_item = self.get_html(self._config["core"]["site"] + url)
        item = self.str_to_class()
        item.site = self._config["core"]["site"]
        item.item_url = url
        for field, field_params in self._config["info"].iteritems():
            try:
                if "unicode" in field_params:
                    xpath_value = html_item.xpath(field_params["xpath"].decode('unicode-escape'))
                else:
                    xpath_value = html_item.xpath(field_params["xpath"])
                self.set_entity_attr(item, field, xpath_value)
            except IndexError:
                pass
                # print "\t" + field
        self._items.append(item)

    def str_to_class(self):

        try:
            module_ = importlib.import_module(self.module_name)
            try:
                class_ = getattr(module_, self.entity_name)()
            except AttributeError:
                print 'Class does not exist'
        except ImportError:
            print 'Module does not exist'

        return class_ or None
