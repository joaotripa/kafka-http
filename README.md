# Streaming data from kafka to an API using http sink connector 

This demo uses Docker and docker-compose to deploy confluent platform and uses kafka to stream data to a test api through http requests using the http sink connector.

## Getting started

1. **Launch the kafka stack**

On Linux:
```
docker-compose up -d  
```

On Windows:
```
docker-compose -f docker-compose-windows.yml up -d  
```

2. **Make sure everything is up and running**

```
docker-compose ps  
```

3. **Create a test topic and some data using ksqlDB**

```
docker exec -it ksqldb-server ksql http://ksqldb-server:8088  

CREATE STREAM riderLocations (profileId VARCHAR, latitude DOUBLE, longitude DOUBLE) WITH (kafka_topic='locations', value_format='json', partitions=1);  

SHOW STREAMS;  
SHOW TOPICS;
	
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('c2309eec', 37.7877, -122.4205);  
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('18f4ea86', 37.3903, -122.0643);  
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('4ab5cbad', 37.3952, -122.0813);  
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('8b6eae59', 37.3944, -122.0813);  
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('4a7c7b41', 37.4049, -122.0822);  
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('4ddad000', 37.7857, -122.4011);  

PRINT locations FROM BEGINNING;
```

4. **Produce data using the Kakfa Rest Proxy**

Using curl we can send a POST request to the Rest Proxy Container available at port 8082, as shown below.

On linux:
```
curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" -H "Accept: application/vnd.kafka.v2+json" -d '{"records":[{"value": {"PROFILEID":"ac23f0ed","LATITUDE":38.1211,"LONGITUDE":-124.6537}},{"value":{"PROFILEID":"34rfg34c","LATITUDE":39.3215,"LONGITUDE":-126.7568}},{"value":{"PROFILEID":"4rdswe28","LATITUDE":39.9087,"LONGITUDE":-127.4432}},{"value":{"PROFILEID":"9238euaf","LATITUDE":40.21738,"LONGITUDE":-128.2145}}]}' "http://localhost:8082/topics/locations" | jq .
```

or

On Windows:
```
curl -X POST http://localhost:8082/topics/locations -H "Content-Type: application/vnd.kafka.json.v2+json" -H "Accept: application/vnd.kafka.v2+json" -d "{""records"":[{""value"": {""PROFILEID"":""ac23f0ed"",""LATITUDE"":38.1211,""LONGITUDE"":-124.6537}},{""value"":{""PROFILEID"":""34rfg34c"",""LATITUDE"":39.3215,""LONGITUDE"":-126.7568}},{""value"":{""PROFILEID"":""4rdswe28"",""LATITUDE"":39.9087,""LONGITUDE"":-127.4432}},{""value"":{""PROFILEID"":""9238euaf"",""LATITUDE"":40.21738,""LONGITUDE"":-128.2145}}]}"
```

Returning to ksql terminal, let's check if data was received
```
PRINT locations FROM BEGINNING;
```

5. **Stream the data to the api with Kafka Connect**

We'll be using ksqlDB to create the connector but Kafka REST Proxy can be used as well.

Obtaining the address of our Kafka Python API container.

On Linux:
```	
KAFKA_API_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-api)
echo ${KAFKA_API_HOST}
```

On Windows:
```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-api
```

Creating the http sink connector. Copy the IP address given by the commands above and paste it in the respective place of the connector's configurations(http.api.url).
```
CREATE SINK CONNECTOR SINK_HTTP_LOCATIONS WITH (
'topics'= 'locations',
'tasks.max'= '1',
'connector.class'= 'io.confluent.connect.http.HttpSinkConnector',
'http.api.url'= 'http://*PASTE_HERE*:5000/api/v1/messages',
'headers'= 'Content-Type: application/json',
'value.converter'= 'org.apache.kafka.connect.storage.StringConverter',
'value.converter.schemas.enable'= 'false',
'key.ignore'= 'true',
'schema.ignore'= 'true',
'confluent.topic.bootstrap.servers'= 'broker:29092',
'confluent.topic.replication.factor'= '1',
'reporter.bootstrap.servers'= 'broker:29092',
'reporter.result.topic.name'= 'success-responses',
'reporter.result.topic.replication.factor'= '1',
'reporter.error.topic.name'= 'error-responses',
'reporter.error.topic.replication.factor'= '1'
);

SHOW CONNECTORS;
```
6. **Testing**

To test the connector, open a terminal and send a request to the API (at port 5000) that returns the messages sent by kafka.

```
curl -X GET http://localhost:5000/api/v1/getmessages
```
7. **Stopping Kafka stack**

On Linux:
```
docker-compose down
```

On Windows:
```
docker-compose -f docker-compose-windows.yml down
```


### Useful links

https://docs.confluent.io/current/connect/kafka-connect-http/index.html  
https://docs.confluent.io/current/connect/managing/extending.html  
https://ksqldb.io/quickstart.html  
