

class ToolbarEditMiddleware:
    """
    current state: not needed!
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # TODO: do we really need this in a middleware!?
        # same code in template tag, for now.
        if 'edit' in request.GET:
            request.session['cms_toolbar_edit'] = True
        if 'edit_off' in request.GET:
            request.session['cms_toolbar_edit'] = False

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
