from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
import markdown2
from markdown2 import Markdown

from . import util

class newWikiPageForm(forms.Form):
    newFormTitle = forms.CharField()
    newFormBody = forms.CharField(widget=forms.Textarea)

class editPageForm(forms.Form):
    editTitle = forms.CharField()
    editBody = forms.CharField(widget=forms.Textarea)  

def index(request):
    """ Returns list of all existing Wiki Pages """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """ 
    Returns the selected wiki page 
    
    1. checking validity on request 
    2. if request returns None pageError is returned
    """
    # check if the title string is a valid wiki entry.
    entry = util.get_entry(title)
    md = Markdown()
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(entry),
            "title": title
        })
    # render error if no wiki page exists    
    else:
        return render(request, "encyclopedia/pageError.html")


def search(request):
    """  
    Search for existing Wiki page from string typed in the "Search Encyclopedia" form from side nav bar

    1. if the string is a title of an existing page you are redirected to that page
    2. if the string typed in has any familiarities with ANY page the results will be printed
    """

    # get form data 
    searchItem = request.GET.get("q")
    # if searchItem is an exact match redirect to that page
    if (util.get_entry(searchItem) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={
                    "title": searchItem
        }))
    # add any pages with the string in it to results list    
    else: 
        results = []
        substring = False
        for title in util.list_entries():
            if searchItem.upper() in title.upper():
                results.append(title)
        if results:
            substring = True
        # return results
        return render(request, "encyclopedia/search.html", {
            "searchItem": searchItem,
            "substring": substring,
            "results": results
        })


def newPage(request):
    """ 
    Allow to create a new Wiki page

    1. Render a blank form to input a new entry
    2. Once saved check if all fields are valid 
    3. Check if entry doesn't already exist
    4. Save entry and redirect user to the new Wiki Page
    """
    newForm = newWikiPageForm()
    newFormTitle = newForm["newFormTitle"]
    newFormBody = newForm["newFormBody"]
    if request.method == "POST":
        form = newWikiPageForm(request.POST)
        # check that all fields are filled
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
            # render template again with the inputted data along with a error message    
            else:
                return render(request, "encyclopedia/newPage.html", {
                    "formTitle": title,
                    "formBody": content,
                    "exists": True
                }) 
        # render template again with error message       
        else:  
            return render(request, "encyclopedia/newPage.html", {
                "formTitle": title,
                "formBody": content,
                "exists": False
            })           
    #when 'create new page' button is clicked user is taken to newPage.html
    else:  
        return render(request, "encyclopedia/newPage.html", {
            "formTitle": newFormTitle,
            "formBody": newFormBody,
            "exists": False
        })

def editPage(request, title):
    """ 
    Edit an existing pages data 
    
    1. Render a prefilled form with the already existing data from the Wiki page 
    2. After save check that all fields are filled then replace data and redirect to editted page 
    """
    entry = util.get_entry(title)
    if request.method == "POST":
        # check if the data is valid then save/replace old data
        form = editPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["editTitle"]
            content = form.cleaned_data["editBody"]

            util.save_entry(title, content)

            # take user to their editted page
            return HttpResponseRedirect(reverse("entry", kwargs={
                "title": title
            }))
    # give user a editting form with existing data filled in by defult.        
    else:
        editForm = editPageForm(initial={
            "editTitle": title,
            "editBody": entry
        })
        editFormTitle = editForm["editTitle"]
        editFormBody = editForm["editBody"]
        return render(request, "encyclopedia/editPage.html", {
            "formTitle": editFormTitle,
            "formBody": editFormBody
        })

def randomPage(request):
    """
    Generate a random entry from wiki list 
    """
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("entry", kwargs={
                "title": random.choice(entries)
            }))



    