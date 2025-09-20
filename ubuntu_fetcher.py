import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_image(url, fetched_dir="Fetched_Images", seen_hashes=set()):
    """
    Fetch an image from a given URL, save it into Fetched_Images directory,
    avoid duplicates, and handle errors gracefully.
    """

    try:
        # Create directory if it doesn't exist
        os.makedirs(fetched_dir, exist_ok=True)

        # Fetch the image with a user-agent header
        headers = {"User-Agent": "Ubuntu-Image-Fetcher/1.0 (Respectful Client)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Check content type
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped: {url} (Not an image, got {content_type})")
            return seen_hashes

        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join(fetched_dir, filename)

        # Compute hash to detect duplicates
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in seen_hashes:
            print(f"✗ Duplicate skipped: {filename}")
            return seen_hashes

        # Save the file
        with open(filepath, "wb") as f:
            f.write(response.content)

        seen_hashes.add(file_hash)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

    return seen_hashes


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter image URLs (comma separated): ").split(",")

    seen_hashes = set()
    for url in [u.strip() for u in urls if u.strip()]:
        seen_hashes = fetch_image(url, seen_hashes=seen_hashes)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
