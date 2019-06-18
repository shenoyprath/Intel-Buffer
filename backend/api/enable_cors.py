def enable_cors(response):
    """
    Add this as the callback to `after_request` of the API to enable CORS.
    Vue Dev Server and Flask Dev Server don't run on the same port. As CORS is disabled, the frontend won't be able
    to ping the API in development. Therefore, we enable CORS when in debug mode.
    Additionally, this also allows cookies to be shared between the two ports when in development mode.

    Warning: Don't use this in production. NOT needed in production as Flask redirects every non-API route to Vue.

    https://stackoverflow.com/a/33091782
    https://stackoverflow.com/a/14802115
    """

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8080"  # Vue dev server url.
    response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, PATCH, POST, PUT, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, X-CSRF-TOKEN"
    return response
