import unittest
import pandas as pd
from io import StringIO
from orders_analysis import load_data, preprocess_data, calculate_monthly_revenue, calculate_product_revenue, calculate_customer_revenue, get_top_customers

class TestOrdersAnalysis(unittest.TestCase):

    def setUp(self):
        '''Sets up the test data for testing the functions from orders_analysis.py file'''
        data = {
            'order_id': [1, 2, 3, 4],
            'customer_id': [101, 102, 101, 103],
            'order_date': ['2023-01-01', '2023-01-02', '2023-02-01', '2023-02-01'],
            'product_id': [1001, 1002, 1001, 1003],
            'product_name': ['Widget A', 'Widget B', 'Widget A', 'Widget C'],
            'product_price': [10.0, 20.0, 10.0, 30.0],
            'quantity': [2, 1, 1, 3]
        }
        self.df = pd.DataFrame(data)
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.preprocessed_df = preprocess_data(self.df)

    def test_load_data(self):
        with self.assertRaises(FileNotFoundError):
            load_data('non_existent_file.csv')
        
        with self.assertRaises(ValueError):
            load_data(StringIO(''))

        self.assertIsInstance(load_data(StringIO(self.df.to_csv(index=False))), pd.DataFrame)
        
        '''To test the wrong file path check'''
        # self.assertIsInstance(load_data('wrong_path.csv'), pd.DataFrame)
        
        '''To test the empty file check'''
        # empty_file = StringIO('')
        # self.assertIsInstance(load_data(empty_file), pd.DataFrame)


    def test_preprocess_data(self):
        with self.assertRaises(ValueError):
            preprocess_data(pd.DataFrame())

        df_invalid_date = self.df.copy()
        df_invalid_date['order_date'] = 'invalid_date'
        with self.assertRaises(ValueError):
            preprocess_data(df_invalid_date)

        preprocessed_df = preprocess_data(self.df)
        self.assertIn('revenue', preprocessed_df.columns)
        self.assertIn('month', preprocessed_df.columns)
        self.assertFalse(preprocessed_df['order_date'].isna().any())
        
        # Check for a non-existent column
        # self.assertIn('non_existent_column', preprocessed_df.columns)

    def test_calculate_monthly_revenue(self):
        monthly_revenue = calculate_monthly_revenue(self.preprocessed_df)
        self.assertEqual(len(monthly_revenue), 2)
        self.assertIn('Total Revenue', monthly_revenue.columns)

        '''Checks whether the precalculated values with the actual returned values from the 
        calculate_monthly_revenue function are equal or not'''
        expected_revenue = pd.DataFrame({
            'Month': [pd.Period('2023-01', freq='M'), pd.Period('2023-02', freq='M')],
            'Total Revenue': [40.0, 100.0]
        })
        pd.testing.assert_frame_equal(monthly_revenue, expected_revenue)
    
    def test_calculate_product_revenue(self):
        product_revenue = calculate_product_revenue(self.preprocessed_df)
        self.assertEqual(len(product_revenue), 3)
        self.assertIn('Total Revenue', product_revenue.columns)

        '''Checks whether the precalculated values with the actual returned values from the 
        calculate_product_revenue function are equal or not'''
        expected_revenue = pd.DataFrame({
            'Product Name': ['Widget A', 'Widget B', 'Widget C'],
            'Total Revenue': [30.0, 20.0, 90.0]
        })
        pd.testing.assert_frame_equal(product_revenue.sort_values(by='Product Name').reset_index(drop=True), expected_revenue)
    
    def test_calculate_customer_revenue(self):
        customer_revenue = calculate_customer_revenue(self.preprocessed_df)
        self.assertEqual(len(customer_revenue), 3)
        self.assertIn('Total Revenue', customer_revenue.columns)

        '''Checks whether the precalculated values with the actual returned values from the 
        calculate_customer_revenue function are equal or not'''
        expected_revenue = pd.DataFrame({
            'Customer ID': [101, 102, 103],
            'Total Revenue': [30.0, 20.0, 90.0]
        })
        pd.testing.assert_frame_equal(customer_revenue.sort_values(by='Customer ID').reset_index(drop=True), expected_revenue)
    
    def test_get_top_customers(self):
        customer_revenue = calculate_customer_revenue(self.preprocessed_df)
        top_customers = get_top_customers(customer_revenue)
        self.assertEqual(len(top_customers), 3)
        self.assertIn('Customer ID', top_customers.columns)

        '''Checks whether the precalculated values with the actual returned values from the 
        get_top_customers function are equal or not'''
        expected_top_customers = pd.DataFrame({
            'Customer ID': [103, 101, 102],
            'Total Revenue': [90.0, 30.0, 20.0]
        })
        pd.testing.assert_frame_equal(top_customers.reset_index(drop=True), expected_top_customers)
    
if __name__ == '__main__':
    unittest.main()
