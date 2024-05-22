import argparse
import re
import subprocess

r = r"[v](\d+).(\d+).(\d+)-(\d+)-g(\w+)"
# v1.2.3-42-gabcd123


def _get_number_revisions(version: str = "HEAD") -> int:
    number_revisions = len(subprocess.check_output(["git", "rev-list", version]).decode().strip().splitlines())
    return number_revisions


def _get_git_revision() -> str:
    revision = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    return revision


def _get_git_description() -> str:
    try:
        version = subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.DEVNULL).decode().strip()
        return version
    except Exception:
        return "v0.0.0"


def _get_docker_tag() -> str:
    version = _get_git_description()
    if version.find("-") > 0:
        return version
    else:
        version = f"{version}-{_get_number_revisions()}-g{_get_git_revision()}"
        return version


def build_major() -> str:
    version = _get_docker_tag()
    m = re.match(pattern=r, string=version)
    if m:
        return f"v{m.group(1)}"
    else:
        raise ValueError("Can not get version from git")


def build_minor() -> str:
    version = _get_docker_tag()
    m = re.match(pattern=r, string=version)
    if m:
        return f"v{m.group(1)}.{m.group(2)}"
    else:
        raise ValueError("Can not get version from git")


def build_commit() -> str:
    version = _get_docker_tag()
    m = re.match(pattern=r, string=version)
    if m:
        return f"v{m.group(1)}.{m.group(2)}.{m.group(3)}-{m.group(4)}-{m.group(5)}"
    else:
        raise ValueError("Can not get version from git")


builders = {"major": build_major, "minor": build_minor, "commit": build_commit}

parser = argparse.ArgumentParser(description="Extract tags for docker images from VCS")
parser.add_argument("tag", metavar="TAG", type=str, help=f"name of the tag {list(builders.keys())}")

args = parser.parse_args()


builder = builders.get(args.tag)
if builder is None:
    print(f"Unknown tag {args.tag}. Choose one from {list(builders.keys())}")
    exit(1)
else:
    print(builder())
