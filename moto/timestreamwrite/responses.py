import json

from moto.core.responses import BaseResponse
from .models import timestreamwrite_backends


class TimestreamWriteResponse(BaseResponse):
    def __init__(self):
        super().__init__()

    @property
    def timestreamwrite_backend(self):
        """Return backend instance specific for this region."""
        return timestreamwrite_backends[self.region]

    def create_database(self):
        database_name = self._get_param("DatabaseName")
        kms_key_id = self._get_param("KmsKeyId")
        tags = self._get_param("Tags")
        database = self.timestreamwrite_backend.create_database(
            database_name=database_name, kms_key_id=kms_key_id, tags=tags
        )
        return json.dumps(dict(Database=database.description()))

    def delete_database(self):
        database_name = self._get_param("DatabaseName")
        self.timestreamwrite_backend.delete_database(database_name=database_name)
        return "{}"

    def describe_database(self):
        database_name = self._get_param("DatabaseName")
        database = self.timestreamwrite_backend.describe_database(
            database_name=database_name
        )
        return json.dumps(dict(Database=database.description()))

    def update_database(self):
        database_name = self._get_param("DatabaseName")
        kms_key_id = self._get_param("KmsKeyId")
        database = self.timestreamwrite_backend.update_database(
            database_name, kms_key_id
        )
        return json.dumps(dict(Database=database.description()))

    def list_databases(self):
        all_dbs = self.timestreamwrite_backend.list_databases()
        return json.dumps(dict(Databases=[db.description() for db in all_dbs]))

    def create_table(self):
        database_name = self._get_param("DatabaseName")
        table_name = self._get_param("TableName")
        retention_properties = self._get_param("RetentionProperties")
        tags = self._get_param("Tags")
        table = self.timestreamwrite_backend.create_table(
            database_name, table_name, retention_properties, tags
        )
        return json.dumps(dict(Table=table.description()))

    def delete_table(self):
        database_name = self._get_param("DatabaseName")
        table_name = self._get_param("TableName")
        self.timestreamwrite_backend.delete_table(database_name, table_name)
        return "{}"

    def describe_table(self):
        database_name = self._get_param("DatabaseName")
        table_name = self._get_param("TableName")
        table = self.timestreamwrite_backend.describe_table(database_name, table_name)
        return json.dumps(dict(Table=table.description()))

    def list_tables(self):
        database_name = self._get_param("DatabaseName")
        tables = self.timestreamwrite_backend.list_tables(database_name)
        return json.dumps(dict(Tables=[t.description() for t in tables]))

    def update_table(self):
        database_name = self._get_param("DatabaseName")
        table_name = self._get_param("TableName")
        retention_properties = self._get_param("RetentionProperties")
        table = self.timestreamwrite_backend.update_table(
            database_name, table_name, retention_properties
        )
        return json.dumps(dict(Table=table.description()))

    def write_records(self):
        database_name = self._get_param("DatabaseName")
        table_name = self._get_param("TableName")
        records = self._get_param("Records")
        self.timestreamwrite_backend.write_records(database_name, table_name, records)
        resp = {
            "RecordsIngested": {
                "Total": len(records),
                "MemoryStore": len(records),
                "MagneticStore": 0,
            }
        }
        return json.dumps(resp)

    def describe_endpoints(self):
        resp = self.timestreamwrite_backend.describe_endpoints()
        return json.dumps(resp)

    def list_tags_for_resource(self):
        resource_arn = self._get_param("ResourceARN")
        tags = self.timestreamwrite_backend.list_tags_for_resource(resource_arn)
        return json.dumps(tags)

    def tag_resource(self):
        resource_arn = self._get_param("ResourceARN")
        tags = self._get_param("Tags")
        self.timestreamwrite_backend.tag_resource(resource_arn, tags)
        return "{}"

    def untag_resource(self):
        resource_arn = self._get_param("ResourceARN")
        tag_keys = self._get_param("TagKeys")
        self.timestreamwrite_backend.untag_resource(resource_arn, tag_keys)
        return "{}"
