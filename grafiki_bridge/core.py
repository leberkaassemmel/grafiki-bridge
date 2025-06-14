import base64
import gzip
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

import pandas as pd
from IPython.display import HTML, display


class GrafikiBridge:
    """
    A Jupyter notebook plugin for compressing pandas DataFrames and generating
    web app links for visualization and saving.
    """

    def __init__(self, base_url: str = "https://www.grafiki.app"):
        """
        Initialize the compressor with your web app's base URL.

        Args:
            base_url: The base URL of your web application
        """
        self.base_url = base_url.rstrip('/')

    @staticmethod
    def compress_dataframe(df: pd.DataFrame,
                           name: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> str:
        """
        Compress a pandas DataFrame to base64 encoded gzip format.

        Args:
            df: The pandas DataFrame to compress
            name: Optional name for the dataset
            tags: Optional list of tags

        Returns:
            Base64 encoded compressed data string
        """
        # Convert DataFrame to the required format
        dataset = {
            "data": df.to_dict('records'),  # Convert to list of dictionaries
            "name": name or f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "tags": tags or [],
        }

        # Convert to JSON string
        json_str = json.dumps({"dataset": dataset}, default=str)

        # Compress using gzip
        compressed_data = gzip.compress(json_str.encode('utf-8'))

        # Encode to base64
        base64_data = base64.b64encode(compressed_data).decode('utf-8')

        return base64_data

    def create_webapp_link(self,
                           df: pd.DataFrame,
                           name: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> str:
        """
        Create a web app link with compressed DataFrame data.

        Args:
            df: The pandas DataFrame
            name: Optional name for the dataset
            tags: Optional list of tags

        Returns:
            Complete URL with compressed data as query parameter
        """
        compressed_data = self.compress_dataframe(df, name, tags)

        # Generate the complete URL
        full_url = f"{self.base_url}/d#{compressed_data}"

        return full_url

    def display_link(self,
                     df: pd.DataFrame,
                     name: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     link_text: str = "Open in Web App") -> None:
        """
        Display a clickable link in the Jupyter notebook.

        Args:
            df: The pandas DataFrame
            name: Optional name for the dataset
            tags: Optional list of tags
            link_text: Text to display for the link
        """
        url = self.create_webapp_link(df, name, tags)
        dataset_name = name or f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create HTML with styling
        html_content = f'''
        <div style="
            border: 1px solid #ddd; 
            border-radius: 8px; 
            padding: 15px; 
            margin: 10px 0; 
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
        ">
            <h3 style="margin-top: 0; color: #333;">📊 {dataset_name}</h3>
            <p style="margin: 5px 0; color: #666;">
                <strong>Shape:</strong> {df.shape[0]} rows × {df.shape[1]} columns<br>
                <strong>Memory:</strong> {df.memory_usage(deep=True).sum() / 1024:.2f} KB<br>
                <strong>Columns:</strong> {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}
            </p>
            <a href="{url}" 
               target="_blank" 
               style="
                   display: inline-block;
                   background-color: #007bff;
                   color: white;
                   padding: 8px 16px;
                   text-decoration: none;
                   border-radius: 4px;
                   font-weight: bold;
                   margin-top: 10px;
               "
               onmouseover="this.style.backgroundColor='#0056b3'"
               onmouseout="this.style.backgroundColor='#007bff'">
                {link_text} 🚀
            </a>
        </div>
        '''

        display(HTML(html_content))

    def get_compression_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get compression statistics for a DataFrame.

        Args:
            df: The pandas DataFrame

        Returns:
            Dictionary with compression statistics
        """
        # Original size
        original_json = json.dumps(df.to_dict('records'), default=str)
        original_size = len(original_json.encode('utf-8'))

        # Compressed size
        compressed_data = self.compress_dataframe(df)
        compressed_size = len(compressed_data.encode('utf-8'))

        return {
            'original_size_bytes': original_size,
            'compressed_size_bytes': compressed_size,
            'original_size_kb': original_size / 1024,
            'compressed_size_kb': compressed_size / 1024,
            'compression_ratio': original_size / compressed_size if compressed_size > 0 else 0,
            'space_saved_percent': ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        }


# Convenience functions for easy use
def bridge_df(df: pd.DataFrame,
              name: Optional[str] = None,
              tags: Optional[List[str]] = None,
              base_url: str = "https://www.grafiki.app") -> str:
    """
    Convenience function to compress a DataFrame and return the webapp link.

    Args:
        df: The pandas DataFrame to compress
        name: Optional name for the dataset
        tags: Optional list of tags
        base_url: Base URL of your web application

    Returns:
        Complete URL with compressed data
    """
    bridge = GrafikiBridge(base_url)
    return bridge.create_webapp_link(df, name, tags)


def show_bridge_link(df: pd.DataFrame,
                     name: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     base_url: str = "https://www.grafiki.app",
                     link_text: str = "Open in Web App") -> None:
    """
    Convenience function to display a clickable link for a DataFrame.

    Args:
        df: The pandas DataFrame
        name: Optional name for the dataset
        tags: Optional list of tags
        base_url: Base URL of your web application
        link_text: Text to display for the link
    """
    bridge = GrafikiBridge(base_url)
    bridge.display_link(df, name, tags, link_text=link_text)
