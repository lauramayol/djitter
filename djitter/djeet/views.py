from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Djeet


@login_required
def feed(request):
    userids = []
    for id in request.user.djeeterprofile.follows.all():
        userids.append(id.id)

    userids.append(request.user.id)
    djeets = Djeet.objects.filter(user_id__in=userids)[:25]

    return render(request, 'feed.html', {'djeets': djeets})
