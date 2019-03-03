from webargs.flaskparser import abort, parser


@parser.error_handler
def handle_error(error, _request, _schema, status_code, _error_headers):
    abort(status_code, errors=error.messages)
