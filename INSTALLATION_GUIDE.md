# Whisper Desktop Application - Installation & User Guide

## 📋 Overview

Whisper Desktop is a professional GUI application for audio transcription using OpenAI's Whisper model. It supports both single file and batch processing with multiple output formats.

## ✨ Features

- **Dual Processing Modes**: Single file and batch processing
- **Multiple Model Options**: tiny, base, small, medium, large
- **Language Support**: Auto-detect or specify from 10+ languages
- **Multiple Output Formats**: TXT, JSON, SRT, VTT
- **Word-level Timestamps**: Optional detailed timing information
- **Batch Processing**: Process entire folders of audio files
- **Real-time Progress Tracking**: Monitor processing status
- **User-friendly Interface**: Clean, professional GUI

## 🔧 Installation

### Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **FFmpeg** (Already installed in your case)
   - Verify: Run `ffmpeg -version` in terminal

### Step 1: Setup Project

```bash
# Create project directory
mkdir WhisperDesktop
cd WhisperDesktop

# Create virtual environment
python -m venv whisper_env

# Activate virtual environment
# On Windows:
whisper_env\Scripts\activate
# On macOS/Linux:
# source whisper_env/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install openai-whisper
pip install torch torchvision torchaudio

# For faster processing (optional):
pip install faster-whisper
```

### Step 3: Download Application Files

Save the `whisper_desktop.py` file to your WhisperDesktop folder.

### Step 4: Run the Application

```bash
python whisper_desktop.py
```

## 🎯 User Guide

### Configuration Panel

**Model Selection:**
- **tiny**: Fastest, lowest accuracy (~32x speed)
- **base**: Good balance (recommended for testing)
- **small**: Better accuracy (~6x speed)
- **medium**: High accuracy (~2x speed)
- **large**: Best accuracy (1x speed, requires significant resources)

**Language:**
- Set to "auto" for automatic detection
- Or specify language code (en, es, fr, de, etc.) for faster processing

**Task:**
- **transcribe**: Convert speech to text in original language
- **translate**: Convert speech to English text

**Output Format:**
- **txt**: Plain text file
- **json**: JSON with detailed metadata
- **srt**: Subtitle format (for videos)
- **vtt**: WebVTT format (for web videos)
- **all**: Generate all formats

### Single File Mode

1. Click **"Browse"** to select an audio file
2. Choose output folder (default: Documents/Whisper_Output)
3. Configure settings in Configuration Panel
4. Click **"🎯 Transcribe File"**
5. Preview appears in the text area
6. Output files saved to selected folder

**Supported Formats:**
- MP3, WAV, M4A, FLAC, OGG, OPUS, WMA

### Batch Processing Mode

1. **Add Files:**
   - Click **"➕ Add Files"** to select multiple files
   - OR click **"📁 Add Folder"** to add entire directory

2. **Review List:**
   - See all files with size and status
   - Click **"🗑️ Clear All"** to start over

3. **Select Output Folder:**
   - Choose where all transcriptions will be saved

4. **Process:**
   - Click **"🚀 Process All Files"**
   - Watch progress in the status bar
   - Each file's status updates in real-time

5. **Results:**
   - All files saved with original names
   - Different extensions for each format
   - Completion notification when done

### Output Files

For a file named `meeting.mp3`, you'll get:

```
Whisper_Output/
├── meeting.txt          # Plain text transcription
├── meeting.json         # Full data with timestamps
├── meeting.srt          # Subtitle format
└── meeting.vtt          # Web video format
```

**TXT Format:**
```
This is the transcribed text of your audio file.
```

**SRT Format:**
```
1
00:00:00,000 --> 00:00:05,120
This is the first segment of transcribed text.

2
00:00:05,120 --> 00:00:10,500
This is the second segment.
```

**JSON Format:**
```json
{
  "text": "Full transcription...",
  "segments": [
    {
      "start": 0.0,
      "end": 5.12,
      "text": "This is the first segment"
    }
  ],
  "language": "en"
}
```

## 💡 Tips & Best Practices

### For Best Accuracy:
1. Use **medium** or **large** models
2. Specify the language if known (faster and more accurate)
3. Enable word-level timestamps for detailed timing
4. Use high-quality audio files

### For Fastest Processing:
1. Use **tiny** or **base** models
2. Specify language instead of auto-detect
3. Disable word-level timestamps
4. Consider using faster-whisper library

### For Batch Processing:
1. Group similar files (same language, quality)
2. Use appropriate model for file count vs. accuracy needs
3. Process overnight for large batches
4. Keep output folder organized by date or project

### Resource Management:
- **tiny/base**: Can run on CPU
- **small**: Recommended minimum 8GB RAM
- **medium**: Recommended 16GB RAM + GPU
- **large**: Requires GPU with 10GB+ VRAM

## 🔍 Troubleshooting

### Issue: Application won't start

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip uninstall openai-whisper
pip install openai-whisper
```

### Issue: "FFmpeg not found"

**Solution:**
```bash
# Verify FFmpeg installation
ffmpeg -version

# If not found, add to PATH or reinstall
```

### Issue: Out of memory error

**Solutions:**
- Use a smaller model (tiny or base)
- Process files individually instead of batch
- Close other applications
- Restart computer to free up memory

### Issue: Slow processing

**Solutions:**
- Use smaller model
- Specify language (skip auto-detection)
- Disable word timestamps
- Install CUDA for GPU acceleration
- Use faster-whisper library

### Issue: Poor accuracy

**Solutions:**
- Use larger model (medium or large)
- Ensure audio quality is good
- Specify correct language
- Check that FFmpeg is properly installed
- Try different audio format (WAV recommended)

## 🎓 Advanced Usage

### Custom Model Path

To use a custom model or cache directory:

```python
# Modify in whisper_desktop.py
model = whisper.load_model("base", download_root="C:/whisper_models")
```

### Batch Processing via Command Line

For automation, create a script:

```python
import whisper
import os

model = whisper.load_model("base")
audio_dir = "C:/audio_files"

for file in os.listdir(audio_dir):
    if file.endswith(('.mp3', '.wav')):
        result = model.transcribe(os.path.join(audio_dir, file))
        with open(f"{file}.txt", 'w') as f:
            f.write(result['text'])
```

### Using GPU Acceleration

If you have NVIDIA GPU:

```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

The application will automatically use GPU if available.

## 📊 Performance Benchmarks

Approximate processing times for 1 hour of audio:

| Model  | CPU (i7) | GPU (RTX 3060) | Accuracy |
|--------|----------|----------------|----------|
| tiny   | 2 min    | 1 min          | 70%      |
| base   | 4 min    | 2 min          | 75%      |
| small  | 10 min   | 3 min          | 85%      |
| medium | 30 min   | 8 min          | 92%      |
| large  | 60 min   | 15 min         | 95%      |

*Actual times vary based on audio quality and system specs*

## 🛠️ Customization

### Changing Default Output Folder

Edit line 28 in `whisper_desktop.py`:

```python
self.single_output_var = tk.StringVar(value="YOUR_PREFERRED_PATH")
```

### Adding More Languages

Edit line 65 in `whisper_desktop.py`:

```python
values=['auto', 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ar', 'hi']
```

### Custom UI Theme

Modify the style configuration (line 32):

```python
style.theme_use('clam')  # Options: 'clam', 'alt', 'default', 'classic'
```

## 📞 Support

For issues or questions:
- Check Whisper documentation: https://github.com/openai/whisper
- Review troubleshooting section above
- Ensure all dependencies are properly installed

## 📄 License

This application uses OpenAI's Whisper model, which is licensed under MIT License.

## 🔄 Updates

To update Whisper:

```bash
pip install --upgrade openai-whisper
```

---

**Version 1.0** - February 2026
**Compatible with:** Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
