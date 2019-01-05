"""
Parse a markdown document, taking a YAML header into account. 
"""
def markdown(md_file):
    """
    Read a markdown file.

    Parameters
    ----------
    md_file : str
        A markdown file to parse.

    Returns
    -------
    A tuple containing the markdown body, and the yaml header, if any.
    """
    with open(md_file, "r") as fdata:
        contents = fdata.readlines()

    yaml_end = -1
    if "---" in contents[0]:
        for idx in range(1, len(contents)):
            if "---" in contents[idx]:
                yaml_end = idx
                break

        if yaml_end == -1:
            raise ValueError("Could not find end of YAML header."
                             "Make sure to end header with '---'.")

        yaml = "".join(contents[1:yaml_end])

    else:
        yaml = None

    contents = "".join(contents[(yaml_end+1):])
    return (contents, yaml)
