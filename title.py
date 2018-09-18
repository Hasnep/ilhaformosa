version_number = "v0.1.158"


def title_print(ruler: str="="):
    title = """
'||' '||  '||                '||''''|
 ||   ||   || ..    ....      ||  .     ...   ... ..  .. .. ..     ...    ....   ....
 ||   ||   ||' ||  '' .||     ||''|   .|  '|.  ||' ''  || || ||  .|  '|. ||. '  '' .||
 ||   ||   ||  ||  .|' ||     ||      ||   ||  ||      || || ||  ||   || . '|.. .|' ||
.||. .||. .||. ||. '|..'|'   .||.      '|..|' .||.    .|| || ||.  '|..|' |'..|' '|..'|'
"""
    title_width = max(len(line) for line in title.split("\n"))
    title = ruler * title_width + "\n" + title + "\n" + ruler * (title_width - len(version_number) - 3) + " " + version_number + " " + ruler
    print(title)
    return
