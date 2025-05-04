# Setting Up Ollama for Local Model Inference

This guide explains how to set up Ollama to run models locally for the Financial Advisor AI Gateway Demo.

## Why Use Local Models?

Using locally-hosted models through Ollama provides several benefits:

1. **Cost Efficiency**: No API usage fees
2. **Privacy**: Data stays on your own hardware
3. **No Internet Requirement**: Works offline
4. **Lower Latency**: Reduced response time (with sufficient hardware)
5. **Customizability**: Fine-tune models for specific use cases

## System Requirements

Ollama can run on various hardware, but for a smooth experience, we recommend:

### Minimum Requirements:
- 8GB RAM
- 4-core CPU
- 10GB free disk space

### Recommended Requirements:
- 16GB+ RAM
- 8-core CPU
- NVIDIA GPU with 8GB+ VRAM
- 30GB+ free disk space

## Installation Steps

### 1. Install Ollama

#### macOS
```bash
brew install ollama
```

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows
Download the installer from [ollama.com/download](https://ollama.com/download)

### 2. Pull Models

After installing Ollama, you'll need to download the models you want to use. The demo is configured to work with:

```bash
# Pull Llama 3 8B (recommended primary model)
ollama pull llama3-8b

# Pull additional models if desired
ollama pull mistral-7b
ollama pull phi-2
ollama pull codellama-7b
ollama pull solar-10.7b
```

## Running with Docker Compose

If you're using Docker Compose to run the demo, Ollama is already configured in the `docker-compose.yaml` file. However, you'll still need to pull the models:

```bash
# Start the Ollama container
docker-compose up -d ollama

# Wait a minute for Ollama to initialize

# Pull models through Docker
docker exec -it ollama ollama pull llama3-8b
docker exec -it ollama ollama pull mistral-7b
docker exec -it ollama ollama pull phi-2
```

## Using NVIDIA GPUs with Docker

To enable GPU acceleration with Docker:

1. Install NVIDIA Container Toolkit:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

2. Verify GPU access:
   ```bash
   docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

## Troubleshooting

### Common Issues

1. **Out of Memory**
   
   If you encounter out-of-memory errors:
   - Try a smaller model (e.g., phi-2 instead of llama3-8b)
   - Close other applications
   - Add swap space

2. **Slow Responses**
   
   If models respond slowly:
   - Use a GPU if available
   - Decrease the max_output_tokens in the Envoy configuration
   - Use smaller models

3. **Docker Container Can't Access GPU**
   
   If your Docker container can't access the GPU:
   - Ensure the NVIDIA Container Toolkit is installed
   - Add the `--gpus all` flag or use the configuration from docker-compose.yaml
   - Verify drivers are up to date

### Checking Ollama Status

To verify Ollama is running correctly:

```bash
# Check running models
ollama list

# Test a simple query
ollama run llama3-8b "Explain what a financial advisor does."

# Check Ollama API
curl http://localhost:11434/api/tags
```

## Performance Optimization

For better performance:

1. **Use Quantized Models**: Try models with 'q4' or 'q5' in their name for reduced memory usage
2. **Adjust Context Length**: Reduce context length for faster responses
3. **GPU Acceleration**: Use a CUDA-compatible GPU
4. **Batch Multiple Requests**: Process requests in parallel when possible

## Comparing Cloud vs. Local Performance

The demo interface allows you to switch between cloud and local models, letting you compare:

- Response quality
- Latency
- Token usage

This helps determine the optimal deployment strategy for your use case.
