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
CONFIG = read_yaml("config/app_tei_docs.yaml")
CURRENT_DIR = os.getcwd()


@app.route('/')
def index():
    global CURRENT_DIR, CONFIG
    include_page_content(CURRENT_DIR)
    about_text = read_markdown(CONFIG['PATHS']['page_content'])
    return render_template('index.html', about_text=about_text)


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/corpus')
def corpus():
    authors = S.get_authors()
    filter_options = prepare_options(db.engine.table_names())
    return render_template(
        'corpus.html',
        authors=authors,
        filter_options=filter_options)


@app.route("/api/documents", methods=["GET", "POST"])
def api_search():
    documents = S.search_documents(request)
    return jsonify(documents)


@app.route("/document/<int:document_id>")
def document_view(document_id):
    global CONFIG
    values = S.get_filename(document_id)
    content = values[1].split('\t')
    formats = [CONFIG['formats'][index]
        for index, format in enumerate(values[2:])
        if format == 1
    ]
    return render_template(
        'document.html', contentList=content,
        filename=values[0], formats=formats)


if __name__ == '__main__':
    app.run(debug=True)
