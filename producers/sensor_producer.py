"""
IoT Sensor Data Producer
Simulates real-time sensor data and publishes to Kafka
"""
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


class SensorProducer:
    """Produces IoT sensor data to Kafka"""

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.topic = 'sensor-data'

    def generate_sensor_data(self, sensor_id: str) -> dict:
        """Generate realistic sensor data"""
        return {
            'sensor_id': sensor_id,
            'timestamp': datetime.utcnow().isoformat(),
            'temperature': round(random.uniform(15.0, 35.0), 2),
            'humidity': round(random.uniform(30.0, 80.0), 2),
            'pressure': round(random.uniform(980.0, 1050.0), 2),
            'location': {
                'latitude': float(fake.latitude()),
                'longitude': float(fake.longitude())
            },
            'status': random.choice(['active', 'active', 'active', 'warning'])
        }

    def produce_messages(self, num_sensors: int = 10, interval: float = 1.0):
        """
        Continuously produce sensor data

        Args:
            num_sensors: Number of sensors to simulate
            interval: Time interval between messages (seconds)
        """
        sensor_ids = [f"SENSOR_{i:03d}" for i in range(num_sensors)]

        logger.info(f"Starting sensor data production for {num_sensors} sensors")

        try:
            while True:
                for sensor_id in sensor_ids:
                    data = self.generate_sensor_data(sensor_id)

                    # Send to Kafka
                    future = self.producer.send(
                        self.topic,
                        key=sensor_id,
                        value=data
                    )

                    # Log result
                    try:
                        record_metadata = future.get(timeout=10)
                        logger.info(
                            f"Sent: {sensor_id} -> "
                            f"partition {record_metadata.partition}, "
                            f"offset {record_metadata.offset}"
                        )
                    except Exception as e:
                        logger.error(f"Failed to send message: {e}")

                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Shutting down producer...")
        finally:
            self.producer.close()


if __name__ == "__main__":
    producer = SensorProducer()
    producer.produce_messages(num_sensors=5, interval=2.0)
