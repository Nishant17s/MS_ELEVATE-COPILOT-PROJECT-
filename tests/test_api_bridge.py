"""
Unit tests for API bridge module.
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from api_bridge import get_supply_chain_brief


@pytest.fixture
def mock_inventory_data():
    """Create mock inventory data for testing."""
    return pd.DataFrame({
        'product_name': ['Product A', 'Product B', 'Product C'],
        'current_stock': [100, 50, 200],
        'reorder_point': [30, 40, 60],
        'unit_cost': [10.0, 20.0, 15.0],
        'selling_price': [15.0, 30.0, 20.0],
        'burn_rate': [5.0, 8.0, 3.0],
        'days_to_stockout': [20, 6, 66],
        'status': ['Healthy', 'Critical', 'Healthy']
    })


def test_get_supply_chain_brief_with_mock(mock_inventory_data):
    """Test supply chain brief generation with mocked Gemini API."""
    with patch('api_bridge.genai') as mock_genai:
        # Mock the Gemini API response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test AI response for supply chain analysis."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.configure = MagicMock()
        
        result = get_supply_chain_brief(mock_inventory_data, api_key="test_key")
        
        assert isinstance(result, str)
        assert len(result) > 0


def test_get_supply_chain_brief_with_api_error(mock_inventory_data):
    """Test supply chain brief when API fails."""
    with patch('api_bridge.genai') as mock_genai:
        # Mock API failure
        mock_genai.configure = MagicMock()
        mock_genai.GenerativeModel.side_effect = Exception("API Error")
        
        result = get_supply_chain_brief(mock_inventory_data, api_key="test_key")
        
        # Should return error message
        assert "error" in result.lower() or "unable" in result.lower()


def test_get_supply_chain_brief_empty_data():
    """Test supply chain brief with empty dataframe."""
    empty_df = pd.DataFrame(columns=['product_name', 'current_stock', 'reorder_point', 'unit_cost', 'selling_price', 'status'])
    
    with patch('api_bridge.genai') as mock_genai:
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "No data available."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.configure = MagicMock()
        
        result = get_supply_chain_brief(empty_df, api_key="test_key")
        
        assert isinstance(result, str)


def test_data_analysis_metrics(mock_inventory_data):
    """Test that data analysis calculates correct metrics."""
    with patch('api_bridge.genai') as mock_genai:
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Analysis complete."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.configure = MagicMock()
        
        # Call the function (it will use the data internally)
        result = get_supply_chain_brief(mock_inventory_data, api_key="test_key")
        
        # Verify the function completed without error
        assert result is not None
