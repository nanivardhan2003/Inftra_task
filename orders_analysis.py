import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file and handle potential file issues.

    Args:
        file_path (str): The path to the CSV file to be loaded.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or cannot be parsed.
        RuntimeError: If an unexpected error occurs.

    Returns:
        pd.DataFrame: The data from the CSV file as a Pandas DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("The file was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The file could not be parsed.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

def preprocess_data(df):
    """
    Preprocess the data by ensuring required columns are present, converting 
    'order_date' to datetime, and calculating additional columns.

    Args:
        df (pd.DataFrame): The input data frame containing order information.

    Raises:
        ValueError: If any required columns are missing.
        ValueError: If there is an error converting 'order_date' to datetime.

    Returns:
        pd.DataFrame: The processed data frame with new columns 'revenue' and 'month'.
    """
    required_columns = ['order_id', 'customer_id', 'order_date', 'product_id', 'product_name', 'product_price', 'quantity']
    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    # Convert 'order_date' to datetime
    df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d', errors='coerce')
    if df['order_date'].isna().any():
        raise ValueError("Error converting 'order_date' to datetime")

    # Calculate revenue and month columns
    df['revenue'] = df['product_price'] * df['quantity']
    df['month'] = df['order_date'].dt.to_period('M')
    return df

def calculate_monthly_revenue(df):
    """
    Calculates the total revenue for each month.

    Args:
        df (pd.DataFrame): The input data frame containing order information. 
                           It must include the 'month' and 'revenue' columns.

    Returns:
        pd.DataFrame: A data frame with two columns: 'Month' and 'Total Revenue', 
                      where 'Month' represents the month and 'Total Revenue' represents the 
                      total revenue for that month.
    """
    # Group the data by 'month', sum the 'revenue' for each group,
    # reset the index of the DataFrame, and rename the columns for clarity
    return df.groupby('month')['revenue'].sum().reset_index().rename(columns={'month': 'Month', 'revenue': 'Total Revenue'})

def calculate_product_revenue(df):
    """
    Calculates the total revenue for each product.

    Args:
        df (pd.DataFrame): The input data frame containing order information.
                           It must include the 'product_name' and 'revenue' columns.

    Returns:
        pd.DataFrame: A data frame with two columns: 'Product Name' and 'Total Revenue',
                      where 'Product Name' represents the name of the product and 
                      'Total Revenue' represents the total revenue for that product.
    """
    # Group the data by 'product_name', sum the 'revenue' for each group,
    # reset the index of the DataFrame, and rename the columns for clarity
    return df.groupby('product_name')['revenue'].sum().reset_index().rename(columns={'product_name': 'Product Name', 'revenue': 'Total Revenue'})

def calculate_customer_revenue(df):
    """
    Calculates the total revenue for each customer.

    Args:
        df (pd.DataFrame): The input data frame containing order information.
                           It must include the 'customer_id' and 'revenue' columns.

    Returns:
        pd.DataFrame: A data frame with two columns: 'Customer ID' and 'Total Revenue',
                      where 'Customer ID' represents the ID of the customer and 
                      'Total Revenue' represents the total revenue for that customer.
    """
    # Group the data in 'customer_id' dataframe by the 'customer_id' column,
    # sum the 'revenue' column for each group, reset the index of the DataFrame,
    # and rename the columns for clarity
    return df.groupby('customer_id')['revenue'].sum().reset_index().rename(columns={'customer_id': 'Customer ID', 'revenue': 'Total Revenue'})

def get_top_customers(customer_revenue):
    """
    Get the top 10 customers based on total revenue.

    Args:
        customer_revenue (pd.DataFrame): The data frame containing customer revenue information.
                                         It must include the 'Customer ID' and 'Total Revenue' columns.

    Returns:
        pd.DataFrame: A data frame with the top 10 customers sorted by 'Total Revenue' in descending order.
                      It includes the same columns as the input data frame.
    """
    # Sort the DataFrame 'customer_revenue' by the 'Total Revenue' column in descending order,
    # then return the top 10 rows
    return customer_revenue.sort_values(by='Total Revenue', ascending=False).head(10)

def main():
    try:
        # Load the data
        df = load_data('orders.csv')
        
        # Preprocess the data
        df = preprocess_data(df)

        # Calculate revenues
        monthly_revenue = calculate_monthly_revenue(df)
        product_revenue = calculate_product_revenue(df)
        customer_revenue = calculate_customer_revenue(df)
        top_customers = get_top_customers(customer_revenue)

        # Print results
        print("Total Revenue by Month:")
        print(monthly_revenue)

        print("\nTotal Revenue by Product:")
        print(product_revenue)

        print("\nTotal Revenue by Customer:")
        print(customer_revenue)

        print("\nTop 10 Customers by Revenue:")
        print(top_customers)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
