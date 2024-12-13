

import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')
