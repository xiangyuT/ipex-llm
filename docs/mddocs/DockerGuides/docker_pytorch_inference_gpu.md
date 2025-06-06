# Python Inference using IPEX-LLM on Intel GPU

We can run PyTorch Inference Benchmark, Chat Service and PyTorch Examples on Intel GPUs within Docker (on Linux or WSL).

> [!NOTE]
> The current Windows + WSL + Docker solution only supports Arc series dGPU. For Windows users with MTL iGPU, it is recommended to install directly via pip install in Miniforge Prompt. Refer to [this guide](../Quickstart/install_windows_gpu.md).

## Install Docker

Follow the [Docker installation Guide](./docker_windows_gpu.md#install-docker) to install docker on either Linux or Windows.

## Launch Docker

Prepare ipex-llm-serving-xpu Docker Image:
```bash
cd docker/llm/serving/xpu/docker
docker build \
  --build-arg http_proxy=.. \
  --build-arg https_proxy=.. \
  --build-arg no_proxy=.. \
  --rm --no-cache -t intelanalytics/ipex-llm-serving-xpu:latest .
```

Start ipex-llm-xpu Docker Container. Choose one of the following commands to start the container:

- For **Linux users**:

  ```bash
  export DOCKER_IMAGE=intelanalytics/ipex-llm-serving-xpu:latest
  export CONTAINER_NAME=my_container
  export MODEL_PATH=/llm/models[change to your model path]

  docker run -itd \
             --net=host \
             --device=/dev/dri \
             --memory="32G" \
             --name=$CONTAINER_NAME \
             --shm-size="16g" \
             -v $MODEL_PATH:/llm/models \
             --entrypoint /bin/bash \
             $DOCKER_IMAGE
  ```

- For **Windows WSL users**:

  ```bash
  #/bin/bash
  export DOCKER_IMAGE=intelanalytics/ipex-llm-serving-xpu:latest
  export CONTAINER_NAME=my_container
  export MODEL_PATH=/llm/models[change to your model path]

  sudo docker run -itd \
                  --net=host \
                  --privileged \
                  --device /dev/dri \
                  --memory="32G" \
                  --name=$CONTAINER_NAME \
                  --shm-size="16g" \
                  -v $MODEL_PATH:/llm/llm-models \
                  -v /usr/lib/wsl:/usr/lib/wsl \ 
                  --entrypoint /bin/bash \
                  $DOCKER_IMAGE
  ```

Access the container:
```
docker exec -it $CONTAINER_NAME bash
```

To verify the device is successfully mapped into the container, run `sycl-ls` to check the result. In a machine with Arc A770, the sampled output is:

```bash
root@arda-arc12:/# sycl-ls
[opencl:acc:0] Intel(R) FPGA Emulation Platform for OpenCL(TM), Intel(R) FPGA Emulation Device 1.2 [2023.16.7.0.21_160000]
[opencl:cpu:1] Intel(R) OpenCL, 13th Gen Intel(R) Core(TM) i9-13900K 3.0 [2023.16.7.0.21_160000]
[opencl:gpu:2] Intel(R) OpenCL Graphics, Intel(R) Arc(TM) A770 Graphics 3.0 [23.17.26241.33]
[ext_oneapi_level_zero:gpu:0] Intel(R) Level-Zero, Intel(R) Arc(TM) A770 Graphics 1.3 [1.3.26241]
```

> [!TIP]
> You can run the Env-Check script to verify your ipex-llm installation and runtime environment.
>
> ```bash
> cd /ipex-llm/python/llm/scripts
> bash env-check.sh
> ```

> [!NOTE]
> For optimal performance, it is recommended to set several environment variables according to your hardware environment.
> 
> ```bash
> # Disable code related to XETLA; only Intel Data Center GPU Max Series supports XETLA, so non-Max machines should set this to OFF.
> # Recommended for use on Intel Arc™ A-Series Graphics and Intel Data Center GPU Flex Series.
> export USE_XETLA=OFF
> 
> # Enable immediate command lists mode for the Level Zero plugin. Improves performance on Intel Arc™ A-Series Graphics and Intel Data Center GPU Max Series; however, it depends on the Linux Kernel, and some Linux kernels may not necessarily provide acceleration.
> # Recommended for use on Intel Arc™ A-Series Graphics and Intel Data Center GPU Max Series, but it depends on the Linux kernel, Upstream i915 kernel drivers may cause performance regressions.
> export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1
> 
> # Controls persistent device compiled code cache. Set to '1' to turn on and '0' to turn off.
> # Recommended for all hardware environments. This environment variable is already set by default in Docker images.
> export SYCL_CACHE_PERSISTENT=1
> 
> # Reduce memory accesses by fusing SDP ops.
> # Recommended for use on Intel Data Center GPU Max Series.
> export ENABLE_SDP_FUSION=1
> ```


## Run Inference Benchmark 

Navigate to benchmark directory, and modify the `config.yaml` under the `all-in-one` folder for benchmark configurations.
```bash
cd /benchmark/all-in-one
vim config.yaml
```

In the `config.yaml`, change `repo_id` to the model you want to test and `local_model_hub` to point to your model hub path. 

```yaml
...
repo_id:
  - 'meta-llama/Llama-2-7b-chat-hf'
local_model_hub: '/path/to/your/mode/folder'
...
``` 

After modifying `config.yaml`, run the following commands to run benchmarking:
```bash
source ipex-llm-init --gpu --device <value>
python run.py
```

**Result Interpretation**

After the benchmarking is completed, you can obtain a CSV result file under the current folder. You can mainly look at the results of columns `1st token avg latency (ms)` and `2+ avg latency (ms/token)` for the benchmark results. You can also check whether the column `actual input/output tokens` is consistent with the column `input/output tokens` and whether the parameters you specified in `config.yaml` have been successfully applied in the benchmarking.


## Run Chat Service

We provide `chat.py` for conversational AI. 

For example, if your model is Llama-2-7b-chat-hf and mounted on /llm/models, you can execute the following command to initiate a conversation:
  ```bash
  cd /llm
  python chat.py --model-path /llm/models/Llama-2-7b-chat-hf
  ```

Here is a demostration:

<a align="left"  href="https://llm-assets.readthedocs.io/en/latest/_images/llm-inference-cpu-docker-chatpy-demo.gif">
            <img src="https://llm-assets.readthedocs.io/en/latest/_images/llm-inference-cpu-docker-chatpy-demo.gif" width='60%' /> 

</a><br>

## Run PyTorch Examples

We provide several PyTorch examples that you could apply IPEX-LLM INT4 optimizations on models on Intel GPUs

For example, if your model is Llama-2-7b-chat-hf and mounted on /llm/models, you can navigate to /examples/llama2 directory, excute the following command to run example:

```bash
cd /examples/<model_dir>
python ./generate.py --repo-id-or-model-path /llm/models/Llama-2-7b-chat-hf --prompt PROMPT --n-predict N_PREDICT
```


Arguments info:
- `--repo-id-or-model-path REPO_ID_OR_MODEL_PATH`: argument defining the huggingface repo id for the Llama2 model (e.g. `meta-llama/Llama-2-7b-chat-hf` and `meta-llama/Llama-2-13b-chat-hf`) to be downloaded, or the path to the huggingface checkpoint folder. It is default to be `'meta-llama/Llama-2-7b-chat-hf'`.
- `--prompt PROMPT`: argument defining the prompt to be infered (with integrated prompt format for chat). It is default to be `'What is AI?'`.
- `--n-predict N_PREDICT`: argument defining the max number of tokens to predict. It is default to be `32`.

**Sample Output**
```log
Inference time: xxxx s
-------------------- Prompt --------------------
<s>[INST] <<SYS>>

<</SYS>>

What is AI? [/INST]
-------------------- Output --------------------
[INST] <<SYS>>

<</SYS>>

What is AI? [/INST]  Artificial intelligence (AI) is the broader field of research and development aimed at creating machines that can perform tasks that typically require human intelligence,
```
