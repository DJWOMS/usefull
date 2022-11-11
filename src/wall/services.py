

def post_view_count(instance):
    instance.view_count += 1
    instance.save()
    return instance
