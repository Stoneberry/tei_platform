# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
from app_tei.app_tei_auxiliary import *
from app_tei.models import db
from app_tei.search import Search


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.app = app
db.init_app(app)
db.create_all()


S = Search()

CONFIG = read_yaml("app_tei/config/app_tei_docs.yaml")
CURRENT_DIR = os.getcwd()
include_page_content(CURRENT_DIR)


@app.route('/')
def index():
    """
    Main page of tei_viewer.
    """
    about_text = read_markdown(CONFIG['PATHS']['about_content'])
    return render_template('index.html', about_text=about_text)


@app.route('/guide')
def guide():
    """
    Guide page of tei_viewer.
    """
    guide_text = read_markdown(CONFIG['PATHS']['guide_content'])
    return render_template('guide.html', guide_text=guide_text)


@app.route('/corpus')
def corpus():
    """
    Corpus page of tei_viewer.
    """
    authors = S.get_authors()
    filter_options = prepare_options(db.engine.table_names())
    return render_template(
        'corpus.html',
        authors=authors,
        filter_options=filter_options)


@app.route("/api/documents", methods=["GET", "POST"])
def api_search():
    """
    API page of tei_viewer.
    """
    documents = S.search_documents(request)
    return jsonify(documents)


@app.route("/document/<int:document_id>")
def document_view(document_id):
    """
    Document page of tei_viewer.
    """
    values = S.get_filename(document_id)
    formats = [CONFIG['FORMATS'][index]
        for index, format in enumerate(values[1:])
        if format == 1
    ]
    return render_template(
        'document.html',
        filename=values[0],
        formats=formats)


if __name__ == '__main__':
    app.run(debug=False)
