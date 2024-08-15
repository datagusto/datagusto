import json
import pandas as pd

data_source_types = ["mysql", "postgresql", "oracle", "duckdb", "sqlite", "file", "bigquery", "mssql", "snowflake"]

class DataSource:
    def __init__(self, owner_id, name, dtype, description, hostname, port, username, password, database_name,\
                 id=None, deleted_at=None, created_at=None, updated_at=None):
        
        self.owner_id = owner_id
        self.name = name
        self.dtype = dtype
        self.description = description
        
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name

        self.id = id
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data_dict):
        """Creates a DataSource instance from a dictionary with nested key mapping."""
        connection_details = data_dict.pop('connection', {})
        remapped_data = {
            'owner_id': data_dict.get('owner_id'),
            'name': data_dict.get('name'),
            'dtype': data_dict.get('type'),  # Remap 'type' to 'data_type'
            'description': data_dict.get('description'),
            
            'hostname': connection_details.get('host'),
            'port': connection_details.get('port'),
            'username': connection_details.get('username'),
            'password': connection_details.get('password'),
            'database_name': connection_details.get('database'),  # Remap 'database' to 'database_name'
            
            'id': data_dict.get('id'),
            'deleted_at': data_dict.get('deleted_at'),
            'created_at': data_dict.get('created_at'),
            'updated_at': data_dict.get('updated_at')
        }
        return cls(**remapped_data)
    
    @classmethod
    def from_json(cls, json_str):
        """Creates a DataSource instance from a JSON string with nested key mapping."""
        data = json.loads(json_str)
        
        # Extract and remap connection details
        connection_details = data.pop('connection')
        remapped_data = {
            'owner_id': data['owner_id'],
            'name': data['name'],
            'dtype': data['type'],  # Remap 'type' to 'data_type'
            'description': data['description'],

            'hostname': connection_details['host'],
            'port': connection_details['port'],
            'username': connection_details['username'],
            'password': connection_details['password'],
            'database_name': connection_details['database'],  # Remap 'database' to 'database_name'

            'id': data.get('id'),
            'deleted_at': data.get('deleted_at'),
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at')
        }
        return cls(**remapped_data)

    def get_details_markdown(self):
        return f"""Data source details:
- **Connection Name:** `{self.name}`
- **Database Type:** `{self.dtype}`
- **Description:** `{self.description}`
- **Hostname:** `{self.hostname}`
- **Port:** `{self.port}`
- **Database Name:** `{self.database_name}`
- **Username:** `{self.username}`
- **Password:** `{'*' * len(self.password)}`
"""

    def display_info(self):
        """Prints the data source information."""
        info = (
            f"Owner ID: {self.owner_id}\n"
            f"Name: {self.name}\n"
            f"Type: {self.dtype}\n"
            f"Description: {self.description}\n"
            f"Host: {self.hostname}\n"
            f"Port: {self.port}\n"
            f"Username: {self.username}\n"
            f"Password: {'*' * len(self.password)}\n"
            f"Database Name: {self.database_name}\n"
            f"ID: {self.id}\n"
            f"Deleted At: {self.deleted_at}\n"
            f"Created At: {self.created_at}\n"
            f"Updated At: {self.updated_at}"
        )
        print(info)

# json_str = '''
# {
#     "owner_id":1,
#     "name":"test02",
#     "type":"mysql",
#     "description":"president database",
#     "connection":{
#         "host":"localhost",
#         "port":3306,
#         "username":"testuser1",
#         "password":"password000",
#         "database":"testdb1"
#     },
#     "id":1,
#     "deleted_at":null,
#     "created_at":"2024-04-03T15:00:35.442755",
#     "updated_at":"2024-04-03T15:00:35.442802"
# }
# '''

# # Create a DataSource instance from JSON
# data_source_from_json = DataSource.from_json(json_str)

# # Display the data source information
# data_source_from_json.display_info()


class Worksheet:
    def __init__(self, worksheet_name, prompt, data_source_id, username, metadata="", preview_data=None, data=None):
        self.worksheet_name = worksheet_name
        self.prompt = prompt
        self.data_source_id = data_source_id
        self.username = username
        self.metadata = metadata
        self.preview_data = pd.DataFrame(preview_data) if preview_data is not None else None
        self.data = pd.DataFrame(data) if data is not None else None

    @classmethod
    def from_dict(cls, data_dict):
        """Instantiate from a dictionary, converting preview_data and data to DataFrames."""
        preview_data = data_dict.get('preview_data', None)
        data = data_dict.get('data', None)

        return cls(
            worksheet_name=data_dict.get('worksheet_name'),
            prompt=data_dict.get('prompt'),
            data_source_id=data_dict.get('data_source_id'),
            username=data_dict.get('username'),
            metadata=data_dict.get('metadata', ""),
            preview_data=preview_data,
            data=data
        )

    @classmethod
    def from_json(cls, json_str):
        """Instantiate from a JSON string."""
        data_dict = json.loads(json_str)
        return cls.from_dict(data_dict)

    def get_details_markdown(self):
        return f"""Data source details:
- **Worksheet Name:** `{self.worksheet_name}`
- **Username:** `{self.username}`
- **Prompt:** `{self.prompt}`
- **Metadata:** `{self.metadata}`
"""

    # Additional methods as needed


# # Example dictionary with list of dictionaries for preview_data and data
# worksheet_dict = {
#     "worksheet_name": "Example Worksheet",
#     "prompt": "Make it happen",
#     "data_source_id": 1,
#     "username": "user1",
#     "metadata": "Sample metadata",
#     "preview_data": [{"column1": 1, "column2": "A"}, {"column1": 2, "column2": "B"}],
#     "data": [{"column1": 1, "column2": "A"}, {"column1": 2, "column2": "B"}]
# }

# # Creating an instance from a dictionary
# worksheet_from_dict = Worksheet.from_dict(worksheet_dict)

# # Example JSON string
# worksheet_json = json.dumps(worksheet_dict)

# # Creating an instance from a JSON string
# worksheet_from_json = Worksheet.from_json(worksheet_json)

# # Example of accessing the DataFrame attribute
# print(worksheet_from_dict.preview_data)
# print(worksheet_from_json.data)
