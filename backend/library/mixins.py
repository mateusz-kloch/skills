from django.shortcuts import redirect


class RedirectAuthenticatedUserMixin:
    """
    Redirects logged in users to index page.
    """
    def dispatch(self, request, *args, **kwargs):
        redirect_to = 'library:index'

        if request.user.is_authenticated:
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
    

class RedirectUnAuthenticatedUserMixin:
    """
    Redirects not logged in users to index page.
    """
    def dispatch(self, request, *args, **kwargs):
        redirect_to = 'library:index'

        if not request.user.is_authenticated:
            return redirect(redirect_to)
        else:
            return super().dispatch(request, *args, **kwargs)
