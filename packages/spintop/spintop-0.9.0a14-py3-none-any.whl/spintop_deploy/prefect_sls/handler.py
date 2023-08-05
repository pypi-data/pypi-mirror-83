import os
import prefect
import time
import platform
from pprint import pprint


from flask import Flask, request

from .agent import ServerlessAgent

app = Flask(__name__)


flow_id = os.getenv('PREFECT__FLOW_ID')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    try:
        data = request.json
        print('POST content:')
        print(data)
    except Exception as e:
        print('Unable to get JSON: ' + str(e))

    ephemeral_agent = ServerlessAgent(name=f'sls-{platform.node()}', labels=[flow_id], show_flow_logs=True)
    ephemeral_agent.run_flow_id(flow_id, labels=[flow_id])
    print('DONE')
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))