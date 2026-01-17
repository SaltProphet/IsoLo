# Hugging Face Spaces Deployment Package

This folder contains everything needed to deploy Loop Architect to Hugging Face Spaces.

## 📁 Files Included

### Core Application Files
- **`app.py`** - Main Gradio application (copied from backend/app.py)
- **`sam_audio_integration.py`** - SAM Audio integration module for AI-powered sound isolation
- **`requirements.txt`** - Python dependencies required to run the app
- **`packages.txt`** - System-level dependencies (ffmpeg, libsndfile1)

### Documentation
- **`README.md`** - Space card with feature descriptions, usage instructions, and setup guide
  - This becomes the main page of your Hugging Face Space
  - Includes YAML metadata for Space configuration
  
- **`DEPLOYMENT.md`** - Complete deployment guide with:
  - Step-by-step deployment instructions
  - Two deployment methods (upload or git)
  - Hardware recommendations
  - Troubleshooting tips
  - Performance optimization
  - Advanced features

### Configuration
- **`.env.example`** - Example environment variables for optional configuration
- **`.gitignore`** - Git ignore rules for Hugging Face Space repository

## 🚀 Quick Start

### Method 1: Direct Upload to Hugging Face
1. Create a new Space at https://huggingface.co/new-space
2. Select "Gradio" as SDK
3. Upload all files from this folder
4. Wait for automatic build and deployment

### Method 2: Git Clone and Push
1. Create a new Space at https://huggingface.co/new-space
2. Clone the space repository
3. Copy all files from this folder
4. Commit and push to deploy

See `DEPLOYMENT.md` for detailed instructions.

## 📦 What's Deployed

The deployed Space provides:
- **Stem Separation** - Separate audio into vocals, drums, bass, other, guitar, piano
- **Musical Analysis** - BPM detection, key detection, harmonic recommendations
- **Loop Generation** - Bar loops and one-shot slicing with BPM/key tagging
- **Advanced Effects** - LFO modulation, filters, normalization, pitch shifting
- **Professional Output** - WAV files with MIDI generation for melodic stems
- **SAM Audio (optional)** - AI-powered named sound isolation

## 💾 Dependencies

### Python Packages (from requirements.txt)
- Core: numpy, scipy, soundfile, librosa, gradio, matplotlib
- Deep Learning: torch, torchaudio (for SAM Audio)
- Optional: sam-audio-infer (for named sound isolation)

### System Packages (from packages.txt)
- ffmpeg - Audio format conversion
- libsndfile1 - Audio file I/O

## ⚙️ Hardware Requirements

### Minimum (Free CPU)
- Works for basic processing
- Slower performance (~5-10 min per track)

### Recommended (CPU Upgraded or GPU)
- Better performance
- GPU required for SAM Audio
- Much faster processing (~30-120 sec per track)

## 🔧 Customization

### Before Deployment

1. **Edit README.md** to customize:
   - Space title and emoji in YAML header
   - Feature descriptions
   - Usage instructions

2. **Modify app.py** if needed:
   - Adjust processing limits
   - Enable/disable features
   - Customize UI theme

3. **Update requirements.txt**:
   - Pin specific versions if needed
   - Add/remove optional dependencies

### After Deployment

- Change hardware tier in Space settings
- Add environment variables as secrets
- Monitor performance in analytics
- Update via git push or file upload

## 📚 Additional Resources

- **Main Repository**: https://github.com/SaltProphet/IsoLo
- **Backend Documentation**: ../backend/README.md
- **SAM Audio Guide**: ../backend/SAM_AUDIO_INTEGRATION.md
- **HF Spaces Docs**: https://huggingface.co/docs/hub/spaces

## 🐛 Troubleshooting

Common issues and solutions:

1. **Build Fails**: Check requirements.txt versions, review build logs
2. **Out of Memory**: Upgrade hardware tier or reduce audio length limits
3. **SAM Audio Not Working**: Requires GPU, check model installation
4. **Slow Processing**: Use GPU hardware, optimize model loading

See `DEPLOYMENT.md` for detailed troubleshooting.

## 📝 Notes

### Stem Separation
The current implementation uses mock stem separation for demonstration. For production:
- Integrate with Demucs (recommended)
- Or use Spleeter
- Or any other source separation model

### SAM Audio
SAM Audio is optional and requires:
- GPU hardware (T4 or better)
- Additional setup (`pip install sam-audio-infer`)
- Falls back gracefully if unavailable

## ✅ Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All files are present (10 files total)
- [ ] README.md has correct YAML metadata
- [ ] requirements.txt includes all dependencies
- [ ] app.py and sam_audio_integration.py are copied correctly
- [ ] DEPLOYMENT.md reviewed for deployment method
- [ ] Hardware tier selected appropriately

## 🎯 Success Criteria

After deployment, verify:
- [ ] Space builds without errors
- [ ] App launches successfully
- [ ] File upload works
- [ ] Stem separation processes audio
- [ ] BPM/key detection works
- [ ] Loop slicing generates files
- [ ] ZIP download works

## 📮 Support

- **Report Issues**: GitHub Issues
- **Ask Questions**: Space Community tab
- **Contribute**: Pull requests welcome

---

**Ready to deploy!** Follow `DEPLOYMENT.md` for step-by-step instructions. 🚀
