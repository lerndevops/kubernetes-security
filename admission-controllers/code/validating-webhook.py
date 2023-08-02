from flask import Flask, request, jsonify
vapp = Flask(__name__)
@vapp.route('/validate', methods=['POST'])
def deployment_webhook():
    request_info = request.get_json()
    if request_info["request"]["object"]["metadata"]["annotations"].get("author"):
        return vapp_response(True, "author annotations exists")
    return vapp_response(False, "Not allowed without author annotations")
def vapp_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})
if __name__ == '__main__':
    vapp.run(host='0.0.0.0', port=443, ssl_context=("/tmp/ssl/tls.crt", "/tmp/ssl/tls.key"))