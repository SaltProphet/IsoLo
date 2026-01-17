# Loop Architect - Setup Instructions

This guide provides complete setup instructions for running Loop Architect locally or deploying to Hugging Face Spaces.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Local Installation](#local-installation)
- [Hugging Face Spaces Deployment](#hugging-face-spaces-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Advanced Setup](#advanced-setup)

---

## 🚀 Quick Start

### For Local Development

```bash
# 1. Navigate to the huggingface folder
cd huggingface/

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open browser to http://localhost:7860
```

### For Hugging Face Spaces

Upload the contents of this folder to a new Gradio Space. See [Deployment Guide](#hugging-face-spaces-deployment) below.

---

## 📦 Prerequisites

### System Requirements

**Minimum Requirements:**
- Python 3.8 or higher
- 4GB RAM
- 1GB free disk space
- CPU with AVX support

**Recommended Requirements:**
- Python 3.10+
- 8GB+ RAM
- 2GB+ free disk space
- CUDA-capable GPU (for SAM Audio)

### Software Dependencies

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **FFmpeg** (for audio file format support)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS (with Homebrew):**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add to PATH
   
   **Verify installation:**
   ```bash
   ffmpeg -version
   ```

3. **Git** (for cloning and deployment)
   - Download from [git-scm.com](https://git-scm.com/)
   - Verify: `git --version`

---

## 💻 Local Installation

### Step 1: Prepare Environment

**Option A: Virtual Environment (Recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**Option B: Conda Environment**

```bash
# Create conda environment
conda create -n loop-architect python=3.10
conda activate loop-architect
```

### Step 2: Install Dependencies

```bash
# Navigate to huggingface folder
cd /path/to/IsoLo/huggingface/

# Install Python packages
pip install -r requirements.txt
```

**Dependencies Installed:**
- `numpy>=1.24.0` - Numerical computing
- `scipy>=1.10.0` - Scientific computing
- `soundfile>=0.12.0` - Audio I/O
- `librosa>=0.10.0` - Audio analysis
- `gradio>=4.0.0` - Web interface
- `matplotlib>=3.7.0` - Visualization
- `torch>=2.0.0` - Deep learning (for SAM Audio)
- `torchaudio>=2.0.0` - Audio processing (for SAM Audio)
- `Pillow>=10.0.0` - Image processing

### Step 3: Optional - Install SAM Audio

SAM Audio enables AI-powered named sound isolation (e.g., "saxophone solo", "crowd applause").

**Option A: Lightweight Version (Recommended)**

```bash
pip install sam-audio-infer
```

**Option B: Official Version (Maximum Quality)**

```bash
git clone https://github.com/facebookresearch/sam-audio.git
cd sam-audio
pip install .
```

**Notes:**
- SAM Audio is optional - app works without it
- Official version requires GPU and Hugging Face token
- Lightweight version runs on CPU

### Step 4: Run the Application

```bash
# From the huggingface folder
python app.py
```

**Expected Output:**
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://XXXXX.gradio.live

To create a public link, set `share=True` in `launch()`.
```

### Step 5: Access the Interface

1. Open browser to `http://localhost:7860`
2. Upload an audio file
3. Click "Separate Stems & Analyze"
4. Configure settings and generate loops

---

## ☁️ Hugging Face Spaces Deployment

### Quick Deployment (5 minutes)

1. **Create Hugging Face Account**
   - Sign up at [huggingface.co](https://huggingface.co/join)
   - Verify email

2. **Create New Space**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Enter Space name (e.g., "loop-architect")
   - Select **Gradio** as SDK
   - Choose SDK version **4.0.0** or later
   - Set visibility (Public/Private)
   - Click "Create Space"

3. **Upload Files**
   
   Upload these files from the `huggingface/` folder:
   - ✅ `app.py`
   - ✅ `sam_audio_integration.py`
   - ✅ `workflow_orchestrator.py`
   - ✅ `workflow_types.py`
   - ✅ `requirements.txt`
   - ✅ `packages.txt` (if present)
   - ✅ `README.md`
   - ✅ `modules/` (entire folder)
   - ⚠️ `.env.example` (optional, for reference)
   - ⚠️ `validate.py` (optional, for testing)

4. **Wait for Build**
   - Hugging Face automatically installs dependencies
   - Check "Logs" tab for build progress
   - Build takes ~3-5 minutes
   - App goes live automatically when ready

5. **Configure Hardware (Optional)**
   - Go to Space Settings → Hardware
   - **CPU Basic (Free)**: Works for basic processing (~5-10 min per track)
   - **GPU T4**: Recommended for SAM Audio (~30-120 sec per track)

### Git-Based Deployment (For Updates)

**One-Time Setup:**

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy files from huggingface folder
cp -r /path/to/IsoLo/huggingface/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

**Future Updates:**

```bash
cd YOUR_SPACE_NAME

# Copy updated files
cp /path/to/IsoLo/huggingface/app.py .
# ... copy other changed files

# Commit and push
git add .
git commit -m "Update: description of changes"
git push
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `huggingface/` folder (optional):

```bash
# SAM Audio Configuration
ENABLE_SAM_AUDIO=true
SAM_AUDIO_MODEL_PATH=/models/sam-audio

# Processing Limits
MAX_AUDIO_LENGTH=600  # Maximum audio length in seconds
MAX_FILE_SIZE=100     # Maximum upload size in MB

# Performance
USE_GPU=auto          # auto, true, false
NUM_WORKERS=4         # Parallel processing workers

# Debug
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Hardware Settings

**For Local Development:**
- CPU: Works on all systems, slower processing
- GPU: Requires CUDA-capable GPU, much faster

**For Hugging Face Spaces:**
- **CPU Basic (Free)**: 2 vCPU, 16GB RAM
- **CPU Upgraded**: 8 vCPU, 32GB RAM
- **GPU T4**: 4 vCPU, 16GB RAM, NVIDIA T4 GPU
- **GPU A10G**: Better performance for SAM Audio

### Customizing the Interface

Edit `app.py` to customize:

```python
# Change theme colors
demo = gr.Blocks(theme=gr.themes.Soft(
    primary_hue="blue",    # Change to: green, red, purple, etc.
    secondary_hue="red"
))

# Change default settings
manual_bpm_input = gr.Number(
    label="BPM",
    value=120.0,  # Change default BPM
    step=0.1
)

# Modify port for local development
if __name__ == "__main__":
    demo.launch(
        debug=True,
        server_port=7860,  # Change port
        share=False        # Set to True for public URL
    )
```

---

## 🔧 Troubleshooting

### Installation Issues

**Problem: `pip install` fails**

Solution:
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific Python version
python3.10 -m pip install -r requirements.txt

# Install packages one by one if batch fails
pip install numpy scipy soundfile librosa gradio matplotlib
```

**Problem: FFmpeg not found**

Solution:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: Download and add to PATH
# Verify: ffmpeg -version
```

**Problem: CUDA/GPU issues**

Solution:
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install CPU-only PyTorch if no GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Runtime Issues

**Problem: App crashes on launch**

Check logs for specific error, common fixes:
```bash
# Missing dependencies
pip install -r requirements.txt

# Port already in use
python app.py --server-port 7861

# Permission issues
chmod +x app.py
```

**Problem: Out of memory**

Solutions:
- Reduce audio file size
- Close other applications
- Increase system swap space
- Use GPU if available

**Problem: SAM Audio not working**

Solutions:
1. Check if installed: `pip list | grep sam-audio`
2. Install if missing: `pip install sam-audio-infer`
3. Verify it's optional - app works without it
4. Check GPU availability for official version

### Deployment Issues

**Problem: Hugging Face build fails**

Check build logs, common fixes:
1. Pin dependency versions in `requirements.txt`
2. Remove incompatible packages
3. Ensure `app.py` has no syntax errors
4. Check SDK version compatibility

**Problem: Space runs but doesn't work**

Solutions:
1. Check browser console for JavaScript errors
2. Verify all files uploaded correctly
3. Check Space logs for Python errors
4. Test locally first before deploying

---

## 🔬 Advanced Setup

### Development Mode

Enable detailed debugging:

```python
# In app.py, change:
if __name__ == "__main__":
    demo.launch(
        debug=True,          # Enable debug mode
        show_error=True,     # Show detailed errors
        show_api=True        # Enable API documentation
    )
```

### Custom Models

To use custom audio models:

1. Create `models/` folder
2. Place model files inside
3. Update `sam_audio_integration.py`:

```python
SAM_AUDIO_MODEL_PATH = "models/custom-model"
```

### Performance Optimization

**For CPU:**
```bash
# Use optimized libraries
pip install intel-extension-for-pytorch  # Intel CPUs
OMP_NUM_THREADS=4 python app.py
```

**For GPU:**
```bash
# Enable CUDA optimizations
CUDA_VISIBLE_DEVICES=0 python app.py
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run application
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t loop-architect .
docker run -p 7860:7860 loop-architect
```

### Testing

Validate your setup:

```bash
# Run validation script (if available)
python validate.py

# Test imports
python -c "
import gradio as gr
import librosa
import numpy as np
import soundfile as sf
print('All imports successful!')
"

# Test basic functionality
python -c "
from sam_audio_integration import SAMAudioSeparator
separator = SAMAudioSeparator()
print(f'SAM Audio available: {separator.is_available()}')
"
```

---

## 📚 Additional Resources

### Documentation
- [Main README](./README.md) - Feature overview
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment details
- [PACKAGE_INFO.md](./PACKAGE_INFO.md) - Package structure
- [Backend README](../backend/README.md) - Backend details
- [SAM Audio Integration](../backend/SAM_AUDIO_INTEGRATION.md) - SAM Audio guide

### External Links
- [Gradio Documentation](https://gradio.app/docs/)
- [Librosa Documentation](https://librosa.org/doc/)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [Project Repository](https://github.com/SaltProphet/IsoLo)

### Support
- **Issues**: [GitHub Issues](https://github.com/SaltProphet/IsoLo/issues)
- **Discussions**: GitHub Discussions
- **Documentation**: Project Wiki

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Python 3.8+ installed
- [ ] FFmpeg installed and accessible
- [ ] All dependencies installed (`pip list`)
- [ ] App launches without errors
- [ ] Web interface loads at localhost:7860
- [ ] Can upload audio files
- [ ] Stem separation works
- [ ] BPM/key detection works
- [ ] Loop generation works
- [ ] ZIP download works
- [ ] (Optional) SAM Audio works if installed

---

## 🎉 You're Ready!

Once setup is complete, you can:
- ✅ Process audio locally
- ✅ Generate loop packs
- ✅ Deploy to Hugging Face Spaces
- ✅ Customize and extend features
- ✅ Share your Space with others

**Need Help?**
- Check [Troubleshooting](#troubleshooting) section
- Review [Documentation](#documentation)
- Open an issue on GitHub
- Check Hugging Face Space logs

---

**Happy Processing!** 🎵✨
