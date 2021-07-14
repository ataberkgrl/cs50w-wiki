from django.shortcuts import render, redirect
from django.http import Http404
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    if request.method == "POST":
        title = request.POST.get("title")
        if util.get_entry(title) != None:
            return HttpResponse("<h1>A page with this title already exists</h1>")
        else:
            content = request.POST.get("content")
            util.save_entry(title, content)
            return redirect("index")

def edit_page(request, article):
    if request.method == "GET":
        content = util.get_entry(article)
        if content != None:
            return render(request, "encyclopedia/edit.html", {
                "title": article,
                "content": content
            })
        else:
            return HttpResponse("<h1>A page doesn't exist</h1>")
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(article, new_content)
        return redirect("/wiki/" + article)

def article(request, article):
    content = util.get_entry(article)
    if content == None:
        raise Http404("Article doesn't exist")
    context = {
        "article_name": article,
        "content": util.MarkdownToHTML(content)
    }
    return render(request, "encyclopedia/article.html", context)

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        search_result = util.search(query)
        print(search_result)
        if isinstance(search_result, list):
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": search_result
            })
        elif isinstance(search_result, str):
            content = util.get_entry(search_result)
            if content == None:
                raise Http404("Article doesn't exist")
            context = {
                "article_name": search_result,
                "content": util.MarkdownToHTML(content)
            }
            return render(request, "encyclopedia/article.html", context)

def random_page(request):
    page_list = util.list_entries()
    return article(request, page_list[random.randint(0, len(page_list) - 1)])


