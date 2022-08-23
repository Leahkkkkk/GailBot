# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-03 11:06:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-03 12:39:22

import shutil
from typing import List
from tqdm.auto import *
import requests
from zipfile import ZipFile
import os

# ---- GLOBALS

# NOTE: These are direct download urls to the plugin suites
URLS = [
    "https://sites.tufts.edu/hilab/files/2022/05/ca_pkg.zip"]


def download_from_urls(urls, download_dir, unzip=True, chunkSize=8192):
    # Create paths
    dataset_download_path = os.path.join(download_dir, "download")
    dataset_extract_path = download_dir
    if os.path.isdir(dataset_download_path):
        shutil.rmtree(dataset_download_path)
    os.makedirs(dataset_download_path)
    os.makedirs(dataset_extract_path, exist_ok=True)
    # Download each url as a zip file.
    extracted_paths = []
    for i, url in enumerate(urls):
        # Create a temp. dir for this specific url
        name = os.path.splitext(os.path.basename(url))[0]
        url_temp_path = "{}.zip".format(
            os.path.join(dataset_download_path, name))
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            pbar = tqdm(
                total=int(r.headers['Content-Length']), desc="{}".format(name))
            with open(url_temp_path, "wb+") as f:
                for chunk in r.iter_content(chunk_size=chunkSize):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        pbar.update(len(chunk))
        if unzip:
            with ZipFile(url_temp_path, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                extract_path = os.path.join(dataset_extract_path, name)
                extracted_paths.append(extract_path)
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)
                os.makedirs(extract_path)
                zipObj.extractall(extract_path)
    # Remove the temp folders
    shutil.rmtree(dataset_download_path)
    return extracted_paths


def download_all_plugins(download_dir: str) -> List[str]:
    return download_from_urls(
        urls=URLS,
        download_dir=download_dir,
        unzip=True)


def download_plugin_from_url(url: str, download_dir: str) -> List[str]:
    return download_from_urls(
        urls=[url],
        download_dir=download_dir,
        unzip=True)


# --------- Tests


def unittest():
    """
    Tests:
        1. Download and extract from a url.
    """
    urls = [
        "https://sites.tufts.edu/hilab/files/2022/05/ca_pkg.zip"]

    download_from_urls(
        urls=urls,
        download_dir="./test")


if __name__ == "__main__":
    unittest()
