import os
import requests
import json
from concurrent.futures import ThreadPoolExecutor


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")


def main():
    download_dir = "downloaded"
    os.makedirs(download_dir, exist_ok=True)

    url = "https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch data from the endpoint. Status code: {response.status_code}")
        return

    data = response.json()["data"]

    download_tasks = []
    for user_id, images in data.items():
        for size, image_url in images.items():
            filename = os.path.join(download_dir, f"{user_id}_{size}.avif")
            download_tasks.append((image_url, filename))

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda x: download_image(*x), download_tasks)


if __name__ == "__main__":
    main()