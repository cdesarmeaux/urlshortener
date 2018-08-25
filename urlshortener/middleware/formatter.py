import json
import falcon


class JSONFormatterMiddleware:
    def process_request(self, req, resp):
        empy_error_message = 'Empty request body. A valid JSON document is required.'
        if req.content_length in (None, 0):
            raise falcon.HTTPBadRequest(empy_error_message)
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(empy_error_message)
        try:
            req.json = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(
                falcon.HTTP_753,
                'Could not decode the request body.'
            )

    def process_response(self, req, resp, resource, req_succeeded):
        native_dict = resp.body
        resp.body = json.dumps(native_dict)
