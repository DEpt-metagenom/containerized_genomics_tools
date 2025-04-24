import requests
import subprocess


def fetch_tag_digest(image_name, tag):
    try:
        url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/{tag}/"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch digest for tag {tag}. Status code: {response.status_code}")
            return None

        data = response.json()
        for image in data.get("images", []):
            if image.get("architecture") == "amd64" and image.get("os") == "linux":
                return image.get("digest")
        return None
    except Exception as e:
        print(f"Error fetching digest for tag {tag}: {e}")
        return None


def fetch_version_tags(image_name):
    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/?page_size=100"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch tags. Status code: {response.status_code}")
            return None

        tags = response.json().get("results", [])
        version_tags = [tag for tag in tags if tag["name"].startswith("v") and tag["name"].count(".") >= 1]
        version_tags.sort(key=lambda t: t["last_updated"], reverse=True)
        return version_tags
    except Exception as e:
        print(f"Error fetching tags: {e}")
        return None


def get_installed_version(image_name):
    try:
        result = subprocess.run(
            ['docker', 'images', '--format', '{{.Tag}}', image_name],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Failed to get installed tags: {result.stderr}")
            return None, None

        installed_tags = [t for t in result.stdout.strip().split('\n') if t]
        if not installed_tags:
            print("No local image found")
            return None, None

        version_tag = next((t for t in installed_tags if t.startswith("v") and t.count(".") >= 1), installed_tags[0])
        
        result = subprocess.run(
            ['docker', 'inspect', '--format', '{{index .RepoDigests 0}}', f"{image_name}:{version_tag}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if '@' in output:
                return version_tag, output.split('@')[1]
        
        print(f"Failed to get installed digest: {result.stderr}")
        return version_tag, None

    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None


def check_image_version(image_name):
    print(f"\n🔍 Checking image: {image_name}")

    installed_version, installed_digest = get_installed_version(image_name)
    if not installed_version:
        print("Could not determine installed version")
        return

    print(f"💻 Installed version: {installed_version}")
    if installed_digest:
        print(f"   Digest: {installed_digest}")

    version_tags = fetch_version_tags(image_name)
    if not version_tags:
        return

    latest_version_info = version_tags[0]
    latest_version = latest_version_info["name"]
    latest_digest = fetch_tag_digest(image_name, latest_version)

    print(f"\n📦 Latest version in registry: {latest_version}")
    print(f"   Updated: {latest_version_info['last_updated']}")
    if latest_digest:
        print(f"   Digest: {latest_digest}")

    if installed_digest and latest_digest:
        if installed_digest == latest_digest:
            print("\n✅ Your installed version matches the registry version")
        else:
            print("\n⚠️  Your installed version has a different digest than the registry version")

    if installed_version == latest_version:
        print("\n🎉 You're running the latest version!")
    else:
        print(f"\n⚠️  Newer version available: {latest_version}")
        print(f"📥 Pull the newer version! Use 'make pull VERSION={latest_version}'")

if __name__ == "__main__":
    image_name = "multiqc/multiqc" 
    check_image_version(image_name)
