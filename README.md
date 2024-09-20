# Wave Mouse

## Overview
This project leverages the MediaPipe library to recognize hand gestures for controlling mouse movements and keyboard shortcuts. Developed using React for web deployment and Flask as the backend, this application allows users to interact with their computers using hand gestures, making for an innovative and hands-free experience.

## Features
- **Gesture-Based Mouse Control**: Navigate your cursor using hand gestures.
- **Custom Click Gestures**: Perform left and right mouse clicks through specific gestures.
- **Keyboard Shortcuts**: Trigger various keyboard shortcuts using predefined gestures.
- **Real-Time Video Feed**: Live camera feed to capture hand movements.

## Technologies Used
- **Frontend**: React
- **Backend**: Flask
- **Computer Vision**: OpenCV, MediaPipe
- **Automation**: PyAutoGUI

## Installation

### Prerequisites
- Python 3.x
- Node.js and npm
- Virtual environment (optional but recommended)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Krishna-Sen-Programming-World/Wave-Mouse.git
   cd your-repo-name
   ```

2. **Install backend dependencies**:
   Make sure to create and activate a virtual environment if desired.
   ```bash
   pip install Flask opencv-python mediapipe pyautogui
   ```

3. **Install frontend dependencies**:
   Navigate to the React app directory (if applicable) and run:
   ```bash
   npm install
   ```

4. **Run the Flask server**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage
1. Allow camera access when prompted.
2. Follow the on-screen instructions to perform gestures.
3. Use the defined gestures to control mouse movements and keyboard shortcuts.

## Gesture Definitions
- **Mouse Movement**: 
  - Gesture to move the cursor left/right/up/down.
  
- **Mouse Clicks**:
  - Specific gesture for left click.
  - Specific gesture for right click.
  
- **On Screen Keyboard**:
  - Gesture for viewing On Screen Keyboard.
  - Gesture for closing On Screen Keyboard.
  
- **Keyboard Shortcuts**:
  - Gesture for Copy (Ctrl + C).
  - Gesture for Paste (Ctrl + V).
  - Add more shortcuts as needed.

## Folder Structure
```
Wave-Mouse/
│
├── backend/
│   ├── app.py                 # Flask application code
│   ├── app backup.py          # Backup of the Flask application
│   └── requirements.txt       # Python dependencies
│
├── static/                    # Static assets for Flask
│
└── templates/                 # HTML templates for Flask
    ├── camera_capture.html     # Template for camera capture
    ├── index.html              # Main HTML template
    │
    └── assets/                 # Asset files for the frontend
        ├── css/                # CSS files
        │   ├── aos.css
        │   ├── bootstrap.min.css
        │   ├── clash-display.css
        │   ├── fancybox.css
        │   ├── remixicon.css
        │   └── style.css
        │
        ├── fonts/              # Font files
        │   ├── ClashDisplay-Variable.eot
        │   ├── ClashDisplay-Variable.ttf
        │   └── remixicon/
        │       ├── remixicon.css
        │       └── remixicon.ttf
        │
        ├── images/             # Image files
        │   ├── about.jpg
        │   ├── keyboard_vr.jpg
        │   └── wave.jpg
        │
        └── js/                 # JavaScript files
                ├── aos.js
                ├── bootstrap.bundle.min.js
                └── main.js

```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.


## Acknowledgments
- [MediaPipe](https://github.com/google-ai-edge/mediapipe)
- [OpenCV](https://opencv.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)

## Contact
For any inquiries, please contact [sengame0@gmail.com] or create an issue on GitHub.

