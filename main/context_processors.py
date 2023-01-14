def group_processor(request):

    user=request.user
    if user.is_superuser:
        group="commercial"
    elif user.is_authenticated:
        if user.groups.filter(name='teacher').exists():
            group = "teacher"
        elif user.groups.filter(name='learner').exists():
            group = "learner"
        elif user.groups.filter(name='commercial').exists():
            group = "commercial"
    else:
        group=""
    return {
        'group': group
    }