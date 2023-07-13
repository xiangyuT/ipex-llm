from bigdl.ppml.attestation import attestation_service, quote_generator
from flask import Flask, request
from configparser import ConfigParser
import ssl, os
import base64

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

# 生成自签名的SSL证书
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

def load_config():
    config = ConfigParser()
    config.read('config.ini')

    app.config['as_url'] = config.get('BIGDL_AS', 'as_url')
    app.config['as_app_id'] = config.get('BIGDL_AS', 'as_app_id')
    app.config['as_api_key'] = config.get('BIGDL_AS', 'as_api_key')

load_config()

@app.route('/gen_quote', methods=['POST'])
def gen_quote():
    data = request.get_json()
    user_report_data = data.get('user_report_data')

    quote_b = quote_generator.generate_tdx_quote(user_report_data)
    quote = base64.b64encode(quote_b.encode()).decode('utf-8')

    return {'quote': quote}

@app.route('/verify_quote', methods=['POST'])
def verify_quote():
    data = request.get_json()
    as_url = app.config['as_url']
    as_app_id = app.config['as_app_id']
    as_api_key = app.config['as_api_key']
    quote = data.get('quote')
    policy_id = data.get('policy_id')
    if policy_id is None:
        policy_id = ''
    
    result = attestation_service.bigdl_attestation_service(as_url, as_app_id, as_api_key, quote_b, policy_id)

    return {'result': result}

@app.route('/attest', methods=['POST'])
def attest():
    data = request.get_json()
    as_url = app.config['as_url']
    as_app_id = app.config['as_app_id']
    as_api_key = app.config['as_api_key']
    user_report_data = data.get('user_report_data')
    quote_b = quote_generator.generate_tdx_quote(user_report_data)
    quote = base64.b64encode(quote_b).decode('utf-8')
    policy_id = data.get('policy_id')
    if policy_id is None:
        policy_id = ''
    result = attestation_service.bigdl_attestation_service(as_url, as_app_id, as_api_key, quote_b, policy_id)

    return {'result': result}

@app.route('/load_data', methods=['POST'])
def load_data():
    raise "TODO"

if __name__ == '__main__':
    if not os.path.exists("/dev/tdx-guest"):
        print("TDX device 'tdx-guest' not found, service stopped.")
        exit
    app.run(host='127.0.0.1', port=9870, ssl_context=context)
