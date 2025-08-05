"""Tasks models."""

import logging

from django.db import models

from accounts.models import Profile
from polymorphic.models import PolymorphicModel
# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your models here.
