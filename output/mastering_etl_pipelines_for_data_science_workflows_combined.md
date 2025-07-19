# Mastering ETL Pipelines for Data Science Workflows

*By Pankaj Nagar*

---

## Chapter 1: Chapter 1 Environment Setup

# Chapter 1: Setting Up Your Environment

This chapter will guide you through preparing your Python environment and obtaining a real-world dataset to use throughout the ebook. By the end, you’ll be ready to follow along with hands-on ETL examples.

---

## 1.1 Install Python and Create a Virtual Environment

- **Recommended:** Python 3.8 or newer.
- Check your version:
  ```sh
  python3 --version
  ```
- (Optional but recommended) Create a virtual environment:
  ```sh
  python3 -m venv etl_env
  source etl_env/bin/activate  # On Windows: etl_env\Scripts\activate
  ```

---

## 1.2 Install Required Packages

Install the core libraries for ETL workflows:

```sh
pip install pandas duckdb sqlalchemy flask
```

- **Pandas**: Data manipulation
- **DuckDB**: In-memory SQL analytics
- **SQLAlchemy**: Database connections
- **Flask**: Serving APIs
- (Optional) Jupyter for interactive exploration:
  ```sh
  pip install notebook
  ```

---

## 1.3 Download a Sample Dataset

We’ll use the Uber NYC TLC dataset as a practical example. You can download it from GitHub or Kaggle.

- **From GitHub:**
  - [Uber TLC FOIL Response](https://github.com/fivethirtyeight/uber-tlc-foil-response)
  - Example (April 2014 data):
    ```sh
    wget https://github.com/fivethirtyeight/uber-tlc-foil-response/raw/master/uber-trip-data/uber-raw-data-apr14.csv
    ```
- **From Kaggle:**
  1. Install Kaggle CLI: `pip install kaggle`
  2. Authenticate with your Kaggle API token.
  3. Download:
     ```sh
     kaggle datasets download -d fivethirtyeight/uber-pickups-in-new-york-city
     unzip uber-pickups-in-new-york-city.zip
     ```

---

## 1.4 Load and Explore the Dataset

**Load the CSV into Pandas:**
```python
import pandas as pd
df = pd.read_csv("uber-raw-data-apr14.csv")  # Use your downloaded file name
print(df.head())
print(df.info())
```

**Inspect the Data:**
```python
print(df.describe())
print(df.isnull().sum())
```

---

## 1.5 (Optional) Register DataFrame with DuckDB

```python
import duckdb
con = duckdb.connect()
con.register("uber_data", df)
result = con.execute("SELECT * FROM uber_data LIMIT 5").fetchdf()
print(result)
```

---

## 1.6 Summary Table

| Step | Action | Command/Link |
|------|--------|--------------|
| 1    | Install Python, create venv, install packages | `pip install pandas duckdb` |
| 2    | Download Uber dataset | [GitHub](https://github.com/fivethirtyeight/uber-tlc-foil-response) or [Kaggle](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city) |
| 3    | Load data in Pandas | `pd.read_csv("filename.csv")` |
| 4    | Register with DuckDB | `con.register("uber_data", df)` |

---

You’re now ready to follow the rest of the ebook and build your ETL pipeline!



---

## Chapter 2: Chapter 2 Extract Phase

# Chapter 2: The "Extract" Phase: Getting Your Data (Expanded)

## 2.1 Understanding the Extract Phase

The **Extract** phase is the starting point of any ETL pipeline. It involves retrieving data from one or more source systems, such as:

- CSV/Excel files
- Relational databases (MySQL, PostgreSQL, SQLite)
- APIs (RESTful services, webhooks)
- Streaming platforms (Kafka, WebSockets)

The goal is to collect raw data and bring it into your working environment in a usable format (typically a Pandas DataFrame).

---

## 2.2 Extracting from CSV Files

### Sample Dataset

We’ll use a sample CSV `uber_trips.csv` containing the following fields:

- `driver_id`
- `trip_date`
- `pickup_location`
- `dropoff_location`
- `trip_distance`
- `fare_amount`
- `rating`

### Practice Code: Extract Function for CSV

def extract_from_csv(file_path):
```python
import pandas as pd

def extract_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully!")
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return pd.DataFrame()

# Usage
csv_path = "data/uber_trips.csv"
df_csv = extract_from_csv(csv_path)
```

*This function attempts to load a CSV file into a DataFrame. If the file is found, it prints a success message and returns the DataFrame; if not, it prints an error and returns an empty DataFrame. The usage example shows how to call the function for a specific file.*

### Tips

- Always validate the file path.
- Use `df_csv.info()` and `df_csv.describe()` to verify data quality.

---

## 2.3 Extracting from Relational Databases with SQLAlchemy

Relational databases are robust data sources commonly used in enterprise applications.

### Prerequisite: Install SQLAlchemy and SQLite driver

```bash
pip install sqlalchemy
```

*This command installs SQLAlchemy, a Python library for working with SQL databases, which is required for the next code example.*

### Practice Code: Extract from SQLite

```python
from sqlalchemy import create_engine

# Create a connection to an existing SQLite DB
engine = create_engine("sqlite:///data/processed_uber_data.db")

# Read a table
df_sql = pd.read_sql("SELECT * FROM trips", con=engine)
print(df_sql.head())
```

*This code connects to a SQLite database using SQLAlchemy, reads the 'trips' table into a DataFrame, and prints the first few rows. It demonstrates how to extract data from a relational database into Pandas.*

### For MySQL or PostgreSQL

Use the appropriate URI:

- MySQL: `mysql+pymysql://username:password@host:port/database`
- PostgreSQL: `postgresql://username:password@host:port/database`

---

## 2.4 Extracting from APIs

For modern web applications, data may come from APIs.

### Practice Code: API Request with Requests

def extract_from_api(url):
```python
import requests

def extract_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        print("Failed to fetch data.")
        return pd.DataFrame()

api_url = "https://api.example.com/uber/trips"
df_api = extract_from_api(api_url)
```

*This function sends a GET request to the specified API URL. If the request is successful, it loads the JSON response into a DataFrame; otherwise, it prints an error and returns an empty DataFrame. The usage example shows how to call the function for a sample API endpoint.*

### Notes:

- Handle authentication (API keys, OAuth) if required.
- Consider rate limits and pagination.

---

## 2.5 Extracting from Streaming Platforms (Introductory)

Streaming data requires real-time handling. Here’s a simplified mockup:

def stream_data_simulator():
```python
import time
import random

def stream_data_simulator():
    while True:
        new_record = {
            'driver_id': random.randint(1000, 9999),
            'trip_distance': round(random.uniform(1, 25), 2),
            'rating': round(random.uniform(3.5, 5.0), 1)
        }
        print(new_record)
        time.sleep(1)

# stream_data_simulator()  # Uncomment to run
```

*This mockup simulates streaming data by generating and printing a new record every second. Each record contains random values for driver ID, trip distance, and rating. This is useful for testing real-time ETL logic.*

For production use, tools like Kafka or WebSockets are recommended.

---

## 2.6 Summary Checklist

✅ Extracted data from CSV using Pandas\
✅ Connected to and read from a relational database using SQLAlchemy\
✅ Pulled data from a REST API using requests\
✅ Simulated streaming data for real-time pipelines

## 2.7 Exercises

1. Create an extract function that supports both CSV and SQLite as input.
2. Modify the API extractor to handle paginated results.
3. Simulate 10 records from the streaming mockup and store them in a list.

---

In the next chapter, we’ll dive into transforming data using **DuckDB SQL**, where you’ll learn to clean, filter, and aggregate your extracted data efficiently.

*End of Chapter 2*



---

## Chapter 3: Chapter 3 Transform Phase

# Chapter 3: The "Transform" Phase – Cleaning and Shaping Data with DuckDB SQL

## 3.1 Why Transform Data?

Once raw data is extracted, it’s often messy, inconsistent, and not ready for analysis or modeling. The **Transform** phase applies business logic, cleans data, reshapes formats, handles missing values, and calculates derived fields. This step ensures your data is analytical-grade.

Benefits:

- Filter out irrelevant or corrupt records
- Normalize formats (dates, currency, strings)
- Apply calculations (e.g., revenue, duration)
- Join data from multiple sources
- Prepare features for machine learning or reporting

---

## 3.2 Why Use DuckDB for Transformations?

DuckDB is a high-performance, in-process SQL OLAP engine designed for analytical tasks. It runs SQL directly on Pandas DataFrames or CSV files, making it ideal for:

- Complex aggregations
- Joins
- Filtering
- Common Table Expressions (CTEs)
- Lightweight ETL scripting

### DuckDB Setup (Recap)

```python
import duckdb
con = duckdb.connect()
con.register("trips", df)  # df is a Pandas DataFrame
```

*This code imports DuckDB, creates a connection, and registers a Pandas DataFrame as a DuckDB table. This allows you to run SQL queries directly on your DataFrame.*

---

## 3.3 Practical Transformations with DuckDB

### 3.3.1 Filtering with Multi-Criteria

Let’s say we want to find drivers eligible for a bonus:

```sql
WHERE rating >= 4.8
AND acceptance_rate > 0.9
AND trips_completed > 50
```

### Example

```python
query = """
SELECT driver_id, rating, trips_completed
FROM trips
WHERE rating >= 4.8 AND acceptance_rate > 0.9 AND trips_completed > 50
"""
qualified = con.execute(query).fetchdf()
print(qualified.head())
```

*This code defines a SQL query to filter drivers who meet all three criteria (high rating, high acceptance rate, and enough completed trips), executes it in DuckDB, and prints the qualifying drivers.*

---

### 3.3.2 Aggregation and Grouping

We can group trips by driver and calculate earnings:

```python
query = """
SELECT driver_id, COUNT(*) AS total_trips, SUM(fare_amount) AS total_earnings
FROM trips
GROUP BY driver_id
"""
summary_df = con.execute(query).fetchdf()
```

*This code groups the trips by driver, counts the number of trips, sums the earnings for each driver, and returns the results as a DataFrame.*

---

### 3.3.3 Boolean Logic: Differences Between Groups

Compare drivers eligible for Program A but not Program B:

```python
query = """
SELECT driver_id
FROM program_a
WHERE driver_id NOT IN (SELECT driver_id FROM program_b)
"""
```

*This query finds drivers who are in Program A but not in Program B by using a subquery in the WHERE clause.*

---

### 3.3.4 Conditional Calculations

Calculate net income with conditional logic:

```python
query = """
SELECT driver_id,
       fare_amount,
       CASE
           WHEN fare_amount > 100 THEN fare_amount * 0.9
           ELSE fare_amount * 0.85
       END AS adjusted_income
FROM trips
"""
```

*This query calculates an adjusted income for each trip using conditional logic: if the fare is above 100, a 10% deduction is applied; otherwise, a 15% deduction is applied.*

---

### 3.3.5 Cohort Analysis Example

Percentage of drivers with <10 trips and >4.7 rating:

```python
query = """
SELECT COUNT(*) * 1.0 / (SELECT COUNT(*) FROM drivers) AS cohort_percentage
FROM drivers
WHERE trips_completed < 10 AND rating > 4.7
"""
```

*This query calculates the percentage of drivers who have fewer than 10 trips and a rating above 4.7, giving insight into a specific cohort.*

---

## 3.4 Using CTEs for Readability

CTEs help structure complex logic.

```python
query = """
WITH bonus_drivers AS (
  SELECT driver_id, SUM(fare_amount) AS earnings
  FROM trips
  GROUP BY driver_id
),
filtered AS (
  SELECT * FROM bonus_drivers WHERE earnings > 1000
)
SELECT COUNT(*) FROM filtered
"""
result = con.execute(query).fetchdf()
```

*This code uses Common Table Expressions (CTEs) to first calculate total earnings per driver, then filter for drivers with earnings above 1000, and finally count how many drivers meet this criterion. CTEs help organize complex SQL logic for readability and reuse.*

---

## 3.5 Summary Checklist

✅ Used DuckDB for SQL queries on Pandas DataFrames\
✅ Applied filters, aggregations, conditional logic, and joins\
✅ Learned cohort analysis and arithmetic logic with SQL\
✅ Used Common Table Expressions (CTEs) for modular transformations

## 3.6 Exercises

1. Write a DuckDB query to calculate total income by city.
2. Create a transformation that identifies top 10% of drivers by earnings.
3. Use a CTE to identify drivers who improved their rating over time.

---

Next, we’ll load this cleaned data into a persistent database (like SQLite) and make it ready for querying via APIs or dashboards.

*End of Chapter 3*



---

## Chapter 4: Chapter 4 Load Phase

# Chapter 4: The "Load" Phase – Storing Processed Data

## 4.1 Purpose of the Load Phase

The **Load** phase is the final step in the ETL process. Once data is cleaned and transformed, it needs to be stored in a persistent, queryable format. This could be for immediate analytics, dashboard use, machine learning pipelines, or natural language querying.

The load phase should:

- Preserve data quality and structure
- Support fast querying (e.g., via SQL or APIs)
- Be lightweight or scalable depending on the use case
- Avoid duplication or data loss

---

## 4.2 Choosing a Target: SQLite for Local and Lightweight Workflows

**SQLite** is a zero-configuration, file-based relational database that works well for:

- Prototypes and POCs
- Flask/FastAPI apps
- Training/testing pipelines
- Offline analysis

### Benefits:

- No server required
- Easy to share as a single `.db` file
- SQL-compliant
- Great integration with Pandas

---

## 4.3 Writing Data with Pandas `to_sql()`

Pandas makes loading transformed data into SQLite very simple.

### Practice Code

```python
import sqlite3

# Load transformed data
conn = sqlite3.connect("data/processed_uber_data.db")

# Assume result_df is your final DataFrame
result_df.to_sql("trips", conn, if_exists="replace", index=False)
conn.close()
```

### Parameters

- `if_exists='replace'`: overwrite existing table
- `index=False`: exclude DataFrame index

### Verification Step

```python
conn = sqlite3.connect("data/processed_uber_data.db")
print(pd.read_sql("SELECT COUNT(*) FROM driver_summary", conn))
conn.close()
```

---

## 4.4 Loading into PostgreSQL or Cloud Databases (Optional)

SQLite is good for local use, but for production:

- Use **PostgreSQL** for scalability
- Use **Cloud SQL / Amazon RDS** for managed services
- Write to **S3 / GCS** as Parquet/CSV for data lakes

With SQLAlchemy, change the engine:

```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@host:port/db")
result_df.to_sql("summary", engine, if_exists="append")
```

---

## 4.5 File-Based Alternatives

If you're not ready for a full database, store transformed data as:

- **CSV**: Portable, readable, large file size
- **Parquet**: Efficient, typed, compressible

### Example

```python
result_df.to_csv("data/final_summary.csv", index=False)
result_df.to_parquet("data/final_summary.parquet")
```

---

## 4.6 Summary Checklist

✅ Wrote final DataFrame to SQLite using `to_sql()`\
✅ Verified table and row counts using SQL queries\
✅ Understood alternatives like PostgreSQL and file formats\
✅ Practiced storing data in structured, persistent formats

## 4.7 Exercises

1. Write a DataFrame to SQLite and then read it back.
2. Try saving the same DataFrame to Parquet format and compare file sizes.
3. Load two different tables (summary and details) and write a SQL join in SQLite to verify data consistency.

---

In Chapter 5, we’ll bring everything together and build a complete, modular ETL pipeline using functions and orchestration best practices.

*End of Chapter 4*



---

## Chapter 5: Chapter 5 Orchestrating Etl

# Chapter 5: Orchestrating Your ETL Pipeline

## 5.1 What is Orchestration in ETL?

Orchestration refers to designing your ETL process in a modular, maintainable, and executable manner. It allows you to control how and when your data pipeline runs, ensure repeatability, and build a foundation for automation and scaling.

Key principles:

- Modularization: Separate extract, transform, and load logic
- Reusability: Use functions that can be reused across datasets
- Clarity: Name functions and variables meaningfully
- Traceability: Log progress and capture errors

---

## 5.2 Building Modular ETL Functions

Let’s start by wrapping our ETL phases into reusable Python functions.

### Example: extract.py

```python
import pandas as pd
from sqlalchemy import create_engine

def extract_from_sqlite(db_path, table_name):
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    return df
```

### Example: transform.py

```python
import duckdb

def transform_driver_data(df):
    con = duckdb.connect()
    con.register("drivers", df)
    query = """
        SELECT driver_id, rating, trips_completed,
               CASE WHEN rating > 4.8 AND trips_completed > 50 THEN 'Top' ELSE 'Standard' END AS status
        FROM drivers
    """
    return con.execute(query).fetchdf()
```

### Example: load.py

```python
import sqlite3

def load_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
```

---

## 5.3 Creating the Master `run_etl_pipeline()` Function

We now integrate all parts into a main runner.

### Example: etl\_pipeline.py

```python
from extract import extract_from_sqlite
from transform import transform_driver_data
from load import load_to_sqlite

def run_etl_pipeline():
    raw_df = extract_from_sqlite("data/processed_uber_data.db", "trips")
    transformed_df = transform_driver_data(raw_df)
    load_to_sqlite(transformed_df, "data/processed_uber_data.db", "trips")
```

This pipeline can now be executed manually, scheduled via cron, or triggered through an API.

---

## 5.4 Adding Logging and Error Handling

### Simple Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.info("ETL pipeline started")
```

### Error Wrapping

```python
try:
    run_etl_pipeline()
    logging.info("ETL pipeline completed successfully")
except Exception as e:
    logging.error(f"ETL failed: {e}")
```

---

## 5.5 Scheduling and Automation

You can schedule your ETL pipeline using:

- **cron** (Linux/macOS)
- **Windows Task Scheduler**
- **Python **``** or **``
- **Workflow tools** like Airflow, Prefect, or Dagster

Example with `schedule`:

```python
import schedule
import time

schedule.every().day.at("00:00").do(run_etl_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 5.6 Summary Checklist

✅ Created separate functions for extract, transform, load\
✅ Integrated them in a master pipeline function\
✅ Added error handling and basic logging\
✅ Learned options to automate your ETL

## 5.7 Exercises

1. Add logging to each ETL phase to track start and end times.
2. Modify the transform function to include bonus eligibility logic.
3. Schedule your pipeline to run every 6 hours using `schedule`.

---

In Chapter 6, we will focus on SQL performance tuning and optimization strategies to scale your ETL workflows efficiently for larger datasets and production environments.

*End of Chapter 5*



---

## Chapter 6: Chapter 6 Sql Optimization

# Chapter 6: Optimizing SQL Queries for High-Performance ETL

## 6.1 Why SQL Optimization Matters in ETL

As your data scales from thousands to millions of records, inefficient SQL queries can severely degrade ETL performance. Optimizing queries ensures:

- Faster data processing
- Lower memory usage
- Reduced load on database servers
- Better scalability

In the context of ETL, optimized SQL improves both extraction and transformation efficiency, especially when using tools like DuckDB, PostgreSQL, or cloud-hosted databases.

---

## 6.2 General Principles for Efficient SQL

### ✅ Select Only What You Need

Avoid `SELECT *`. Specify only the required columns.

```sql
SELECT driver_id, rating, trips_completed FROM trips;
```

### ✅ Filter Early and Precisely

Apply `WHERE` clauses as early as possible.

```sql
SELECT * FROM trips WHERE rating >= 4.8 AND trips_completed > 50;
```

### ✅ Use Indexes (for DBMS like PostgreSQL)

Create indexes on columns used in `JOIN`, `WHERE`, or `ORDER BY`.

```sql
CREATE INDEX idx_driver_rating ON trips(rating);
```

### ✅ Avoid Functions on Indexed Columns

This breaks index usage:

```sql
WHERE YEAR(trip_date) = 2024  -- ❌ inefficient
```

Use instead:

```sql
WHERE trip_date >= '2024-01-01' AND trip_date < '2025-01-01'  -- ✅ efficient
```

### ✅ Prefer INNER JOINs with ON

```sql
SELECT *
FROM trips d
INNER JOIN trips t ON d.driver_id = t.driver_id;
```

---

## 6.3 Optimizing Aggregations and Subqueries

### ✅ Minimize Use of Subqueries

Refactor deeply nested queries using CTEs or joins.

### ✅ Aggregate Only What You Need

Avoid unnecessary `DISTINCT` or `GROUP BY` on non-essential columns.

### Example

```sql
WITH driver_stats AS (
  SELECT driver_id, COUNT(*) AS trips, SUM(fare_amount) AS earnings
  FROM trips
  WHERE trip_date >= '2024-01-01'
  GROUP BY driver_id
)
SELECT * FROM driver_stats WHERE earnings > 1000;
```

---

## 6.4 Reducing Data Volume Early

Apply filters as early as possible in your ETL logic—whether in the SQL layer or Python/DuckDB.

```sql
SELECT * FROM trips
WHERE trip_date >= CURRENT_DATE - INTERVAL '30 days';
```

Use `LIMIT` or `OFFSET` for previewing data:

```sql
SELECT * FROM trips LIMIT 100;
```

---

## 6.5 Best Practices Summary Table

| Technique                        | Benefit                            |
| -------------------------------- | ---------------------------------- |
| Select specific columns          | Reduces memory and transfer time   |
| Index frequently filtered fields | Accelerates search and joins       |
| Filter early                     | Reduces processed rows early       |
| Avoid subqueries                 | Simplifies logic, speeds execution |
| Partition large tables           | Reduces data scan time             |
| Avoid functions in WHERE         | Keeps index usage intact           |

---

## 6.6 SQL Optimization in DuckDB

While DuckDB is in-memory and fast by default, good practices still help:

- Avoid wide `SELECT *` queries
- Use `WHERE` to reduce in-memory filtering
- Leverage `LIMIT`, `GROUP BY`, and `CTE` for large datasets

```python
query = """
WITH eligible AS (
  SELECT driver_id, COUNT(*) AS trip_count
  FROM trips
  WHERE trip_date >= '2024-01-01'
  GROUP BY driver_id
)
SELECT * FROM eligible WHERE trip_count > 10;
"""
df = con.execute(query).fetchdf()
```

---

## 6.7 Advanced Optimization Concepts

### Materialized Views

- Store precomputed query results for frequent use

### Stored Procedures (for PostgreSQL, MySQL)

- Encapsulate complex logic inside the database
- Reduce network overhead

### Batch Processing

- Avoid row-by-row inserts/updates; use bulk loads

---

## 6.8 Summary Checklist

✅ Avoided `SELECT *` and chose only required columns\
✅ Applied WHERE clauses early\
✅ Used CTEs and minimized subqueries\
✅ Considered indexing and partitioning\
✅ Practiced SQL tuning inside DuckDB

## 6.9 Exercises

1. Rewrite an existing `SELECT *` query to retrieve only the necessary columns.
2. Refactor a nested subquery into a Common Table Expression.
3. Benchmark query performance with and without WHERE filters.

---

In Chapter 7, we’ll explore how to adapt your ETL pipelines for **real-time data processing** using APIs, streams, and event-driven workflows.

*End of Chapter 6*



---

## Chapter 7: Chapter 7 Real Time Etl

# Chapter 7: Adapting ETL for Real-Time Data Updates

## 7.1 From Batch to Real-Time ETL

Traditional ETL processes are designed for scheduled execution (e.g., daily, hourly). However, many modern applications—such as ride-sharing, finance, and monitoring systems—require near-instant updates. This chapter explores how to shift your ETL architecture to support **real-time or streaming data workflows**.

Real-time ETL benefits:

- Immediate data availability
- Timely insights and alerts
- Live dashboards and APIs

---

## 7.2 Key Components of Real-Time ETL

| Phase     | Strategy                     | Tools                         |
| --------- | ---------------------------- | ----------------------------- |
| Extract   | Event stream ingestion       | Kafka, WebSocket, API polling |
| Transform | In-memory, incremental logic | Pandas, DuckDB                |
| Load      | Incremental DB updates       | SQLite, PostgreSQL            |
| Serve     | Push to clients or endpoints | Flask, SSE, WebSocket         |

---

## 7.3 Real-Time Extraction Examples

### Option 1: Polling APIs

```python
import requests
import time

while True:
    response = requests.get("https://api.example.com/uber/trips")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        print(df.head())
    time.sleep(10)  # poll every 10 seconds
```

### Option 2: Simulated Streaming

```python
import random
import time

def stream_data():
    while True:
        record = {
            'driver_id': random.randint(1000, 9999),
            'trip_distance': round(random.uniform(1, 20), 2),
            'timestamp': pd.Timestamp.now()
        }
        print(record)
        time.sleep(1)
```

---

## 7.4 Real-Time Transformation with DuckDB

You can register streamed data with DuckDB and apply lightweight SQL transforms on the fly.

```python
import duckdb
import pandas as pd

con = duckdb.connect()

# Suppose `df` is incoming data
con.register("stream", df)

transformed = con.execute("""
    SELECT driver_id, trip_distance,
           CASE WHEN trip_distance > 10 THEN 'Long' ELSE 'Short' END AS trip_type
    FROM stream
""").fetchdf()
```

---

## 7.5 Real-Time Loading

Use incremental inserts or upserts to store streamed records:

```python
import sqlite3

def load_incremental(df, db_path, table):
    conn = sqlite3.connect(db_path)
    df.to_sql(table, conn, if_exists='append', index=False)
    conn.close()
```

Use a unique key (e.g., trip\_id) to prevent duplication in production systems.

---

## 7.6 Serving Real-Time Data with Flask & SSE

**Server-Sent Events (SSE)** allow Flask to push live updates to browsers:

```python
from flask import Flask, Response
import time, json

app = Flask(__name__)

def generate_stream():
    while True:
        data = {"timestamp": str(pd.Timestamp.now())}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(2)

@app.route('/stream')
def stream():
    return Response(generate_stream(), mimetype='text/event-stream')
```

---

## 7.7 Best Practices for Real-Time ETL

- **Asynchronous Processing:** Use Celery or asyncio to offload ETL from Flask threads
- **Micro-Batching:** Group events in short intervals (1–5 seconds) for processing
- **Idempotency:** Avoid duplicate inserts by handling keys/versions
- **Scalability:** Use Kafka, Redis Streams, or cloud pub/sub systems for high volume
- **Monitoring:** Log ETL events and track latency metrics

---

## 7.8 Summary Checklist

✅ Streamed data from APIs or simulated sources\
✅ Transformed using DuckDB on the fly\
✅ Loaded incrementally to SQLite or PostgreSQL\
✅ Served live data to clients with SSE\
✅ Applied real-time ETL best practices

## 7.9 Exercises

1. Simulate 50 records and transform them in-memory using DuckDB.
2. Write a streaming ETL loop that saves data every 5 seconds.
3. Add a Flask SSE endpoint that broadcasts the most recent transformed record.

---

In Chapter 8, we’ll deploy our ETL pipeline to the cloud using FastAPI, Docker, and managed hosting services.

*End of Chapter 7*



---

## Chapter 8: Chapter 8 Cloud Deployment

# Chapter 8: Building and Deploying ETL Pipelines for the Cloud

## 8.1 Why Deploy ETL to the Cloud?

Cloud deployment enables your ETL pipeline to scale, be accessible from anywhere, and integrate with broader systems like data warehouses, analytics platforms, and AI services. This chapter covers:

- Building a FastAPI-based ETL app
- Containerizing with Docker
- Deploying on cloud services
- Applying cloud-native best practices

---

## 8.2 FastAPI: Lightweight API for Triggering ETL

Use FastAPI to create a simple HTTP interface for your pipeline.

### Example: `app/main.py`

```python
from fastapi import FastAPI
from etl_pipeline import run_etl_pipeline

app = FastAPI()

@app.get("/run-etl")
def trigger_etl():
    run_etl_pipeline()
    return {"message": "ETL completed successfully"}
```

### Directory Structure

```
app/
├── main.py
├── etl_pipeline.py
├── extract.py
├── transform.py
├── load.py
Dockerfile
requirements.txt
```

---

## 8.3 Containerizing with Docker

### Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Build and Run Locally

```bash
docker build -t etl-app .
docker run -p 80:80 etl-app
```

---

## 8.4 Deploying on the Cloud

### Options

- **Render.com / Railway** – Simple auto-deploy from GitHub
- **AWS EC2** – Full control, manual setup
- **Google Cloud Run** – Serverless container execution
- **Azure App Service** – Integrated CI/CD

### General Deployment Steps

1. Push your code to GitHub
2. Connect your repo to a cloud platform (Render/GCR/etc.)
3. Configure build commands and Docker settings
4. Set environment variables (e.g., DB path, API keys)
5. Deploy and test with `/run-etl` endpoint

---

## 8.5 Cloud-Native Best Practices

- **Use environment variables:** Never hard-code credentials
- **Monitor with logs:** Use `logging` or services like CloudWatch, GCP Logging
- **Use managed databases:** Prefer RDS, Cloud SQL over local SQLite
- **Auto-scale:** Use container-based scaling (Cloud Run, ECS, K8s)
- **Secure your endpoints:** Add authentication to ETL triggers

---

## 8.6 Bonus: Natural Language Querying with LangChain + SQL

Integrate OpenAI or LangChain to allow users to query your database using plain English.

### Example

```python
from langchain.chains import SQLDatabaseChain
from langchain.llms import OpenAI

from langchain.sql_database import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///data/processed_uber_data.db")
llm = OpenAI(temperature=0)

chain = SQLDatabaseChain.from_llm(llm, db)
response = chain.run("What was the average rating of drivers last week?")
print(response)
```

---

## 8.7 Summary Checklist

✅ Built an ETL API with FastAPI\
✅ Containerized with Docker\
✅ Deployed to a cloud provider\
✅ Applied cloud-native best practices\
✅ Connected with AI query interface (optional)

## 8.8 Exercises

1. Build a minimal FastAPI app that wraps your ETL pipeline.
2. Deploy your app using Render or Google Cloud Run.
3. (Optional) Add authentication and logging to your `/run-etl` endpoint.

---

In the final chapter, we’ll summarize what you’ve learned and explore how to advance into deeper data engineering topics.

*End of Chapter 8*



---

## Chapter 9: Chapter 9 Conclusion

# Chapter 9: Conclusion and Next Steps in Data Engineering

## 9.1 Recap of the ETL Journey

Congratulations! You’ve completed a full walkthrough of designing, building, and deploying ETL pipelines tailored for modern data workflows.

Here’s what you’ve accomplished:
- **Chapter 1–2:** Setup, data loading, and extraction from files, APIs, and databases
- **Chapter 3:** Transformation using DuckDB SQL – from filtering to aggregation and CTEs
- **Chapter 4:** Persisting data using SQLite and exploring alternatives
- **Chapter 5:** Writing modular pipelines using Python functions and orchestrating them
- **Chapter 6:** Optimizing SQL queries for performance and scalability
- **Chapter 7:** Handling real-time ETL use cases with streaming and Flask
- **Chapter 8:** Deploying pipelines to the cloud using FastAPI, Docker, and managed services

This foundation positions you to build production-grade ETL systems that are scalable, testable, and extensible.

---

## 9.2 What’s Next?

After mastering basic and intermediate ETL concepts, here are the next steps to grow further as a data engineer or backend automation specialist:

### Learn Workflow Orchestration Tools
- **Prefect** or **Apache Airflow** for managing DAGs and scheduling

### Build Data Lakes and Warehouses
- Integrate with **BigQuery**, **Snowflake**, or **Redshift**
- Use **Parquet**, **Delta Lake**, or **Iceberg** for analytical storage

### Stream Data at Scale
- Adopt tools like **Kafka**, **Apache Flink**, **Redpanda**, or **Spark Structured Streaming**

### Improve Data Quality
- Add **validation tests** with **Great Expectations** or **pandera**
- Integrate **unit testing** into your ETL functions

### Connect with the Modern Data Stack
- Tools like **dbt**, **Metabase**, **Superset**, **Dagster**
- Monitor with **Prometheus**, **Grafana**, or **ELK Stack**

---

## 9.3 Final Reflections

Remember, a great ETL pipeline is not only fast—it is reliable, observable, and maintainable. It transforms raw data into trustable knowledge that fuels decisions.

As data grows, automation becomes essential. What you’ve built here can serve as:
- A prototype for client dashboards
- A back-end system for live business metrics
- A plug-and-play template for consulting work

Stay curious. Stay practical. Keep automating!

---

## 9.4 Suggested Resources

- [DuckDB Documentation](https://duckdb.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [LangChain](https://www.langchain.com)
- [Apache Airflow](https://airflow.apache.org)
- [Awesome ETL Tools List](https://github.com/pawl/awesome-etl)

---

## 9.5 Final Exercises
1. Extend your ETL pipeline to support weekly auto-runs using Prefect.
2. Replace SQLite with PostgreSQL on a cloud provider.
3. Connect your pipeline to a dashboard frontend using Streamlit or Metabase.

---

Thank you for reading. You’re now well-equipped to build powerful, real-world ETL workflows.

*End of Book*



---

## Chapter 10: Chapter A Bonus Chapter Lang Chain Sql

# Bonus Chapter: Step-by-Step Tutorial – Natural Language Querying with LangChain + SQL

## B.1 Introduction

In this bonus chapter, you’ll learn how to build a simple natural language interface over your SQLite database using **LangChain** and **OpenAI**. This will enable users to ask questions like:

> "What is the average driver rating last month?"

and receive a SQL-backed response.

This feature is powerful for internal analytics tools, customer-facing dashboards, or rapid prototyping for startups.

---

## B.2 Prerequisites

Install the required libraries:

```bash
pip install langchain openai sqlalchemy
```

Also, ensure your SQLite database (e.g., `processed.db`) has tables with relevant data (like `drivers`, `trips`, etc.).

You’ll need an OpenAI API key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

Set it as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Windows (Command Prompt):

```cmd
set OPENAI_API_KEY=your-api-key
```

---

## B.3 Sample SQLite Database

Assume you’ve already saved a processed DataFrame:


```python
import sqlite3

conn = sqlite3.connect("data/processed_uber_data.db")
df.to_sql("trips", conn, if_exists="replace", index=False)
conn.close()
```

*This code connects to a SQLite database file, saves a DataFrame as a table named 'drivers', and then closes the connection. It is used to persist processed data for later querying.*

Example table `drivers`:

| driver\_id | rating | city | total\_trips |
| ---------- | ------ | ---- | ------------ |
| 1001       | 4.9    | NY   | 120          |
| 1002       | 4.7    | LA   | 80           |

---

## B.4 Code to Set Up LangChain + SQL


```python
from langchain.chains import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from langchain.llms import OpenAI
import os

# Make sure your OpenAI key is set as an env variable
assert os.getenv("OPENAI_API_KEY") is not None

# Connect to SQLite DB
db = SQLDatabase.from_uri("sqlite:///data/processed_uber_data.db")

# Set up LLM
llm = OpenAI(temperature=0)

# Create chain
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Ask a question
question = "What is the average rating of drivers in New York?"
response = chain.run(question)
print(response)
```

*This code sets up a LangChain SQLDatabaseChain using OpenAI as the language model and connects it to your SQLite database. It allows you to ask natural language questions, which are translated to SQL, executed, and the results are returned. The example asks for the average rating of drivers in New York and prints the answer.*

---

## B.5 How It Works

- LangChain uses GPT via OpenAI to parse your natural language
- It translates the query into valid SQL (e.g., `SELECT AVG(rating) FROM drivers WHERE city = 'NY'`)
- Then it executes that SQL via SQLAlchemy and returns the result

### Output Example:

```
The average driver rating in New York is 4.87
```

---

## B.6 Tips for Best Results

✅ Ensure table and column names are clean and intuitive\
✅ Seed your tables with enough sample data\
✅ Set `temperature=0` for factual precision\
✅ Use `verbose=True` to see underlying SQL translations

---

## B.7 Security Warning

This setup sends queries and data to OpenAI’s API. Do **not** use this for production or sensitive datasets without:

- Sanitizing user inputs
- Limiting table access
- Using a self-hosted LLM for data privacy

---

## B.8 Exercises

1. Create another table (`trips`) and ask, "How many trips were taken last week?"
2. Modify the prompt to limit responses to 2 sentences.
3. Deploy this interface as an endpoint in your FastAPI app.

---

With this setup, you can now integrate AI-powered querying directly into dashboards, apps, and reports.

*End of Bonus Chapter*



---

