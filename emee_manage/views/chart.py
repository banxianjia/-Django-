from django.shortcuts import render,redirect,HttpResponse

def chart_list(req):
    return render(
        req,
        "chart_list.html",
        {
            "req":req,
        }
    )