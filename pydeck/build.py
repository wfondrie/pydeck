"""
Build a remark slide deck from a markdown file.
"""
import os
import re
import pkgutil

def _add_css(header, css_list, include_css):
    """Add css file links to header"""
    link = "    <link rel=\"stylesheet\" href=\"{}\">\n"
    for css_file in css_list:
        if os.path.splitext(css_file)[1] and not include_css:
            header = header + link.format(css_file)
        else:
            if not os.path.splitext(css_file)[1]:
                css_file = os.path.join("css", css_file + ".css")
                style = pkgutil.get_data("pydeck", css_file).decode()
            else:
                with open(css_file, "r") as style_sheet:
                    style = style_sheet.read()

            header = header + "<style>\n" + style + "</style>\n"

    return header

def _make_remark(param_dict):
    """Turn remark config dictionary into valid JavaScript"""
    remarks = str(param_dict)
    remarks = re.sub(r"'(\w+)':", r"\1:", remarks)
    remarks = re.sub("True", "true", remarks)
    remarks = re.sub("False", "false", remarks)
    return remarks


def deck(boilerplate, markdown, **kwargs):
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
            0 - The HTML header. This is a string with `{title}`
            1 - The HTML ending the header and starting the body.
            2 - The HTML footer. This is a string with `{remarkjs}`
                and `{remark_params}`.

    **kwargs : dict
         These should be the attributes of a Slide_Deck() object.
    """
    if kwargs["mathjax"]:
        mathjax = ("<script src='https://cdnjs.cloudflare.com/ajax/libs/"
                   "mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML&delay"
                   "StartupUntil=configured' type='text/javascript'>"
                   "</script>\n")
        mathjax_config = ("MathJax.Hub.Config({tex2jax:{skipTags:['script',"
                          "'noscript', 'style', 'textarea', 'pre']}});\n"
                          "MathJax.Hub.Configured();\n")
    else:
        mathjax = ""
        mathjax_config = ""

    header = boilerplate[0].format(title=kwargs["title"])
    header = _add_css(header, kwargs["css"], kwargs["self_contained"])
    remark_params = _make_remark(kwargs["remark_config"])
    footer = boilerplate[2].format(remarkjs=kwargs["remarkjs"],
                                   remark_params=remark_params,
                                   mathjax=mathjax,
                                   mathjax_config=mathjax_config)

    html = "".join([header, boilerplate[1], markdown, footer])

    with open(kwargs["html_out"], "w") as out_file:
        out_file.write(html)
