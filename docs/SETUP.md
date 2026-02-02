# 🚀 Quick Setup Guide

Follow these steps to get your chatbot running!

## Step 1: Get Your Azure Credentials

### Azure OpenAI (Required)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your **Azure OpenAI** resource
3. Click **Keys and Endpoint** in the left menu
4. Copy:
   - **Endpoint** → paste into `AZURE_AI_ENDPOINT`
   - **KEY 1** → paste into `AZURE_AI_API_KEY`

5. Go to [Azure AI Studio](https://ai.azure.com)
6. Find your **Deployment name** → paste into `AZURE_AI_DEPLOYMENT`

### Azure AI Search (Optional - for RAG)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your **Azure AI Search** resource
3. From **Overview**, copy the **URL** → paste into `AZURE_SEARCH_ENDPOINT`
4. From **Keys**, copy an **Admin key** → paste into `AZURE_SEARCH_KEY`
5. From **Indexes**, copy your **Index name** → paste into `AZURE_SEARCH_INDEX`

## Step 2: Configure Your Environment

1. Open the `.env` file (or copy from `.env.example`)
2. Fill in your values:

```
AZURE_AI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_AI_API_KEY=your-key-here
AZURE_AI_DEPLOYMENT=gpt-4

# Optional for RAG:
AZURE_SEARCH_ENDPOINT=https://YOUR-SEARCH.search.windows.net
AZURE_SEARCH_KEY=your-search-key
AZURE_SEARCH_INDEX=your-index-name
```

## Step 3: Run the App

```bash
python app.py
```

## Step 4: Open Your Browser

Navigate to: **http://localhost:5000**

🎉 Start chatting!

---

## Common Issues

| Problem | Solution |
|---------|----------|
| "Missing credentials" | Check your `.env` file exists and has correct values |
| "Model not found" | Verify deployment name matches exactly in Azure AI Studio |
| Connection timeout | Check Azure firewall settings allow your IP |
| Port 5000 in use | Stop other services or change port in `app.py` |
