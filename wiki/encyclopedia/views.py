from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # if statement checking if the entry after wiki/ is a valid wiki page.
        entries = util.list_entries()
        for entry in entries:
            if title == entry:
            # render entry template with given info from the requested entry.
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry
                })
    # else statement if page doesn't exist     
            else:
                return render(request, "encyclopedia/pageError.html")