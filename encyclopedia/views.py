from http.client import HTTPResponse
from logging import PlaceHolder
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse 

from . import util

class NewQueryForm(forms.Form):
    query=forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Wikipedia', 'style': 'width:100%'}))

class NewEntryForm(forms.Form):
    title=forms.CharField(label="Title")
    content=forms.CharField(label="Content", widget=forms.Textarea(attrs={'name': 'content', 'rows':2, 'cols':1 }))

class NewEditForm(forms.Form):
    edit=forms.CharField(label="Edit Content", widget=forms.Textarea(attrs={'name': 'content', 'rows':2, 'cols':1 }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewQueryForm()
    })

def get_page(request, title):
    
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": NewQueryForm()
        })
    
    return render(request, "encyclopedia/page.html",{
        "title": title,
        "content": content,
        "form": NewQueryForm()
    })

def search(request):
    if request.method == "POST":

        all_entries = util.list_entries()
        found_entries = []

        form = NewQueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in all_entries:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)                    
                    return HttpResponseRedirect(reverse("title", args=[title]))
                
                if query.lower() in entry.lower():
                    found_entries.append(entry)
            return render(request, 'encyclopedia/search.html', {
                "results": found_entries,
                "query": query,
                "form": NewQueryForm()
            })
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": NewQueryForm()
    })

def create(request):
    if request.method == "POST":
        all_entries=util.list_entries()

        form = NewEntryForm(request.POST)
        if form.is_valid():
            new_title=form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]

            for entry in all_entries:
                if new_title.lower() == entry.lower():
                    return render(request, "encyclopedia/create.html",{
                        "form": NewQueryForm(),
                        "entry_form": NewEntryForm(),
                        "exists": True,
                        "wiki_entry": entry
                    })

            util.save_entry(new_title, new_content)
            return render(request, 'encyclopedia/page.html',{
                "form": NewQueryForm(),
                "title": new_title,
                "content": new_content
            })

    return render(request, "encyclopedia/create.html",{
        "form": NewQueryForm(),
        "entry_form": NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": NewQueryForm(),
            "edit_form": NewEditForm(),
            "title": title,
            "content": content
        })