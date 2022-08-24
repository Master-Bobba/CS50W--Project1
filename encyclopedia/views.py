from http.client import HTTPResponse
from logging import PlaceHolder
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse 

from . import util

class NewTaskForm(forms.Form):
    query=forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Wikipedia', 'style': 'width:100%'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })

def get_page(request, title):
    
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    return render(request, "encyclopedia/page.html",{
        "title": title,
        "content": content
    })

def search(request):
    if request.method == "POST":

        all_entries = util.list_entries()
        found_entries = []

        form = NewTaskForm(request.POST)
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
                "form": NewTaskForm()
            })
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": NewTaskForm()
    })