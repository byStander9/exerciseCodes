Installation guide for Triton Inference Server & TensorRT_LLM (Backend Engine)
==========================================

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
