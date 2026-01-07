from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Market Settings
# Mix of Tech (Naspers), Banking (Standard Bank), Mining (Anglo), and Benchmark (Top 40 ETF)
TICKERS = ["NPN.JO", "SBK.JO", "AGL.JO", "STX40.JO"] 

START_DATE = "2018-01-01"
END_DATE = "2024-12-31"