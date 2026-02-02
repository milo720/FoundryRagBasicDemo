import os
from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Azure OpenAI client
client = None

def get_client():
    """Get or create Azure OpenAI client using Azure Identity (az login)."""
    global client
    if client is None:
        endpoint = os.getenv("AZURE_AI_ENDPOINT")
        
        if not endpoint:
            raise ValueError("Missing AZURE_AI_ENDPOINT in environment variables")
        
        # Use DefaultAzureCredential - requires 'az login' first
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-02-15-preview"
        )
    return client

def get_search_config():
    """Get Azure AI Search configuration if available."""
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key = os.getenv("AZURE_SEARCH_KEY")
    search_index = os.getenv("AZURE_SEARCH_INDEX")
    
    if search_endpoint and search_key and search_index:
        return {
            "endpoint": search_endpoint,
            "key": search_key,
            "index": search_index
        }
    return None

@app.route("/")
def index():
    """Serve the main chat interface."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    try:
        data = request.json
        user_message = data.get("message", "")
        conversation_history = data.get("history", [])
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        openai_client = get_client()
        deployment = os.getenv("AZURE_AI_DEPLOYMENT", "gpt-4")
        
        # Build messages array
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer questions clearly and concisely. If you're using information from a knowledge base, mention that in your response."
            }
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Check if RAG is configured
        search_config = get_search_config()
        extra_body = None
        
        if search_config:
            # Use Azure AI Search for RAG
            extra_body = {
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_config["endpoint"],
                            "key": search_config["key"],
                            "index_name": search_config["index"],
                            "query_type": "semantic",
                            "semantic_configuration": "default",
                            "top_n_documents": 5
                        }
                    }
                ]
            }
        
        # Call Azure OpenAI
        if extra_body:
            response = openai_client.chat.completions.create(
                model=deployment,
                messages=messages,
                extra_body=extra_body,
                max_tokens=1000,
                temperature=0.7
            )
        else:
            response = openai_client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
        
        assistant_message = response.choices[0].message.content
        
        # Extract citations if available (for RAG responses)
        citations = []
        if hasattr(response.choices[0].message, 'context') and response.choices[0].message.context:
            context = response.choices[0].message.context
            if 'citations' in context:
                citations = context['citations']
        
        return jsonify({
            "message": assistant_message,
            "citations": citations,
            "rag_enabled": search_config is not None
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/health")
def health():
    """Health check endpoint."""
    config_status = {
        "azure_ai_configured": bool(os.getenv("AZURE_AI_ENDPOINT") and os.getenv("AZURE_AI_API_KEY")),
        "rag_configured": bool(get_search_config())
    }
    return jsonify(config_status)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 Foundry RAG Chatbot")
    print("="*50)
    print("\n📋 Checking configuration...")
    
    if os.getenv("AZURE_AI_ENDPOINT") and os.getenv("AZURE_AI_API_KEY"):
        print("✅ Azure AI endpoint configured")
    else:
        print("⚠️  Azure AI endpoint NOT configured - please update .env file")
    
    if get_search_config():
        print("✅ Azure AI Search (RAG) configured")
    else:
        print("ℹ️  Azure AI Search (RAG) not configured - running without RAG")
    
    print("\n🚀 Starting server at http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
