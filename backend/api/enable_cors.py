def enable_cors(response):
    """
    Add this as the callback to `after_request` of the API to enable CORS.
    Vue Dev Server and the Flask Server don't run on the same port. As CORS is disabled, the frontend won't be able
    to ping the API in development. Therefore, we enable CORS when in debug mode.

    Warning: Don't use this in production. NOT needed in production as Flask redirects every non-API route to Vue.
    """

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return response
