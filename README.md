# 🤖 Azure AI Foundry RAG Chatbot Tutorial

A hands-on tutorial for building a RAG (Retrieval-Augmented Generation) chatbot using Azure AI Foundry. You'll start with a basic UI and progressively add AI capabilities.

## 🎯 What You'll Learn

By the end of this tutorial, you will have:
- ✅ A working chat UI connected to Azure OpenAI
- ✅ RAG capabilities using Azure AI Search
- ✅ Understanding of how these components work together

## 📋 Prerequisites

- A GitHub account
- An Azure subscription with access to Azure OpenAI
- Basic familiarity with Python

---

## Step 1: Launch the Codespace and Explore

### 1.1 Start the Codespace

1. Click the **"Code"** button on this GitHub repository
2. Select **"Open with Codespaces"** → **"Create codespace on main"**
3. Wait for the environment to build (this takes a few minutes)

### 1.2 Explore the Project Structure

Once the Codespace is ready, take a look at the files:

```
FoundryRagBasicDemo/
├── app.py                   # Flask backend (you'll modify this!)
├── templates/
│   └── index.html           # Chat UI (already complete)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md                # This tutorial
```

### 1.3 Run the App

1. Open the terminal in VS Code
2. Run the app:
   ```bash
   python app.py
   ```
3. When the popup appears, click **"Open in Browser"** (or go to the Ports tab and click the globe icon)

### 1.4 Test the UI

You'll see a chat interface. Try sending a message - you'll get:

> 💡 Chat not configured yet! Complete Step 2 in the README to connect to Azure OpenAI.

This is expected! The UI works, but we haven't connected it to an AI model yet.

---

## Step 2: Connect to Azure OpenAI

Now let's make the chatbot actually chat!

### 2.1 Get Your Azure OpenAI Details

You'll need these from the Azure Portal:

| Item | Where to Find |
|------|---------------|
| **Endpoint URL** | Azure Portal → Your OpenAI resource → Keys and Endpoint |
| **Deployment Name** | Azure AI Foundry → Deployments (e.g., `gpt-4`, `gpt-4o`) |

### 2.2 Login to Azure

In the terminal, run:
```bash
az login --use-device-code
```

Follow the instructions to authenticate with your Azure account.

### 2.3 Update the .env File

Open `.env` and add your values:
```bash
AZURE_AI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_AI_DEPLOYMENT=gpt-4
```

### 2.4 Update app.py - Add Imports

Open `app.py` and find the TODO comment near the top. **Uncomment** these imports:

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
```

### 2.5 Update app.py - Add the Chat Logic

Find the `chat()` function with the placeholder response. **Replace** the entire function with:

```python
@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    try:
        data = request.json
        user_message = data.get("message", "")
        conversation_history = data.get("history", [])
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get Azure OpenAI client
        endpoint = os.getenv("AZURE_AI_ENDPOINT")
        if not endpoint:
            return jsonify({"error": "Azure AI endpoint not configured"}), 500
        
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-02-15-preview"
        )
        
        deployment = os.getenv("AZURE_AI_DEPLOYMENT", "gpt-4")
        
        # Build messages array
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer questions clearly and concisely."
            }
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call Azure OpenAI
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        return jsonify({
            "message": assistant_message,
            "citations": [],
            "rag_enabled": False
        })
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
```

### 2.6 Test Your Chat

1. Restart the app (press `Ctrl+C` and run `python app.py` again)
2. Refresh your browser
3. Try chatting - you should now get real AI responses! 🎉

---

## Step 3: Add RAG with Azure AI Search

Now let's add the ability to chat with your own documents!

### 3.1 Create an Azure Storage Account

1. Go to the **Azure Portal**
2. Create a new **Storage Account**
3. Once created, go to **Containers** and create a container (e.g., `documents`)
4. Upload some PDF, Word, or text files to the container

### 3.2 Create an Azure AI Search Index

1. Go to the **Azure Portal** and create an **Azure AI Search** service
2. Once created, click **"Import and vectorize data"**
3. Select **Azure Blob Storage** as your data source
4. Connect to your storage account and select your container
5. Choose your **Azure OpenAI** resource for embeddings
6. Select an embeddings model (e.g., `text-embedding-ada-002`)
7. Complete the wizard and wait for indexing to finish
8. Note the **index name** that was created

### 3.3 Get Your Search Key

1. In your **Azure AI Search** service, go to **Settings** → **Keys**
2. Copy the **Primary admin key**

### 3.4 Update .env with Search Settings

Add these lines to your `.env` file:
```bash
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your-admin-key-here
AZURE_SEARCH_INDEX=your-index-name
```

### 3.5 Update app.py - Add RAG Support

**Replace** the `chat()` function with this enhanced version that includes RAG:

```python
@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests with optional RAG."""
    try:
        data = request.json
        user_message = data.get("message", "")
        conversation_history = data.get("history", [])
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get Azure OpenAI client
        endpoint = os.getenv("AZURE_AI_ENDPOINT")
        if not endpoint:
            return jsonify({"error": "Azure AI endpoint not configured"}), 500
        
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-02-15-preview"
        )
        
        deployment = os.getenv("AZURE_AI_DEPLOYMENT", "gpt-4")
        
        # Build messages array
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer questions clearly and concisely. If you're using information from a knowledge base, mention that in your response."
            }
        ]
        
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})
        
        # Check if RAG is configured
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_KEY")
        search_index = os.getenv("AZURE_SEARCH_INDEX")
        
        extra_body = None
        rag_enabled = False
        
        if search_endpoint and search_key and search_index:
            rag_enabled = True
            extra_body = {
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_endpoint,
                            "index_name": search_index,
                            "authentication": {
                                "type": "api_key",
                                "key": search_key
                            },
                            "query_type": "simple",
                            "top_n_documents": 5
                        }
                    }
                ]
            }
        
        # Call Azure OpenAI
        if extra_body:
            response = client.chat.completions.create(
                model=deployment,
                messages=messages,
                extra_body=extra_body,
                max_tokens=1000,
                temperature=0.7
            )
        else:
            response = client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
        
        assistant_message = response.choices[0].message.content
        
        # Extract citations if available
        citations = []
        if hasattr(response.choices[0].message, 'context') and response.choices[0].message.context:
            context = response.choices[0].message.context
            if 'citations' in context:
                citations = context['citations']
        
        return jsonify({
            "message": assistant_message,
            "citations": citations,
            "rag_enabled": rag_enabled
        })
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
```

### 3.6 Test RAG

1. Restart the app
2. Ask questions about the content in your uploaded documents
3. You should see a **"📚 Using knowledge base"** badge on responses!

---

## 🎉 Congratulations!

You've built a RAG chatbot! Here's what you accomplished:

1. ✅ Set up a development environment with Codespaces
2. ✅ Connected a web UI to Azure OpenAI
3. ✅ Added RAG capabilities with Azure AI Search

## 🚀 Next Steps

Try these enhancements:

- **Customize the system prompt** to give your bot a personality
- **Modify the UI** in `templates/index.html`
- **Try different models** by changing the deployment
- **Experiment with search settings** like `query_type: "semantic"`

## ❓ Troubleshooting

### "Chat not configured" message persists
- Make sure you uncommented the imports in `app.py`
- Verify `.env` has the correct `AZURE_AI_ENDPOINT` value

### Authentication errors
- Run `az login --use-device-code` again
- Ensure you have the **"Cognitive Services OpenAI User"** role on the Azure OpenAI resource

### "Model not found"
- Check that `AZURE_AI_DEPLOYMENT` matches your deployment name exactly

### RAG not working
- Verify all three search variables are set in `.env`
- Make sure your search index has documents in it

## 📚 Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Flask Documentation](https://flask.palletsprojects.com/)
