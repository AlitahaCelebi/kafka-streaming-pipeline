"""
Analytics Consumer
Consumes sensor data and performs real-time analytics
"""
import json
from kafka import KafkaConsumer
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyticsConsumer:
    """Consumes and analyzes sensor data"""

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaConsumer(
            'sensor-data',
            bootstrap_servers=bootstrap_servers,
            group_id='analytics-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        # Analytics state
        self.stats = defaultdict(lambda: {
            'count': 0,
            'total_temp': 0,
            'total_humidity': 0,
            'warnings': 0
        })

    def process_message(self, message):
        """Process individual sensor message"""
        data = message.value
        sensor_id = data['sensor_id']

        # Update statistics
        stats = self.stats[sensor_id]
        stats['count'] += 1
        stats['total_temp'] += data['temperature']
        stats['total_humidity'] += data['humidity']

        if data['status'] == 'warning':
            stats['warnings'] += 1

        # Calculate averages
        avg_temp = stats['total_temp'] / stats['count']
        avg_humidity = stats['total_humidity'] / stats['count']

        logger.info(
            f"Sensor: {sensor_id} | "
            f"Temp: {data['temperature']:.1f}°C (avg: {avg_temp:.1f}) | "
            f"Humidity: {data['humidity']:.1f}% (avg: {avg_humidity:.1f}) | "
            f"Warnings: {stats['warnings']}"
        )

        # Alert on anomalies
        if data['temperature'] > 30:
            logger.warning(f"HIGH TEMPERATURE ALERT: {sensor_id} - {data['temperature']}°C")

    def consume(self):
        """Start consuming messages"""
        logger.info("Starting analytics consumer...")

        try:
            for message in self.consumer:
                self.process_message(message)

        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()

    def print_summary(self):
        """Print analytics summary"""
        logger.info("=== Analytics Summary ===")
        for sensor_id, stats in self.stats.items():
            avg_temp = stats['total_temp'] / stats['count'] if stats['count'] > 0 else 0
            logger.info(f"{sensor_id}: {stats['count']} messages, avg temp: {avg_temp:.2f}°C")


if __name__ == "__main__":
    consumer = AnalyticsConsumer()
    consumer.consume()
