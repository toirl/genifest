"""Console script for genifest"""

import sys

import click

from genifest.logger import get_logger, setup_logging
from genifest.main import main

logger = get_logger()

# Names of manifest files
path_manifest_template = "./manifest-template.yaml"


@click.command()
@click.option("-h", "--host", default="http://localhost:9090", help="Host of the data provider", show_default=True)
@click.option("-o", "--output", help="Path to the generate manifest file. If None is provided result goes to stdout")
@click.option(
    "-t", "--template", default=path_manifest_template, help="Path to the manifest template file", required=True
)
@click.option("-v", "--verbosity", default=0, count=True, help="Verbosity of logging")
def cli(host: str, verbosity: int, output: str, template: str, args=None):
    """Console script for genifest"""
    setup_logging(verbosity=verbosity)
    main(template, host, output)
    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
