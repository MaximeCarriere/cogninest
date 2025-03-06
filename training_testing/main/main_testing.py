# main.py
import time
import nest
import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Only install if it's not already loaded
installed_modules = nest.GetKernelStatus().get("loaded_modules", [])
if "felixmodule" not in installed_modules:
    nest.Install('felixmodule')
else:
    print("Felix Module is already installed, skipping installation.")
    
from network.test_runner import run_all_tests
from utils.visualization_testing import *

print(f"Python interpreter: {sys.executable}")

if __name__ == "__main__":
    print("🚀 Starting FelixNet Testing...")
    run_all_tests()
    print("✅ All tests completed successfully!")

    # Run Graph Plotting
    print("📊 Generating Graphs...")
    plot_graphs()
    print("✅ Graphs Generated Successfully!")
