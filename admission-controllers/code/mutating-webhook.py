from flask import Flask, request, jsonify
import base64
import jsonpatch
mapp = Flask(__name__)
@mapp.route('/mutate/deployments', methods=['POST'])
def mutate():
    request_info = request.get_json()
    return patch(True, "Adding project label", json_patch = jsonpatch.JsonPatch([{"op": "add", "path": "/metadata/labels/project", "value": "chandrayan"}]))
def patch(allowed, message, json_patch):
    base64_patch = base64.b64encode(json_patch.to_string().encode("utf-8")).decode("utf-8")
    return jsonify({"response": {"allowed": allowed,"status": {"message": message},"patchType": "JSONPatch","patch": base64_patch}})
if __name__ == '__main__':
    mapp.run(host='0.0.0.0', port=443, ssl_context=("/tmp/ssl/tls.crt", "/tmp/ssl/tls.key"))