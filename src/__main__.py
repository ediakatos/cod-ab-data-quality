from .checks.__main__ import main as checks
from .download.__main__ import main as download
from .metadata.__main__ import main as metadata
from .reports.__main__ import main as reports
from .scores.__main__ import main as scores


def main() -> None:
    """Main function, runs all modules in sequence.

    Note the following outputs and dependencies between modules:

    - module: metadata
        - depends: none
        - outputs: data/tables/metadata.csv
    - module: download
        - depends: data/tables/metadata.csv
        - outputs: data/boundaries/*.gpkg
    - module: checks
        - depends: data/tables/metadata.csv, data/boundaries/*.gpkg
        - outputs: data/tables/checks.csv
    - module: scores
        - depends: data/tables/metadata.csv, data/tables/checks.csv
        - outputs: data/tables/scores.csv
    - module: reports
        - depends: data/tables/metadata.csv, data/boundaries/*.gpkg
        - outputs: data/attributes/*.csv, data/images/*.png
    """
    metadata()
    download()
    checks()
    scores()
    reports()


if __name__ == "__main__":
    main()
