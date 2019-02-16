from webargs.flaskparser import abort, parser


# noinspection PyUnusedLocal
@parser.error_handler
def handle_error(error, request, schema, status_code, error_headers):
    abort(status_code, errors=error.messages)
