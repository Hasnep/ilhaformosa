version_number = "v0.1.104"


def title_print(ruler: str="~"):
    title = " '||' '||  '||                '||''''| \n  ||   ||   || ..    ....      ||  .     ...   ... ..  .. .. ..     ...    ....   .... \n  ||   ||   ||' ||  '' .||     ||''|   .|  '|.  ||' ''  || || ||  .|  '|. ||. '  '' .|| \n  ||   ||   ||  ||  .|' ||     ||      ||   ||  ||      || || ||  ||   || . '|.. .|' || \n .||. .||. .||. ||. '|..'|'   .||.      '|..|' .||.    .|| || ||.  '|..|' |'..|' '|..'|' "
    title_width = max(len(line) for line in title.split("\n"))
    title = ruler * title_width + "\n\n" + title + "\n\n" + ruler * (title_width - len(version_number) - 3) + " " + version_number + " " + ruler
    print(title)
    return
