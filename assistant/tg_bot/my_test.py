from rzn.models import TasksKey

a: TasksKey = TasksKey.objects.get(id=14)
print(a.value)
