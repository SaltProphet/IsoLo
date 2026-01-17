# Deploying Loop Architect to Hugging Face Spaces

This guide walks you through deploying Loop Architect to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account** - Sign up at [huggingface.co](https://huggingface.co/)
2. **Git** - For cloning and pushing code
3. **Git LFS** (optional) - For large model files

## Quick Start

### Option 1: Direct Upload (Easiest)

1. **Create a New Space**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Choose "Gradio" as the SDK
   - Select SDK version 4.0.0 or later
   - Set space visibility (Public/Private)

2. **Upload Files**
   - Click "Files and versions" tab
   - Upload all files from this `huggingface/` folder:
     - `app.py`
     - `sam_audio_integration.py`
     - `requirements.txt`
     - `packages.txt`
     - `README.md`
   
3. **Wait for Build**
   - Hugging Face Spaces will automatically install dependencies
   - Check the "Logs" tab for build progress
   - Once complete, your app will be live!

### Option 2: Git Push (Recommended for Updates)

1. **Create a New Space**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Choose "Gradio" as the SDK
   - Note your space name (e.g., `username/loop-architect`)

2. **Clone the Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cd YOUR_SPACE_NAME
   ```

3. **Copy Files**
   ```bash
   # Copy all files from this huggingface folder
   cp /path/to/IsoLo/huggingface/* .
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial deployment of Loop Architect"
   git push
   ```

5. **Monitor Build**
   - Visit your Space URL
   - Check build logs in the "Logs" tab
   - App will be live once build completes

## Configuration

### Hardware Settings

Loop Architect can run on different hardware tiers:

1. **CPU Basic (Free)** - ✅ Recommended for demo
   - Works for basic audio processing
   - Slower stem separation
   - ~5-10 minutes per track

2. **CPU Upgraded** - Better performance
   - Faster processing
   - Can handle longer tracks
   - ~2-5 minutes per track

3. **GPU (T4 or better)** - 🚀 Best performance
   - Required for SAM Audio
   - Very fast processing
   - ~30-120 seconds per track

To change hardware:
- Go to your Space settings
- Click "Hardware" section
- Select desired tier

### Environment Variables (Optional)

Add secrets in Space settings:

```bash
# For SAM Audio (if using)
SAM_AUDIO_MODEL_PATH=/models/sam-audio
ENABLE_SAM_AUDIO=true

# Processing limits
MAX_AUDIO_LENGTH=600
```

### Customizing README

The `README.md` in this folder becomes your Space's Card. Edit it to:
- Change the emoji/colors in the YAML header
- Update title and description
- Add custom usage instructions
- Include demo videos/images

YAML Header options:
```yaml
---
title: Your Custom Title
emoji: 🎵  # Any emoji
colorFrom: blue  # blue, red, green, etc.
colorTo: red
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false  # Pin to your profile
license: mit
---
```

## Troubleshooting

### Build Fails

**Problem:** Dependencies fail to install

**Solution:**
1. Check `requirements.txt` for compatibility
2. Review build logs for specific errors
3. Try pinning specific versions:
   ```
   numpy==1.24.0
   librosa==0.10.1
   ```

### App Crashes on Launch

**Problem:** App starts but crashes immediately

**Solution:**
1. Check "Logs" tab for Python errors
2. Ensure all imports are available
3. Test locally first:
   ```bash
   cd huggingface
   python app.py
   ```

### Out of Memory

**Problem:** App crashes during processing

**Solution:**
1. Upgrade to better hardware tier
2. Reduce `MAX_AUDIO_LENGTH` in code
3. Add memory-efficient processing:
   ```python
   # In app.py, add:
   import gc
   gc.collect()  # After heavy operations
   ```

### SAM Audio Not Working

**Problem:** Named sound isolation fails

**Solution:**
1. SAM Audio requires GPU hardware
2. Install with: `pip install sam-audio-infer`
3. Check model is available
4. Falls back to traditional stems if unavailable

### Slow Processing

**Problem:** Audio processing takes too long

**Solution:**
1. Upgrade to GPU hardware for SAM Audio
2. Reduce audio length limits
3. Consider batch processing limits
4. Add progress indicators (already included)

## Performance Tips

### Optimize for Spaces

1. **Lazy Model Loading**
   - Models load on first use, not startup
   - Already implemented in `sam_audio_integration.py`

2. **Caching**
   - Gradio automatically caches results
   - Clear cache periodically in settings

3. **Concurrent Users**
   - Free tier: 1 concurrent user
   - Paid tiers: Multiple concurrent users
   - Queue system handles overflow

### Monitoring

Check Space metrics:
- CPU/GPU usage
- Memory consumption
- Request queue length
- Error logs

Access at: `https://huggingface.co/spaces/USERNAME/SPACE/settings`

## Updates and Maintenance

### Updating Your Space

**Via Git:**
```bash
cd YOUR_SPACE_NAME
# Make changes to files
git add .
git commit -m "Update: description of changes"
git push
```

**Via Web UI:**
- Go to "Files and versions"
- Click "Upload files"
- Replace existing files

### Version Control

Tag important versions:
```bash
git tag -a v1.0.0 -m "First stable release"
git push --tags
```

### Monitoring Usage

Check analytics:
- Visit counts
- Compute time used
- User feedback (via Community tab)

## Advanced Features

### Custom Domain

1. Go to Space settings
2. Add custom domain
3. Update DNS records
4. SSL automatic via HF

### API Access

Use your Space as an API:

```python
from gradio_client import Client

client = Client("USERNAME/SPACE_NAME")
result = client.predict(
    audio_file="path/to/audio.mp3",
    api_name="/separate_stems"
)
```

### Embedding

Embed in your website:
```html
<iframe
  src="https://USERNAME-SPACE_NAME.hf.space"
  width="100%"
  height="800"
></iframe>
```

### Duplicating the Space

Users can duplicate your Space:
- Add "Duplicate this Space" button
- Include in README:
  ```markdown
  [![Duplicate Space](https://huggingface.co/datasets/huggingface/badges/raw/main/duplicate-this-space-lg.svg)](https://huggingface.co/spaces/USERNAME/SPACE_NAME?duplicate=true)
  ```

## Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs)
- [GitHub Repository](https://github.com/SaltProphet/IsoLo)

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/SaltProphet/IsoLo/issues)
- **Discussions**: Ask questions in Space Community tab
- **Updates**: Watch repository for updates

---

**Happy Deploying!** 🚀
