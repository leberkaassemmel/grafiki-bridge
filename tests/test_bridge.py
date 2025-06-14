import pandas as pd
from grafiki.core import bridge_df

def test_bridge_df_generates_valid_url():
    # Sample DataFrame
    df = pd.DataFrame({
        "x": [1, 2, 3],
        "y": ["a", "b", "c"]
    })

    url = bridge_df(df, name="Test DF", tags=["unit", "test"])

    # Check that it returns a valid-looking Grafiki URL
    assert url.startswith("https://www.grafiki.app/d#")

    # Extract the data part and ensure it's valid base64
    base64_data = url.split("/d#")[-1]
    assert base64_data.endswith('6tWSkksSSxOLVGyUqgGs4GM6GqlCiBlqKOgVAmklRKVanUUIGJGMLEkhJgxTCxZqTYWyM5LzE0FcUNSi0sUXNyUgEIlienFIIOVSvMyS8ACQDml2NpaAPBAIdGAAAAA')
