from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

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

    substring = False
    # get form data 
    searchItem = request.GET.get("q")
    entry = util.get_entry(searchItem)
    # if searchItem isn't an exact match check for substring matches
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": searchItem
        })
    else: 
        results = []
        for title in util.list_entries():
            if searchItem.upper() in title.upper():
                results.append(title)
        if results:
            substring = True  
        #return values from search
        return render(request, "encyclopedia/search.html", {
            "searchItem": searchItem,
            "substring": substring,
            "results": results
        })


