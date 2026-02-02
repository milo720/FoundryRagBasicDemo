# 🤖 Azure AI Foundry RAG Chatbot Lab

A simple, hands-on lab for building a RAG (Retrieval-Augmented Generation) chatbot using Azure AI Foundry.

![Chatbot Screenshot](docs/screenshot.png)

## 🎯 What You'll Build

A web-based chatbot that:
- Connects to Azure AI Foundry (Azure OpenAI)
- Optionally uses Azure AI Search for RAG capabilities
- Runs locally in your browser
- Maintains conversation history

## 🚀 Quick Start

### Option 1: GitHub Codespaces (Recommended)

1. Click the **"Code"** button on GitHub
2. Select **"Open with Codespaces"**
3. Wait for the environment to build
4. Copy `.env.example` to `.env` and fill in your credentials
5. Run `python app.py`
6. Open the forwarded port in your browser

### Option 2: Local Development

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/FoundryRagBasicDemo.git
   cd FoundryRagBasicDemo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` with your Azure credentials (see Configuration section below)

6. Run the application:
   ```bash
   python app.py
   ```

7. Open http://localhost:5000 in your browser

## ⚙️ Configuration

### Required Settings

Edit your `.env` file with these values:

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `AZURE_AI_ENDPOINT` | Your Azure OpenAI endpoint URL | Azure Portal → Azure OpenAI → Keys and Endpoint |
| `AZURE_AI_API_KEY` | Your Azure OpenAI API key | Azure Portal → Azure OpenAI → Keys and Endpoint |
| `AZURE_AI_DEPLOYMENT` | Name of your deployed model | Azure AI Studio → Deployments |

### Optional: RAG with Azure AI Search

For RAG capabilities, also configure:

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `AZURE_SEARCH_ENDPOINT` | Your Azure AI Search endpoint | Azure Portal → Azure AI Search → Overview |
| `AZURE_SEARCH_KEY` | Your Azure AI Search admin key | Azure Portal → Azure AI Search → Keys |
| `AZURE_SEARCH_INDEX` | Name of your search index | Azure Portal → Azure AI Search → Indexes |

## 📁 Project Structure

```
FoundryRagBasicDemo/
├── .devcontainer/
│   └── devcontainer.json    # Codespaces configuration
├── templates/
│   └── index.html           # Chat web interface
├── .env.example             # Environment template
├── .gitignore
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 How It Works

1. **Frontend** (`templates/index.html`): A simple HTML/CSS/JavaScript chat interface
2. **Backend** (`app.py`): Flask server that handles API requests
3. **Azure AI**: Processes messages using Azure OpenAI
4. **Azure AI Search** (optional): Provides RAG capabilities by searching your knowledge base

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌────────────────────┐
│   Browser   │────▶│ Flask App   │────▶│ Azure OpenAI       │
│  (Chat UI)  │◀────│ (Python)    │◀────│ (Chat Completion)  │
└─────────────┘     └─────────────┘     └────────────────────┘
                           │                      ▲
                           │                      │
                           ▼                      │
                    ┌─────────────┐               │
                    │ Azure AI    │───────────────┘
                    │ Search      │  (RAG - retrieves context)
                    └─────────────┘
```

## 🧪 Lab Exercises

### Exercise 1: Basic Chat
1. Configure your `.env` with Azure OpenAI credentials
2. Start the server and chat with the AI
3. Try different types of questions

### Exercise 2: Enable RAG
1. Create an Azure AI Search resource
2. Upload documents and create an index
3. Configure the RAG settings in `.env`
4. Notice the "Using knowledge base" badge in responses

### Exercise 3: Customize the Bot
1. Modify the system prompt in `app.py`
2. Change the UI styling in `templates/index.html`
3. Add new features like conversation export

## ❓ Troubleshooting

### "Missing AZURE_AI_ENDPOINT or AZURE_AI_API_KEY"
- Make sure you copied `.env.example` to `.env`
- Verify your credentials are correct in the `.env` file

### "Model not found"
- Check that `AZURE_AI_DEPLOYMENT` matches your deployment name exactly
- Ensure the model is deployed in Azure AI Studio

### Connection errors
- Verify your Azure OpenAI resource is active
- Check if your IP is allowed in the Azure networking settings

## 📚 Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## 📄 License

MIT License - Feel free to use this for learning and building!
