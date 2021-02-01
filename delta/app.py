from flask import jsonify, Flask, request
import requests
import datetime
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter

app = Flask("api")

counter = 0
@app.route('/delta', methods=["POST"])
def compute():
    # create errors sometimes
    global counter
    counter += 1
    if counter % 3 == 0:
        error_request = requests.get("httpx2://www.invalidschema.com")

    name = request.json["name"]

    status = requests.post(os.getenv("ECHO_SVC"), json={
        "name": name
    })
    if status.ok:
        return jsonify({"data": f"Hello {name} from Delta Service!", "echo_response": status.json()})

    return jsonify({"data": f"Hello {name} from Delta Service!"})


if __name__ == '__main__':
    endpoint = "{}:{}".format(os.getenv("OTC_HOST"), os.getenv("OTC_PORT", "55680"))
    print('OTC Collector endpoint set to {}'.format(endpoint))

    trace.set_tracer_provider(TracerProvider(resource=Resource({"service.name": "delta"})))
    trace.get_tracer_provider().add_span_processor(BatchExportSpanProcessor(OTLPSpanExporter(endpoint=endpoint,
                                                                                             insecure=True)))

    app.run(debug=True, host='0.0.0.0')
