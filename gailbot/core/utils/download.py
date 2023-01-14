# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 13:39:44
# @Last Modified by:   Muhammad Umair

import shutil
from typing import List
from tqdm.auto import *
import requests
from zipfile import ZipFile
import os

def download_from_urls(
    urls : List[str],
    download_dir : str,
    unzip : bool = True,
    chunkSize : int = 8192
) -> List[str]:
    """
    Download from a list of urls and return a path to the directory containing
    the data from each url
    """
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