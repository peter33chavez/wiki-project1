from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    #check if the title string is a valid wiki entry.
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })
    # render error if no wiki page exists    
    else:
        return render(request, "encyclopedia/pageError.html")

