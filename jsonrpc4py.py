import requests
import base64
import json

# http timeout seconds
HTTP_TIMEOUT = 0.002

class JsonRPC(object):
    def __init__(self, host, port, username, password, timeout=HTTP_TIMEOUT):
        self.conn = requests
        self.url = "http://%s:%s" % (host, port)
        self.timeout = timeout
        self.credentials = base64.b64encode("%s:%s" % (username, password))
        self.headers = {
            'Content-Type': 'text/json',
            'Authorization': 'Basic %s' % self.credentials,
        }

    def _call_raw(self, data):
        res = self.conn.post(self.url, data=data, headers=self.headers, timeout=self.timeout)
        return res

    def _call(self, method, params):
        result = None
        try:
            result = self._call_raw(json.dumps({
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': '1',
            })).json()
        except requests.exceptions.Timeout as timeout_exception:
            #print('timeout exception: %s' % timeout_exception)
            result = None
        except Exception as e:
            #print('unknown exception: %s' % e)
            result = None

        return result or {'error': 'response is None.'}

