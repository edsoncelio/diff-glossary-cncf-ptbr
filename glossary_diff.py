from asyncio.subprocess import PIPE
import subprocess
import os 

def clone_repo(branch, uri):
    """clone GH repo"""
    if branch != "main":
        if not os.path.isdir("upstream/"):
            cmd_main = ['git', 'clone', '-b', "main", uri, "upstream"]
            subprocess.check_output(cmd_main)
        if not os.path.isdir(f"{branch}/"):
            cmd_dev = ['git', 'clone', '-b', branch, uri, branch]
            subprocess.check_output(cmd_dev)


def get_uncompleted(upstream_path):
    """get uncompleted definitions"""
    uncompleted= []
    cmd_diff = ["grep", "-r", "status: Feedback Appreciated", upstream_path]
    try:
        out = subprocess.run(cmd_diff, stdout=PIPE)
        uncompleted = (out.stdout.decode('ascii')).splitlines()
        return uncompleted
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
            if "Only in" in item:
                only_upstream.append(item)
        return only_upstream, diff_dev
    except subprocess.CalledProcessError as exception:
        return exception


def diff_repo():
    """diff repos"""
    only_upstream = []
    diff_dev = []
    cmd_diff = ["diff", "--brief", "upstream/content/en", "dev-pt/content/en"]

    try:
        out = subprocess.run(cmd_diff, stdout=PIPE)
        out_list = (out.stdout.decode('ascii')).splitlines()
        for item in out_list:
            if "Files " in item:
                diff_dev.append(item)
            if "Only in" in item:
                only_upstream.append(item)
        return only_upstream, diff_dev
    except subprocess.CalledProcessError as exception:
        return exception


if __name__ == "__main__":
    REPO_URI = "https://github.com/cncf/glossary.git"
    BRANCH_DEV = "dev-pt"
    METADATA_LIST = ["upstream/content/en/style-guide/_index.md", "upstream/content/en/_TEMPLATE.md"]
    clone_repo(BRANCH_DEV, REPO_URI)
    out_diff = diff_repo()
    print("English updated content: ")
    for line in out_diff[1]:
        print(line.split(" ")[1])
    print("\n")

    print("Updated metadata: ")
    out_diff_mt = diff_metadata()
    for line in out_diff_mt[1]:
        print(line.split(" ")[1])
    print("\n")
    
    print("Uncompleted files - status: Feedback Appreciated: ")
    out_uncompleted = get_uncompleted("upstream/content/en")
    for line in out_uncompleted:
        if line.split(":")[0] not in METADATA_LIST:
            print(line.split(":")[0])
    print("\n")
        

