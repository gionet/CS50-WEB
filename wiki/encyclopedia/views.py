import random

from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    textarea = forms.CharField(label="Text Area", widget=forms.Textarea(attrs={'class': 'form-control'}))
    

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    html_content = md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": f"The title {title} is not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title, 
            "content": html_content
        })

def search(request):
    if request.method == "GET":
        title = request.GET.get('q', '')
        
        value = md_to_html(title)
        if value is not None:
            return HttpResponseRedirect(reverse('entry', args=[title]))
            
        else:
            entries = util.list_entries()
            substring = []
            for entry in entries:
                if title.lower() in entry.lower():
                    substring.append(entry)
            return render(request, "encyclopedia/search.html", {
                "substring": substring
            })
            
def newpage(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['textarea']
            exist = util.get_entry(title)
            if exist is not None:
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "message": f"There is an existing file with title {title}."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=[title]))
    
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            "form": NewTaskForm()
        })
        
def edit(request):
    if request.method == "GET":
        title = request.GET.get('title', '')
        form = NewTaskForm(initial={
            'title': title, 
            'textarea': util.get_entry(title)
        })
        
        form.fields['title'].widget.attrs['hidden'] = 'True'
        
        return render(request, "encyclopedia/edit.html", {
                "form": form,
        })
    
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['textarea']
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))    
        
def random_page(request):
    title = random.choice(util.list_entries())
    print(title)
    html_content = md_to_html(title)
    return render(request, "encyclopedia/random.html", {
            "title":title, 
            "content": html_content
        })