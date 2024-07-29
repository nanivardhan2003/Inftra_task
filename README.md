# Overview

This project consists of several functions for loading, preprocessing, and analyzing sales data from an `orders.csv` file. It includes functions to calculate monthly revenue, product revenue, and customer revenue. Additionally, there are tests for these functions to ensure they work correctly. The project also contains a script to generate synthetic sales data for testing purposes.

## Requirements

- Python 3.6+
- pandas
- numpy
- Faker
- Docker

## Usage

To build the Docker images and start the services, use the following commands:

1. Build the Docker images:
   ```bash
   docker-compose build
   ```
   
2. Start the task service:
   ```bash
   docker-compose up task
   ```
   
3. Start the test service:
   ```bash
   docker-compose up test
   ```

## Files

- **generate_csv.py**: This file generates the required CSV data to analyze.
- **orders_analysis.py**: This file includes the functions to perform the operations mentioned in the task.
- **test.py**: This file includes the unit test cases.
- **readme.md**: This file provides an overview and instructions for the project.
