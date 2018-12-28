"""
Rebuild and reload a presentation after a change to the markdown
or CSS dependencies.
"""
import livereload
from pydeck.build import _build

def serve(md_file, open_url_delay=5, **kwargs):
    """
    Serve a pydeck slide deck and reload on file changes.
    """
    build_params = _build(return_params=True,
                          md_file=md_file,
                          **kwargs)

    def rebuild():
        """Rebuild the slide decks"""
        _build(return_params=False,
               **build_params)

    server = livereload.Server()
    server.watch(md_file, rebuild)
    for css in build_params["css"]:
        server.watch(css, rebuild)

    server.serve(open_url_delay=open_url_delay,
                 root=build_params["html_out"])

