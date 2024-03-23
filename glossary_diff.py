from asyncio.subprocess import PIPE
import subprocess
import os
from sys import stdout 

def clone_repo(branch, uri):
    """clone GH repo"""
    if branch != "main":
        if not os.path.isdir("upstream/"):
            cmd_main = ['git', 'clone', '-b', "main", uri, "upstream"]
            subprocess.check_output(cmd_main, stderr=subprocess.DEVNULL)
        if not os.path.isdir(f"{branch}/"):
            cmd_dev = ['git', 'clone', '-b', branch, URI, "dev-pt"]
            subprocess.check_output(cmd_dev, stderr=subprocess.DEVNULL)


def get_uncompleted(upstream_path):
    """get uncompleted definitions"""
    uncompleted = []
    out_uncompleted = []
    cmd_diff = ["grep", "-r", "status: Feedback Appreciated", upstream_path]
    try:
        out = subprocess.run(cmd_diff, stdout=PIPE)
        uncompleted = (out.stdout.decode('ascii')).splitlines()
        for line in uncompleted:
            out_uncompleted.append(line.split(":")[0])
        return out_uncompleted
    except subprocess.CalledProcessError as exception:
        return exception

def diff_metadata():
    """diff repos metadata"""
    only_upstream = []
    diff_dev = []
    cmd_diff = ["diff", "--brief", "upstream/", "dev-pt/"]
    try:
        out = subprocess.run(cmd_diff, stdout=PIPE)
        out_list = (out.stdout.decode('ascii')).splitlines()
        for item in out_list:
            if "Files " in item:
                diff_dev.append(item)
            if "Only in" in item and item:
                only_upstream.append(item)
        return only_upstream, diff_dev
    except subprocess.CalledProcessError as exception:
        return exception


def diff_repo(upstream_path):
    """diff repos"""
    only_upstream = []
    diff_dev = []
    uncompleted_files = get_uncompleted(upstream_path)
    cmd_diff = ["diff", "--brief", "upstream/content/en", "dev-pt/content/en"]

    try:
        out = subprocess.run(cmd_diff, stdout=PIPE)
        out_list = (out.stdout.decode('ascii')).splitlines()
        for item in out_list:
            if "Files " in item and item.split(" ")[1] not in uncompleted_files:
                diff_dev.append(item)
            if "Only in" in item:
                only_upstream.append(item)
        return only_upstream, diff_dev
    except subprocess.CalledProcessError as exception:
        return exception


if __name__ == "__main__":
    REPO_URI = "https://github.com/cncf/glossary.git"
    BRANCH_DEV = "a83e5b0"
    METADATA_LIST = ["upstream/content/en/style-guide/_index.md", "upstream/content/en/_TEMPLATE.md", "upstream/content/en/style-guide/_index.md","upstream/content/en/contributor-ladder/_index.md" ]
    clone_repo(BRANCH_DEV, REPO_URI)
    out_diff = diff_repo("upstream/content/en")

    print("## Updated content")
    for line in out_diff[1]:
        print(line.split(" ")[1])
    print("\n")

    print("## Updated metadata")
    out_diff_mt = diff_metadata()
    for line in out_diff_mt[1]:
        print(line.split(" ")[1])
    print("\n")
