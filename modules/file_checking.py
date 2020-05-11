from re import sub, DOTALL, MULTILINE, compile


def check_file(content, filename):

    elucipy_regex = compile("# elucipy{([^\n]*)}{(.*)}", DOTALL)

    match = elucipy_regex.search(content)

    if match is None:
        return False, None, None, None
    else:
        if match.group(1) == '':
            title = filename
        else:
            title = match.group(1)

        content = sub(elucipy_regex, "", content)

        intro = sub(r"^\s*# ", "", match.group(2), flags=MULTILINE)
        if "NOTE" in intro:
            intro = intro.replace("NOTE", '<span class="note">NOTE</span>')
        if "TODO" in intro:
            intro = intro.replace("TODO", '<span class="todo">TODO</span>')
        if "BUG" in intro:
            intro = intro.replace("BUG", '<span class="bug">BUG</span>')

        return True, content, title, intro
