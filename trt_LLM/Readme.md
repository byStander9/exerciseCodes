Installation guide for Triton Inference Server & TensorRT_LLM
==========================================
[RTX 3090, Nvidia Driver Version: 560.35.03, Cuda v12.4]
======================================================

### Installing NVIDIA Container Toolkit

#### With apt: Ubuntu, Debian

1. Configure the production repository:
   ```console
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```

2. Update the packages list from the repository:
   ```console
   sudo apt-get update
   ```

3. Install the NVIDIA Container Toolkit packages:
   ```console
   sudo apt-get install -y nvidia-container-toolkit
   ```
#### Configuring Docker

1. Configure the container runtime by using the nvidia-ctk command:
    ```console
    sudo nvidia-ctk runtime configure --runtime=docker
    ```
    The nvidia-ctk command modifies the /etc/docker/daemon.json file on the host. The file is updated so that Docker can use the NVIDIA Container Runtime.
   
3. Restart the Docker daemon:
   ```console
   sudo systemctl restart docker
   ```

-----------------------------

### Build and test TRT-LLM engine
Reference: https://nvidia.github.io/TensorRT-LLM/installation/linux.html

## 1. Retrieve and launch the Docker container (optional)
   ```console
   # Pre-install the environment using the NVIDIA Container Toolkit to avoid manual environment configuration
   docker run --rm --ipc=host --runtime=nvidia --gpus '"device=0"' --entrypoint /bin/bash -it nvidia/cuda:12.4.1-devel-ubuntu22.04
   ```
## 2. Install TensorRT-LLM
   ```console
   # Install dependencies, TensorRT-LLM requires Python 3.10
   apt-get update && apt-get -y install python3.10 python3-pip openmpi-bin libopenmpi-dev git git-lfs

   # Install TensorRT-LLM (v0.11.0)
   pip3 install tensorrt_llm==0.11.0 --extra-index-url https://pypi.nvidia.com
   
   # Check installation
   python3 -c "import tensorrt_llm"
   ```
## 3. Clone the TRT-LLM repo with the Phi-3 conversion script
   ```console
   git clone -b v0.11.0 https://github.com/NVIDIA/TensorRT-LLM.git
   cd TensorRT-LLM/examples/phi/

   # only need to install requirements.txt if you want to test the summarize.py example
   # if so, modify requirements.txt such that tensorrt_llm==0.11.0
   # pip install -r requirements.txt
   ```
-------------
### Build and test TRT-LLM engine (My way)
Reference: https://nvidia.github.io/TensorRT-LLM/installation/linux.html

## 1. Retrieve and launch the Docker container (optional)
   # Recommended to mount a directory from the host PC in Docker to store and reuse downloaded LLM models.
   ```console
   # Pre-install the environment using the NVIDIA Container Toolkit to avoid manual environment configuration
   # docker run --rm --ipc=host --runtime=nvidia --gpus '"device=0"' --entrypoint /bin/bash -it nvidia/cuda:12.4.1-devel-ubuntu22.04
   docker run --ipc=host --runtime=nvidia --gpus '"device=0"' --entrypoint /bin/bash -it nvidia/cuda:12.4.1-devel-ubuntu22.04 
   ```
## 2. Install TensorRT-LLM
   ```console
   # Install dependencies, TensorRT-LLM requires Python 3.10
   apt-get update && apt-get -y install python3.10 python3-pip

   # Install TensorRT-LLM (v0.11.0)
   # pip3 install tensorrt_llm==0.11.0 --extra-index-url https://pypi.nvidia.com

   # https://nvidia.github.io/TensorRT-LLM/installation/linux.html
   # Install latest TensorRT-LLM (v0.11.0 error occur)
   sudo apt-get -y install libopenmpi-dev && pip3 install --upgrade pip setuptools && pip3 install tensorrt_llm --extra-index-url https://pypi.nvidia.com
   
   # Check installation
   python3 -c "import tensorrt_llm"
   ```
## 3. Clone the TRT-LLM repo with the Phi-3 conversion script
   ```console
   # git clone -b v0.11.0 https://github.com/NVIDIA/TensorRT-LLM.git
   # cd TensorRT-LLM/examples/phi/
   git clone https://github.com/NVIDIA/TensorRT-LLM.git
   cd TensorRT-LLM/examples/phi/

   # only need to install requirements.txt if you want to test the summarize.py example
   # if so, modify requirements.txt such that tensorrt_llm==0.11.0
   pip install -r requirements.txt
   ```

-------------------
## Build the TRT-LLM Engine
Reference: [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/phi)

## 4. Download Phi-3-mini-4k-instruct
   ```console
   git lfs install
   git clone https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
   ```
## 5. Convert weights from HF Transformers to TensorRT-LLM format
   ```console
   python3 ./convert_checkpoint.py \
                       --model_dir ./Phi-3-mini-4k-instruct \
                       --output_dir ./phi-checkpoint \
                       --dtype float16
   ```
## 6. Build TensorRT engine(s)
   ```console
   # Build a float16 engine using a single GPU and HF weights.
   # Enable several TensorRT-LLM plugins to increase runtime performance. It also helps with build time.
   # --tp_size and --pp_size are the model shard size
   trtllm-build \
       --checkpoint_dir ./phi-checkpoint \
       --output_dir ./phi-engine \
       --gemm_plugin float16 \
       --max_batch_size 8 \
       --max_input_len 1024 \
       --max_seq_len 2048 \
       # --tp_size 1 \
       # --pp_size 1
   ```
