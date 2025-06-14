# Grafiki Bridge

A Python package that creates shareable, interactive data visualizations from pandas DataFrames through compressed URL links.

## Overview

This package allows you to convert pandas DataFrames into compressed, browser-compatible links that open in the Grafiki web application for interactive data exploration and visualization.

## Features

- 📊 Convert pandas DataFrames to interactive visualizations
- 🔗 Generate shareable web links with data compression
- 🌐 Cross-browser compatibility checking
- 📈 Memory-efficient data encoding
- ⚡ Quick data exploration and sharing

## Installation

Install from PyPI:

```bash
pip install grafiki-bridge
```

Or install the latest development version:

```bash
pip install git+https://github.com/yourusername/grafiki-bridge.git
```

## Usage

### Basic Example

```python
import pandas as pd
import grafiki

# Create sample data
sample_data = {
    'year': [1949, 1949, 1949, 1950, 1950, 1950],
    'month': ['January', 'February', 'March', 'January', 'February', 'March'],
    'passengers': [112, 118, 132, 115, 126, 141]
}

df = pd.DataFrame(sample_data)

# Generate shareable visualization link
grafiki.show_bridge_link(df, 'My First Dataset')
```

### What You Get

When you run `show_bridge_link()`, you'll see:

- **Dataset Overview**: Rows, columns, and memory usage
- **Compression Stats**: Data compression ratio and space saved
- **Browser Compatibility**: Automatic detection and compatibility checking
- **Shareable Link**: Direct URL to open your data in the Grafiki web app

## Key Benefits

- **Compressed Data**: Automatically compresses your data (up to 1.5x compression in this example)
- **Browser Optimized**: Checks URL length limits for different browsers
- **Instant Sharing**: No need to upload files - data is encoded in the URL
- **Privacy Friendly**: Data stays in your control through URL encoding

## Browser Compatibility

The tool automatically detects your browser and shows compatibility:

- **Chrome/Edge**: Up to ~2MB of data
- **Firefox**: Up to ~64KB of data  
- **Safari**: Up to ~80KB of data

## Requirements

- Python 3.6+
- pandas
- Dependencies are automatically installed with the package

## Getting Started

1. Install the package: `pip install grafiki-bridge`
2. Import and use in your Python environment:

```python
import pandas as pd
import grafiki

# Your DataFrame
df = pd.read_csv('your_data.csv')

# Generate shareable link
grafiki.show_bridge_link(df, 'Your Dataset Name')
```

## Use Cases

Perfect for:
- Quick data sharing with colleagues
- Creating portable data visualizations
- Prototyping data analysis workflows
- Educational demonstrations
- Lightweight data distribution

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/yourusername/grafiki-bridge.git
cd grafiki-bridge
pip install -e ".[dev]"
```

## License

This project is open source and available under the MIT License.