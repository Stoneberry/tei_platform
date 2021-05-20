# -*- coding: utf-8 -*-
from collections import defaultdict
from operator import itemgetter

from app_tei.tei_transformer.tei_transformer import TEITransformer
from app_tei.app_tei_auxiliary import *

import sqlite3
from sqlite3 import Error


TT = TEITransformer()
APP_DIR = os.getcwd()
CONFIG = read_yaml("config/library_tei_docs.yaml")


class Library:

    @staticmethod
    def __load_library_paths():
        files = defaultdict(list)
        for filename in os.listdir(CONFIG['PATHS']['library']):
            fname, fextension = os.path.splitext(filename)
            fname = os.path.split(fname)[-1]
            files[fname].append(fextension)
        return files

    def __transform(self, filename, output_format='html'):
        fullname = "{}.{}".format(filename, output_format)
        output_path = os.path.join(CONFIG['PATHS']['library'], fullname)
        TT.transform(
            output_format=output_format, scenario="drama",
            keep_all=False, output_filename=output_path,
            custom_css_path=None)
        self.__transfer_files(filename, output_format=output_format)

    @staticmethod
    def __create_link(cur_dir, new_dir, filename):
        os.chdir(new_dir)
        os.system('ln -s {}/{}'.format(cur_dir, filename))
        os.chdir(APP_DIR)

    def __transfer_files(self, filename, output_format='html'):
        fullname = "{}.{}".format(filename, output_format)
        self.__create_link(
            CONFIG['PATHS']['library_static'],
            CONFIG['PATHS']['static'], fullname)
        if output_format == 'html':
            self.__create_link(
                CONFIG['PATHS']['library_templates'],
                CONFIG['PATHS']['templates'], fullname)

    def __parse_xml(self, filename, formats, files):
        schema_path = "../library/schema.rng"
        fullname = "{}.{}".format(filename, 'xml')
        tei_path = os.path.join(CONFIG['PATHS']['library'], fullname)
        TT.load_tei(tei_path, schema_path=schema_path)
        self.__transfer_files(filename, output_format='xml')
        if '.html' not in formats:
            self.__transform(filename, output_format='html')
            files[filename].append('.html')
        if '.docx' not in formats:
            self.__transform(filename, output_format='docx')
            files[filename].append('.docx')
        return files

    def parse_library(self):
        files = self.__load_library_paths()
        for filename in files:
            formats = files[filename]
            if '.html' in formats:
                self.__transfer_files(filename, output_format='html')
            if '.xml' in formats:
                files = self.__parse_xml(filename, formats, files)
        return files


class LibraryDB(Library):

    def __init__(self):
        self.create_db()

    def create_db(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(
                CONFIG['PATHS']['dbname'])
            self.cur = self.conn.cursor()
            self.create_tables()
        except Error as e:
            print(e)

    def create_tables(self):
        global CONFIG
        self.conn.execute(CONFIG['SQL_QUERIES']['drop_documents'])
        self.conn.execute(CONFIG['SQL_QUERIES']['drop_authors'])
        self.conn.execute(CONFIG['SQL_QUERIES']['create_documents'])
        self.conn.execute(CONFIG['SQL_QUERIES']['create_authors'])

    @staticmethod
    def get_element_text(soup, *args, findall=False, **kwargs):
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

    @staticmethod
    def add_content_id(soup, path):
        content = soup.findAll(class_='head')
        text_content = []
        for index, item in enumerate(content):
            item.attrs['id'] = index
            text_content.append(item.text)
        save_html(soup, path)
        return '\t'.join(text_content)

    def __html_search_metadata(self, filename):
        full_name = "{}.{}".format(filename, 'html')
        path = os.path.join(CONFIG['PATHS']['templates'], full_name)
        soup = read_html(path)
        metadata = self.create_metadata(filename)
        for tagset in CONFIG['METAINFO_TAGS']:
            tag_value = self.__parse_tagset_class(soup, tagset)
            metadata[tagset[-3] + '_' + tagset[-2]] = tag_value
        metadata['inner_id_author'] = generate_id(metadata['titleStmt_author'])
        metadata['content'] = self.add_content_id(soup, path)
        return metadata

    @staticmethod
    def __find_tag(sp, tagset):
        if sp:
            for tag in tagset[:-2]:
                sp = sp.find(class_=tag)
                if not sp: break
        return sp

    def __parse_tagset_class(self, soup, tagset):
        sp = soup.find(class_='teiHeader')
        sp = self.__find_tag(sp, tagset)
        if sp:
            tag_value = self.get_element_text(
                sp, class_=tagset[-2], findall=tagset[-1])
        else: tag_value = 'Not defined'
        return tag_value

    def __parse_tagset(self, soup, tagset):
        sp = soup.find('teiHeader')
        for tag in tagset[:-2]:
            sp = sp.find(tag)
            if not sp: break
        if sp:
            tag_value = self.get_element_text(
                sp, tagset[-2], findall=tagset[-1])
        else:
            tag_value = 'Not defined'
        return tag_value

    @staticmethod
    def __add_formats(formats, metadata):
        for frm in formats:
            col_name = "{}_format".format(frm[1:])
            metadata[col_name] = 1
        return metadata

    # def __xml_search_metadata(self, filename):
    #     path = os.path.join(CONFIG['PATHS']['library'], filename + '.xml')
    #     soup = read_xml(path)
    #     metadata = self.create_metadata(filename)
    #     for tagset in CONFIG['METAINFO_TAGS']:
    #         tag_value = self.__parse_tagset(soup, tagset)
    #         metadata[tagset[-3] + '_' + tagset[-2]] = tag_value
    #     metadata['inner_id_author'] = generate_id(metadata['titleStmt_author'])
    #     return metadata

    @staticmethod
    def create_metadata(filename):
        return {
            'docx_format': 0,
            'html_format': 0,
            'xml_format': 0,
            'filename': filename,
            'inner_id_document': generate_id(filename)
        }

    def collect_data(self):
        files = self.parse_library()
        meta_info = []
        for filename in files:
            formats = files[filename]
            if '.html' in formats:
                metadata = self.__html_search_metadata(filename)
                metadata = self.__add_formats(formats, metadata)
                self.add_document_info(metadata)
        return meta_info

    def add_document_info(self, metadata):
        document = itemgetter(*CONFIG['DB_COLUMNS']['document'])(metadata)
        author = itemgetter(*CONFIG['DB_COLUMNS']['author'])(metadata)
        q_doc = CONFIG['SQL_QUERIES']['insert_document'].format(*document*2)
        q_author = CONFIG['SQL_QUERIES']['insert_author'].format(*author*2)
        self.cur.execute(q_doc)
        self.cur.execute(q_author)
        self.conn.commit()
