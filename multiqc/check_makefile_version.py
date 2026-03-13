import re
import requests

MAKEFILE_PATH = "Makefile"
IMAGE_NAME = "multiqc/multiqc"


def extract_version_from_makefile(makefile_path):
    with open(makefile_path, "r") as f:
        content = f.read()
    match = re.search(r'^VERSION\s*[:?]?=\s*v?([\d.]+)', content, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def fetch_latest_version_from_dockerhub(image_name):
    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/?page_size=100"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch tags from Docker Hub")
        return None

    tags = response.json().get("results", [])
    version_tags = [tag["name"] for tag in tags if tag["name"].startswith("v") and tag["name"].count(".") >= 1]
    version_tags.sort(reverse=True, key=lambda s: list(map(int, s.strip("v").split("."))))
    return version_tags[0].lstrip("v") if version_tags else None


def main():
    makefile_version = extract_version_from_makefile(MAKEFILE_PATH)
    if not makefile_version:
        print("❌ Could not find VERSION in Makefile.")
        return

    print(f"🔍 Version in Makefile: v{makefile_version}")

    latest_version = fetch_latest_version_from_dockerhub(IMAGE_NAME)
    if not latest_version:
        print("❌ Could not retrieve latest version from Docker Hub.")
        return

    print(f"📦 Latest version on Docker Hub: v{latest_version}")

    if makefile_version == latest_version:
        print("✅ Makefile version is up to date.")
    else:
        print("⚠️  Makefile version is outdated.")
        print(f"👉 Consider updating it to: v{latest_version}")
        print(f"\nTo update run 'make pull VERSION=v{latest_version}'")


if __name__ == "__main__":
    main()
