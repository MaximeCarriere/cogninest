# Docker Installation for NEST Simulator and Felix Module

## 🐳 Run with Docker (Recommended)
To quickly set up and run the NEST Simulator with the Felix Module, use the provided Docker image.

### **1️⃣ Pull the Docker Image**
```bash
docker pull maxc93/cogninest
```

### **2️⃣ Run the Container**
```bash
docker run --rm -it maxc93/cogninest
```

If the application runs a web service, use:
```bash
docker run -d -p 8080:80 maxc93/cogninest
```
Then access it at `http://localhost:8080`.

### **3️⃣ Enter the Container (Optional Debugging Mode)**
To explore the environment:
```bash
docker run --rm -it maxc93/cogninest /bin/bash
```

---

# Manual Installation Guide for NEST Simulator and Felix Module

## 📌 Prerequisites
Ensure your system is up to date and has the required dependencies installed:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential cmake git libtinfo-dev wget
```

## 📥 Install Miniconda
Download and install Miniconda for managing Python environments:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
```

Add Miniconda to the system PATH:
```bash
export PATH="$HOME/miniconda3/bin:$PATH"
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc  # Reload shell configuration
```

## 🛠 Install and Build NEST Simulator
Clone the NEST repository and switch to the desired branch:
```bash
git clone --branch 3.6-develop https://github.com/nest/nest-simulator.git
```

Create and activate a Conda environment for NEST:
```bash
conda env create --name nest --file=nest-simulator/environment.yml  
conda activate nest
```

### 🔧 Build and Install NEST
Create a build directory:
```bash
mkdir -p ~/nest_build && cd ~/nest_build
```

Ensure a clean build by removing old files:
```bash
rm -rf CMakeCache.txt CMakeFiles
```

Configure the NEST build:
```bash
CMAKE_PREFIX_PATH=${CONDA_PREFIX} cmake -DCMAKE_INSTALL_PREFIX:PATH=`pwd`/install ~/nest-simulator
```

Compile and install NEST:
```bash
make -j$(nproc) install
make installcheck
```

Set NEST environment variables:
```bash
source install/bin/nest_vars.sh
echo 'source ~/nest_build/install/bin/nest_vars.sh' >> ~/.bashrc
source ~/.bashrc  # Apply changes
```

### 🔧 Build and Install Felix
Create and enter the Felix build directory:
```bash
mkdir -p ~/felix_build && cd ~/felix_build
```

Remove any old build files:
```bash
rm -rf ~/felix_build/*
```

Configure the Felix module:
```bash
CMAKE_PREFIX_PATH=${CONDA_PREFIX} cmake -Dwith-nest=../nest_build/install/bin/nest-config ../nest_test
```

Compile and install Felix:
```bash
make -j$(nproc)
make install
```

## 🏗 Install Cogninest
Clone the Cogninest repo:
```bash
git clone https://github.com/MaximeCarriere/cogninest.git
```

Install additional dependencies:
```bash
cd cogninest
pip install -r requirements.txt
```

---

## ✅ **Final Checks**
1. **Verify NEST Installation:**
   ```bash
   nest --version
   ```
2. **Test Felix Module:**
   ```python
   import nest
   nest.Install('felixmodule')
   ```

---

## 🌟 **Running a Simulation**
To run a simulation, navigate to the correct directory and execute the Python script:
```bash
cd ~/cogninest/training_testing/main/
python main_training.py
```

🚀 **You're now ready to use NEST and Cogninest!**

