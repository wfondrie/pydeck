"""
Build a remark slide deck from a markdown file.
"""
import os
import pkgutil

def _add_css(header, css_list):
    """Add css file links to header"""
    link = "    <link rel=\"stylesheet\" href=\"{}\">\n"
    for css_file in css_list:
        if not os.path.splitext(css_file)[1]:
            filepath = os.path.join("css", css_file + ".css")
            style = pkgutil.get_data("pydeck", filepath).decode()
            header = header + "<style>\n" + style + "</style>\n"
        else:
            header = header + link.format(css_file)

    return header


def _make_remark(param_dict):
    """Turn parameter dictionary into array for remark.create()"""
    incr = str(param_dict["countIncrementalSlides"]).lower()
    remarks = ("ratio: '{}', ".format(param_dict["ratio"])
               + "countIncrementalSlides: {}, ".format(incr))

    nav = [k + ": " +  str(v).lower() for k, v
           in param_dict["navigation"].items()]
    remarks += ("navigation: {" + ", ".join(nav) + "}, ")

    highlight = [k + ": '" + v + "'" for k, v
                 in param_dict["highlighting"].items()]
    remarks += ("highlighting: {" + ", ".join(highlight) + "}")
    remarks = "{" + remarks + "}"
    return remarks


def deck(boilerplate, **kwargs):
    """
    The workhorse of the build function.

    Takes the parameters of the pydeck.build(), creates a remark
    slide deck from a markdown file, and optionally returns
    the paramaters used.

    Parameter
    ---------
    boilerplate : list
        List containing the boilerplate HTML needed to make a remark
        presentation. The elements are in the following order:
            0 - The HTML header. This is an f-string with `{title}`
            1 - The HTML ending the header and starting the body.
            2 - The HTML footer. This is an f-string with `{remarkjs}`
                and `{remark_params}`.

    **kwargs : dict
         These should be the attributes of a Slide_Deck() object.
    """
    header = boilerplate[0].format(title=kwargs["title"])
    header = _add_css(header, kwargs["css"])

    remark_params = _make_remark(kwargs["remark_config"])
    footer = boilerplate[2].format(remarkjs=kwargs["remarkjs"],
                                   remark_params=remark_params)

    html = "".join([header, boilerplate[1], kwargs["markdown"], footer])

    with open(kwargs["html_out"], "w") as out_file:
        out_file.write(html)
