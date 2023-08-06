# Resilient data exporters
Resilient-exporters abstracts away common tasks when sending or saving data from an application. It has been designed to send data to different targets and manage common issues for applications running on edge devices such as a Raspberry Pi or Nvidia Jetson Nano:
- Internet connection interruptions;
- Highly variable frequency of data transfers;

If a connection is lost, it automatically saves the data and retries later when the connection is recovered and when a new request to send data is made. To avoid consuming too much memory or disk space, it has a specific configurable flush.

If an application wants to send more data than is momentally manageable, it multiplies the transmission jobs (using multithreading, if available) and saves the data (queuing), to avoid back-pressure and reducing the application's speed.

Of course, it can break if:
- the data to transmit is _almost always_ more important than the available bandwidth;
- the interruptions are too long compared to the available memory or disk space;

We have designed it particularly for a Raspberry Pi 3B+ device running a Linux distribution.

## Installation
```
pip install resilient-exporters
```

## Usage
Currently supported:
- Text file
- MongoDB
- ElasticSearch

Some features for some exporters might be missing. Raise an issue on Github to ask for an implementation and help improve the package.

### Store in a file
```python
from resilient_exporters import FileExporter

exporter = FileExporter(target_file="mydata.txt",
                        max_lines=1000,
                        keep_new_data=True)

mydata = ["value1", "value2"]
exporter.send(mydata)
```

### To MongoDB
```python
from resilient_exporters import MongoDBExporter

exporter = MongoDBExporter(target_ip="127.0.0.1",
                           target_port=27017,
                           username="username",
                           password="password",
                           default_db="my_db",
                           default_collection="my_collection")

mydata = {"field1": "value1"}
exporter.send(mydata)
```

### To ElasticSearch
```python
from resilient_exporters import ElasticSearchExporter

exporter = ElasticSearchExporter(target_ip="127.0.0.1",
                                 default_index="my_index",
                                 use_ssl=True,
                                 ssl_certfile="/path/to/file",
                                 sniff_on_start=True)

mydata = {"field1": "value1"}
exporter.send(mydata)
```

### Multiple distant targets - Pools
Edge devices are more and more powerful, and are capable of managing multiple distant targets without much overhead thanks to `resilient-exporters`. If you're taking advantage of this, you might need sometimes to replicate data across different databases of the same type (e.g. NoSQL, document-based databases). However, if you use multiple exporters, all the features will be duplicated and can generate inefficiencies (multiple temporary files, multiple queues, etc.).

Instead, use `resilient_exporters.ExporterPool` which pools exporters _and_ other pools to expose only one `send` method for all the exporters and to ensure a more efficient management of the resources. To use it:
```python
from resilient_exporters import ExporterPool
from resilient_exporters import MongoDBExporter, ElasticSearchExporter

exporters = [
  MongoDBExporter(target_ip="127.0.1.10",
                  target_port=1234,
                  default_db="my_db",
                  default_collection="my_collection"),
  ElasticSearchExporter(cloud_id="cloud id",
                        api_key="api key",
                        default_index="my_index")]

pool = ExporterPool(exporters, use_memory=False)

mydata = {"metric": 2}
pool.send(mydata)
```

## Transform data before sending
To transform data before it gets sent by an exporter or a pool, one can add a function that takes the input data and returns the transformed data:
```python
from resilient_exporters import MongoDBExporter

def transform(data):
  data["metric"] = (data["metric"] / 2) * .5
  return data

exporter = MongoDBExporter(target_ip="127.0.1.10",
                           target_port=1234,
                           default_db="my_db",
                           default_collection="my_collection",
                           transform=transform)

mydata = {"metric": 2}
exporter.send(mydata)
```
>**NOTE**: it can also be passed to a pool with the same key argument `tranform` at initialisation. When doing so, transform functions of individual exporters will be superseded by the pool's transform function.

## Additional information
The `resilient_exporters.Exporter` and `resilient_exporters.ExporterPool` are the core of the package. All the other exporters inherits from one of them.

`Exporter` manages the export of data to a target, however each target need specific logic to send data. All these subclasses, such as `FileExporter` or `MongoDBExporter`, implement the `Exporter.send` method and manage the needed options. Some exporters might need additional packages to be usable:
- `pymongo` for `MongoDBExporter`
- `elasticsearch` for `ElasticSearchExporter`

## Suggestions and contribution
Please open a GitHub issue for bugs or feature requests.
Contact the contributors for participating.
