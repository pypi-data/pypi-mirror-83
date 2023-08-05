import json
import logging
import copy
from actingweb import auth
from actingweb.handlers import base_handler


def merge_dict(d1, d2):
    """ Modifies d1 in-place to contain values from d2.

    If any value in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    Thanks to Edward Loper on stackoverflow.com
    """
    for k, v2 in list(d2.items()):
        v1 = d1.get(k)  # returns None if v1 has no value for this key
        if isinstance(v1, dict) and isinstance(v2, dict):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


def delete_dict(d1, path):
    """ Deletes path (an array of strings) in d1 dict.

    d1 is modified to no longer contain the attr/value pair
    or dict that is specified by path.
    """
    if not d1:
        # logging.debug('Path not found')
        return False
    # logging.debug('d1: ' + json.dumps(d1))
    # logging.debug('path: ' + str(path))
    if len(path) > 1 and path[1] and len(path[1]) > 0:
        return delete_dict(d1.get(path[0]), path[1:])
    if len(path) == 1 and path[0] and path[0] in d1:
        # logging.debug('Deleting d1[' + path[0] + ']')
        try:
            del d1[path[0]]
            return True
        except KeyError:
            return False
    return False


class PropertiesHandler(base_handler.BaseHandler):

    def get(self, actor_id, name):
        if self.request.get('_method') == 'PUT':
            self.put(actor_id, name)
            return
        if self.request.get('_method') == 'DELETE':
            self.delete(actor_id, name)
            return
        (myself, check) = auth.init_actingweb(appreq=self,
                                              actor_id=actor_id, path='properties', subpath=name,
                                              config=self.config)
        if not myself or check.response["code"] != 200:
            return
        if not name:
            path = {0: None}
        else:
            path = name.split('/')
            name = path[0]
        if not check.check_authorisation(path='properties', subpath=name, method='GET'):
            self.response.set_status(403)
            return
        # if name is not set, this request URI was the properties root
        if not name:
            self.listall(myself)
            return
        lookup = myself.property[name]
        if not lookup:
            self.response.set_status(404, "Property not found")
            return
        try:
            jsonblob = json.loads(lookup)
            try:
                out = jsonblob
                if len(path) > 1:
                    del path[0]
                    for p in path:
                        out = out[p]
                out = self.on_aw.get_properties(path=path, data=out)
                if out is None:
                    self.response.set_status(404)
                    return
                out = json.dumps(out)
            except (TypeError, ValueError, KeyError):
                self.response.set_status(404)
                return
            out = out.encode('utf-8')
        except (TypeError, ValueError, KeyError):
                out = lookup
        self.response.set_status(200, "Ok")
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(out)

    def listall(self, myself):
        properties = myself.get_properties()
        if not properties or len(properties) == 0:
            self.response.set_status(404, "No properties")
            return
        pair = dict()
        for name, value in list(properties.items()):
            try:
                js = json.loads(value)
                pair[name] = js
            except ValueError:
                pair[name] = value
        pair = self.on_aw.get_properties(path=None, data=pair)
        if pair is None:
            self.response.set_status(404)
            return
        out = json.dumps(pair)
        self.response.write(out.encode('utf-8'))
        self.response.headers["Content-Type"] = "application/json"
        return

    def put(self, actor_id, name):
        (myself, check) = auth.init_actingweb(appreq=self,
                                              actor_id=actor_id, path='properties', subpath=name,
                                              config=self.config)
        if not myself or check.response["code"] != 200:
            return
        resource = None
        if not name:
            path = []
        else:
            path = name.split('/')
            name = path[0]
            if len(path) >= 2 and len(path[1]) > 0:
                resource = path[1]
        if not check.check_authorisation(path='properties', subpath=name, method='PUT'):
            self.response.set_status(403)
            return
        body = self.request.body.decode('utf-8', 'ignore')
        if len(path) == 1:
            old = myself.property[name]
            try:
                old = json.loads(old)
            except (TypeError, ValueError, KeyError):
                old = {}
            try:
                new = json.loads(body)
                is_json = True
            except (TypeError, ValueError, KeyError):
                new = body
                is_json = False
            new = self.on_aw.put_properties(path=path, old=old, new=new)
            if new is None:
                self.response.set_status(400, 'Payload is not accepted')
                return
            if is_json:
                myself.property[name] = json.dumps(new)
            else:
                myself.property[name] = new
            myself.register_diffs(target='properties', subtarget=name, blob=body)
            self.response.set_status(204)
            return
        # Keep text blob for later diff registration
        blob = body
        # Make store var to be merged with original struct
        try:
            body = json.loads(body)
        except (TypeError, ValueError, KeyError):
            pass
        store = {path[len(path) - 1]: body}
        # logging.debug('store with body:' + json.dumps(store))
        # Make store to be at same level as orig value
        i = len(path)-2
        while i > 0:
            c = copy.copy(store)
            store = {path[i]: c}
            # logging.debug('store with i=' + str(i) + ' (' + json.dumps(store) + ')')
            i -= 1
        # logging.debug('Snippet to store(' + json.dumps(store) + ')')
        orig = myself.property[name]
        logging.debug('Original value(' + orig + ')')
        try:
            orig = json.loads(orig)
            merge_dict(orig, store)
            res = orig
        except (TypeError, ValueError, KeyError):
            res = store
        res = self.on_aw.put_properties(path=path, old=orig, new=res)
        if res is None:
            self.response.set_status(400, 'Payload is not accepted')
            return
        res = json.dumps(res)
        logging.debug('Result to store( ' + res + ') in /properties/' + name)
        myself.property[name] = res
        myself.register_diffs(target='properties', subtarget=name, resource=resource, blob=blob)
        self.response.set_status(204)

    def post(self, actor_id, name):
        (myself, check) = auth.init_actingweb(appreq=self,
                                              actor_id=actor_id, path='properties', subpath=name,
                                              config=self.config)
        if not myself or check.response["code"] != 200:
            return
        if not check.check_authorisation(path='properties', subpath=name, method='POST'):
            self.response.set_status(403)
            return
        if len(name) > 0:
            self.response.set_status(400)
        pair = dict()
        # Handle the simple form
        if self.request.get("property") and self.request.get("value"):
            val = self.on_aw.post_properties(prop=self.request.get("property"), data=self.request.get("value"))
            if val is None:
                self.response.set_status(403)
                return
            pair[self.request.get("property")] = val
            myself.property[self.request.get("property")] = self.request.get("value")
        elif len(self.request.arguments()) > 0:
            for name in self.request.arguments():
                val = self.on_aw.post_properties(prop=name, data=self.request.get(name))
                if val is None:
                    continue
                pair[name] = val
                myself.property[name] = val
        else:
            try:
                params = json.loads(self.request.body.decode('utf-8', 'ignore'))
            except (TypeError, ValueError, KeyError):
                self.response.set_status(400, "Error in json body")
                return
            for key in params:
                val = self.on_aw.post_properties(prop=key, data=params[key])
                if val is None:
                    continue
                pair[key] = val
                if isinstance(val, dict):
                    text = json.dumps(val)
                else:
                    text = val
                myself.property[key] = text
        if not pair:
            self.response.set_status(403, "No attributes accepted")
            return
        out = json.dumps(pair)
        myself.register_diffs(target='properties', blob=out)
        self.response.write(out.encode('utf-8'))
        self.response.headers["Content-Type"] = "application/json"
        self.response.set_status(201, 'Created')

    def delete(self, actor_id, name):
        (myself, check) = auth.init_actingweb(appreq=self,
                                              actor_id=actor_id, path='properties', subpath=name,
                                              config=self.config)
        if not myself or check.response["code"] != 200:
            return
        resource = None
        if not name:
            path = []
        else:
            path = name.split('/')
            name = path[0]
            if len(path) >= 2 and len(path[1]) > 0:
                resource = path[1]
        if not check.check_authorisation(path='properties', subpath=name, method='DELETE'):
            self.response.set_status(403)
            return
        if not name:
            if self.on_aw.delete_properties(path=path, old=myself.get_properties(), new=dict()) is False:
                self.response.set_status(403)
                return
            myself.delete_properties()
            myself.register_diffs(target='properties', subtarget=None, blob='')
            self.response.set_status(204)
            return
        if len(path) == 1:
            if self.on_aw.delete_properties(path=path, old=myself.property[name], new=dict()) is False:
                self.response.set_status(403)
                return
            myself.property[name] = None
            myself.register_diffs(target='properties', subtarget=name, blob='')
            self.response.set_status(204)
            return
        orig = myself.property[name]
        old = orig
        logging.debug('DELETE /properties original value(' + orig + ')')
        try:
            orig = json.loads(orig)
        except (TypeError, ValueError, KeyError):
            # Since /properties/something was handled above
            # orig must be json loadable
            self.response.set_status(404)
            return
        if not delete_dict(orig, path[1:]):
            self.response.set_status(404)
            return
        if self.on_aw.delete_properties(path=path, old=old, new=orig) is False:
            self.response.set_status(403)
            return
        res = json.dumps(orig)
        logging.debug('Result to store( ' + res + ') in /properties/' + name)
        myself.property[name] = res
        myself.register_diffs(target='properties', subtarget=name, resource=resource, blob='')
        self.response.set_status(204)
