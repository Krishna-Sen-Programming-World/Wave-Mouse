# Wave Mouse
Here's a structured `README.md` file for your GitHub project. Feel free to modify any sections to better match your project's details and style!


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
   git clone https://github.com/yourusername/your-repo-name.git
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

- **Keyboard Shortcuts**:
  - Gesture for Copy (Ctrl + C).
  - Gesture for Paste (Ctrl + V).
  - Add more shortcuts as needed.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [MediaPipe](https://google.github.io/mediapipe/)
- [OpenCV](https://opencv.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)

## Contact
For any inquiries, please contact [your email address] or create an issue on GitHub.
```

Make sure to replace placeholders like `yourusername`, `your-repo-name`, and `your email address` with the appropriate values. This `README.md` provides a clear overview of your project and guides users through installation and usage effectively!
