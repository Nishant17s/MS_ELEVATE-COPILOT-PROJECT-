"""
Unit tests for ML logic module.
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from engine.ml_logic import calculate_burn_rate_and_stockout


def test_calculate_burn_rate_with_data():
    """Test burn rate calculation with sufficient data."""
    # Create mock inventory item
    inventory_item = pd.Series({
        'id': 1,
        'product_name': 'Test Product',
        'current_stock': 100,
        'reorder_point': 30
    })
    
    # Create mock sales data
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    sales_df = pd.DataFrame({
        'product_id': [1] * 30,
        'sale_date': dates,
        'quantity_sold': [5] * 30
    })
    
    result = calculate_burn_rate_and_stockout(inventory_item, sales_df)
    
    assert 'burn_rate' in result
    assert 'days_to_stockout' in result
    assert 'status' in result
    assert result['burn_rate'] >= 0
    assert isinstance(result['days_to_stockout'], (int, float))
    assert result['status'] in ['Critical', 'Warning', 'Healthy']


def test_calculate_burn_rate_with_empty_data():
    """Test burn rate calculation with empty dataframe."""
    inventory_item = pd.Series({
        'id': 1,
        'product_name': 'Test Product',
        'current_stock': 100,
        'reorder_point': 30
    })
    
    sales_df = pd.DataFrame(columns=['product_id', 'sale_date', 'quantity_sold'])
    
    result = calculate_burn_rate_and_stockout(inventory_item, sales_df)
    
    assert result['burn_rate'] == 0.0
    assert result['days_to_stockout'] == float('inf')
    assert result['status'] == 'No Data'


def test_calculate_burn_rate_critical_status():
    """Test that critical status is assigned correctly."""
    inventory_item = pd.Series({
        'id': 1,
        'product_name': 'Test Product',
        'current_stock': 50,
        'reorder_point': 30
    })
    
    # Create data that will result in < 7 days to stockout
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    sales_df = pd.DataFrame({
        'product_id': [1] * 30,
        'sale_date': dates,
        'quantity_sold': [20] * 30  # High burn rate
    })
    
    result = calculate_burn_rate_and_stockout(inventory_item, sales_df)
    
    # With 20 units sold per day and 50 in stock, should be critical (< 7 days)
    assert result['status'] == 'Critical'
    assert result['days_to_stockout'] < 7


def test_calculate_burn_rate_healthy_status():
    """Test that healthy status is assigned correctly."""
    inventory_item = pd.Series({
        'id': 1,
        'product_name': 'Test Product',
        'current_stock': 1000,
        'reorder_point': 30
    })
    
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    sales_df = pd.DataFrame({
        'product_id': [1] * 30,
        'sale_date': dates,
        'quantity_sold': [1] * 30  # Low burn rate
    })
    
    result = calculate_burn_rate_and_stockout(inventory_item, sales_df)
    
    # With low burn and high stock, should be healthy
    assert result['status'] in ['Warning', 'Healthy']


def test_calculate_burn_rate_zero_stock():
    """Test burn rate calculation with zero stock."""
    inventory_item = pd.Series({
        'id': 1,
        'product_name': 'Test Product',
        'current_stock': 0,
        'reorder_point': 30
    })
    
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    sales_df = pd.DataFrame({
        'product_id': [1] * 30,
        'sale_date': dates,
        'quantity_sold': [5] * 30
    })
    
    result = calculate_burn_rate_and_stockout(inventory_item, sales_df)
    
    assert result['days_to_stockout'] == 0
    assert result['status'] == 'Critical'
