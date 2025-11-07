# Real-time Data Streaming with Apache Kafka

A real-time data streaming pipeline using Apache Kafka for processing IoT sensor data and event streams.

## Features

- Real-time event streaming with Kafka
- Producer for simulating IoT sensor data
- Consumer with message processing
- Stream processing with Kafka Streams
- Message serialization with Avro
- Monitoring and metrics

## Technologies

- Apache Kafka 3.5+
- Python 3.9+
- kafka-python
- confluent-kafka
- Docker & Docker Compose

## Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Producer  │────────▶│    Kafka    │────────▶│   Consumer   │
│  (IoT Data) │         │   Cluster   │         │  (Analytics) │
└─────────────┘         └─────────────┘         └──────────────┘
```

## Project Structure

```
kafka-streaming-pipeline/
├── producers/
│   ├── sensor_producer.py    # IoT sensor data producer
│   └── event_producer.py     # Event data producer
├── consumers/
│   ├── analytics_consumer.py # Real-time analytics
│   └── storage_consumer.py   # Data storage consumer
├── processors/
│   └── stream_processor.py   # Stream processing logic
├── config/
│   ├── kafka_config.py       # Kafka configuration
│   └── docker-compose.yml    # Docker setup
├── tests/
├── requirements.txt
└── README.md
```

## Quick Start

1. Start Kafka cluster:
```bash
docker-compose up -d
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run producer:
```bash
python producers/sensor_producer.py
```

4. Run consumer:
```bash
python consumers/analytics_consumer.py
```

## Topics

- `sensor-data`: IoT sensor readings
- `events`: Application events
- `alerts`: Processed alerts
- `analytics`: Aggregated analytics

## Author

Alitaha Celebi - Data Engineer
