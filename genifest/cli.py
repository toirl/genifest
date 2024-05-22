"""Console script for genifest"""
import sys

import click

from genifest.logger import get_logger, setup_logging

logger = get_logger()


@click.command()
@click.option("-v", "--verbosity", default=0, count=True, help="Verbosity of logging")
def main(verbosity: int, args=None):
    """Console script for genifest"""
    setup_logging(verbosity=verbosity)
    click.echo("Replace this message by putting your code into genifest.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    logger.info("This is a test INFO log message")
    logger.debug("This is a test DEBUG log message")
    logger.warning("This is a test WARNING log message")
    logger.error("This is a test ERROR log message")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
