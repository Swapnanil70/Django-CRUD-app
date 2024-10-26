from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweet_list = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweet_list})

@login_required
def tweet_create(request):
    # If case meh kya data aa raha hai form me seh
    """
    View to create a tweet

    If the request is a POST request, then the form is validated. If the form is valid, the tweet is saved in the database
    and the user is redirected to the tweet list page. If the form is not valid, the form is rendered again with the
    validation errors.

    If the request is a GET request, a blank form is rendered.

    :param request: The request object
    :return: The rendered template
    """
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save() # Save the tweet in db
            return redirect('tweet_list') # redirect to the tweet list method above 
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    """
    View to edit a tweet
    
    If the request is a POST request, then the form is validated. If the form is valid, the tweet is saved in the database
    and the user is redirected to the tweet list page. If the form is not valid, the form is rendered again with the
    validation errors.
    
    If the request is a GET request, the form is rendered with the tweet's data populated in the fields.
    
    :param request: The request object
    :param tweet_id: The ID of the tweet to be edited
    :return: The rendered template
    """
    
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    # If case meh kya data aa raha hai form me seh
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save() # Save the tweet in db
            return redirect('tweet_list') # redirect to the tweet list method above 
    else:
        form = TweetForm(instance=tweet)
        
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    """
    View to delete a tweet

    :param request: The request object
    :param tweet_id: The ID of the tweet to be deleted
    :return: A redirect to the tweet list page
    """
    
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    """
    View to handle user registration
    
    If the request is a POST request, the form is validated. If the form is valid, the user is created in the database,
    the user is logged in, and the user is redirected to the tweet list page. If the form is not valid, the form is 
    rendered again with the validation errors.
    
    If the request is a GET request, a blank form is rendered.
    
    :param request: The request object
    :return: The rendered template
    """
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegisterForm()
        
    return render(request, 'registration/register.html', {'form': form})