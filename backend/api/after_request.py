from api import api_bp


@api_bp.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
