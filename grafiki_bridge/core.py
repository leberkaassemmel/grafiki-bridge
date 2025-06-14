import base64
import gzip
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

import pandas as pd
from IPython.display import display, HTML


class GrafikiBridge:
    """
    A Jupyter notebook plugin for compressing pandas DataFrames and generating
    web app links for visualization and saving.
    """

    # Browser URL length limits
    BROWSER_LIMITS = {
        'chrome': 2048000,  # Chrome: ~2MB
        'firefox': 65536,  # Firefox: 64KB
        'safari': 80000,  # Safari: ~80KB
        'edge': 2048000,  # Edge: ~2MB (similar to Chrome)
        'ie': 2083,  # Internet Explorer: ~2KB (legacy)
        'default': 65536  # Conservative default (Firefox limit)
    }

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

    def get_url_length_info(self, url: str) -> Dict[str, Any]:
        """
        Get URL length information and browser compatibility.

        Args:
            url: The complete URL to analyze

        Returns:
            Dictionary with URL length analysis
        """
        url_length = len(url)
        browser_info = {}

        for browser, limit in self.BROWSER_LIMITS.items():
            if browser == 'default':
                continue
            percentage = (url_length / limit) * 100
            browser_info[browser] = {
                'limit': limit,
                'percentage': percentage,
                'exceeds': url_length > limit
            }

        # Find the most restrictive browser that still works
        compatible_browsers = [b for b, info in browser_info.items() if not info['exceeds']]

        return {
            'url_length': url_length,
            'browser_info': browser_info,
            'compatible_browsers': compatible_browsers,
            'has_issues': len(compatible_browsers) == 0 or any(info['exceeds'] for info in browser_info.values())
        }

    @staticmethod
    def detect_browser() -> str:
        """
        Detect the user's browser using JavaScript in Jupyter.

        Returns:
            String identifying the detected browser
        """
        js_code = """
        <script>
        function detectBrowser() {
            const userAgent = navigator.userAgent.toLowerCase();
            let browser = 'unknown';

            if (userAgent.includes('chrome') && !userAgent.includes('edg')) {
                browser = 'chrome';
            } else if (userAgent.includes('firefox')) {
                browser = 'firefox';
            } else if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
                browser = 'safari';
            } else if (userAgent.includes('edg')) {
                browser = 'edge';
            } else if (userAgent.includes('trident') || userAgent.includes('msie')) {
                browser = 'ie';
            }

            // Store in a global variable that Python can access
            window.detectedBrowser = browser;

            // Also update the display immediately
            const browserSpans = document.querySelectorAll('.current-browser');
            browserSpans.forEach(span => {
                span.textContent = browser.charAt(0).toUpperCase() + browser.slice(1);
                span.style.fontWeight = 'bold';
                span.style.color = '#007bff';
            });

            // Update browser-specific warnings
            const browserWarnings = document.querySelectorAll('.browser-warning');
            browserWarnings.forEach(warning => {
                const browserInfo = JSON.parse(warning.dataset.browserInfo);
                const currentBrowserInfo = browserInfo[browser];

                if (currentBrowserInfo && currentBrowserInfo.exceeds) {
                    warning.style.display = 'block';
                    warning.innerHTML = `
                        <strong>⚠️ Your Browser (${browser.charAt(0).toUpperCase() + browser.slice(1)}) Alert!</strong><br>
                        This URL is ${currentBrowserInfo.percentage.toFixed(1)}% of your browser's limit and may not work properly.
                    `;
                } else if (currentBrowserInfo) {
                    warning.style.display = 'block';
                    warning.style.backgroundColor = '#d4edda';
                    warning.style.color = '#155724';
                    warning.innerHTML = `
                        <strong>✅ Your Browser (${browser.charAt(0).toUpperCase() + browser.slice(1)})</strong><br>
                        URL uses ${currentBrowserInfo.percentage.toFixed(1)}% of your browser's limit - You're good to go!
                    `;
                }
            });
        }

        // Run detection immediately
        detectBrowser();
        </script>
        """

        display(HTML(js_code))
        return "detected"  # Actual detection happens in JavaScript

    def display_link(self,
                     df: pd.DataFrame,
                     name: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     link_text: str = "Open in Web App") -> None:
        """
        Display a clickable link in the Jupyter notebook with compression stats and URL validation.

        Args:
            df: The pandas DataFrame
            name: Optional name for the dataset
            tags: Optional list of tags
            link_text: Text to display for the link
        """
        url = self.create_webapp_link(df, name, tags)
        dataset_name = name or f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Get compression statistics
        compression_stats = self.get_compression_stats(df)

        # Get URL length information
        url_info = self.get_url_length_info(url)

        # Create browser compatibility info
        button_disabled = ""
        button_style = """
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 10px;
            cursor: pointer;
        """

        # Create detailed browser breakdown for advanced users
        browser_details = "<br>".join([
            f"<strong>{browser.title()}:</strong> {info['percentage']:.1f}% of limit ({info['limit']:,} chars) {'❌' if info['exceeds'] else '✅'}"
            for browser, info in url_info['browser_info'].items()
        ])

        # Add current browser detection
        current_browser_status = f'''
        <div class="browser-warning" style="display: none; background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 4px; margin: 10px 0;" 
             data-browser-info='{json.dumps(url_info["browser_info"])}'>
            Detecting your browser...
        </div>
        '''

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
                <strong>Compression Ratio:</strong> {compression_stats['compression_ratio']:.1f}x 
                ({compression_stats['space_saved_percent']:.1f}% saved)<br>
                <strong>Your Browser:</strong> <span class="current-browser">Detecting...</span><br>
                <strong>Columns:</strong> {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}
            </p>

            {current_browser_status}

            <details style="margin: 10px 0; font-size: 0.9em;">
                <summary style="cursor: pointer; color: #666;">Browser Compatibility Details</summary>
                <div style="margin-top: 10px; padding: 10px; background-color: #fff; border-radius: 4px;">
                    {browser_details}
                </div>
            </details>

            <a href="{url if not button_disabled else '#'}" 
               target="_blank" 
               style="{button_style}"
               {button_disabled}
               onmouseover="if(!this.onclick || this.onclick()) this.style.backgroundColor='#0056b3'"
               onmouseout="if(!this.onclick || this.onclick()) this.style.backgroundColor='#007bff'">
                {link_text} {'🚀' if not button_disabled else '🚫'}
            </a>
        </div>
        '''

        display(HTML(html_content))

        # Run browser detection after displaying the HTML
        self.detect_browser()

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
