import json
import os
import shutil
import subprocess
import re

import zlib
from pathlib import Path


def make_file(path):
    if not os.path.exists(path):
        with open(path, 'w'):
            print(" [*] Make a file : {}".format(path))
            pass


def make_dir(path):
    if not os.path.exists(path):
        print(" [*] Make directories : {}".format(path))
        os.makedirs(path)


def remove_file(path):
    if os.path.exists(path):
        print(" [*] Removed: {}".format(path))
        os.remove(path)


def remove_dir(path):
    if os.path.exists(path):
        print(" [*] Removed: {}".format(path))
        shutil.rmtree(path)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


def load_json(path):
    with open(path) as f:
        data = json.loads(f.read())
    return data


def get_json_headers_with_token(token):
    try:
        authentication = 'token ' + token
    except TypeError:
        print('Token is not set!')
        return

    headers = {
        'Content-Type': 'application/json',
        'Authentication': authentication
    }

    return headers


def calculate_crc32c(filename):
    with open(filename, 'rb') as fh:
        h = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            h = zlib.crc32(s, h)
        return "%X" % (h & 0xFFFFFFFF)


def read_in_chunks(filename, blocksize=65535, chunks=-1):
    """Lazy function (generator) to read a file piece by piece."""
    with open(filename, 'rb') as f:
        while chunks:
            data = f.read(blocksize)
            if not data:
                break
            yield data
            chunks -= 1


def wait_all_futures(futures):
    return [future.result() for future in futures]


def get_github_repo():
    origin = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).strip().decode('utf-8')
    regex = re.compile(r'((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?')
    repo = regex.search(origin).group(7).split('/')
    # TODO: check github path
    return repo[-2], repo[-1]


def get_active_branch_name():
    head_dir = Path(".") / ".git" / "HEAD"
    with head_dir.open("r") as f:
        content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode("utf-8")


def is_committed():
    from git import Repo
    repo = Repo(search_parent_directories=True)
    changed_files = [item.a_path for item in repo.index.diff(None)]
    for file in changed_files:
        if file == 'savvihubfile.yml' or file == '.gitignore':
            continue
        else:
            return False
    return True