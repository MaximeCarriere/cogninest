# Cogninest — Installation Guide

## Quick Install (pip-based, ~5 minutes)

NEST 3.8+ is now pip-installable, which eliminates the need to build NEST from source.
The felix C++ module still needs a one-time compile, but that takes under a minute.

### Prerequisites

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install -y build-essential cmake git libboost-dev
```

**macOS:**
```bash
brew install cmake boost libomp
```

### 1. Clone and set up the environment

```bash
git clone https://github.com/MaximeCarriere/cogninest.git
cd cogninest
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install nest-simulator
pip install -r requirements.txt
```

### 2. Patch nest-config (first-time only)

The pip-installed `nest-config` contains hardcoded build paths. Make the wrapper
executable so cmake can find NEST:

```bash
chmod +x nest-config-pip
```

### 3. Build and install the felix module

```bash
rm -f CMakeCache.txt          # clear any stale cache from root
mkdir -p build_pip && cd build_pip
cmake -Dwith-nest=../nest-config-pip ..
make -j$(sysctl -n hw.logicalcpu 2>/dev/null || nproc)
make install
cd ..
```

This installs `felixmodule.so` to `lib/nest/` inside the repo.

### 4. Run a simulation

```bash
export DYLD_LIBRARY_PATH="$(pwd)/lib/nest:$DYLD_LIBRARY_PATH"   # macOS
# export LD_LIBRARY_PATH="$(pwd)/lib/nest:$LD_LIBRARY_PATH"     # Linux
python3 training_testing/main_training.py
```

Or in Python:
```python
import nest
nest.Install('felixmodule')
# felix_exc, felix_inh, felix_spike_recorder are now available
```

---

## Docker (alternative)

```bash
docker pull maxc93/cogninest
docker run --rm -it maxc93/cogninest
```

---

## Legacy Manual Install (NEST built from source)

The original build-from-source instructions are preserved below for reference.
They target NEST 3.6-develop and are no longer the recommended path.

<details>
<summary>Click to expand legacy instructions</summary>

### Prerequisites
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential cmake git libtinfo-dev wget
```

### Install Miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"
```

### Build NEST from source
```bash
git clone --branch 3.6-develop https://github.com/nest/nest-simulator.git
conda env create --name nest --file=nest-simulator/environment.yml
conda activate nest
mkdir -p ~/nest_build && cd ~/nest_build
CMAKE_PREFIX_PATH=${CONDA_PREFIX} cmake -DCMAKE_INSTALL_PREFIX:PATH=`pwd`/install ~/nest-simulator
make -j$(nproc) install
source install/bin/nest_vars.sh
```

### Build the felix module
```bash
mkdir -p ~/felix_build && cd ~/felix_build
CMAKE_PREFIX_PATH=${CONDA_PREFIX} cmake -Dwith-nest=../nest_build/install/bin/nest-config ../cogninest
make -j$(nproc) && make install
```

</details>

