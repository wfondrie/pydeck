"""
Build a remark slide deck from a markdown file.
"""
import os
import yaml
import pkgutil
import pydeck.parse as parse

_HEADER = """
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8">
"""

_MD_START = """
  </head>
  <body>
    <textarea id="source">
"""

_FOOTER = """
    </textarea>
    <script src="{remarkjs}">
    </script>
    <script>
      var slideshow = remark.create({remark_params});
    </script>
  </body>
</html>
"""

def build(md_file,
          html_out=None,
          title=None,
          css=None,
          ratio=None,
          navigation=None,
          count_incremental_slides=None,
          highlighting=None,
          remarkjs=None,
          return_params=False):
    """
    Build a slide deck from a markdown file.

    Slides are created using remark. Optional parameters can be included
    either in the function call, or as part of a YAML header in the
    markdown file. In cases where both are present, the former will be
    used.

    Parameters
    ----------
    md_file : str
        The markdown file to make into a slide deck.

    html_out : str
        Specifies the output HTML file (the slide deck). Defaults to
        `md_file`, but with a `.html` extension.

    title : str
        This is just the title of the webpage. It has nothing to
        do with the title slide in your deck. Defaults to `"pydeck"`.

    css : list
        Specifies CSS files to use. The order they are provided will
        be the same in the resulting HTML file.

    ratio : str
        The aspect ratio for slides. The default is `"16:9"`. This
        differs from the remark default of `"4:3"`.

    navigation : dict
        A dictionary of navigation options. Possible keys are `"scroll"`,
        `"touch"`, and `"click"`. All must be boolean values.

    count_incremental_slides : bool
        Should incremental slides count toward slide numbers? The
        default is `True`.

    highlighting : dict
        Controls code highlighting. Code highlighting is performed
        using Highlight.js. Possible keys are "highlightLanguage",
        "highlightStyle", "highlightLines", and "highlightSpans".
        For details on their possible values, see the `remark wiki
        <https://github.com/gnab/remark/wiki/Configuration>`_.
        Defaults to no code highlighting.

    remarkjs : str
        Specifies where to load the remark library from, even locally.
        Defaults to
        "https://remarkjs.com/downloads/remark-latest.min.js"
    """
    _build(return_params=False,
           md_file=md_file,
           html_out=html_out,
           title=title,
           css=css,
           ratio=ratio,
           navigation=navigation,
           count_incremental_slides=count_incremental_slides,
           highlighting=highlighting,
           remarkjs=remarkjs)


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
    incr = str(param_dict["count_incremental_slides"]).lower()
    remarks = ("ratio: '{}', ".format(param_dict["ratio"])
               + "countIncrementalSlides: {}, ".format(incr))

    nav = [k + ": " +  str(v).lower() for k, v
           in param_dict["navigation"].items()]
    remarks += ("navigation: {" + ", ".join(nav) + "}, ")

    hl = [k + ": '" + v + "'" for k, v
          in param_dict["highlighting"].items()]
    remarks += ("highlighting: {" + ", ".join(hl) + "}")
    remarks = "{" + remarks + "}"
    return remarks


def _build(return_params, **kwargs):
    """
    The workhorse of the build function.

    Takes the parameters of the pydeck.build(), creates a remark
    slide deck from a markdown file, and optionally returns
    the paramaters used.

    Parameter
    ---------
    return_params : bool
        Should the the final parameters be returned as a dictionary?
        By default this is False, but it can be useful for debugging
        a presentation.
    """
    md_file = kwargs['md_file']
    params = kwargs

    markdown, yaml_params = parse.markdown(md_file)
    if yaml_params is not None:
        yaml_params = yaml.load(yaml_params)
    else:
        yaml_params = {}

    default_params = {"html_out": os.path.splitext(md_file)[0] + ".html",
                      "css": ["default-fonts"],
                      "remarkjs": ("https://remarkjs.com/downloads/"
                                   "remark-latest.min.js"),
                      "title": "pydeck",
                      "ratio": "16:9",
                      "navigation": {"scroll": True,
                                     "touch": True,
                                     "click": False},
                      "count_incremental_slides": True,
                      "highlighting": {"highlightLanguage": "-"}}

    for param, vals in default_params.items():
        if param in params.keys():
            if params[param] is not None:
                continue
        elif param in yaml_params.keys():
            params[param] = yaml_params[param]
        else:
            params[param] = default_params[param]
            
    header = _HEADER.format(title=params["title"])
    header = _add_css(header, params["css"])

    remark_params = _make_remark(params)
    footer = _FOOTER.format(remarkjs=params["remarkjs"],
                            remark_params=remark_params)

    html = "".join([header, _MD_START, markdown, footer])

    with open(params["html_out"], "w") as out_file:
        out_file.write(html)

    if return_params:
        return params
