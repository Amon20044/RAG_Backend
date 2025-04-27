# 🧠 RAG-BOT: Multi-PDF Knowledge Chatbot by Amon

> **Built With**: FastAPI ⚡ | LangChain 🧠 | React.js ⚛️ | Datastax Astra DB 🚀 | Supabase PostgreSQL 🗃️ | Meta-Llama 4 Maverick 17B Model 🦙 | Together AI

---

## 📚 Overview

RAG-BOT is an advanced **Retrieval Augmented Generation (RAG)** chatbot that allows users to upload **multiple PDFs**, **ask complex questions**, and receive **smart, contextual answers**.

It is **full-stack**, **scalable**, **vector-database driven**, and **ready for production**!

---

## 🛠 Tech Stack

| Layer | Technology |
|:---|:---|
| Backend | FastAPI (Python) |
| NLP Engine | LangChain |
| Model | Meta-Llama 4 Maverick 17B 128E FP8 |
| Vector Storage | Datastax Astra DB |
| SQL Storage | Supabase PostgreSQL |
| Frontend | Next.js (React + TypeScript) |
| Temp Storage | Local Server Filesystem (for processing uploads) |

---

## ⚡️ Features

- ✅ Upload **multiple** PDFs.
- ✅ Intelligent document **chunking and embedding**.
- ✅ Context-aware **question understanding** (structured parsing).
- ✅ **Section-based** retrieval: beginning, middle, end.
- ✅ **Contextual Prompt Engineering** (custom RAG prompt).
- ✅ Built-in **JWT Authentication** (Coming Soon 🔒).
- ✅ **Dockerized** and **CI/CD ready**.
- ✅ Ultra-lightweight API for **easy frontend integration**.

---

## 📂 Project Structure

```
/server
│
├── app/
│   ├── classes/        # Pydantic data classes (Question, Answer)
│   ├── db/             # Database connections (Supabase, AstraDB)
│   ├── langchain/
│   │   ├── initialize/ # Model, Embedding, Vector store initialization
│   │   └── chatFlow.py # Core RAG business logic
│   ├── routes/
│   │   └── chatRoute.py # API Endpoints
│   └── main.py          # FastAPI entrypoint
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🌐 API Endpoints

### POST `/chat/{id}`

#### ➡️ Description:
Upload one or multiple PDFs and ask a natural language question.  
The system will parse, chunk, embed the documents, search for context, and answer.

#### 🛎️ Request:
- **Path Parameter**: `id` → Random chatId for session.
- **Body (multipart/form-data)**:
  | Field | Type | Description |
  |:---|:---|:---|
  | files | List of UploadFile (PDFs) | Required |
  | question | String | Required |

#### 🧩 Example cURL:
```bash
curl -X POST "http://127.0.0.1:8080/chat/123456" \
  -H "accept: application/json" \
  -F "question=What are the key findings of this report?" \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.pdf"
```

#### 🛎️ Response:
```json
{
  "question": "What are the key findings of this report?",
  "answer": "The key findings highlight the major contributions made by the project, divided across its beginning, middle, and concluding sections. Thanks for asking!"
}
```

---

## 🛡 Environment Variables

Create a `.env` file in `/server`:

```env
# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:password@host:port/postgres
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# Datastax Astra VectorDB
ASTRA_NAMESPACE=default_keyspace
ASTRA_TOKEN=your-astra-token
ASTRA_ENDPOINT=https://your-region.apps.astra.datastax.com

# LangSmith (Optional for Observability)
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=your-project

# Together AI / NVIDIA API Keys (optional future upgrades)
TOGETHER_API_KEY=your-together-ai-key
NVIDIA_API_KEY=your-nvidia-api-key
```

---

## 🛠 Setup (Local)

1. Clone the repo
```bash
git clone https://github.com/Amon20044/RAG_Backend.git
cd RAG_Backend/server
```

2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Requirements
```bash
pip install -r requirements.txt
```

4. Start Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Open browser:  
👉 http://127.0.0.1:8080/docs (Swagger UI auto-generated)

---

## 🐳 Docker Deployment

```bash
docker build -t rag-bot .
docker run -d -p 8080:8080 --name rag-bot-container rag-bot
```

Server will be running at:  
👉 `http://127.0.0.1:8080`

---

## 🧠 Flow Diagram (System Architecture)

```plaintext
[Frontend (React.js)]
        ↓
  [FastAPI Server (Backend)]
        ↓
 [File Upload (Temp Storage)]
        ↓
 [Chunk & Embed (LangChain)]
        ↓
 [Vector DB (Astra DB)]
        ↓
 [Meta Llama 4 (Inference)]
        ↓
  [Return Answer to User]
```
![diagram-export-4-27-2025-6_17_11-AM](https://github.com/user-attachments/assets/bdbf28a6-b572-4a3f-bd85-77178a0d3a7c)


---

## 🚀 Future Work (Roadmap)

- [x] JWT Authentication Middleware for Protected Routes
- [x] Frontend: React.js + Tailwind UI Integration
- [x] Supabase PostgreSQL for storing metadata (user, chat history)
- [ ] Deploy on Railway or AWS EC2
- [ ] Multiple Model Switching (e.g., GPT-4, Claude, Llama)

---

## 🤝 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Datastax Astra](https://www.datastax.com/astra)
- [Supabase](https://supabase.com/)
- [Meta AI (Llama-4 Maverick)](https://ai.meta.com/)

---

## ✨ Built with ❤️ by [Amon Sharma](https://github.com/Amon20044)

> *"Learning every day. Building future today."* 🚀

---

# 🚀 **[Star 🌟 this Repo if you loved the project!]**
