from .state import AbstractState
from constants import MEASUREMENTS_FILE
from helpers import convert_temp
import ujson
import time


class Publishing(AbstractState):
    """Publishing state - sends measurements via MQTT in Smart Department format."""

    def enter(self):
        pass

    def exec(self):

        # Check if MQTT is configured
        if not self.device.settings.mqtt_broker:
            print('MQTT not configured, skipping publish')
            from .sleep import Sleep
            self.device.change_state(Sleep(self.device))
            return

        try:
            # Load measurements
            measurements = []
            try:
                with open(MEASUREMENTS_FILE, "r") as f:
                    measurements = ujson.load(f)
            except:
                print('No measurements to publish')
                from .sleep import Sleep
                self.device.change_state(Sleep(self.device))
                return

            if not measurements:
                print('No measurements to publish')
                from .sleep import Sleep
                self.device.change_state(Sleep(self.device))
                return

            # Publish via MQTT
            success = self.publish_measurements(measurements)

            if success:
                # Clear measurements file after successful publish
                with open(MEASUREMENTS_FILE, "w") as f:
                    ujson.dump([], f)
                print('Measurements published and cleared')
            else:
                print('Publishing failed, keeping measurements for retry')

        except Exception as e:
            print(f'Publishing error: {e}')

        # Always go to sleep after publishing attempt
        from .sleep import Sleep
        self.device.change_state(Sleep(self.device))

    def publish_measurements(self, measurements):
        try:
            from lib.umqtt.simple import MQTTClient
            import machine
            import ubinascii

            # Generate unique client ID
            client_id = ubinascii.hexlify(machine.unique_id())

            # MQTT broker settings
            broker = self.device.settings.mqtt_broker
            port = self.device.settings.mqtt_port or 1883

            # Smart Department topic format
            status_topic = self.device.settings.get_mqtt_topic('status')
            data_topic = self.device.settings.get_mqtt_topic('data')

            print(f'Connecting to MQTT broker: {broker}:{port}')
            print(f'Status topic: {status_topic}')
            print(f'Data topic: {data_topic}')

            # Create MQTT client
            client = MQTTClient(
                client_id,
                broker,
                port=port,
                keepalive=60
            )

            # Set Last Will and Testament
            lwt_message = ujson.dumps({'status': 'offline'})
            client.set_last_will(status_topic, lwt_message, retain=True, qos=1)

            # Connect to broker
            result = client.connect()
            if result != 0:
                print(f'MQTT connection failed with code: {result}')
                return False

            print('Connected to MQTT broker')

            # Publish online status
            online_message = ujson.dumps({'status': 'online'})
            client.publish(status_topic, online_message, retain=True, qos=1)

            # Create Smart Department payload format
            metrics = []
            for measurement in measurements:
                # Convert temperature to user's preferred unit
                temp = convert_temp(
                    measurement['temperature'],
                    self.device.settings.units
                )

                # Add temperature metric
                metrics.append({
                    'dt': self.format_iso8601(measurement['time']),
                    'name': 'temperature',
                    'value': round(temp, 2),
                    'units': self.device.settings.units
                })

                # Add humidity metric
                metrics.append({
                    'dt': self.format_iso8601(measurement['time']),
                    'name': 'humidity',
                    'value': round(measurement['humidity'], 2),
                    'units': '%'
                })

            # Create payload with current timestamp
            payload = ujson.dumps({
                'dt': self.format_iso8601(time.time()),
                'metrics': metrics
            })

            # Publish data
            client.publish(data_topic, payload, qos=1)
            print(f'Published {len(measurements)} measurements')
            print(f'Payload: {payload[:100]}...')

            # Disconnect cleanly
            client.disconnect()

            return True

        except Exception as e:
            print(f'MQTT error: {e}')
            return False

    def format_iso8601(self, timestamp):
        try:
            import time
            # Convert timestamp to time tuple
            dt = time.gmtime(int(timestamp))
            # Format as ISO 8601
            return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
                dt[0], dt[1], dt[2],  # Year, Month, Day
                dt[3], dt[4], dt[5]  # Hour, Minute, Second
            )
        except:
            return "1970-01-01T00:00:00Z"

    def exit(self):
        pass