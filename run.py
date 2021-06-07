from werkzeug.serving import run_simple
from dispatcher import application


if __name__ == '__main__':
    """
    run_simple is a development server. 
    Use another server for production.
    See https://flask.palletsprojects.com/en/1.0.x/deploying/#deployment.
    """

    run_simple(
        'localhost',
        5000,
        application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True)