DOCUMENT_TEMPLATE = r"""
<!DOCTYPE html>
<html>
    <head>
        <title> {0:s} </title>

        <meta charset="utf-8">

        <meta name="viewport" content="width=device-width">
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js">
        </script>

        <style>
            {1:s}
            * {{ font-size: large }}
            table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
        </style>
    </head>

    <body>

        <h1> {0:s} </h1>

        <!--
        <p class="intro">
        </p>
        -->

        <table style="width:100%">
            {2:s}
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
