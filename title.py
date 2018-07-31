version_number = "v0.1.095"


def title_print(ruler="~"):
    title = " '||' '||  '||                '||''''| \n  ||   ||   || ..    ....      ||  .     ...   ... ..  .. .. ..     ...    ....   .... \n  ||   ||   ||' ||  '' .||     ||''|   .|  '|.  ||' ''  || || ||  .|  '|. ||. '  '' .|| \n  ||   ||   ||  ||  .|' ||     ||      ||   ||  ||      || || ||  ||   || . '|.. .|' || \n .||. .||. .||. ||. '|..'|'   .||.      '|..|' .||.    .|| || ||.  '|..|' |'..|' '|..'|' "
    title_width = max(len(line) for line in title.split("\n")) - 1
    title = ruler * title_width + "\n\n" + title + "\n\n" + ruler * (title_width - len(version_number) - 2) + " " + version_number + " " + ruler
    print(title)
