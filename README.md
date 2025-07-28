# GenTale

AI-powered interactive storytelling platform where your choices create unique narratives.

## Features

- **AI-Powered Story Generation**: Create personalized stories with OpenAI's GPT-3.5-turbo
- **Interactive Choices**: Make decisions that shape your story's direction
- **Beautiful UI**: Medieval/fantasy themed interface with smooth animations
- **Story Export**: View your completed story in a beautiful book format
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Quick Start

### Prerequisites
- Python 3.7+
- Node.js and npm
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GenTale_UHv5
   ```

2. **Set up Python environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   npm install
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Build CSS**
   ```bash
   npm run build
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5001`

## How to Use

1. **Start a Story**: Enter your setting, main character, and goal
2. **Make Choices**: Select from AI-generated options to continue your tale
3. **Watch it Unfold**: See your story develop with typewriter effects
4. **Complete Your Journey**: Reach the ending and view your story in book format

## Technologies Used

Python, Flask, JavaScript, HTML/CSS, Tailwind CSS, OpenAI GPT-3.5-turbo API, Node.js, npm, Jinja2, python-dotenv, PostCSS, Autoprefixer

## Project Structure

```
GenTale_UHv5/
├── app.py                 # Flask backend application
├── prompt_utils.py        # AI prompt utilities
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
├── templates/            # HTML templates
│   ├── landing.html      # Landing page
│   ├── index.html        # Main story interface
│   └── ending.html       # Story completion page
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── Images/          # Images and icons
└── myenv/               # Python virtual environment
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
