from influxdb_client import InfluxDBClient, Point, WritePrecision


class InfluxDB:
    def __init__(self, url, token, org):
        self.client = InfluxDBClient(url=url, token=token, org=org)

    def write(self, bucket, measurement, tags, fields):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        p = Point(measurement).tag(tags).field(fields)
        write_api.write(bucket=bucket, record=p)
        write_api.close()

    def query(self, query):
        query_api = self.client.query_api()
        return query_api.query(query)

    def close(self):
        self.client.close()
