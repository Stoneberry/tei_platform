# -*- coding: utf-8 -*-
from collections import defaultdict
from operator import itemgetter

import TEItransformer as TEIT
from app_tei_auxiliary import *

import sqlite3
from sqlite3 import Error


APP_DIR = os.getcwd()
CONFIG = read_yaml("config/library_tei_docs.yaml")


class Library:

    """
    Collect library.
    """

    @staticmethod
    def __load_library_paths():
        """
        Get document names and extensions form the library dir.
        :return: dict
        """
        files = defaultdict(list)
        for filename in os.listdir(CONFIG['PATHS']['library']):
            if not filename.startswith('.'):
                fname, fextension = os.path.splitext(filename)
                fname = os.path.split(fname)[-1]
                files[fname].append(fextension)
        return files

    @staticmethod
    def __create_link(cur_dir, new_dir, filename):
        """
        Create soft links to app_tei directories.
        :param cur_dir: str
        :param new_dir: str
        :param filename: str
        :return: None
        """
        os.chdir(new_dir)
        os.system('ln -s {}/{}'.format(cur_dir, filename))
        os.chdir(APP_DIR)

    def __transfer_files(self, fullname, output_format='html'):
        """
        Create soft links to transformed files to app_tei directories.
        :param fullname: str
        :param output_format: str
        :return: None
        """
        self.__create_link(
            CONFIG['PATHS']['library_docs'],
            CONFIG['PATHS']['static'], fullname)
        if output_format == 'html':
            self.__create_link(
                CONFIG['PATHS']['library_templates'],
                CONFIG['PATHS']['templates'], fullname)

    def __transform_format(self, TT, filename, files, output_format, **kwargs):
        """
        Transform file to a format.
        :param TT: TEItransformer object
        :param filename: str
        :param files: dict
        :param output_format: str
        :param kwargs: kwargs for transform method
        :return: None
        """
        full_name = "{}.{}".format(filename, output_format)
        output_filename = "{}/{}".format(
            CONFIG['PATHS']['library'], filename)
        TT.transform(
            output_format=output_format,
            output_filename=output_filename,
            enable_valid=False, **kwargs)
        self.__transfer_files(full_name, output_format=output_format)
        files[filename].append('.' + output_format)

    def __parse_xml(self, TT, filename, files, schema_path=None, **kwargs):
        """
        Parse xml file.
        :param TT: TEItransformer object
        :param filename: str
        :param files: dict
        :param schema_path: str
        :param kwargs: kwargs for transform method
        :return: dict
        """
        full_name = "{}.xml".format(filename)
        tei_path = os.path.join(CONFIG['PATHS']['library'], full_name)

        if schema_path:
            schema_path = os.path.join(CONFIG['PATHS']['library'], schema_path)
        TT.load_tei(tei_path, schema_path=schema_path)

        self.__transfer_files(full_name, output_format='xml')
        self.__transform_format(TT, filename, files, 'html', full_page=True, **kwargs)
        self.__transform_format(TT, filename, files, 'docx', **kwargs)
        self.__transform_format(TT, filename, files, 'json')
        return files

    def parse_library(self, scenario='drama', **kwargs):
        """
        Parse library files.
        :param scenario: str
        :param kwargs: kwargs for transform method
        :return: dict
        """
        TT = TEIT.TEITransformer(scenario=scenario)
        files = self.__load_library_paths()
        for filename in files:
            formats = files[filename]
            if '.xml' in formats:
                files = self.__parse_xml(TT, filename, files, **kwargs)
        return files


class LibraryDB(Library):

    """
    Library creation interface.
    """

    def __init__(self):
        self.create_db()

    def create_db(self):
        """
        Create db and tables.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(
                CONFIG['PATHS']['dbname'])
            self.cur = self.conn.cursor()
            self.create_tables()
        except Error as e:
            print(e)

    def create_tables(self):
        """
        Create tables.
        """
        self.conn.execute(CONFIG['SQL_QUERIES']['drop_documents'])
        self.conn.execute(CONFIG['SQL_QUERIES']['drop_authors'])
        self.conn.execute(CONFIG['SQL_QUERIES']['create_documents'])
        self.conn.execute(CONFIG['SQL_QUERIES']['create_authors'])

    @staticmethod
    def get_element_text(soup, *args, findall=False, **kwargs):
        """
        Try to extract text from tag.
        :param soup: bs4 object
        :param args: args for findAll method
        :param findall: whether to find all the child nodes
        :param kwargs: kwargs for findAll method
        :return: str
        """
        if findall:
            element = soup.findAll(*args, **kwargs)
        else:
            element = soup.find(*args, **kwargs)
            element = [element]
        if not element or element == [None]:
            return 'Not defined'
        text = [i.text for i in element]
        text = ', '.join(text)
        return text

    def __html_search_metadata(self, filename):

        full_name = "{}.{}".format(filename, 'html')
        path = os.path.join(CONFIG['PATHS']['templates'], full_name)
        soup = read_html(path)
        metadata = self.create_metadata(filename)

        for tagset in CONFIG['METAINFO_TAGS']:
            tag_value = self.__parse_tagset_class(soup, tagset)
            metadata[tagset[-3] + '_' + tagset[-2]] = tag_value

        metadata['inner_id_author'] = generate_id(metadata['titleStmt_author'])
        return metadata

    @staticmethod
    def __find_tag(sp, tagset):
        """
        Find tag for meta information
        :param sp: b4s element
        :param tagset: list
        :return: b4s element
        """
        if sp:
            for tag in tagset[:-2]:
                sp = sp.find(class_=tag)
                if not sp: break
        return sp

    def __parse_tagset_class(self, soup, tagset):
        """
        Parse tags for metadata.
        :param soup: bs4 soup
        :param tagset: list
        :return: str
        """
        sp = soup.find(class_='teiHeader')
        sp = self.__find_tag(sp, tagset)
        if sp:
            tag_value = self.get_element_text(
                sp, class_=tagset[-2], findall=tagset[-1])
        else: tag_value = 'Not defined'
        return tag_value

    # def __parse_tagset(self, soup, tagset):
    #     """
    #     Parse tags for metadata.
    #     :param soup: bs4 soup
    #     :param tagset: list
    #     :return: str
    #     """
    #     sp = soup.find('teiHeader')
    #     for tag in tagset[:-2]:
    #         sp = sp.find(tag)
    #         if not sp: break
    #     if sp:
    #         tag_value = self.get_element_text(
    #             sp, tagset[-2], findall=tagset[-1])
    #     else:
    #         tag_value = 'Not defined'
    #     return tag_value

    @staticmethod
    def __add_formats(formats, metadata):
        """
        Add formats to metadata
        :param formats: list
        :param metadata: dict
        :return:
        """
        for frm in formats:
            col_name = "{}_format".format(frm[1:])
            metadata[col_name] = 1
        return metadata

    @staticmethod
    def create_metadata(filename):
        """
        Create metadata template
        :param filename: str
        :return: dict
        """
        return {
            'docx_format': 0,
            'html_format': 0,
            'xml_format': 0,
            'json_format': 0,
            'filename': filename,
            'inner_id_document': generate_id(filename)
        }

    def collect_data(self, **kwargs):
        """
        Collect data from library files.
        :param kwargs: kwargs for parse_library function
        :return: list
        """
        files = self.parse_library(**kwargs)
        meta_info = []
        for filename in files:
            formats = files[filename]
            if '.html' in formats:
                metadata = self.__html_search_metadata(filename)
                metadata = self.__add_formats(formats, metadata)
                self.add_document_info(metadata)
        return meta_info

    def add_document_info(self, metadata):
        """
        Add data to DB tables
        :param metadata: dict
        :return: None
        """
        document = itemgetter(*CONFIG['DB_COLUMNS']['document'])(metadata)
        author = itemgetter(*CONFIG['DB_COLUMNS']['author'])(metadata)
        q_doc = CONFIG['SQL_QUERIES']['insert_document'].format(*document*2)
        q_author = CONFIG['SQL_QUERIES']['insert_author'].format(*author*2)
        self.cur.execute(q_doc)
        self.cur.execute(q_author)
        self.conn.commit()
