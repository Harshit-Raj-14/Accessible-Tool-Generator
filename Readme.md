# 🛠️ Accessible Tool Generator

An AI-powered tool that transforms natural language descriptions into fully functional, accessible web applications. 

**Live Website - https://accessible-tool-generator.streamlit.app/**

## ✨ Features

### 🚀 **Core Functionality**
- **AI-Powered Generation**: Uses AI for intelligent tool creation
- **Accessibility-First Design**: All tools follow WCAG 2.1 AA compliance standards
- **Instant Preview**: See your tool working immediately in the browser
- **One-Click Download**: Get standalone HTML files ready for deployment
- **Live Tool View**: Full-screen experience for using generated tools

### 📚 **Tool History & Management**
- **Persistent History**: Keep track of all generated tools in the sidebar
- **Quick Actions**: Instantly open or download any previous tool
- **Tool Switching**: Load any historical tool into the main interface
- **History Limit**: Automatically maintains the 10 most recent tools

### ♿ **Accessibility Standards**
Every generated tool includes:
- ✅ Semantic HTML structure
- ✅ ARIA labels and roles
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ High contrast colors (4.5:1+ ratio)
- ✅ Large touch targets (44px minimum)
- ✅ Focus indicators
- ✅ Responsive design for all devices

## 🎯 Demo

![Tool Generator Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Accessible+Tool+Generator)

### Example Generated Tools:
- Voice-controlled shopping lists with screen reader support
- Large-button calculators for motor accessibility
- High-contrast timers with audio/visual alerts
- Color-blind friendly expense trackers
- Voice-activated note-taking applications

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/accessible-tool-generator.git
cd accessible-tool-generator
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Click "Create API Key"
   - Copy your API key

5. **Configure environment variables**
   - Create a `.env` file in the project root
   - Add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

6. **Run the application**
```bash
streamlit run app.py
```

7. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start generating accessible tools!

## 💡 Usage Examples

### Basic Usage
1. **Describe your tool**: "I need a voice-controlled shopping list that works with screen readers"
2. **Click Generate**: The AI creates a fully functional, accessible tool
3. **Preview instantly**: See your tool working in the browser
4. **Download or use live**: Get the HTML file or open in full-screen mode

### Advanced Features
- **Load from history**: Click any tool in the sidebar to switch to it
- **Quick actions**: Use sidebar buttons for instant tool access
- **Tool management**: Clear history when needed


## 🎯 Generated Tool Examples

### Voice-Controlled Shopping List
```
Description: "A voice-controlled shopping list that works with screen readers"
Features: Speech recognition, audio feedback, ARIA labels, keyboard shortcuts
```

### Accessible Calculator
```
Description: "A large-button calculator for people with motor difficulties"
Features: 44px+ buttons, high contrast, keyboard navigation, clear focus indicators
```

### Timer with Alerts
```
Description: "A simple timer with visual and audio alerts"
Features: Multiple alert types, high contrast display, accessible controls
```

## 📚 Dependencies

### Core Requirements
- `streamlit>=1.28.0` - Web application framework
- `google-generativeai>=0.8.0` - Google Gemini API client
- `python-dotenv>=1.0.0` - Environment variable management

### Optional Dependencies
- `pandas>=2.0.0` - Data processing
- `numpy>=1.24.0` - Numerical operations
- `requests>=2.31.0` - HTTP requests

### Development Dependencies
- `pytest>=7.4.0` - Testing framework
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Code linting


### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)



**Made with ❤️ for accessibility and inclusion**

*This tool aims to make digital accessibility easier for everyone. Every generated tool follows WCAG 2.1 AA standards to ensure usability for people with disabilities.*
