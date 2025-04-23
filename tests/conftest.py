import sys
import os

# Ensure the project root is on PYTHONPATH so imports like 'service.core' work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
