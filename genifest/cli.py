"""Console script for genifest"""

import sys
from datetime import UTC, datetime, timedelta

import click

from genifest.logger import get_logger, setup_logging
from genifest.main import main

logger = get_logger()

# Names of manifest files
path_manifest_template = "./manifest-template.yaml"
path_manifest_static = "./manifest-static.yaml"

# URL für die Prometheus-API-Abfrage
url = "http://localhost:9090/api/v1/query_range"  # Daten über einen Zeitraum

# Zeitstempel für den Start und das Ende des Zeitbereichs
end_time = datetime.now(tz=UTC)
start_time = end_time - timedelta(hours=1)

# Abfrageparameter
query = "100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode='idle'}[1m])))"
params = {
    "query": query,
    "start": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "step": "60s",  # Schrittweite der Abfrage (1 Minute)
}


@click.command()
@click.option("-v", "--verbosity", default=0, count=True, help="Verbosity of logging")
def cli(verbosity: int, args=None):
    """Console script for genifest"""
    setup_logging(verbosity=verbosity)
    main(path_manifest_template, url, params, path_manifest_static)
    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
