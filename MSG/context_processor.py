from django.db.models import Q

from .models import *

def Instances(request):
    context = dict()
    if request.user.is_authenticated:
        user = request.user
        sentRequests = FriendRequest.objects.filter(sender__user=user, isAccepted__exact=True)
        receivedRequests = FriendRequest.objects.filter(receiver__user=user, isAccepted__exact=True)
        profiles = Profile.objects.filter(Q(user_id__in=sentRequests.values('receiver__user_id'))|Q(user_id__in=receivedRequests.values('sender__user_id')))
        context['profiles'] = profiles
    return context