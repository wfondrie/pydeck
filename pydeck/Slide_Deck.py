"""
This module defines the Slide_Deck class, which is the main class that
pydeck defines.
"""
import os
import yaml
import livereload
import pydeck.parse
import pydeck.build

class Slide_Deck():
    """The main class of pydeck."""
    __boilerplate = [("<!DOCTYPE html><html><head><title>{title}</title>"
                      "<meta charset='utf-8'>"),
                     "</head><body><textarea id='source'>",
                     ("</textarea><script src='{remarkjs}'></script>"
                      "<script src='https://cdnjs.cloudflare.com/ajax/libs/"
                      "mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML&delay"
                      "StartupUntil=configured' type='text/javascript'>"
                      "</script><script>"
                      "var slideshow = remark.create({remark_params});\n"
                      "MathJax.Hub.Config({{tex2jax:{{skipTags:['script',"
                      "'noscript', 'style', 'textarea', 'pre']}}}});\n"
                      "MathJax.Hub.Configured();\n"
                      "</script></body></html>")]

    def __init__(self,
                 md_file,
                 html_out=None,
                 css=None,
                 include_css=None,
                 title=None,
                 remarkjs=None,
                 remark_config=None):
        """
        Create a new Slide_Deck object.

        A Slide_Deck is defined by a markdown source file
        and the css stylesheet.

        Parameters:
        -----------
        md_file : str
            The markdown source file. This file must conform to
            remark-flavored formatting. Additionally, the markdown
            file may contain a YAML header which can specify any of
            the style and remark configuration options. Options
            specified in the YAML header are always overridden by
            parameters specified in Slide_Deck methods.

        css : list of str
            A list of CSS files that are used to style the slide deck.
            These are applied in the order listed. If `None`, the default
            theme and fonts are used.

        include_css : bool
            Should the CSS style sheets be linked or included in the
            HTML output? Linked style sheets must be available wherever
            you intend to show the presentation. Integrated style sheets
            result in larger html output files, but the styles are
            self-contained in the output HTML. This parameter is ignored
            in the case of built-in themes, which are included in the
            HTML output. This averts the need for pydeck to be installed
            in a location accessible to all created slide decks.
            Default: True.

        title : str
            The title of the webpage. This has no affect on the content
            of the slide deck. Default is "pydeck".

        remarkjs : str
            Specifies where to load the remark library from, even
            locally. Defaults to
            "https://remarkjs.com/downloads/remark-latest.min.js"

        remark_config : dict
            A dictionary specifying additional remark slide deck options.
            These are detailed in full at the `remark wiki
            <https://github.com/gnab/remark/wiki/Configuration>`_. The
            default, `None`, is equivalent to passing::
                {"ratio": "16:9",
                 "navigation": {"scroll": True,
                                "touch": True,
                                "click": False},
                 "countIncrementalSlides": True,
                 "highlighting": {"highlightLanguage": "-"}}
        """
        # TODO: Argument checking
        self.md_file = md_file
        self.passed_params = {"html_out": html_out,
                              "css": css,
                              "include_css": include_css,
                              "title": title,
                              "remarkjs": remarkjs,
                              "remark_config": remark_config}
        self.refresh()

    def refresh(self):
        """
        Parses the markdown file and extracts parameters.

        Using the `refresh()` method reloads the specified `md_file`
        into memory and re-extracts the parameters listed in the YAML
        header. This method is useful when the source markdown file has
        been edited after the creation of the Slide_Deck object.
        """
        params = {}
        markdown, yaml_params = pydeck.parse.markdown(self.md_file)

        if yaml_params is not None:
            yaml_params = yaml.load(yaml_params)
        else:
            yaml_params = {}

        remark_default = {"ratio": "16:9",
                          "navigation": {"scroll": True,
                                         "touch": True,
                                         "click": False},
                          "countIncrementalSlides": True,
                          "highlighting": {"highlightLanguage": "-"}}

        default_md_file = os.path.splitext(self.md_file)[0] + ".html"
        default_params = {"html_out": default_md_file,
                          "css": ["default-fonts", "default"],
                          "include_css": True,
                          "remarkjs": ("https://remarkjs.com/downloads/"
                                       "remark-latest.min.js"),
                          "title": "pydeck",
                          "remark_config": remark_default}

        for param, val in self.passed_params.items():
            if val is not None:
                params[param] = val
            elif param in yaml_params.keys():
                params[param] = yaml_params[param]
            else:
                params[param] = default_params[param]

        self.html_out = params["html_out"]
        self.css = params["css"]
        self.title = params["title"]
        self.include_css = params["include_css"]
        self.remarkjs = params["remarkjs"]
        self.remark_config = params["remark_config"]
        self.markdown = markdown

    def build(self):
        """Build the slide deck from a Slide_Deck object."""
        param_dict = vars(self)
        pydeck.build.deck(self.__boilerplate, **param_dict)

    def serve(self, open_url_delay=1):
        """
        Serve a pydeck slide deck and reload on file changes.

        Parameters
        ----------
        open_url_delay : int
            Open web browser after the delay in seconds.
        """
        def rebuild():
            self.refresh()
            self.build()

        rebuild()
        server = livereload.Server()
        server.watch(self.md_file, rebuild)

        print("Watching:\n{}".format(self.md_file))
        for css in self.css:
            server.watch(css, rebuild)
            print(css)


        print(self.html_out)
        server.serve(open_url_delay=open_url_delay,
                     root=self.html_out)
