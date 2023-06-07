from django.shortcuts import render, redirect

def main(request):
    context = { }
    return render(request, "base/main.html", context)

def error(request):
    context = { }
    return render(request, "error.html", context)