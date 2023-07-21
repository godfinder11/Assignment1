
Set up Kafka --

Create 2 folders in any drive--
kafka_logs-- zookeeper
kafka_logs-- server_logs

change the zookeeper.properties:
------------------------------------------------------
dataDir=F:/kafka_logs/zookeeper
maxClientCnxns=1

This property limits the number of active connections from a host, specified by IP address, to a single ZooKeeper server.

change the server.properties:
----------------------------------------------------
uncomment listeners
log.dirs=F:/kafka_logs/server_logs
zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=60000

Start Zookeeper:
---------------------------------------
F:/kafka_2.12-3.2.0/bin/windows/zookeeper-server-start.bat F:/kafka_2.12-3.2.0/config/zookeeper.properties

Start Kafka-server:
-----------------------------------------
F:/kafka_2.12-3.2.0/bin/windows/kafka-server-start.bat F:/kafka_2.12-3.2.0/config/server.properties

Create topic:
------------------------------------
F:/kafka_2.12-3.2.0/bin/windows/kafka-topics.bat --create --topic assignment --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

Start Producer:
--------------------------------------
F:/kafka_2.12-3.2.0/bin/windows/kafka-console-producer.bat --topic assignment --bootstrap-server localhost:9092

Start Consumer:
-------------------------------------
F:/kafka_2.12-3.2.0/bin/windows/kafka-console-consumer.bat --topic assignment --from-beginning --bootstrap-server localhost:9092

kafka-python installation:
--------------------------------------------------
pip install kafka-python


