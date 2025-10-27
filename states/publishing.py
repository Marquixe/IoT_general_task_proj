from .state import AbstractState
from constants import MEASUREMENTS_FILE
from helpers import convert_temp
import ujson
import time


class Publishing(AbstractState):

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
            # Keep measurements for next attempt

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
            topic = self.device.settings.mqtt_topic or 'sensor/data'

            print(f'Connecting to MQTT broker: {broker}:{port}')

            # Create MQTT client
            client = MQTTClient(
                client_id,
                broker,
                port=port,
                keepalive=60
            )

            # Set Last Will and Testament (LWT)
            # Broker will send this if device disconnects unexpectedly
            lwt_topic = f'{topic}/status'
            lwt_message = ujson.dumps({'status': 'offline'})
            client.set_last_will(lwt_topic, lwt_message, retain=True, qos=1)

            # Connect to broker
            result = client.connect()
            if result != 0:
                print(f'MQTT connection failed with code: {result}')
                return False

            print('Connected to MQTT broker')

            # Publish online status
            online_message = ujson.dumps({'status': 'online'})
            client.publish(lwt_topic, online_message, retain=True, qos=1)

            # Publish each measurement
            published_count = 0
            for measurement in measurements:
                try:
                    # Convert temperature to user's preferred unit
                    temp = convert_temp(
                        measurement['temperature'],
                        self.device.settings.units
                    )

                    # Create payload with ISO 8601 timestamp
                    payload = ujson.dumps({
                        'timestamp': measurement['time'],
                        'temperature': round(temp, 2),
                        'humidity': round(measurement['humidity'], 2),
                        'unit': self.device.settings.units
                    })

                    # Publish with QoS 1 (at least once delivery)
                    client.publish(topic, payload, qos=1)
                    published_count += 1
                    print(f'Published: {payload}')

                    # Small delay between publishes
                    time.sleep(0.1)

                except Exception as e:
                    print(f'Failed to publish measurement: {e}')
                    continue

            print(f'Successfully published {published_count}/{len(measurements)} measurements')

            # Disconnect cleanly
            client.disconnect()

            return published_count > 0

        except Exception as e:
            print(f'MQTT error: {e}')
            return False

    def exit(self):
        pass