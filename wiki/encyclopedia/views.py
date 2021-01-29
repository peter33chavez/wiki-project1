from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    #check if the title after "wiki/" is a valid entry.
    entry = util.get_entry(title)
    if entry is not None:
    # render entry template with given info from the requested entry.
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })
# else statement if page doesn't exist     
    else:
        return render(request, "encyclopedia/pageError.html")