from genifest.extract import CPUandMem, PrometheusDataExtractor
from genifest.transform import Transformer
from genifest.write import ManifestWriter


def main(path_manifest_template: str, url: str, path_manifest_static: str):
    query = CPUandMem()
    loader = PrometheusDataExtractor(base_url=url)
    raw_data = loader.fetch_data(query=query)

    transformer = Transformer()
    transformed_data = transformer.transform(data=raw_data)

    writer = ManifestWriter(template_path=path_manifest_template)
    manifest = writer.generate(transformed_data)
    if path_manifest_static:
        writer.write(path_manifest_static, manifest)
    else:
        writer.print(manifest)
