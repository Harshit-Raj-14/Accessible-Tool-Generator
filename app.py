import streamlit as st
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Accessible Tool Generator", 
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic UI
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        /* Card styling */
        .example-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: none;
            width: 100%;
            text-align: left;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .example-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        /* Override Streamlit button styling for examples */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            width: 100%;
            margin: 0.25rem 0;
        }
        
        .stButton > button[kind="secondary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
        }
        
        .stButton > button[kind="secondary"]:focus {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            box-shadow: 0 0 10px rgba(240, 147, 251, 0.5);
        }
        
        .tool-preview-container {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        .instructions-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        /* Button styling */
        .action-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            margin: 0.5rem 0;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        
        .download-button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        
        .live-button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            width: 100%;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        
        .stDownloadButton > button:focus {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            box-shadow: 0 0 10px rgba(17, 153, 142, 0.5);
        }
        
        /* Input styling */
        .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }
        
        /* Success message styling */
        .success-message {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
            font-weight: 600;
        }
        
        /* Features grid */
        .features-grid {
            background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
        }
        
        .feature-item {
            background: white;
            padding: 0.5rem;
            border-radius: 8px;
            margin: 0.25rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 0.9rem;
        }
        
        /* Loading animation */
        .loading-container {
            text-align: center;
            padding: 2rem;
        }
        
        .loading-spinner {
            animation: spin 2s linear infinite;
            font-size: 2rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Back button styling */
        .back-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        
        /* Live tool full screen */
        .live-tool-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 15px;
            margin: 1rem 0;
        }
        
        /* Sidebar styling */
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .history-item {
            background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
            padding: 0.75rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
        }
        
        .history-title {
            font-weight: 600;
            color: #333;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .history-description {
            color: #666;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }
        
        .sidebar-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.8rem;
            margin: 0.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .sidebar-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .empty-history {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 2rem 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize Gemini API
@st.cache_resource
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in environment variables")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_accessible_tool(description: str, model) -> Dict[str, Any]:
    """Generate accessible HTML/CSS/JS code based on natural language description"""
    
    prompt = f"""
    Create a fully functional, accessible web tool based on this description: "{description}"

    Requirements:
    1. Generate complete HTML, CSS, and JavaScript in a single HTML file
    2. Make it fully accessible (WCAG 2.1 AA compliant):
       - Proper ARIA labels and roles
       - Keyboard navigation support
       - Screen reader compatibility
       - High contrast colors
       - Large touch targets (44px minimum)
    3. Include voice control if requested using Web Speech API
    4. Make it responsive and mobile-friendly
    5. Use semantic HTML elements
    6. Add clear focus indicators
    7. Include skip links if needed
    8. Ensure color contrast ratio > 4.5:1

    Return ONLY the complete HTML code with embedded CSS and JavaScript.
    Do not include any explanations or markdown formatting.
    Start directly with <!DOCTYPE html>
    """
    
    try:
        response = model.generate_content(prompt)
        return {
            "success": True,
            "code": response.text.strip(),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "code": None,
            "error": str(e)
        }

def generate_tool_instructions(description: str, model) -> str:
    """Generate instructions and features for the tool"""
    
    prompt = f"""
    Based on this accessible tool description: "{description}"
    
    Generate a brief, user-friendly guide that includes:
    1. How to use this tool (2-3 sentences)
    2. Key accessibility features included (3-4 bullet points)
    3. Tips for best experience (1-2 tips)
    
    Keep it concise and helpful. Use simple language.
    Format as plain text, no markdown.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "This tool has been designed with accessibility in mind, including keyboard navigation, screen reader support, and high contrast design for the best user experience."

def extract_and_clean_html(code_text: str) -> str:
    """Extract and clean HTML code from the response"""
    # Remove markdown code blocks if present
    code_text = re.sub(r'```html\n?', '', code_text)
    code_text = re.sub(r'```\n?', '', code_text)
    
    # Ensure it starts with DOCTYPE
    if not code_text.strip().startswith('<!DOCTYPE'):
        code_text = '<!DOCTYPE html>\n' + code_text
    
    return code_text.strip()

def show_sidebar():
    """Display the sidebar with tool history and quick actions"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            📚 Tool History
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.tool_history:
            st.markdown("""
            <div class="empty-history">
                🔧 No tools generated yet.<br>
                Create your first accessible tool!
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, tool_data in enumerate(reversed(st.session_state.tool_history)):
                actual_index = len(st.session_state.tool_history) - 1 - i
                
                # Create tool card
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-title">🛠️ Tool #{actual_index + 1}</div>
                    <div class="history-description">{tool_data['description'][:80]}{'...' if len(tool_data['description']) > 80 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔗 Open", key=f"open_{actual_index}", help="Open this tool"):
                        load_tool_from_history(actual_index)
                        st.query_params.tool = "live"
                        st.rerun()
                
                with col2:
                    st.download_button(
                        label="📥 Download",
                        data=tool_data['html'],
                        file_name=f"tool_{actual_index + 1}.html",
                        mime="text/html",
                        key=f"download_history_{actual_index}",
                        help="Download this tool's HTML"
                    )
                
                st.markdown("---")
        
        # Clear history button
        if st.session_state.tool_history:
            if st.button("🗑️ Clear History", use_container_width=True, help="Clear all tool history"):
                st.session_state.tool_history = []
                st.session_state.current_tool_index = -1
                st.rerun()

def load_tool_from_history(index):
    """Load a tool from history into the current session"""
    if 0 <= index < len(st.session_state.tool_history):
        tool_data = st.session_state.tool_history[index]
        st.session_state.generated_html = tool_data['html']
        st.session_state.tool_description = tool_data['description']
        st.session_state.tool_instructions = tool_data['instructions']
        st.session_state.has_generated_tool = True
        st.session_state.current_tool_index = index

def add_tool_to_history(html, description, instructions):
    """Add a new tool to the history"""
    tool_data = {
        'html': html,
        'description': description,
        'instructions': instructions,
        'timestamp': st.session_state.get('timestamp', 'Unknown')
    }
    
    # Add to beginning of history (most recent first)
    st.session_state.tool_history.append(tool_data)
    st.session_state.current_tool_index = len(st.session_state.tool_history) - 1
    
    # Limit history to 10 tools to prevent memory issues
    if len(st.session_state.tool_history) > 10:
        st.session_state.tool_history = st.session_state.tool_history[-10:]
        st.session_state.current_tool_index = len(st.session_state.tool_history) - 1

# Main app
def main():
    apply_custom_css()
    
    # Initialize session state
    if 'generated_html' not in st.session_state:
        st.session_state.generated_html = None
    if 'tool_description' not in st.session_state:
        st.session_state.tool_description = ""
    if 'tool_instructions' not in st.session_state:
        st.session_state.tool_instructions = ""
    if 'description' not in st.session_state:
        st.session_state.description = ""
    if 'selected_description' not in st.session_state:
        st.session_state.selected_description = ""
    if 'has_generated_tool' not in st.session_state:
        st.session_state.has_generated_tool = False
    if 'tool_history' not in st.session_state:
        st.session_state.tool_history = []
    if 'current_tool_index' not in st.session_state:
        st.session_state.current_tool_index = -1
    
    # Check if we're in live tool mode
    query_params = st.query_params
    
    if "tool" in query_params and query_params["tool"] == "live":
        show_live_tool()
        return
    
    # Show sidebar with tool history
    show_sidebar()
    
    # Regular app interface
    show_main_interface()

def show_live_tool():
    """Display only the generated tool in full screen"""
    if st.session_state.generated_html is None:
        st.markdown("""
        <div class="main-header">
            <h1 class="main-title">⚠️ No Tool Generated</h1>
            <p class="main-subtitle">Please go back and generate a tool first</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Generator", key="back_from_error"):
            st.query_params.clear()
            st.rerun()
        return
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Generator", key="back_to_main"):
            st.query_params.clear()
            st.rerun()
    
    with col2:
        st.markdown(f"### 🎯 Live Tool: {st.session_state.tool_description[:50]}...")
    
    # Display the tool in full screen with custom styling
    st.markdown('<div class="live-tool-container">', unsafe_allow_html=True)
    st.components.v1.html(
        st.session_state.generated_html,
        height=800,
        scrolling=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

def show_main_interface():
    """Display the main tool generator interface"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛠️ Accessible Tool Generator</h1>
        <p class="main-subtitle">Transform your ideas into accessible digital tools instantly!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Gemini model
    model = init_gemini()
    
    # Example descriptions with custom styling
    st.markdown("### 💡 Try These Ideas:")
    examples = [
        "A voice-controlled shopping list that works with screen readers",
        "A large-button calculator for people with motor difficulties", 
        "A high-contrast daily planner with keyboard shortcuts",
        "A simple timer with visual and audio alerts",
        "A color-blind friendly expense tracker",
        "A voice-activated note-taking app"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            # Use Streamlit button with custom styling
            if st.button(
                f"💡 {example}", 
                key=f"example_{i}", 
                help=f"Click to use: {example}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.selected_description = example
                st.rerun()

    # Main input
    st.markdown("### 📝 Describe Your Tool:")
    
    # Use selected description if available, then clear it
    current_value = ""
    if st.session_state.selected_description:
        current_value = st.session_state.selected_description
        st.session_state.selected_description = ""  # Clear after using
    else:
        current_value = st.session_state.get('description', '')
    
    description = st.text_area(
        "What accessibility tool do you need?",
        value=current_value,
        height=120,
        placeholder="Example: I need a voice-controlled shopping list that announces items when I add them...",
        key="description_input"
    )
    
    # Update session state with current description
    st.session_state.description = description
    
    # Generate button with custom styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Accessible Tool", type="primary", use_container_width=True, disabled=not description):
            generate_tool(description, model)
    
    # Show existing generated tool if available
    if st.session_state.has_generated_tool and st.session_state.generated_html:
        show_generated_tool()

def generate_tool(description: str, model):
    """Generate the tool and handle the result"""
    with st.spinner("🔧 Creating your accessible tool..."):
        # Show loading animation
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner">🛠️</div>
            <p>Generating your accessible tool...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate both the tool and instructions
        result = generate_accessible_tool(description, model)
        
        if result["success"]:
            # Store in session state with explicit persistence
            clean_code = extract_and_clean_html(result["code"])
            st.session_state.generated_html = clean_code
            st.session_state.tool_description = description
            
            # Generate instructions
            instructions = generate_tool_instructions(description, model)
            st.session_state.tool_instructions = instructions
            
            # Mark that we have generated content
            st.session_state.has_generated_tool = True
            
            # Add to history
            add_tool_to_history(clean_code, description, instructions)
            
            # Clear the loading and show success message only
            st.success("✅ Tool generated successfully!")
            # Rerun to update the interface with the new tool
            st.rerun()
            
        else:
            handle_generation_error(result["error"])

def show_generated_tool():
    """Display the generated tool with all UI elements"""
    
    # Success message
    st.markdown("""
    <div class="success-message">
        ✅ Your accessible tool has been generated successfully!
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns: tool and instructions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="tool-preview-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Your Accessible Tool:")
        
        # Render the generated tool
        try:
            st.components.v1.html(
                st.session_state.generated_html,
                height=600,
                scrolling=True
            )
        except Exception as e:
            st.error(f"Error rendering tool: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="instructions-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 How to Use:")
        st.info(st.session_state.tool_instructions)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("#### 🚀 Actions:")
        
        # Live tool button - same tab only
        if st.button("🔗 Open Live Tool", use_container_width=True, type="secondary", key="live_same_tab"):
            st.query_params.tool = "live"
            st.rerun()
        
        # Download button with session state preservation
        if st.session_state.generated_html:
            st.download_button(
                label="📥 Download HTML File",
                data=st.session_state.generated_html,
                file_name="accessible_tool.html",
                mime="text/html",
                use_container_width=True,
                key=f"download_button_{hash(st.session_state.generated_html[:100])}"  # Unique key to prevent conflicts
            )
        
        # Add option to clear and start over
        st.markdown("---")
        if st.button("🔄 Generate New Tool", use_container_width=True, help="Clear current tool and start fresh"):
            # Clear session state for new generation (but keep history)
            st.session_state.generated_html = None
            st.session_state.tool_description = ""
            st.session_state.tool_instructions = ""
            st.session_state.has_generated_tool = False
            st.session_state.description = ""
            st.session_state.current_tool_index = -1
            st.rerun()
    
    # Accessibility features
    show_accessibility_features()

def show_accessibility_features():
    """Display accessibility features in a nice grid"""
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    st.markdown("### ♿ Accessibility Features Included:")
    
    accessibility_features = [
        "✅ Semantic HTML structure",
        "✅ ARIA labels and roles",
        "✅ Keyboard navigation support", 
        "✅ High contrast colors",
        "✅ Large touch targets (44px+)",
        "✅ Screen reader compatibility",
        "✅ Focus indicators",
        "✅ Responsive design"
    ]
    
    feature_cols = st.columns(4)
    for i, feature in enumerate(accessibility_features):
        with feature_cols[i % 4]:
            st.markdown(f'<div class="feature-item">{feature}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_generation_error(error):
    """Handle and display generation errors"""
    st.error(f"❌ Error generating tool: {error}")
    
    error_messages = {
        "404": "❌ Model not available. Check your API access.",
        "403": "❌ API key invalid or insufficient permissions", 
        "quota": "❌ API quota exceeded. Try again later or upgrade your plan",
        "limit": "❌ API quota exceeded. Try again later or upgrade your plan"
    }
    
    error_str = str(error).lower()
    for key, message in error_messages.items():
        if key in error_str:
            st.markdown(f"**Troubleshooting:** {message}")
            return
    
    st.markdown("**Troubleshooting:**")
    st.markdown("- Check your .env file has the correct GEMINI_API_KEY")
    st.markdown("- Try a simpler description")
    st.markdown("- Ensure you have internet connectivity")

if __name__ == "__main__":
    main()