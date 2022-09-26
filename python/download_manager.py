from asyncio import subprocess
import os
import shlex
import tarfile

import subprocess

from pathlib import Path
from urllib.parse import urlparse


#
def download(data_file_url, output_dir):

    file_name=os.path.basename(urlparse(data_file_url).path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file_path=os.path.join(output_dir, file_name)

    downloaded = False
    if not os.path.isfile(output_file_path):
        download_cmd = "wget -O %s %s" % (output_file_path, data_file_url)
        print (download_cmd)
        download_process = subprocess.Popen(shlex.split(download_cmd))
        download_process.wait()
        downloaded=True
        
    return downloaded, output_file_path


def extract(targz_file_path):
    # extract.
    if targz_file_path.endswith(".tar.gz"):
        print ("Extracting...")
        model_dir = Path(targz_file_path).parent.absolute()
        tar = tarfile.open(targz_file_path, "r:gz")
        tar.extractall(model_dir)
        tar.close()

        h,t = os.path.split(targz_file_path)
        return t
        
    return 
    #Path(output_file_path).unlink()
