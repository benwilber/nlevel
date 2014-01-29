
from flask import Flask
from flask.ext.restful import Api, Resource, request

import redis

import nlevel

app = Flask(__name__)
api = Api(app)

r = redis.Redis()

def flat_dict(d):
    return {k: v[0] for k, v in dict(d).items()}

class NodeListResource(Resource):

    def get(self, key=None):
        if key:
            return nlevel.nodes(r, key)
        else:
            return nlevel.roots(r)

    def post(self, key=None):
        info = flat_dict(request.form)
        node_key = nlevel.node(r, info, parent=key)
        return nlevel.info(r, node_key)


class NodeInfoResource(Resource):

    def get(self, key):
        return nlevel.info(r, key)

api.add_resource(NodeListResource,
        '/api/v1/nodes',
        '/api/v1/nodes/<string:key>/nodes')

api.add_resource(NodeInfoResource,
        '/api/v1/nodes/<string:key>')

if __name__ == '__main__':
    app.run(debug=True)