# Agentic AI Platform

An enterprise-ready, production-quality Agentic AI platform built with Python, FastAPI, and LangGraph.

## Overview

This platform enables the creation and orchestration of intelligent agents capable of:

- **Conversational Interaction**: Natural multi-turn conversations with memory
- **Multi-Agent Orchestration**: Coordinate multiple agents working together
- **Tool Integration**: Extensible tool calling framework with built-in tools
- **Reasoning & Planning**: Complex reasoning with LangGraph workflows
- **Memory Management**: Short-term and long-term memory systems
- **RAG Support**: Retrieve Augmented Generation with vector stores
- **Task Execution**: Autonomous task execution with human oversight
- **Enterprise Features**: Security, observability, compliance, and scalability

## Technology Stack

### Backend
- **Python 3.12+**
- **FastAPI**: High-performance REST API
- **Pydantic**: Data validation and serialization
- **LangGraph**: Agent orchestration and workflows
- **SQLAlchemy**: Database ORM
- **Alembic**: Database migrations

### Data & Storage
- **PostgreSQL**: Primary data store
- **Redis**: Caching and session management
- **Qdrant**: Vector database for embeddings/RAG

### LLM & AI
- **LangChain**: LLM integration (where appropriate)
- **OpenAI-compatible APIs**: Primary LLM provider
- **AWS Bedrock**: Alternative LLM provider
- **Ollama**: Local model support (optional)

### Frontend
- **Streamlit**: Initial UI (easily replaced with React)
- **WebSocket**: Real-time agent interactions

### Testing & Quality
- **pytest**: Unit and integration testing
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting

### Deployment & DevOps
- **Docker**: Container images
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipelines
- **AWS**: Production deployment target

### Observability
- **Python logging**: Structured logging
- **OpenTelemetry**: Distributed tracing (optional)
- **Prometheus**: Metrics (optional)

## Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL (or use Docker Compose)
- Redis (or use Docker Compose)
- Qdrant (or use Docker Compose)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/tulubenti/usetai-agentic-ai.git
   cd usetai-agentic-ai
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**
   ```bash
   pip install -e .
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the API server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Start the Streamlit UI** (in another terminal)
   ```bash
   streamlit run frontend/app.py
   ```

### Access Points
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Qdrant**: http://localhost:6333

## Project Structure

```
agentic-ai-platform/
├── app/                          # FastAPI application
│   ├── main.py                   # Application entry point
│   ├── config.py                 # Configuration management
│   ├── dependencies.py           # Dependency injection
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   ├── conversations.py      # Conversation endpoints
│   │   ├── agents.py             # Agent management endpoints
│   │   ├── tools.py              # Tool management endpoints
│   │   ├── memory.py             # Memory endpoints
│   │   └── health.py             # Health check endpoints
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── agent.py              # Agent orchestration
│   │   ├── memory.py             # Memory systems
│   │   ├── tools.py              # Tool framework
│   │   ├── llm.py                # LLM abstraction layer
│   │   └── workflows.py          # LangGraph workflows
│   ├── models/                   # Database models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model with common fields
│   │   ├── conversation.py       # Conversation model
│   │   ├── message.py            # Message model
│   │   ├── agent.py              # Agent model
│   │   ├── memory.py             # Memory models
│   │   └── execution.py          # Execution tracking
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── conversation.py       # Conversation schemas
│   │   ├── message.py            # Message schemas
│   │   ├── agent.py              # Agent schemas
│   │   └── response.py           # API response schemas
│   ├── database/                 # Database utilities
│   │   ├── __init__.py
│   │   ├── session.py            # Database session management
│   │   ├── migrations.py         # Migration utilities
│   │   └── seed.py               # Database seeding
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── conversation.py       # Conversation service
│   │   ├── agent.py              # Agent service
│   │   ├── memory.py             # Memory service
│   │   ├── llm.py                # LLM service
│   │   ├── tool.py               # Tool service
│   │   └── rag.py                # RAG service
│   ├── integrations/             # External integrations
│   │   ├── __init__.py
│   │   ├── llm/                  # LLM provider integrations
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── openai.py
│   │   │   ├── bedrock.py
│   │   │   └── ollama.py
│   │   ├── vector_store/         # Vector store integrations
│   │   │   ├── __init__.py
│   │   │   └── qdrant.py
│   │   ├── cache/                # Cache integrations
│   │   │   ├── __init__.py
│   │   │   └── redis.py
│   │   └── mcp/                  # MCP server integration
│   │       └── __init__.py
│   ├── tools/                    # Built-in tools
│   │   ├── __init__.py
│   │   ├── base.py               # Tool base classes
│   │   ├── web.py                # Web browsing tool
│   │   ├── code.py               # Code execution tool
│   │   └── file.py               # File operations tool
│   ├── monitoring/               # Observability
│   │   ├── __init__.py
│   │   ├── logging.py            # Logging configuration
│   │   ├── tracing.py            # Tracing (OpenTelemetry)
│   │   └── metrics.py            # Metrics collection
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── validators.py         # Validation utilities
│       ├── transformers.py       # Data transformation
│       └── decorators.py         # Helpful decorators
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest configuration & fixtures
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_agent.py
│   │   ├── test_memory.py
│   │   ├── test_tools.py
│   │   ├── test_llm.py
│   │   └── test_schemas.py
│   ├── integration/             # Integration tests
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_workflow.py
│   │   ├── test_database.py
│   │   └── test_services.py
│   └── fixtures/                # Test data and fixtures
│       └── sample_data.py
├── frontend/                    # Streamlit UI
│   ├── app.py                   # Main Streamlit app
│   ├── pages/                   # Multi-page app
│   │   ├── 01_conversations.py
│   │   ├── 02_agents.py
│   │   ├── 03_memory.py
│   │   └── 04_tools.py
│   ├── components/              # Reusable components
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── sidebar.py
│   │   └── dialogs.py
│   ├── config.py                # Frontend configuration
│   └── utils.py                 # Frontend utilities
├── data/                        # Data directory (git-ignored)
│   ├── .gitkeep
│   ├── uploads/                 # User uploaded files
│   ├── cache/                   # Local cache
│   └── exports/                 # Exported data
├── scripts/                     # Utility scripts
│   ├── init_db.py               # Initialize database
│   ├── seed_db.py               # Seed sample data
│   ├── test_llm.py              # Test LLM connectivity
│   └── generate_docs.py         # Generate documentation
├── config/                      # Configuration files
│   ├── settings.py              # Application settings
│   ├── logging.yaml             # Logging configuration
│   └── database.py              # Database configuration
├── .github/
│   └── workflows/               # GitHub Actions
│       ├── ci.yml               # CI pipeline
│       ├── test.yml             # Test pipeline
│       └── deploy.yml           # Deploy pipeline
├── docs/                        # Documentation
│   ├── architecture.md          # Architecture overview
│   ├── api.md                   # API documentation
│   ├── agents.md                # Agent development guide
│   ├── tools.md                 # Tool development guide
│   ├── deployment.md            # Deployment guide
│   ├── security.md              # Security guidelines
│   └── contributing.md          # Contributing guidelines
├── alembic/                     # Database migrations
│   ├── versions/                # Migration scripts
│   └── env.py                   # Migration environment
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── Dockerfile                   # Production Docker image
├── docker-compose.yml           # Development environment
├── pyproject.toml               # Python project configuration
└── LICENSE                      # MIT License
```

## Architecture

This platform follows clean architecture principles with clear separation of concerns:

- **API Layer**: FastAPI endpoints handling HTTP requests
- **Service Layer**: Business logic and orchestration
- **Core Layer**: Agent logic, memory, tools, and workflows
- **Integration Layer**: External service integrations (LLMs, databases, etc.)
- **Database Layer**: Persistent storage and ORM models

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Development Guidelines

1. **Code Quality**: Follow PEP 8, use type hints, write docstrings
2. **Testing**: Aim for >80% coverage on core components
3. **Documentation**: Document public APIs and complex logic
4. **Secrets**: Never commit API keys; use environment variables
5. **Dependencies**: Keep the dependency tree minimal
6. **Performance**: Optimize for latency in critical paths

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

Key configuration categories:
- **LLM**: Provider selection, API keys, model parameters
- **Database**: Connection strings and pool settings
- **Redis**: Cache and session management
- **Qdrant**: Vector store configuration
- **Security**: CORS, authentication, rate limiting
- **Logging**: Log levels and output format

## Testing

Run the test suite:

```bash
# All tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/unit/test_agent.py

# With verbose output
pytest -v
```

## Deployment

### Docker Compose (Development)
```bash
docker-compose up
```

### Docker (Production)
```bash
docker build -t agentic-ai-platform .
docker run -p 8000:8000 --env-file .env agentic-ai-platform
```

### AWS Deployment
See [docs/deployment.md](docs/deployment.md) for AWS-specific deployment instructions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the development guidelines
4. Write tests for new features
5. Submit a pull request

See [docs/contributing.md](docs/contributing.md) for detailed guidelines.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Status**: Initial development - Architecture and infrastructure setup phase
