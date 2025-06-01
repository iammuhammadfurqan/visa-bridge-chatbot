# VisaBridge AI Assistant 🤖

VisaBridge AI is an intelligent chatbot designed to help users navigate complex visa and immigration processes. Built with LangChain and OpenAI, it provides accurate, context-aware responses about visa requirements, application procedures, and immigration guidance for over 20 countries.

## Features 🌟

- **Intelligent Responses**: Powered by GPT-4 for accurate and context-aware answers
- **Multi-Country Support**: Information about visa processes for 20+ countries
- **Multilingual Support**: Understands and responds to queries in both English and Urdu (اردو)
- **Document Guidance**: Help with required documentation and preparation
- **Conversation Memory**: Maintains context across the entire conversation
- **Modern Interface**: Clean, user-friendly Streamlit web interface
- **Performance Tracking**: Built-in evaluation and metrics tracking

## Prerequisites 📋

- Python 3.8 or higher
- OpenAI API key
- pip (Python package installer)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/iammuhammadfurqan/visabridge-chatbot.git
cd visabridge-chatbot
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Project Structure 📁

```
visabridge-ai/
├── app.py                 # Streamlit web interface
├── chatbot.py            # Core chatbot implementation
├── config.py             # Configuration settings
├── evaluation.py         # Evaluation and metrics tracking
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (not tracked)
├── .gitignore           # Git ignore rules
├── data/                # Knowledge base documents
│   ├── about.txt
│   ├── features.txt
│   └── faq.txt
└── README.md            # This file
```

## Usage 💻

1. Start the Streamlit interface:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Start chatting with the AI assistant about visa and immigration questions

## Available Commands 🎮

- Type your question to get started
- Use the "Clear Conversation" button to start a new chat
- Click "Show Summary" to view conversation metrics
- Type 'help' for available commands

## Features in Detail 🔍

### Knowledge Base
- Comprehensive information about visa processes
- Document requirements and checklists
- Application procedures and timelines
- Country-specific guidance

### Interface
- Modern, responsive design
- Real-time chat experience
- Conversation history
- Performance metrics
- Error handling and logging

### Technical Features
- LangChain integration for enhanced capabilities
- FAISS vector store for efficient document retrieval
- Conversation memory for context awareness
- Performance evaluation and logging
- Secure API key handling

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security 🔒

- API keys are stored in environment variables
- No sensitive data is logged or stored
- Regular security updates and dependency checks

## Logging and Monitoring 📊

The application includes comprehensive logging:
- Conversation history
- Response times
- Error tracking
- Performance metrics

Logs are stored in `chatbot.log` and metrics in `evaluation_metrics.json`

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments 🙏

- OpenAI for the GPT models
- LangChain for the framework
- Streamlit for the web interface
- FAISS for vector storage

## Support 💬

For support, please:
1. Check the FAQ in the application
2. Open an issue in the repository
3. Contact the development team

## Roadmap 🗺️

- [ ] Add support for more countries
- [ ] Implement document upload and analysis
- [ ] Add multilingual support with Urdu
- [ ] Enhance conversation memory
- [ ] Add user authentication
- [ ] Implement API endpoints
- [ ] Expand language support to include more languages

---

Made with ❤️ by Muhammad Furqan for VisaBridge Team 
