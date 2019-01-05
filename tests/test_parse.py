"""
This file contains the tests for the markdown parsing function.
"""
import os
import pytest
import pydeck.parse

YAML = ["---\n",
        "test: yes\n",
        "---\n"]

MD_CONTENT = ["# Test Header First Line  \n",
              "Some content  \n",
              "---\n",
              "A second slide  \n",
              "The last line."]

def _make_parse(md_data, tmpdir):
    """Creates a temporary markdown file and parses it."""
    md_file = os.path.join(tmpdir.strpath, "test.md")
    with open(md_file, "w") as md_handle:
        md_handle.write(md_data)

    return pydeck.parse.markdown(md_file)


def test_bare_md(tmpdir):
    """Test parsing of a markdown file without a YAML header"""
    md_data = "".join(MD_CONTENT)
    md_parsed, yaml_parsed = _make_parse(md_data, tmpdir) 

    assert yaml_parsed is None
    assert md_parsed == "".join(MD_CONTENT)


def test_yaml_md(tmpdir):
    """Test parsing of a markdown file with a YAML header"""
    md_data = "".join(YAML + MD_CONTENT)
    md_parsed, yaml_parsed = _make_parse(md_data, tmpdir)

    assert yaml_parsed == YAML[1]
    assert md_parsed == "".join(MD_CONTENT)

def test_no_yaml_end(tmpdir):
    """Test that an error occurs if YAML header is not closed"""
    md_oneslide = "".join(YAML[:2] + MD_CONTENT[:2])
    with pytest.raises(ValueError):
        _, _ = _make_parse(md_oneslide, tmpdir)

    # Unfortunately, right now the error will not catch a missing YAML
    # for a markdown file with more than one slide. This is because the
    # remark.js slide delimiter is a '---' as well. ¯\_(ツ)_/¯
    md_twoslide = "".join(YAML[0:2] + MD_CONTENT)
    md_parsed, yaml_parsed = _make_parse(md_twoslide, tmpdir)
    assert yaml_parsed == "".join(YAML[1:2] + MD_CONTENT[:2])
    assert md_parsed == "".join(MD_CONTENT[3:])
