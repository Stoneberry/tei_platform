# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


db = SQLAlchemy()


class Authors(db.Model):
    __tablename__ = 'authors'
    id_author = db.Column(db.Integer, primary_key=True)
    inner_id_author = db.Column(db.Text)
    id_author_wiki = db.Column(db.Text)
    author_name = db.Column(db.Text)
    birthday = db.Column(db.Text)
    deathday = db.Column(db.Text)
    description = db.Column(db.Text)


class Documents(db.Model):
    __tablename__ = 'documents'
    id_document = db.Column(db.Integer, primary_key=True)
    inner_id_document = db.Column(db.Text)
    id_document_wiki = db.Column(db.Text)
    title = db.Column(db.Text)
    filename = db.Column(db.Text)
    genre = db.Column(db.Text)
    language = db.Column(db.Text)
    publication_date = db.Column(db.Text)
    creation_date = db.Column(db.Text)
    description = db.Column(db.Text)
    html_format = db.Column(db.Integer)
    docx_format = db.Column(db.Integer)
    xml_format = db.Column(db.Integer)
    content = db.Column(db.Text)
    inner_id_author = db.Column(db.Text, ForeignKey("authors.inner_id_author"))
    authors = db.relationship(
        "Authors", uselist=False,
        primaryjoin="Authors.inner_id_author==Documents.inner_id_author")


