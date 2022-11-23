from rzn.models import Tasks, TasksKey, TasksData, TasksType, TasksNotice
from users.models import CustomUser
from users.models import CustomUser
from django.db import transaction
import rzn.actions as act

import json

act.completeness_check_all()