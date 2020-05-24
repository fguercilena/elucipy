from subprocess import run
import json

from pygments.formatters import HtmlFormatter
from pygments.util import get_bool_opt, get_list_opt


class EFormatter(HtmlFormatter):

    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)

        if get_bool_opt(options, "ctags", False):

            files = get_list_opt(options, "files", [])

            try:
                command = "ctags"
                options = ["--fields='+n'", "--output-format=json", "-f -"]
                tagsfile = run([command, *options, *files],
                               capture_output=True, check=True)
                tagsfile = tagsfile.stdout.decode("utf-8")
                tagsfile = "[" + tagsfile.replace("\n", ",")[:-1] + "]"
                data = json.loads(tagsfile)

            except Exception as excp:
                print(excp)
                raise

            tags = {}
            for tag in data:
                if tag["_type"] == "tag":
                    tags[tag["name"]] = tag
                    del tags[tag["name"]]["name"]

            self._ctags = tags
            self.tagurlformat = "%(fname)s.html"
            self.tagsfile = "internal"

    def _lookup_ctag(self, token):

        if token in self._ctags:
            return self._ctags[token]["path"], self._ctags[token]["line"]

        return None, None
