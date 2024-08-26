from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

# Create your views here.

# openai_api_key = ''
# openai.api_key = openai_api_key

# def ask_openai(message):
#     response = openai.Completion.create(
#         model = "text-davinci-003",
#         prompt = message,
#         max_tokens = 150,
#         n = 1,
#         stop=None,
#         temprature=0.7,
#     )
  
#     answer = response.choice[0].text.strip()
#     return answer


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    
    if request.method == 'POST':
       message = request.POST.get('message')
       response = 'hi this is ai response to msg'

       chat = Chat(user=request.user ,message=message, response=response, created_at=timezone.now)
       chat.save()
       return JsonResponse({'message': message, 'response' : response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username , password=password)
        if user is None:
            error_message = 'Invalid Password or'
            return render(request, 'login.html', {'error_message' : error_message})
        if not user.is_active:
            return render(request, 'login.html', {'error_message' : error_message})

        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return redirect('chatbot')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error Creating Account'
                return render(request, 'register.html', {'error_message' : error_message})
        else:
            error_message = 'Password Dont match'
            return render(request, 'register.html', {'error_message' : error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')