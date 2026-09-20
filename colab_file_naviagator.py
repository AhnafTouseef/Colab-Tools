from pathlib import Path
import shutil
import pandas as pd

def help():
    dictionary = {
        "new_folder(path)": "Create a new folder.",
        "new_file(path)": "Create a new file.",
        "copy(source, destination)": "Copy file or folder.",
        "move(source, destination)": "Move file or folder.",
        "move_from(source, destination)": "Move contents from one folder to another.",
        "copy_from(source, destination)": "Copy contents from one folder to another.",
        "rename(path, new_name)": "Rename a file or folder.",
        "delete(path)": "Delete file or folder.",
        "delete_content(path)": "Delete contents of a folder.",
        "exists(path)": "Check if a path exists.",
        "open_folder(path)": "Return contents of folder.",
        "search(location, keyword)": "Search files and folders.",
        "find(location, extension)": "Find files by extension.",
        "folder_size(path)": "Get size of folder.",
        "properties(path)": "Get properties of file or folder."
    }
    df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Description'])
    return df.style.set_properties(**{'text-align': 'left'})\
             .set_table_styles([dict(selector='th', props=[('text-align', 'left')])])

# -----------------------------
# Create
# -----------------------------

def new_folder(path):
    """
    Create a new folder.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    return f"New folder: {path}"


def new_file(path, content=""):
    """
    Create a new file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return f"New file: {path}"



# -----------------------------
# File operations
# -----------------------------

def copy(source, destination):
    """
    Copy file or folder. Preserves the root folder when copying directories.
    """
    source = Path(source)
    destination = Path(destination) # Convert destination to Path object too

    if source.is_dir():
        # FIX: Append the source folder's name to the destination path
        final_destination = destination / source.name
        shutil.copytree(
            source,
            final_destination,
            dirs_exist_ok=True
        )
    else:
        final_destination = destination
        shutil.copy2(
            source,
            final_destination
        )

    return f"Copied: '{source}' to: '{final_destination}'"



def move(source, destination):
    """
    Move file or folder.
    """
    shutil.move(str(source),str(destination))
    return f"Moved: '{source}' to: '{destination}'"


def move_from(source, destination):
    """
    Move contents from one folder to another.
    """
    try:
          delete(destination+'/.ipynb_checkpoints')
    except:
        pass
    items = list(Path(source).iterdir())
    for item in items:
          move(item, destination)
    return f"Cut to: '{destination}'"


def copy_from(source, destination):
    """
    Copy contents from one folder to another.
    """
    try:
        delete(destination+'/.ipynb_checkpoints')
    except:
      pass
    items = list(Path(source).iterdir())
    for item in items:
        copy(item, destination)
    return f"Copied to: '{destination}'"


def rename(path, new_name):
    """
    Rename a file or folder.
    """

    path = Path(path)

    new_path = path.parent / new_name

    return f" Renamed: '{path}' to: '{path.rename(new_path)}'"



def delete(path):
    """
    Delete file or folder.
    """

    path = Path(path)

    if path.is_dir():
        shutil.rmtree(path)

    else:
        path.unlink()
    return f"Deleted: '{path}'"



def delete_content(path):
    """
    Delete contents of a folder.
    """
    path = Path(path)
    if path.is_dir():
        for item in Path.iterdir(path):
            delete(item)
        return f"Deleted contents of: '{path}'"
    else:
        return f"Not a directory: '{path}'"




# -----------------------------
# Navigation
# -----------------------------

def exists(path):
    return Path(path).exists()



def open_folder(path):
    """
    Return contents of folder.
    """
    File = []
    Address = []
    df = pd.DataFrame(columns=["Address", "Files"])
    try:
        for item in Path(path).iterdir():
            Address.append(str(item))
            File.append(item.name)
        df = pd.DataFrame({"Address": Address, "Files": File})
    except Exception as e:
        print(str(e))
    return df.style.set_properties(subset=['Address', "Files"], **{'text-align': 'left'})\
             .set_table_styles([dict(selector='th', props=[('text-align', 'center')])])



def search(location, keyword):
    """
    Search files and folders.
    """

    results = []

    for item in Path(location).rglob("*"):

        if keyword.lower() in item.name.lower():
            results.append(item)

    return results



def find(location, extension):
    """
    Find files by extension.
    """

    return list(
        Path(location).rglob(f"*.{extension}")
    )



# -----------------------------
# Information
# -----------------------------

def folder_size(path):
    """
    Get size of folder.
    """
    path = Path(path)

    total = 0
    if path.is_dir():
        for item in path.rglob("*"):
            if item.is_file():
                try:
                    total += item.stat().st_size
                except OSError:
                    pass
        print(f"Total size: {total / (1024 * 1024):.2f} MB")
        return total
    else:
        return f"Not a directory: '{path}'"

def properties(path):
    """
    Get properties of file or folder.
    """
    p = Path(path)

    def format_size(size_bytes):
        if size_bytes == 0:
            return "0 B"

        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        i = min(i, len(size_name) - 1)

        value = round(size_bytes / (1024 ** i), 2)

        return f"{value} {size_name[i]}"

    import math

    if p.is_dir():
        size_in_bytes = folder_size(p)
    else:
        size_in_bytes = p.stat().st_size

    return {
        "name": p.name,
        "location": str(p.parent),
        "type": "folder" if p.is_dir() else "file",
        "size": format_size(size_in_bytes)
    }

try:
  delete('/content/sample_data')
except:
  pass

print('''Type "help()" for help''')
