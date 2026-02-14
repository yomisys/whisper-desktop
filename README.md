# 🎙️ Whisper Desktop - Professional Audio Transcription Tool

A complete desktop application for audio transcription powered by OpenAI's Whisper model. Features both single file and batch processing with an intuitive graphical interface.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Key Features

### 🎯 Dual Processing Modes
- **Single File Mode**: Quick transcription with live preview
- **Batch Processing**: Process entire folders automatically

### 🧠 Multiple AI Models
- tiny (fastest, ~70% accuracy)
- base (balanced, ~75% accuracy) ⭐ Recommended
- small (better, ~85% accuracy)
- medium (high quality, ~92% accuracy)
- large (best quality, ~95% accuracy)

### 🌍 Multi-Language Support
- Auto-detect language or specify from 10+ languages
- Support for English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, and more

### 📄 Multiple Output Formats
- **TXT**: Plain text transcription
- **JSON**: Full metadata with timestamps
- **SRT**: Standard subtitle format
- **VTT**: Web video text tracks
- **ALL**: Generate all formats at once

### ⚡ Advanced Features
- Word-level timestamps
- Real-time progress tracking
- Batch processing with status monitoring
- Translation to English
- Comprehensive output logging
- User-friendly GUI

## 🚀 Quick Start

### 1. Run Setup (First Time Only)

```bash
# Double-click setup.bat or run in terminal:
setup.bat
```

This will:
- Verify Python and FFmpeg installation
- Create virtual environment
- Install all dependencies automatically

### 2. Launch Application

```bash
# Double-click run_whisper.bat or run in terminal:
run_whisper.bat
```

### 3. Start Transcribing!

**For Single Files:**
1. Click "Browse" to select audio file
2. Choose output location
3. Click "🎯 Transcribe File"

**For Batch Processing:**
1. Switch to "Batch Processing" tab
2. Click "➕ Add Files" or "📁 Add Folder"
3. Click "🚀 Process All Files"

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space
- **FFmpeg**: Required for audio processing

### Recommended for Best Performance
- **RAM**: 16GB
- **GPU**: NVIDIA GPU with 6GB+ VRAM
- **CPU**: Modern multi-core processor
- **Storage**: SSD with 10GB+ free space

## 📦 What's Included

```
WhisperDesktop/
├── whisper_desktop.py      # Main application
├── setup.bat               # Automated setup script
├── run_whisper.bat         # Application launcher
├── requirements.txt        # Python dependencies
├── INSTALLATION_GUIDE.md   # Detailed installation guide
└── README.md              # This file
```

## 🎨 Interface Overview

### Configuration Panel
- **Model Selection**: Choose AI model based on speed vs. accuracy
- **Language**: Auto-detect or specify language
- **Task**: Transcribe or translate to English
- **Output Format**: Select desired file format(s)
- **Word Timestamps**: Enable for detailed timing

### Single File Mode
- File browser for easy selection
- Output directory customization
- Live transcription preview
- Progress tracking

### Batch Processing Mode
- Add multiple files or entire folders
- Visual file list with size and status
- Batch progress monitoring
- Automatic file naming

### Output Console
- Real-time processing logs
- Error reporting
- Completion notifications

## 💻 Usage Examples

### Example 1: Quick Transcription
```
1. Select "Single File" tab
2. Browse to your audio file
3. Keep default settings (base model, auto language)
4. Click "Transcribe File"
5. View preview and save to output folder
```

### Example 2: High-Quality Transcription
```
1. Set Model to "medium" or "large"
2. Specify language (e.g., "en" for English)
3. Enable "Word-level timestamps"
4. Select "all" for output format
5. Process your file
```

### Example 3: Batch Process Podcast Episodes
```
1. Switch to "Batch Processing" tab
2. Click "Add Folder" and select podcast directory
3. Set output folder to organized location
4. Choose "small" model for balance
5. Set format to "srt" for subtitles
6. Click "Process All Files"
7. Get coffee while it processes! ☕
```

### Example 4: Translate Foreign Audio
```
1. Select audio file
2. Set Task to "translate"
3. Choose appropriate source language
4. Process to get English translation
```

## 🔧 Configuration Tips

### For Speed:
- Use **tiny** or **base** model
- Specify language (skip auto-detection)
- Disable word timestamps
- Process on SSD

### For Accuracy:
- Use **medium** or **large** model
- Specify correct language
- Enable word timestamps
- Use high-quality audio sources

### For Batch Jobs:
- Group similar files
- Use consistent settings
- Monitor first few files
- Process overnight for large batches

## 📊 Performance Guide

**Processing Time** (1 hour of audio):

| Model  | CPU Time | GPU Time | Best For                    |
|--------|----------|----------|-----------------------------|
| tiny   | ~2 min   | ~1 min   | Quick drafts, testing       |
| base   | ~4 min   | ~2 min   | General use, podcasts       |
| small  | ~10 min  | ~3 min   | Meetings, interviews        |
| medium | ~30 min  | ~8 min   | Professional work           |
| large  | ~60 min  | ~15 min  | Maximum accuracy needed     |

## 🛠️ Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Verify FFmpeg is installed: `ffmpeg -version`
- Check PATH environment variable
- Reinstall FFmpeg if needed

**"Out of memory"**
- Use smaller model (tiny or base)
- Close other applications
- Process fewer files at once
- Consider upgrading RAM

**"Model loading failed"**
- Check internet connection (first download)
- Verify disk space (models are 1-3GB)
- Try different model size

**Slow processing**
- Use GPU acceleration if available
- Choose smaller model
- Specify language explicitly
- Disable word timestamps

**Poor accuracy**
- Use larger model
- Verify audio quality
- Specify correct language
- Check audio format (WAV recommended)

## 🔄 Updating

To update Whisper to the latest version:

```bash
whisper_env\Scripts\activate
pip install --upgrade openai-whisper
```

## 📝 Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- OPUS (.opus)
- WMA (.wma)

*Note: WAV and FLAC provide best quality for transcription*

## 🎓 Advanced Usage

### Using GPU Acceleration

If you have NVIDIA GPU:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Custom Model Directory

Edit `whisper_desktop.py` to specify custom model path:

```python
model = whisper.load_model("base", download_root="C:/whisper_models")
```

### Command-Line Batch Processing

For automation or integration:

```python
import whisper
import glob

model = whisper.load_model("base")
for audio_file in glob.glob("*.mp3"):
    result = model.transcribe(audio_file)
    with open(f"{audio_file}.txt", "w") as f:
        f.write(result["text"])
```

## 📚 Additional Resources

- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Whisper Model Card](https://github.com/openai/whisper/blob/main/model-card.md)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🤝 Contributing

This is a standalone desktop application. For suggestions or improvements:
1. Test thoroughly
2. Document changes
3. Consider backward compatibility

## 📄 License

This application uses OpenAI's Whisper model, licensed under MIT License.

## 🆘 Support

For help:
1. Check INSTALLATION_GUIDE.md for detailed setup
2. Review troubleshooting section above
3. Verify all dependencies are installed
4. Check Whisper GitHub issues

## 🎯 Use Cases

Perfect for:
- 📝 Meeting transcriptions
- 🎙️ Podcast subtitles
- 🎬 Video captioning
- 📚 Lecture notes
- 💼 Interview documentation
- 🌍 Translation services
- ♿ Accessibility features

## ⚡ Quick Tips

1. **Test with small files first** to find optimal settings
2. **Specify language** for 2x faster processing
3. **Use batch mode** for multiple similar files
4. **Enable word timestamps** for precise timing
5. **Choose "all" format** to have maximum flexibility
6. **Monitor memory usage** during large batch jobs

## 🔮 Future Enhancements

Potential features for future versions:
- Real-time transcription
- Speaker diarization
- Custom model fine-tuning
- Cloud processing integration
- Audio editing integration
- Multi-language output

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Developed by**: Yomi (EMBB0008)  
**Powered by**: OpenAI Whisper

For professional transcription services and consulting, contact Global Lean Six Sigma Consulting.
