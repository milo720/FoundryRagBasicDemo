import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
# TODO Step 2: Uncomment these imports when connecting to Azure OpenAI
# from openai import AzureOpenAI
# from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main chat interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    
    return jsonify({
        "message": "💡 Chat not configured yet! Complete Step 2 in the README to connect to Azure OpenAI.",
        "citations": [],
        "rag_enabled": False
    })


@app.route("/api/health")
def health():
    """Health check endpoint."""
    config_status = {
        "chat_configured": bool(os.getenv("AZURE_AI_ENDPOINT")),
        "rag_configured": bool(os.getenv("AZURE_SEARCH_ENDPOINT"))
    }
    return jsonify(config_status)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 Foundry RAG Chatbot - Tutorial")
    print("="*50)
    
    print("\n📋 Current Status:")
    if os.getenv("AZURE_AI_ENDPOINT"):
        print("   ✅ Chat: Configured")
    else:
        print("   ⚠️  Chat: Not configured (complete Step 2)")
    
    if os.getenv("AZURE_SEARCH_ENDPOINT"):
        print("   ✅ RAG: Configured")
    else:
        print("   ℹ️  RAG: Not configured (complete Step 3)")
    
    print("\n🚀 Starting server at http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
    
    app.run(debug=True, host="0.0.0.0", port=5000)
