from django.shortcuts import render
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # check if the title string is a valid wiki entry.
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })
    # render error if no wiki page exists    
    else:
        return render(request, "encyclopedia/pageError.html")

def search(request):
    if request.method == "POST":
    # entry- what the user types into the search form
        if request.POST.get("q"):
            substring = False
        # get for data 
            searchItem = request.POST.get["q"]
            entry = util.get_entry(searchItem)
            # if searchItem isn't an exact match check for substring matches
            if entry is None:
                results = []
                for title in util.list_entries():
                    if title.find(searchItem) == -1:
                        continue
                    else:
                        results.append(title)
                if results:
                    substring = True  

            #return values from search
            return render(request, "encyclopedia/search.html", {
                "entry": entry,
                "substring": substring,
                "results": results
            })


