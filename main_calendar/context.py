def my_cp(request):
    ctx = {
        "logged_user":request.user
    }
    return ctx