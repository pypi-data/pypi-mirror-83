import amqp
import calendar
from six.moves import urllib
from datetime import datetime, timezone
from .wire.conversion import WireV1
from .tracing.tracer import Tracer
from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from opencensus.common.transports.async_ import AsyncTransport

class Channel(object):
    def __init__(self, uri="amqp://guest:guest@localhost:5672", exchange="is"):
        url = urllib.parse.urlparse(uri)

        self.connection = amqp.Connection(
            host="{}:{}".format(url.hostname or "localhost", url.port or 5672),
            userid=url.username or "guest",
            password=url.password or "guest",
            virtual_host='/'
            if not url.path or url.path == '/' else url.path[1:],
            connect_timeout=5.0,
        )
        self.connection.connect()

        self._channel = self.connection.channel()
        self._channel.auto_decode = False

        self._exchange = exchange
        self._channel.exchange_declare(
            exchange=self._exchange,
            type="topic",
            durable=False,
            auto_delete=False,
        )

        self.subscriptions = []
        self.amqp_message = None

    def _on_message(self, message):
        self.amqp_message = message

    def publish(self, message, topic=None):
        """ Publishes a message to the given topic. The topic on the message
        is used when no topic is passed to this function. If no valid topic is
        passed a RuntimeError is raised."""
        if not message.has_topic() and not topic:
            raise RuntimeError("Trying to publish message without topic")

        if 'timestamp_send' in message.metadata:
            del message.metadata['timestamp_send']
        now = datetime.now()
        dt_str = int(datetime.timestamp(now)*1000000)
        # print("Timestamp_Send: {}".format(dt_str))
        message.metadata.update({'timestamp_send':dt_str})

        amqp_message = amqp.Message(body=message.body,
                                    channel=self._channel,
                                    **WireV1.to_amqp_properties(message))
        
        
        self._channel.basic_publish(
            amqp_message,
            exchange=self._exchange,
            routing_key=message.topic if topic is None else topic,
            immediate=False,
            mandatory=False,
        )

    def consume(self, timeout=None):
        """ Blocks waiting for a new message to arrive. If no timeout
        (in seconds) is provided the function blocks forever.
        Args:
            timeout (float): Period in seconds to block waiting for messages.
            Must be a positive number. If 0 is passed the call is non-blocking.
            If no message was received after this period a socket.timeout
            Exception is raised.
        Returns:
            Message: Received message.
        """

        exporter = ZipkinExporter(
        service_name="CommTracer",
        host_name="10.10.2.7", 
        port="30200",
        transport=AsyncTransport,
        )

        if timeout is not None:
            assert timeout >= 0.0

        self.amqp_message = None
        while self.amqp_message is None:
            self.connection.drain_events(timeout)
        message = WireV1.from_amqp_message(self.amqp_message)      
        
        if 'timestamp_send' in message.metadata:
            tmstmp_send = message.metadata['timestamp_send']
            tmstmp_send = datetime.utcfromtimestamp(int(tmstmp_send)/1000000.0).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            del message.metadata['timestamp_send']
            now = datetime.now(timezone.utc)
            tmstmp_rcvd = datetime.utcfromtimestamp(int(datetime.timestamp(now)*1000000000)/1000000000.0).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            # print("Timestamp_Rcvd: {} ({})".format(now,tmstmp_rcvd))
            
            timestamps = (tmstmp_send,tmstmp_rcvd)
            # print("Debug<T1,T2>: {},{}".format(timestamps[0],timestamps[1]))
            tracer = Tracer(exporter,message.extract_tracing())
            with tracer.span(name="TC_{}".format(message.subscription_id),timestamps=timestamps) as tspan:
                pass
            message.inject_tracing(tspan)
            

            # msg.properties['application_headers'] = tfp.to_carrier(
            #     span_context, msg.properties['application_headers'])
            
            # print(msg.properties['application_headers'])
        
        return message

    def close(self):
        self.connection.close()
