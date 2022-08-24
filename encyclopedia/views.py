from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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

