from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class newWikiPageForm(forms.Form):
    newFormTitle = forms.CharField(label="Title")
    newFormBody = forms.CharField(widget=forms.Textarea, label="Description")

class editPageForm(forms.Form):
    editTitle = forms.CharField(label="Title")
    editBody = forms.CharField(widget=forms.Textarea, label="Description")  

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

        # get form data 
        searchItem = request.GET.get("q")
        # if searchItem isn't an exact match check for substring matches
        if (util.get_entry(searchItem) is not None):
            return HttpResponseRedirect(reverse("entry", kwargs={
                        "title": searchItem
            }))
        else: 
            results = []
            substring = False
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

def newPage(request):
    #when the save btn is pressed run post check
    if request.method == "POST":
        form = newWikiPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["newFormTitle"]
            content = form.cleaned_data["newFormBody"]

            # add new wiki page if page doesn't already exist
            if util.get_entry(title) is None:

                util.save_entry(title, content)

                # take user to their newly created page
                return HttpResponseRedirect(reverse("entry", kwargs={
                    "title": title
                }))
            else:
                return render(request, "encyclopedia/newPage.html", {
                    "form": form,
                    "exists": True,
                    "title": title
                }) 
        else:  
            return render(request, "encyclopedia/newPage.html", {
                "form": form,
                "exists": False
            })           
    #when 'create new page' button is clicked user is taken to newPage.html
    else:  
        return render(request, "encyclopedia/newPage.html", {
            "form": newWikiPageForm(),
            "exists": False
        })

def editPage(request, title):

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["editTitle"]
            content = form.cleaned_data["editBody"]

            util.save_entry(title, content)

            # take user to their editted page
            return HttpResponseRedirect(reverse("entry", kwargs={
                "title": title
            }))
    else:
        form = editPageForm()
        entry = util.get_entry(title)
        form.fields["editTitle"].initial = title
        form.fields["editBody"].initial = entry
        return render(request, "encyclopedia/editPage.html", {
            "form": form,
            "title": form.fields["editTitle"].initial
        })
    