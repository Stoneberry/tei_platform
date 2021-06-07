# -*- coding: utf-8 -*-
from app_tei.models import Documents, Authors
from app_tei.app_tei_auxiliary import *


class Search:

    """
    API search interface.
    """

    @staticmethod
    def check_author_presence(data):
        """
        Check if author is present in DB.
        """
        result = Authors.query.filter(
            Authors.author_name == data.get('author', '-')
        ).one_or_none()
        if result:
            return result, True
        return result, False

    @staticmethod
    def check_file_presence(data):
        """
        Check if filename is present in DB.
        """
        result = Documents.query.filter(
            Documents.filename == data.get('filename')
        ).one_or_none()
        if result:
            return result, True
        return result, False

    @staticmethod
    def get_authors():
        """
        Get authors.
        """
        result = Authors.query. \
            with_entities(Authors.author_name). \
            distinct(Authors.author_name).all()
        return prepare_options(result)

    @staticmethod
    def get_filename(id_document):
        """
        Get filenames.
        """
        result = Documents.query.filter(
            Documents.id_document == id_document). \
            with_entities(
            Documents.filename,  # Documents.content,
            Documents.docx_format, Documents.html_format,
            Documents.xml_format, Documents.json_format
        ).distinct(Documents.id_document).first()
        return result

    @staticmethod
    def __covert_result_to_dict(results):
        """
        Present search results as a dict.
        """
        documents = {}
        for item in results:
            keys = list(item.keys())[1:]
            documents[item[0]] = dict(zip(keys, item[1:]))
        return documents

    @staticmethod
    def get_all_documents():
        """
        Get all the documents.
        """
        result = Documents.query.join(
            Authors, Documents.inner_id_author == Authors.inner_id_author) \
            .with_entities(
            Documents.id_document, Documents.title, Documents.id_document_wiki,
            Authors.author_name, Authors.id_author_wiki,
            Documents.genre, Documents.language,
            Documents.publication_date, Documents.creation_date,
            Documents.description, Documents.genre,
            Documents.language, Documents.html_format, Documents.json_format,
            Documents.docx_format, Documents.xml_format,
            )
        return result.all()

    @staticmethod
    def __prepare_author_docs(author):
        """
        Filter documents according to the author name.
        """
        result = Documents.query \
            .join(Authors, Documents.inner_id_author == Authors.inner_id_author) \
            .filter(Authors.author_name.in_(author)) \
            .with_entities(
                Documents.id_document, Documents.title,
                Documents.id_document_wiki,
                Authors.author_name, Authors.id_author_wiki,
                Documents.genre, Documents.language,
                Documents.publication_date, Documents.creation_date,
                Documents.description, Documents.genre,
                Documents.language, Documents.html_format,
                Documents.docx_format, Documents.xml_format
                )
        return result.all()

    @staticmethod
    def __prepare_title_docs(title):
        """
        Filter documents according to the title.
        """
        result = Documents.query \
            .join(Authors, Documents.inner_id_author == Authors.inner_id_author) \
            .filter(Documents.title.in_(title)) \
            .with_entities(
                Documents.id_document, Documents.title,
                Documents.id_document_wiki,
                Authors.author_name, Authors.id_author_wiki,
                Documents.genre, Documents.language,
                Documents.publication_date, Documents.creation_date,
                Documents.description, Documents.genre,
                Documents.language, Documents.html_format,
                Documents.docx_format, Documents.xml_format,
            )
        return result.all()

    @staticmethod
    def __prepare_title_author_docs(author, title):
        """
        Filter documents according to the title and author name.
        """
        result = Documents.query \
            .join(Authors, Documents.inner_id_author == Authors.inner_id_author) \
            .filter(Documents.title.in_(title)) \
            .filter(Authors.author_name.in_(author)) \
            .with_entities(
                Documents.id_document, Documents.title,
                Documents.id_document_wiki,
                Authors.author_name, Authors.id_author_wiki,
                Documents.genre, Documents.language,
                Documents.publication_date, Documents.creation_date,
                Documents.description, Documents.genre,
                Documents.language, Documents.html_format,
                Documents.docx_format, Documents.xml_format,
                )
        return result.all()

    def __parse_form_values(self, form_values):
        """
        Parse search values.
        """
        author = form_values.get('author')
        title = form_values.get('title')

        con1 = author != [''] and author is not None
        con2 = title != [''] and title is not None

        if con2:
            title = preprocess_string(title)
        if con1 and con2:
            result = self.__prepare_title_author_docs(author, title)
        elif con2:
            result = self.__prepare_title_docs(title)
        elif con1:
            result = self.__prepare_author_docs(author)
        else:
            result = self.get_all_documents()
        return result

    def search_documents(self, request):
        """
        Search DB.
        """
        form_values = request.args.to_dict(flat=False)
        if form_values:
            result = self.__parse_form_values(form_values)
        else:
            result = self.get_all_documents()
        return self.__covert_result_to_dict(result)
