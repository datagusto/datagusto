import enum


class DataSourceType(str, enum.Enum):
    PostgreSQL = "postgresql"
    BigQuery = "bigquery"
    Snowflake = "snowflake"
    Redshift = "redshift"
    Databricks = "databricks"
    DuckDB = "duckdb"
    MicrosoftSQLServer = "mssql"
    CSVFile = "csvfile"
    ExcelFile = "excelfile"
    TabularFile = "tabularfile"
    MongoDB = "mongodb"
    Oracle = "oracle"
    SAPHana = "saphana"
    SQLite = "sqlite"
    MySQL = "mysql"
    Gorgias = "gorgias"
    SpreadSheet = "spreadsheet"
    Notion = "notion"
    Shopify = "shopify"
