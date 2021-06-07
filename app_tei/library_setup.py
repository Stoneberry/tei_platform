from app_tei.library import LibraryDB


if __name__ == '__main__':
    """
    Run this file to setup the database.
    """

    library = LibraryDB()
    library.collect_data(
        scenario="drama",
        keep_all=False,
        links=True,
        modules=[],
        odd_path=None,
        custom_css_path=None,
        schema_path="schema.rng",
    )