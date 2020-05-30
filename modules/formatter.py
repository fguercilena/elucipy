import json

from pygments.formatters import HtmlFormatter


class EFormatter(HtmlFormatter):

    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)

        self.ctagsfile = options.get("ctagsfile", None)

        if self.ctagsfile is not None:

            # ctags --fields='+n' --output-format=json -f ctagsfile
            with open(self.ctagsfile, 'r') as inctags:
                tmp = inctags.readlines()

            tags = {}
            for tag in tmp:
                tag = json.loads(tag)
                if tag["_type"] == "tag":
                    tags[tag["name"]] = tag
                    del tags[tag["name"]]["name"]

            self._ctags = tags
            self.tagurlformat = "%(fname)s%(fext)s.html"
            self.tagsfile = "placeholder"

    def _lookup_ctag(self, token):

        if token in self._ctags:
            return self._ctags[token]["path"], self._ctags[token]["line"]

        return None, None
