from pathlib import Path
import sys

vendor_dir = Path(__file__).parent / "vendor"
sys.path.insert(0, str(vendor_dir))
