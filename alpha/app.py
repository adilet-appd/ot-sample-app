from flask import Flask, jsonify
import requests
import datetime
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter

app = Flask("api")


@app.route('/alpha/<username>')
def hello_world(username):

    beta_status = requests.post(os.getenv("BETA_SVC"), json={
        "name": username,
        "date": datetime.datetime.today().strftime('%Y-%m-%d')
    })
    if not beta_status.ok:
        return 'bad request to ' + os.getenv("BETA_SVC"), 400

    delta_status = requests.post(os.getenv("DELTA_SVC"), json={
        "name": username,
        "date": datetime.datetime.today().strftime('%Y-%m-%d')
    })
    if not delta_status.ok:
        return 'bad request to ' + os.getenv("DELTA_SVC"), 400

    curr_time = datetime.datetime.today().strftime('%Y-%m-%d : %H:%M:%S')
    return jsonify({"time": curr_time, "beta_response": beta_status.json(), "delta_response": delta_status.json()})


if __name__ == '__main__':
    endpoint = "{}:{}".format(os.getenv("OTC_HOST"), os.getenv("OTC_PORT", "55680"))
    print('OTC Collector endpoint set to {}'.format(endpoint))

    trace.set_tracer_provider(TracerProvider(resource=Resource({"service.name": "alpha"})))
    trace.get_tracer_provider().add_span_processor(BatchExportSpanProcessor(OTLPSpanExporter(endpoint=endpoint,
                                                                                             insecure=True)))

    app.run(debug=True, host='0.0.0.0')
