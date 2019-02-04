import json

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from MSG.models import Profile, FriendRequest, Message
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'MSG/index.html')


def chatters(request):
    return render(request, 'MSG/chatters.html')


def messages(request, user_id):
    data = dict()
    if request.method == "POST":
        user = request.user
        friend_user = User.objects.get(id=user_id)
        friend = friend_user.profile
        data['user_id'] = mark_safe(json.dumps(user.id))
        data['p'] = friend
        messages = Message.objects.filter(
            Q(sender_id__exact=user.profile.id) | Q(receiver_id__exact=user.profile.id),
            Q(sender_id__exact=friend.id) | Q(receiver_id__exact=friend.id)).order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(messages, 10)
        try:
            data['messages'] = paginator.page(page)
        except PageNotAnInteger:
            data['messages'] = paginator.page(1)
        except EmptyPage:
            data['messages'] = paginator.page(paginator.num_pages)

        data['messages'] = messages
        template = render_to_string('MSG/includes/chat_box.html', data, request)
        print(data)
        return JsonResponse(template, safe=False)

def disconnect(request):
    if request.user.is_authenticated:
        p = request.user.profile
        p.isOnline = False
        p.disconnect()
        p.save()
        return HttpResponse('Disconnected')

def unread_messages(request, user_id):
    if request.user.is_authenticated:
        data = dict()
        friend = User.objects.get(id=user_id).profile
        data['unread_messages_count'] = Message.objects.filter(Q(receiver=friend)|Q(sender=friend), Q(receiver=request.user.profile)|Q(sender=request.user.profile), isRead=False).count()
        return JsonResponse(data, safe=False)

def read_messages(request, user_id):
    if request.user.is_authenticated:
        data = dict()
        friend = User.objects.get(id=user_id).profile
        msgs = Message.objects.filter(receiver=request.user.profile, sender=friend, isRead=False)
        for msg in msgs:
            msg.isRead = True
            msg.save()
        data['status'] = True
        data['unread_messages_counter'] = Message.objects.filter(receiver=request.user.profile, sender=friend, isRead=False).count()
        return JsonResponse(data, safe=False)






