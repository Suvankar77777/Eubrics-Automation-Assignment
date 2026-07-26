# Lead Profiling Workflow

## Objective

Automatically process website visitor leads without manual work.

## Workflow

Webhook

↓

Edit Fields

↓

Basic LLM Chain (Gemma3)

↓

Google Sheets

↓

Gmail

↓

Respond to Webhook

## Features

- Receives visitor information
- Simulates browsing history
- Uses an LLM to classify leads
- Stores results in Google Sheets
- Sends an email notification
- Returns a success response through the webhook

## AI Prompt

The LLM analyses:

- Name
- Email
- Visitor Message
- Browsing History

and classifies each lead into:

- Sales Bots
- Organizational Development

## Example Request

```bash
curl -X POST http://localhost:5678/webhook-test/lead-profile ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"message\":\"I want to purchase a sales bot for my website.\",\"history\":\"home,pricing,demo\"}"
```

Example Response

```json
{
  "status":"success",
  "message":"Lead processed successfully.",
  "category":"Sales Bots"
}
```

## Technologies

- n8n
- Ollama
- Gemma 3
- Google Sheets
- Gmail

## Setup

1. Install Ollama
2. Pull Gemma 3
3. Install n8n
4. Import workflow.json
5. Configure Google Sheets credentials
6. Configure Gmail credentials
7. Execute the workflow
