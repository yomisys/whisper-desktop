"""
Whisper Desktop Application
A professional GUI application for audio transcription using OpenAI Whisper
Supports both single file and batch processing
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import json
from datetime import datetime
from pathlib import Path
import whisper

class WhisperDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Desktop - Audio Transcription Tool")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.model = None
        self.current_model_name = "base"
        self.processing = False
        self.processing_queue = queue.Queue()
        self.audio_files = []
        
        # Supported audio formats
        self.supported_formats = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus', '.wma')
        
        # Setup UI
        self.setup_ui()
        
        # Load default model in background
        self.load_model_async(self.current_model_name)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header
        self.create_header(main_container)
        
        # Configuration Panel
        self.create_config_panel(main_container)
        
        # Processing Mode Tabs
        self.create_mode_tabs(main_container)
        
        # Progress and Status
        self.create_progress_panel(main_container)
        
        # Output Console
        self.create_output_console(main_container)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🎙️ Whisper Desktop", 
                               font=('Segoe UI', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Professional Audio Transcription Tool",
                                  font=('Segoe UI', 10))
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
    
    def create_config_panel(self, parent):
        """Create configuration panel"""
        config_frame = ttk.LabelFrame(parent, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Model selection
        ttk.Label(config_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(config_frame, textvariable=self.model_var, 
                                   values=['tiny', 'base', 'small', 'medium', 'large'],
                                   state='readonly', width=15)
        model_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        model_combo.bind('<<ComboboxSelected>>', self.on_model_change)
        
        # Language selection
        ttk.Label(config_frame, text="Language:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.language_var = tk.StringVar(value="auto")
        language_combo = ttk.Combobox(config_frame, textvariable=self.language_var,
                                     values=['auto', 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja'],
                                     state='readonly', width=15)
        language_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Task selection
        ttk.Label(config_frame, text="Task:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.task_var = tk.StringVar(value="transcribe")
        task_combo = ttk.Combobox(config_frame, textvariable=self.task_var,
                                 values=['transcribe', 'translate'],
                                 state='readonly', width=15)
        task_combo.grid(row=0, column=5, sticky=tk.W)
        
        # Output format
        ttk.Label(config_frame, text="Output Format:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0), padx=(0, 10))
        self.output_format_var = tk.StringVar(value="txt")
        format_combo = ttk.Combobox(config_frame, textvariable=self.output_format_var,
                                   values=['txt', 'json', 'srt', 'vtt', 'all'],
                                   state='readonly', width=15)
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(0, 20))
        
        # Word timestamps
        self.word_timestamps_var = tk.BooleanVar(value=False)
        word_check = ttk.Checkbutton(config_frame, text="Word-level timestamps",
                                    variable=self.word_timestamps_var)
        word_check.grid(row=1, column=2, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Model status
        self.model_status_label = ttk.Label(config_frame, text="Model Status: Loading base model...",
                                           foreground='blue')
        self.model_status_label.grid(row=2, column=0, columnspan=6, sticky=tk.W, pady=(10, 0))
    
    def create_mode_tabs(self, parent):
        """Create tabbed interface for single and batch mode"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Single File Tab
        self.single_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.single_frame, text="Single File")
        self.create_single_mode(self.single_frame)
        
        # Batch Processing Tab
        self.batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.batch_frame, text="Batch Processing")
        self.create_batch_mode(self.batch_frame)
    
    def create_single_mode(self, parent):
        """Create single file processing interface"""
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # File selection
        ttk.Label(parent, text="Audio File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.single_file_var = tk.StringVar()
        file_entry = ttk.Entry(parent, textvariable=self.single_file_var)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=(0, 10))
        
        browse_btn = ttk.Button(parent, text="Browse", command=self.browse_single_file)
        browse_btn.grid(row=0, column=2, sticky=tk.W, pady=(0, 10))
        
        # Output directory
        ttk.Label(parent, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.single_output_var = tk.StringVar(value=str(Path.home() / "Documents" / "Whisper_Output"))
        output_entry = ttk.Entry(parent, textvariable=self.single_output_var)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=(0, 10))
        
        output_browse_btn = ttk.Button(parent, text="Browse", command=self.browse_output_folder)
        output_browse_btn.grid(row=1, column=2, sticky=tk.W, pady=(0, 10))
        
        # Preview area
        preview_label = ttk.Label(parent, text="Transcription Preview:")
        preview_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.single_preview = scrolledtext.ScrolledText(parent, height=15, wrap=tk.WORD)
        self.single_preview.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Process button
        self.single_process_btn = ttk.Button(parent, text="🎯 Transcribe File",
                                            command=self.process_single_file,
                                            style='Accent.TButton')
        self.single_process_btn.grid(row=4, column=0, columnspan=3, pady=(10, 0))
    
    def create_batch_mode(self, parent):
        """Create batch processing interface"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # File list controls
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(controls_frame, text="➕ Add Files", 
                  command=self.add_batch_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="📁 Add Folder", 
                  command=self.add_batch_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🗑️ Clear All", 
                  command=self.clear_batch_files).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(controls_frame, text="Output Folder:").pack(side=tk.LEFT, padx=(0, 10))
        self.batch_output_var = tk.StringVar(value=str(Path.home() / "Documents" / "Whisper_Output"))
        output_entry = ttk.Entry(controls_frame, textvariable=self.batch_output_var, width=40)
        output_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="Browse", 
                  command=self.browse_batch_output).pack(side=tk.LEFT)
        
        # File list with treeview
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for files
        columns = ('filename', 'size', 'status')
        self.batch_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.batch_tree.heading('filename', text='File Name')
        self.batch_tree.heading('size', text='Size')
        self.batch_tree.heading('status', text='Status')
        
        self.batch_tree.column('filename', width=400)
        self.batch_tree.column('size', width=100)
        self.batch_tree.column('status', width=150)
        
        self.batch_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.batch_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.batch_tree.configure(yscrollcommand=scrollbar.set)
        
        # Batch process button
        self.batch_process_btn = ttk.Button(parent, text="🚀 Process All Files",
                                           command=self.process_batch_files,
                                           style='Accent.TButton')
        self.batch_process_btn.grid(row=2, column=0, pady=(0, 0))
    
    def create_progress_panel(self, parent):
        """Create progress and status panel"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, sticky=tk.W)
    
    def create_output_console(self, parent):
        """Create output console"""
        console_frame = ttk.LabelFrame(parent, text="Output Log", padding="10")
        console_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(4, weight=1)
        
        self.console = scrolledtext.ScrolledText(console_frame, height=8, wrap=tk.WORD,
                                                background='#1e1e1e', foreground='#d4d4d4',
                                                font=('Consolas', 9))
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log("Application initialized successfully")
    
    # Event Handlers
    
    def on_model_change(self, event):
        """Handle model selection change"""
        new_model = self.model_var.get()
        if new_model != self.current_model_name:
            self.load_model_async(new_model)
    
    def browse_single_file(self):
        """Browse for single audio file"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", " ".join(f"*{fmt}" for fmt in self.supported_formats)),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.single_file_var.set(filename)
            self.log(f"Selected file: {os.path.basename(filename)}")
    
    def browse_output_folder(self):
        """Browse for output folder (single mode)"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.single_output_var.set(folder)
    
    def browse_batch_output(self):
        """Browse for output folder (batch mode)"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.batch_output_var.set(folder)
    
    def add_batch_files(self):
        """Add files to batch processing list"""
        filenames = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", " ".join(f"*{fmt}" for fmt in self.supported_formats)),
                ("All Files", "*.*")
            ]
        )
        
        for filename in filenames:
            if filename not in self.audio_files:
                self.audio_files.append(filename)
                size = os.path.getsize(filename)
                size_mb = f"{size / (1024*1024):.2f} MB"
                self.batch_tree.insert('', 'end', values=(os.path.basename(filename), size_mb, 'Pending'))
        
        self.log(f"Added {len(filenames)} file(s) to batch queue")
    
    def add_batch_folder(self):
        """Add all audio files from a folder"""
        folder = filedialog.askdirectory(title="Select Folder with Audio Files")
        if folder:
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(self.supported_formats):
                        filepath = os.path.join(root, file)
                        if filepath not in self.audio_files:
                            self.audio_files.append(filepath)
                            size = os.path.getsize(filepath)
                            size_mb = f"{size / (1024*1024):.2f} MB"
                            self.batch_tree.insert('', 'end', values=(os.path.basename(filepath), size_mb, 'Pending'))
                            count += 1
            
            self.log(f"Added {count} file(s) from folder: {folder}")
    
    def clear_batch_files(self):
        """Clear all files from batch list"""
        self.audio_files.clear()
        for item in self.batch_tree.get_children():
            self.batch_tree.delete(item)
        self.log("Cleared batch file list")
    
    # Processing Functions
    
    def load_model_async(self, model_name):
        """Load Whisper model in background thread"""
        self.model_status_label.config(text=f"Loading {model_name} model...", foreground='orange')
        self.log(f"Loading {model_name} model...")
        
        def load_model():
            try:
                self.model = whisper.load_model(model_name)
                self.current_model_name = model_name
                self.root.after(0, lambda: self.model_status_label.config(
                    text=f"Model Status: {model_name} loaded ✓", foreground='green'))
                self.root.after(0, lambda: self.log(f"{model_name} model loaded successfully"))
            except Exception as e:
                self.root.after(0, lambda: self.model_status_label.config(
                    text=f"Model Status: Error loading {model_name}", foreground='red'))
                self.root.after(0, lambda: self.log(f"Error loading model: {str(e)}", level='error'))
        
        thread = threading.Thread(target=load_model, daemon=True)
        thread.start()
    
    def process_single_file(self):
        """Process single audio file"""
        if not self.single_file_var.get():
            messagebox.showwarning("No File", "Please select an audio file first")
            return
        
        if not self.model:
            messagebox.showerror("Model Not Loaded", "Please wait for the model to load")
            return
        
        if self.processing:
            messagebox.showwarning("Processing", "Already processing. Please wait.")
            return
        
        self.processing = True
        self.single_process_btn.config(state='disabled')
        self.single_preview.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self._process_single_thread, daemon=True)
        thread.start()
    
    def _process_single_thread(self):
        """Background thread for single file processing"""
        try:
            audio_file = self.single_file_var.get()
            output_dir = self.single_output_var.get()
            
            self.update_status("Transcribing audio file...")
            self.log(f"Processing: {os.path.basename(audio_file)}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Transcribe
            language = None if self.language_var.get() == 'auto' else self.language_var.get()
            
            result = self.model.transcribe(
                audio_file,
                language=language,
                task=self.task_var.get(),
                word_timestamps=self.word_timestamps_var.get(),
                verbose=False
            )
            
            # Generate output filename
            base_name = Path(audio_file).stem
            
            # Save outputs
            self.save_transcription(result, output_dir, base_name)
            
            # Update preview
            self.root.after(0, lambda: self.single_preview.insert(1.0, result['text']))
            
            self.update_status("Transcription complete!")
            self.log(f"Successfully transcribed: {base_name}")
            self.update_progress(100)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Transcription complete!\nSaved to: {output_dir}"
            ))
            
        except Exception as e:
            self.log(f"Error processing file: {str(e)}", level='error')
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed:\n{str(e)}"))
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.single_process_btn.config(state='normal'))
            self.update_progress(0)
    
    def process_batch_files(self):
        """Process all files in batch queue"""
        if not self.audio_files:
            messagebox.showwarning("No Files", "Please add audio files to the batch queue first")
            return
        
        if not self.model:
            messagebox.showerror("Model Not Loaded", "Please wait for the model to load")
            return
        
        if self.processing:
            messagebox.showwarning("Processing", "Already processing. Please wait.")
            return
        
        self.processing = True
        self.batch_process_btn.config(state='disabled')
        
        thread = threading.Thread(target=self._process_batch_thread, daemon=True)
        thread.start()
    
    def _process_batch_thread(self):
        """Background thread for batch processing"""
        output_dir = self.batch_output_var.get()
        os.makedirs(output_dir, exist_ok=True)
        
        total_files = len(self.audio_files)
        language = None if self.language_var.get() == 'auto' else self.language_var.get()
        
        for idx, audio_file in enumerate(self.audio_files, 1):
            try:
                base_name = os.path.basename(audio_file)
                self.update_status(f"Processing {idx}/{total_files}: {base_name}")
                self.log(f"[{idx}/{total_files}] Processing: {base_name}")
                
                # Update tree view status
                self.update_batch_tree_status(idx-1, "Processing...")
                
                # Transcribe
                result = self.model.transcribe(
                    audio_file,
                    language=language,
                    task=self.task_var.get(),
                    word_timestamps=self.word_timestamps_var.get(),
                    verbose=False
                )
                
                # Save outputs
                file_stem = Path(audio_file).stem
                self.save_transcription(result, output_dir, file_stem)
                
                # Update tree view status
                self.update_batch_tree_status(idx-1, "✓ Complete")
                self.log(f"[{idx}/{total_files}] Completed: {base_name}")
                
                # Update progress
                progress = (idx / total_files) * 100
                self.update_progress(progress)
                
            except Exception as e:
                self.log(f"Error processing {base_name}: {str(e)}", level='error')
                self.update_batch_tree_status(idx-1, "✗ Failed")
        
        self.update_status(f"Batch processing complete! Processed {total_files} files")
        self.log(f"Batch processing complete. Output saved to: {output_dir}")
        
        self.root.after(0, lambda: messagebox.showinfo(
            "Batch Complete", 
            f"Processed {total_files} files\nOutput saved to:\n{output_dir}"
        ))
        
        self.processing = False
        self.root.after(0, lambda: self.batch_process_btn.config(state='normal'))
        self.update_progress(0)
    
    def save_transcription(self, result, output_dir, base_name):
        """Save transcription in requested formats"""
        output_format = self.output_format_var.get()
        
        if output_format == 'all':
            formats = ['txt', 'json', 'srt', 'vtt']
        else:
            formats = [output_format]
        
        for fmt in formats:
            if fmt == 'txt':
                self.save_as_txt(result, output_dir, base_name)
            elif fmt == 'json':
                self.save_as_json(result, output_dir, base_name)
            elif fmt == 'srt':
                self.save_as_srt(result, output_dir, base_name)
            elif fmt == 'vtt':
                self.save_as_vtt(result, output_dir, base_name)
    
    def save_as_txt(self, result, output_dir, base_name):
        """Save as plain text"""
        output_file = os.path.join(output_dir, f"{base_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])
    
    def save_as_json(self, result, output_dir, base_name):
        """Save as JSON"""
        output_file = os.path.join(output_dir, f"{base_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    
    def save_as_srt(self, result, output_dir, base_name):
        """Save as SRT subtitle format"""
        output_file = os.path.join(output_dir, f"{base_name}.srt")
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments'], 1):
                start = self.format_timestamp_srt(segment['start'])
                end = self.format_timestamp_srt(segment['end'])
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    def save_as_vtt(self, result, output_dir, base_name):
        """Save as WebVTT format"""
        output_file = os.path.join(output_dir, f"{base_name}.vtt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            for segment in result['segments']:
                start = self.format_timestamp_vtt(segment['start'])
                end = self.format_timestamp_vtt(segment['end'])
                f.write(f"{start} --> {end}\n")
                f.write(f"{segment['text'].strip()}\n\n")
    
    @staticmethod
    def format_timestamp_srt(seconds):
        """Format timestamp for SRT format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    @staticmethod
    def format_timestamp_vtt(seconds):
        """Format timestamp for VTT format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    # UI Update Methods
    
    def update_status(self, message):
        """Update status label"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def update_progress(self, value):
        """Update progress bar"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def update_batch_tree_status(self, index, status):
        """Update status in batch tree view"""
        def update():
            items = self.batch_tree.get_children()
            if index < len(items):
                item = items[index]
                values = list(self.batch_tree.item(item, 'values'))
                values[2] = status
                self.batch_tree.item(item, values=values)
        
        self.root.after(0, update)
    
    def log(self, message, level='info'):
        """Add message to console log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if level == 'error':
            prefix = "❌ ERROR"
        elif level == 'warning':
            prefix = "⚠️  WARN"
        else:
            prefix = "ℹ️  INFO"
        
        log_message = f"[{timestamp}] {prefix}: {message}\n"
        
        def append_log():
            self.console.insert(tk.END, log_message)
            self.console.see(tk.END)
        
        self.root.after(0, append_log)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = WhisperDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
