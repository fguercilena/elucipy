DOCUMENT_TEMPLATE = r"""
<html>
    <head>
        <title> {0:s} </title>

        <meta http-equiv="content-type" content="text/html; charset=utf-8">

        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6">
        </script>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>

        <link rel="stylesheet" href="{1:s}.css" type="text/css">
    </head>

    <body>

        <h1> {0:s} </h1>

        <p class="intro">
            {2:s}
        </p>

        <table style="width:100%">
            {3:s}
        </table>

    </body>

</html>
"""

ROW_TEMPLATE_RIGHT = r"""
<tr>
    <td style="vertical-align: top">
        {0:s}
    </td>
    <td style="vertical-align: top" class="explanation">
        {1:s}
    </td>
</tr>
"""

ROW_TEMPLATE_LEFT = r"""
<tr>
    <td style="vertical-align: top" class="explanation">
        {0:s}
    </td>
    <td style="vertical-align: top">
        {1:s}
    </td>
</tr>
"""

HEADER_TEMPLATE = r"""
<tr>
    <td style="vertical-align: center; font-variant: small-caps"
        colspan="2" class="explanation">
        <h3> <br> {0:s} </h3>
    </td>
</tr>
"""
