from django.contrib.auth import authenticate, login  # Django's inbuilt authentication methods
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer, CheckMessageSerializer


# Users View
@csrf_exempt  # Make the view csrf exempt.
def user_list(request, pk=None):
    """
    List all users, an unique user or create a new one.
    """
    if request.method == 'GET':
        if pk:  # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)  # Select only that particular user
        else:
            users = User.objects.all()  # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)  # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # On POST, parse the request object to obtain the data in json
        try:
            # serializer = UserSerializer(data=data)  # Serialize the data
            # if serializer.is_valid():
            #     serializer.save()  # Save it if valid
            # return JsonResponse(serializer.data, status=201)  # Return back the data on success
            # return JsonResponse(serializer.errors, status=400)  # Return back the errors  if not valid
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


# Message view
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if sender is None:
            messages = Message.objects.filter(receiver_id=receiver, is_read=False)
            serializer = CheckMessageSerializer(messages, many=True, context={'request': request})
        else:
            messages = Message.objects.filter(receiver_id=receiver, sender_id=sender, is_read=False)
            serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        print('------>', serializer.data)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Login page
def index(request):
    if request.user.is_authenticated:  # If the user is authenticated then redirect to the chat console
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":  # Authentication of user
        username, password = request.POST['username'], request.POST[
            'password']  # Retrieving username and password from the POST data.
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


# Simply render the template
def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


# View for listing the users
def chat_view(request):
    """
    Render the template with required context variables
    """
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        print('será que tá chegando aqui?')
        return render(request, 'chat/chat.html',
                      {
                          'users': User.objects.exclude(
                              username=request.user.username),
                          'is_customer': UserProfile.objects.get(user=User.objects.get(id=request.user.id)).is_customer,
                          'is_waiting' : True
                      })  # Returning context for all users except the current logged-in user


# View to render template for sending and receiving messages
# Takes arguments 'sender' and 'receiver' to identify the message list to return
def message_view(request, sender, receiver):
    """
    Render the template with required context variables
    """
    if not request.user.is_authenticated or (request.user.id != sender and request.user.id != receiver):
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),  # List of users
                       'is_customer': UserProfile.objects.get(user=User.objects.get(id=request.user.id)).is_customer,
                       'is_waiting': False,
                       'receiver': User.objects.get(id=receiver),  # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver,
                                                          receiver_id=sender)})  # Return context with message objects where users are either sender or receiver.
