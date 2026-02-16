import os
import subprocess
from urllib.parse import urlparse

BASE_REPO_DIR = "../../data/repos"

def extract_repo_name(repo_url:str)->str:
    path = urlparse(repo_url).path
    repo_name = path.strip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return repo_name

def clone_repo(repo_url:str)->str:
    repo_name = extract_repo_name(repo_url)
    local_repo_path = os.path.join(BASE_REPO_DIR,repo_name)

    os.makedirs(BASE_REPO_DIR,exist_ok=True)

    if os.path.exists(local_repo_path):
        return local_repo_path
    
    try:
        subprocess.run(
            ['git','clone',repo_url,local_repo_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"failed to clone repo : {e.stderr.decode()}")
    
    return local_repo_path