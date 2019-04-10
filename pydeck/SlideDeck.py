"""
This module defines the Slide_Deck class, which is the main class that
pydeck defines.
"""
import os
import logging
import yaml
import livereload
import pydeck.parse
import pydeck.build

class SlideDeck():
    """The main class of pydeck."""
    __boilerplate = [("<!DOCTYPE html><html>\n<head>\n<title>{title}</title>"
                      "\n<meta charset='utf-8'>\n"),
                     "</head>\n<body>\n<textarea id='source'>\n",
                     ("</textarea>\n<script src='{remarkjs}'></script>\n"
                      "{mathjax}<script>\n"
                      "var slideshow = remark.create({remark_params});\n"
                      "{mathjax_config}"
                      "</script>\n</body>\n</html>")]

    def __init__(self, md_file: str):
        """
        Create a new Slide_Deck object.

        A Slide_Deck is defined by a markdown source file
        and the css stylesheet.

        Parameters:
        -----------
        md_file : str
            The markdown source file. This file must conform to
            remark-flavored formatting. This markdown file can
            optionally have a YAML header with the following fields:

                css: A list of CSS files to be used to style the slide
                    deck. These are applied in the order listed. CSS files
                    that are included with pydeck should be listed without
                    a path or extension.
                    The default is ["default-fonts", "default"]

                js: A list of JavaScript files to include. These typically
                    define new remark macros.

                self_contained: Boolean indicating if the CSS style sheets
                    and the JavaScript files should be embedded in the
                    resulting HTML file.

                title: A string to used as the webpage title. This has no
                     effect on the actual presentation.

                remarkjs : Specifies where to load the remark library from,
                    even locally. Defaults to
                    "https://remarkjs.com/downloads/remark-latest.min.js"

               remark_config : Specify additional remark slide deck options.
                   These are detailed in full at the `remark wiki
                   <https://github.com/gnab/remark/wiki/Configuration>`.
        """
        self.md_file = md_file
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
                          "js": None,
                          "self_contained": True,
                          "mathjax": True,
                          "remarkjs": ("https://remarkjs.com/downloads/"
                                       "remark-latest.min.js"),
                          "title": "pydeck",
                          "remark_config": remark_default}

        for param, val in default_params.items():
            if param in yaml_params.keys():
                params[param] = yaml_params[param]
            else:
                params[param] = val

        self.params = params
        self.markdown = markdown

    def build(self):
        """Build the slide deck from a Slide_Deck object."""
        pydeck.build.deck(self.__boilerplate, self.markdown, **self.params)

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

        logging.info("Watching:\n%s", self.md_file)
        for css in self.params["css"]:
            if os.path.splitext(css)[1]:
                logging.info("%s", css)
                server.watch(css, rebuild)

        server.serve(open_url_delay=open_url_delay,
                     root=self.params["html_out"])
