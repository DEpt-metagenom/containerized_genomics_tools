import requests
import subprocess


def fetch_tags_and_digests(image_name):
    """
    Fetch Docker image tags and their digests from Docker Hub, ignoring specific tags.
    """
    # API URL for fetching tags
    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/?page_size=10"  # Fetch up to 10 tags
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch tags. Status code: {response.status_code}")
            return None

        data = response.json()
        tags = data.get("results", [])

        # Filter out 'dev' tags and sort by last updated date
        filtered_tags = [
            tag for tag in tags if tag["name"] != "dev"
        ]
        if len(filtered_tags) < 2:
            print("Not enough valid tags to compare.")
            return None

        # Sort by `last_updated` to ensure proper ordering
        filtered_tags.sort(key=lambda t: t["last_updated"], reverse=True)

        # Extract the latest two tags and their digests
        latest_tag = filtered_tags[0]
        second_latest_tag = filtered_tags[1]

        # Fetch the digest for both tags
        latest_digest = fetch_digest_for_tag(image_name, latest_tag["name"])
        second_latest_digest = fetch_digest_for_tag(image_name, second_latest_tag["name"])

        latest_info = {
            "tag": latest_tag["name"],
            "digest": latest_digest,
        }
        second_latest_info = {
            "tag": second_latest_tag["name"],
            "digest": second_latest_digest,
        }

        return latest_info, second_latest_info

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def fetch_digest_for_tag(image_name, tag):
    """
    Fetch the digest for a specific tag from Docker Hub.
    """
    try:
        url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/{tag}/"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch digest for tag {tag}. Status code: {response.status_code}")
            return None

        data = response.json()

        if 'digest' in data:
            return data['digest']
        else:
            print(f"No digest found for tag {tag}")
            return "No digest available"
    except Exception as e:
        print(f"Error occurred while fetching digest for tag {tag}: {e}")
        return "Error fetching digest"


def get_installed_image_digest(image_name):
    """
    Get the digest of the installed Docker image.
    """
    try:
        result = subprocess.run(
            ['docker', 'inspect', '--format', '{{index .RepoDigests 0}}', image_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            installed_digest = result.stdout.strip()
            if installed_digest:
                return installed_digest.split('@')[1]  # Extract just the digest after '@'
            else:
                print(f"Error: No digest found for the image '{image_name}'.")
                return None
        else:
            print(f"Failed to fetch installed digest. Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def compare_tags(tag1, tag2):
    """
    Compare two Docker tags and their digests.
    """
    print(f"Latest tag: {tag1['tag']} (Digest: {tag1['digest']})")
    print(f"Second latest tag: {tag2['tag']} (Digest: {tag2['digest']})")

    if tag1["digest"] == tag2["digest"]:
        print("The latest two tags have the same digest.")
    else:
        print("The latest two tags have different digests.")


if __name__ == "__main__":
    image_name = "multiqc/multiqc" 

    tags = fetch_tags_and_digests(image_name)
    
    installed_digest = get_installed_image_digest(image_name)

    if tags:
        latest, second_latest = tags
        compare_tags(latest, second_latest)

        # Compare the latest tag digest from Docker Hub with the installed image digest
        if installed_digest:
            print(f"Installed Digest: {installed_digest}")
            if installed_digest == latest["digest"]:
                print("Installed image matches the latest tag from the registry.")
            else:
                print(f"Version {second_latest} of MultiQC is now awailable! Use 'make pull' to pull the latest docker image")
