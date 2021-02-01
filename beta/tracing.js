const { LogLevel } = require("@opentelemetry/core");
const { NodeTracerProvider } = require("@opentelemetry/node");
const { BasicTracerProvider, SimpleSpanProcessor } = require('@opentelemetry/tracing');
const { CollectorTraceExporter } =  require('@opentelemetry/exporter-collector-grpc');

const collectorOptions = {
  serviceName: 'beta',
//   url: 'otel-collector:55680' // url is optional and can be omitted - default is localhost:55680
//   url: 'http://localhost:55680' // url is optional and can be omitted - default is localhost:55680
  url: 'otel-collector:55680' // url is optional and can be omitted - default is localhost:55680
};

const provider = new NodeTracerProvider({
    logLevel: LogLevel.ERROR,
    plugins: {
      '@grpc/grpc-js': {
        enabled: true,
        // You may use a package name or absolute path to the file.
        path: '@opentelemetry/plugin-grpc-js',
        // gRPC-js plugin options
      }
    }
  // plugins: {
  //   grpc: {
  //     enabled: true,
  //     // You may use a package name or absolute path to the file.
  //     path: '@opentelemetry/plugin-grpc',
  //     // gRPC plugin options
  //   }
  // }
});

// const provider = new BasicTracerProvider();
const exporter = new CollectorTraceExporter(collectorOptions);
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));

provider.register();
