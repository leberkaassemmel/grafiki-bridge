import base64
import gzip
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

import pandas as pd
from IPython.display import display, HTML


class GrafikiBridge:
    """
    Jupyter notebook plugin for compressing pandas DataFrames
    and generating web app links for visualization.
    """

    # Browser URL length limits (bytes)
    BROWSER_LIMITS = {
        'chrome': 2048000,
        'firefox': 65536,
        'safari': 80000,
        'edge': 2048000,
        'default': 65536
    }

    def __init__(self, base_url: str = "https://www.grafiki.app"):
        """Initialize with web app base URL."""
        self.base_url = base_url.rstrip('/')

    @staticmethod
    def compress_dataframe(df: pd.DataFrame, name: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> str:
        """Compress DataFrame to base64 encoded gzip format."""
        dataset = {
            "data": df.to_dict('records'),
            "name": name or f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "tags": tags or []
        }

        json_str = json.dumps({"dataset": dataset}, default=str)
        compressed_data = gzip.compress(json_str.encode('utf-8'))
        return base64.b64encode(compressed_data).decode('utf-8')

    def create_webapp_link(self, df: pd.DataFrame, name: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> str:
        """Create web app link with compressed DataFrame data."""
        compressed_data = self.compress_dataframe(df, name, tags)
        return f"{self.base_url}/d#{compressed_data}"

    def _get_compression_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate compression statistics."""
        original_json = json.dumps(df.to_dict('records'), default=str)
        original_size = len(original_json.encode('utf-8'))
        compressed_size = len(self.compress_dataframe(df).encode('utf-8'))

        return {
            'compression_ratio': original_size / compressed_size if compressed_size > 0 else 0,
            'space_saved_percent': ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        }

    def _check_url_compatibility(self, url: str) -> Dict[str, Any]:
        """Check URL compatibility across browsers."""
        url_length = len(url)

        # Check major browsers
        compatible_browsers = []
        for browser, limit in self.BROWSER_LIMITS.items():
            if browser != 'default' and url_length <= limit:
                compatible_browsers.append(browser)

        return {
            'url_length': url_length,
            'compatible_browsers': compatible_browsers,
            'has_compatibility_issues': len(compatible_browsers) < 3  # Less than 3 major browsers
        }

    def display_link(self, df: pd.DataFrame, name: Optional[str] = None,
                     tags: Optional[List[str]] = None, link_text: str = "Open Dataset") -> None:
        """Display dataset link with key statistics."""

        url = self.create_webapp_link(df, name, tags)
        dataset_name = name or f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Get statistics
        compression_stats = self._get_compression_stats(df)
        url_info = self._check_url_compatibility(url)

        # Determine status
        if not url_info['compatible_browsers']:
            status_class = "error"
            status_text = "URL too long for browser compatibility"
            button_disabled = True
        elif url_info['has_compatibility_issues']:
            status_class = "warning"
            status_text = f"Limited compatibility ({len(url_info['compatible_browsers'])} browsers)"
            button_disabled = False
        else:
            status_class = "success"
            status_text = "Compatible with all major browsers"
            button_disabled = False

        # JavaScript for browser detection and dynamic updates
        js_code = f"""
        <script>
        (function() {{
            const userAgent = navigator.userAgent.toLowerCase();
            let browser = 'unknown';

            if (userAgent.includes('chrome') && !userAgent.includes('edg')) browser = 'chrome';
            else if (userAgent.includes('firefox')) browser = 'firefox';
            else if (userAgent.includes('safari') && !userAgent.includes('chrome')) browser = 'safari';
            else if (userAgent.includes('edg')) browser = 'edge';

            const browserSpan = document.querySelector('.detected-browser');
            if (browserSpan) {{
                browserSpan.textContent = browser.charAt(0).toUpperCase() + browser.slice(1);

                // Update compatibility for user's browser
                const limits = {json.dumps(self.BROWSER_LIMITS)};
                const urlLength = {url_info['url_length']};
                const userLimit = limits[browser] || limits.default;
                const percentage = ((urlLength / userLimit) * 100).toFixed(1);

                const statusSpan = document.querySelector('.browser-status');
                if (statusSpan) {{
                    if (urlLength > userLimit) {{
                        statusSpan.innerHTML = `<span style="color: #dc3545;">⚠️ May not work (${{percentage}}% of limit)</span>`;
                    }} else {{
                        statusSpan.innerHTML = `<span style="color: #28a745;">✓ Compatible (${{percentage}}% of limit)</span>`;
                    }}
                }}
            }}
        }})();
        </script>
        """

        html_content = f'''
        <div style="
            border: 1px solid #e1e5e9;
            border-radius: 6px;
            padding: 20px;
            margin: 15px 0;
            background: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #24292e; font-size: 16px; font-weight: 600;">
                    📊 {dataset_name}
                </h3>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; font-size: 14px; color: #586069;">
                <div>
                    <div><strong>Rows:</strong> {df.shape[0]:,}</div>
                    <div><strong>Columns:</strong> {df.shape[1]}</div>
                    <div><strong>Memory:</strong> {df.memory_usage(deep=True).sum() / 1024:.1f} KB</div>
                </div>
                <div>
                    <div><strong>Compression:</strong> {compression_stats['compression_ratio']:.1f}x</div>
                    <div><strong>Space Saved:</strong> {compression_stats['space_saved_percent']:.1f}%</div>
                    <div><strong>Your Browser:</strong> <span class="detected-browser">Detecting...</span></div>
                </div>
            </div>

            <div style="
                padding: 12px;
                border-radius: 4px;
                margin-bottom: 16px;
                font-size: 13px;
                background-color: {'#f8f9fa' if status_class == 'success' else '#fff3cd' if status_class == 'warning' else '#f8d7da'};
                color: {'#155724' if status_class == 'success' else '#856404' if status_class == 'warning' else '#721c24'};
                border: 1px solid {'#d4edda' if status_class == 'success' else '#ffeaa7' if status_class == 'warning' else '#f5c6cb'};
            ">
                <div><strong>Status:</strong> {status_text}</div>
                <div><strong>URL Length:</strong> {url_info['url_length']:,} characters</div>
                <div class="browser-status">Checking browser compatibility...</div>
            </div>

            <a href="{url if not button_disabled else '#'}" 
               target="_blank"
               style="
                   display: inline-block;
                   background-color: {'#0366d6' if not button_disabled else '#6c757d'};
                   color: white;
                   padding: 8px 16px;
                   text-decoration: none;
                   border-radius: 4px;
                   font-size: 14px;
                   font-weight: 500;
                   transition: background-color 0.15s ease;
                   {'cursor: not-allowed;' if button_disabled else ''}
               "
               {'onclick="return false;"' if button_disabled else ''}
               onmouseover="if (!this.onclick) this.style.backgroundColor='#0256cc'"
               onmouseout="if (!this.onclick) this.style.backgroundColor='#0366d6'">
                {link_text} {'🔗' if not button_disabled else '🚫'}
            </a>
        </div>
        {js_code}
        '''

        display(HTML(html_content))


# Convenience functions for easy use
def bridge_df(df: pd.DataFrame,
              name: Optional[str] = None,
              tags: Optional[List[str]] = None,
              base_url: str = "https://www.grafiki.app") -> str:
    """
    Convenience function to compress a DataFrame and return the webapp link.
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
    """
    bridge = GrafikiBridge(base_url)
    bridge.display_link(df, name, tags, link_text=link_text)
