from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse
from django.http import JsonResponse

from .models import Gator, Response, Comment

def create(request):

    if request.method == "POST":
        gator_name = request.POST["name"]


def index(request):

    latest_gator_list = Gator.objects.all()[:5]
    context = {
        "latest_gator_list": latest_gator_list
    }

    if request.method == "POST":
        try:
            gator = Gator.objects.get(slug=request.POST['slug'].lower())
            return HttpResponseRedirect(reverse('gator:detail', args=[gator.slug]))
        except Gator.DoesNotExist:
            context["error_message"] = "Sorry, that gator doesn't exist."
            return render(request, "gator/index.html", context)

    return render(request, "gator/index.html", context)


def detail(request, slug):
    gator = get_object_or_404(Gator, slug=slug)

    if request.method == 'POST':
        choice = request.POST['choice']
        new_response = Response(gator=gator, value=choice)
        new_response.save()

        return HttpResponseRedirect(reverse('gator:comment', args=(new_response.id,)))

    choices = Response.Value.choices
    context = {"gator": gator, "choices": choices}
    return render(request, 'gator/detail.html', context)

def comment(request, response_id):

    try:
        comment = Comment.objects.get(rating__id = response_id)
        return HttpResponseRedirect(reverse('gator:index'))
    except Comment.DoesNotExist:
        response = get_object_or_404(Response, pk=response_id)

        if request.method == 'POST':
            comment = request.POST['comment']
            new_comment = Comment(rating=response, text=comment)
            new_comment.save()
            return HttpResponseRedirect(reverse('gator:results', args=[new_comment.rating.gator.slug]))
        return render(request, "gator/comment.html", {"response": response})

def agree(request):
    if request.method == 'GET':
           comment = Comment.objects.get(pk=request.GET['post_id'])
           comment.agree += 1
           comment.save()
           return HttpResponse("Success!") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")

def disagree(request):
    if request.method == 'GET':
           comment = Comment.objects.get(pk=request.GET['post_id'])
           comment.disagree += 1
           comment.save()
           return HttpResponse("Success!") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")

def abuse(request):
    if request.method == 'GET':
           comment = Comment.objects.get(pk=request.GET['post_id'])
           comment.abuse += 1
           comment.save()
           return HttpResponse("Success!") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")
    

def thanks(request):
    return render(request, "gator/thanks.html")

def get_average_rating(ratings):
    values = [float(x.value) for x in ratings]
    print(values, sum(values), len(values))
    return sum(values)/len(values)

def results(request, slug):
    comments = get_list_or_404(Comment, rating__gator__slug=slug)
    comments = [x for x in comments if len(x.text) > 0]
    
    ratings = get_list_or_404(Response, gator__slug=slug)
    mean_rating = get_average_rating(ratings)

    gator = get_object_or_404(Gator, slug=slug)
    context = {
        "gator": gator,
        "comments": comments,
        "mean_rating": mean_rating,
        "total_rating": len(ratings)
    }
    return render(request, "gator/results.html", context)


