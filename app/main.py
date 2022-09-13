import falcon
import json

from falcon_cors import CORS


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body', 
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource, req_succeeded):
            if not hasattr(resp.context, 'result'):
                    return

            resp.body = json.dumps(resp.context.result)

class HelloWorldResource:

    def on_get(self, request, response):

        response.media = ('Hello World from Falcon Python with' +
                          ' Gunicorn running in an Alpine Linux container.')

# Sample resource from the docs to test the api is running correctly.
class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'I\'ve always been more interested in the future than in the past.',
            'author': 'Grace Hopper'
        }

        resp.body = json.dumps(quote)

cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True
)

# this can't be in __main__ for some reason...TODO find out why
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
    cors.middleware
    ])

app.add_route('/', HelloWorldResource())
app.add_route('/quote', QuoteResource())

if __name__ == 'model_server':  
        # we expect, as a hand-shake agreement, that there is a .yml config file in top level of lib/configs directory
        config_dir = os.path.join('.')
        yaml_path = os.path.join(config_dir, 'model_server.yml')
        with open(yaml_path, "r") as stream:
                config = yaml.load(stream)
