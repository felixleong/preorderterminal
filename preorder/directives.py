import hug


@hug.directive()
def ip_addr(default=None, request=None, **kwargs):
    """
    Directive to access the IP address of the requesting client.
    """
    return request and request.access_route
