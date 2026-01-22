"""
Unit tests for database manager module.
"""
import pytest
import pandas as pd
from engine.db_manager import init_db, get_inventory_df, get_sales_df


def test_init_db():
    """Test database initialization."""
    init_db()
    # If no exception is raised, test passes
    assert True


def test_get_inventory_df():
    """Test retrieving inventory dataframe."""
    init_db()
    df = get_inventory_df()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'id' in df.columns
    assert 'product_name' in df.columns
    assert 'current_stock' in df.columns
    assert 'reorder_point' in df.columns


def test_get_sales_df():
    """Test retrieving sales dataframe."""
    init_db()
    df = get_sales_df()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'product_id' in df.columns
    assert 'sale_date' in df.columns
    assert 'quantity_sold' in df.columns


def test_inventory_data_types():
    """Test that inventory data has correct types."""
    init_db()
    df = get_inventory_df()
    
    assert df['current_stock'].dtype in ['int64', 'int32']
    assert df['reorder_point'].dtype in ['int64', 'int32']
    assert df['unit_cost'].dtype in ['float64', 'float32']
    assert df['selling_price'].dtype in ['float64', 'float32']


def test_sales_data_types():
    """Test that sales data has correct types."""
    init_db()
    df = get_sales_df()
    
    assert df['quantity_sold'].dtype in ['int64', 'int32']
    assert 'sale_date' in df.columns
