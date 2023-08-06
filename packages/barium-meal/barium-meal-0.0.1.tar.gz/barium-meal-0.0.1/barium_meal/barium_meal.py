from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

class BariumMeal():

    def __init__(self, jaeger_config=None):
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

        # create a JaegerSpanExporter
        if jaeger_config is not None:
            jaeger_exporter = jaeger.JaegerSpanExporter(
                service_name=jaeger_config['service_name'],
                collector_host_name=jaeger_config['collector_host_name'],
                collector_port=14268,
            )

            # create a BatchExportSpanProcessor and add the exporter to it
            span_processor = BatchExportSpanProcessor(jaeger_exporter)

            # add to the tracer factory
            trace.get_tracer_provider().add_span_processor(span_processor)

    def get_tracer(self):
        return self.tracer