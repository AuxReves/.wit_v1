import sys
import os
import shutil
from pathlib import Path

def usage(pname):
    print(f"Usage: \n\t{pname} init\n\t{pname} add <absolute_path_to_resource>")

def init():
    # cwd = os.getcwd()
    cwd_imgs = ".wit"
    os.makedirs(cwd_imgs)
    os.chdir(cwd_imgs)
    os.makedirs("images")
    os.makedirs("staging_area")

def add(filepath):  # path can be a directory
    #   assumes path is absolute path, else should throw error

    filepath = Path(filepath)
    parent_dir_path = Path(filepath).parent

    while not (parent_dir_path / ".wit").exists():  #   Find "root" of our version controlled project (closest parent with .wit directory)
        if parent_dir_path == parent_dir_path.parent:
            raise FileNotFoundError("No parent directory containing .wit directory")
        parent_dir_path = Path(parent_dir_path).parent


    # If /absolute/path/to/file is absolute
    # And absolute contains .wit directory
    # Then result of 'add' will be:
    # "/absolute/.wit/staging_area/path/to/file"

    rel_path = filepath.relative_to(parent_dir_path)   
    src = filepath
    dest = parent_dir_path / ".wit/staging_area" / rel_path
    dest = Path(dest)

    #   2 cases handled differently: 1) file    2) direcectory
    if os.path.isfile(filepath):
        shutil.copy(src, dest) # Copy src file to dest

    elif os.path.isdir(filepath):

        if dest.exists():
            shutil.rmtree(dest)

        shutil.copytree(src, dest) # Copy src directory tree to dest
    
    else:
        raise ValueError(f"The path {filepath} is neither a file nor directory!")

def main():
    argv = sys.argv

    if len(argv) < 2:
        usage(argv[0])
    else:
        if argv[1] == "init":
            # check if already initialzed
            init()
        
        if argv[1] == "add":
            add(argv[2])

if __name__ == "__main__":
    main()