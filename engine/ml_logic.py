"""
ml_logic.py
===========
Machine Learning & Predictive Analytics Module

This module contains ML models for inventory analysis and forecasting.
It calculates:
- Burn Rate: Daily consumption rate of inventory items
- Stockout Prediction: Estimated days until inventory depletion
- Status Classification: Health status (Critical/Warning/Healthy)

Models:
- Linear Regression: Used for trend analysis on 30-day sales history
- Fallback: Simple averaging for insufficient data points

Author: InsightPro Team
Version: 2.1
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import numpy as np

def calculate_burn_rate_and_stockout(inventory_item, sales_history):
    """
    Calculates the Burn Rate (items/day) and predicted Stockout Days.
    
    Returns:
        dict: {'burn_rate': float, 'days_to_stockout': float (or inf), 'status': str}
    """
    product_sales = sales_history[sales_history['product_id'] == inventory_item['id']].copy()
    
    if product_sales.empty:
         return {'burn_rate': 0.0, 'days_to_stockout': float('inf'), 'status': 'No Data'}

    # Filter for last 30 days for trend analysis
    last_30_days = datetime.now() - timedelta(days=30)
    product_sales['sale_date'] = pd.to_datetime(product_sales['sale_date'])
    recent_sales = product_sales[product_sales['sale_date'] >= last_30_days]
    
    if recent_sales.empty:
        return {'burn_rate': 0.0, 'days_to_stockout': float('inf'), 'status': 'Stable'}

    # Group by date
    daily_sales = recent_sales.groupby('sale_date')['quantity_sold'].sum().reset_index()
    daily_sales['days_since'] = (daily_sales['sale_date'] - daily_sales['sale_date'].min()).dt.days
    
    # Linear Regression to find trend
    if len(daily_sales) > 5: # Need enough data points
        X = daily_sales[['days_since']]
        y = daily_sales['quantity_sold']
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict usage for "tomorrow" (next step in trend)
        latest = daily_sales['days_since'].max()
        burn_rate = model.predict([[latest + 1]])[0]
        # Clean up negative predictions
        burn_rate = max(0.1, burn_rate) 
    else:
        # Fallback to simple average
        burn_rate = daily_sales['quantity_sold'].mean()

    current_stock = inventory_item['current_stock']
    
    if burn_rate <= 0:
        days_to_stockout = float('inf')
    else:
        days_to_stockout = current_stock / burn_rate
        
    return {
        'burn_rate': round(burn_rate, 2),
        'days_to_stockout': round(days_to_stockout, 1),
        'status': 'Critical' if days_to_stockout < 7 else 'Healthy'
    }
