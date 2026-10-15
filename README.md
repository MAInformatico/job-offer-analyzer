# Job Analyzer

**Job Analyzer** is a backend tool that helps job seekers evaluate whether a job offer is worth applying to, using LLM-powered analysis of both the offer text and the company's reputation.

## Problem

Job hunting is time-consuming and often demoralizing. Many offers look good on the surface but hide red flags: toxic culture, unrealistic expectations, or poor career growth. Manual research (Glassdoor, LinkedIn, news) is slow and inconsistent.

## Solution

Job Analyzer uses an LLM to:

- Analyze the offer text against personal criteria (remote, stack, role, salary range).
- Research the company's reputation (culture, reviews, red flags).
- Return a clear recommendation with reasons, red flags, and positive signals.

## Architecture

1. User submits an offer text and/or company name via REST API.
2. The service uses an LLM (LangChain + Groq API) to extract key signals from the offer.
3. A company reputation module searches the web (DuckDuckGo) for reviews and signals about the company and passes the results to the LLM.
4. Both results are combined into a final recommendation.

## Technologies

- Python
- FastAPI
- LangChain
- Groq API (`openai/gpt-oss-20b`)
- DuckDuckGo Search
- Pydantic
- Docker

## API Endpoints

### Analyze a job offer

`POST /api/v1/analyze`

**Request:**

```json
{
  "offer_text": "paste the full job offer text here"
}
```

**Response:**

```json
{
  "should_apply": false,
  "reasons": ["salary range not disclosed", "role responsibilities are unclear"],
  "summary": "Remote Python role at a global services company",
  "red_flags": ["no salary range disclosed", "vague role responsibilities"],
  "salary_info": null
}
```

### Analyze a company's reputation

`POST /api/v1/company`

**Request:**

```json
{
  "company_name": "My business imaginary"
}
```

**Response:**

```json
{
  "company_name": "My business imaginary",
  "reputation_score": "mixed",
  "summary": "Mixed reputation with concerns about culture and leadership",
  "red_flags": ["poor culture ratings", "high turnover reported"],
  "positive_signals": ["interesting projects", "flexible schedule"],
  "sources_consulted": ["https://glassdoor.com/..."]
}
```

### Full analysis (offer + company)

`POST /api/v1/analyze/full`

**Request:**

```json
{
  "offer_text": "paste the full job offer text here",
  "company_name": "Company Name"
}
```

**Response:**

```json
{
  "offer_analysis": { "...": "..." },
  "company_analysis": { "...": "..." },
  "final_recommendation": "Not recommended to apply"
}
```

## How to run it

With Docker:

```bash
cp config.example.yaml config.yaml
export GROQ_API_KEY=your_key
docker-compose up --build
```

Or locally (also requires `config.yaml` and `GROQ_API_KEY` as above):

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Design decisions

- **Groq with an open-weight model (`gpt-oss-20b`):** low latency and near-zero inference cost for a self-hosted tool, at the price of a smaller model than frontier APIs.
- **DuckDuckGo for web search:** no API key or paid plan required, which keeps the tool easy to run and self-host.
- **Synchronous REST API:** the use case is one request, one analysis; a queue would add complexity without benefit at this scale.
- **Structured output:** LLM responses are requested as JSON and validated with Pydantic models, so the API returns a predictable schema.

## Limitations

- Company reputation depends on DuckDuckGo search results; sources may be sparse, outdated or biased, and no source ranking is applied.
- The LLM can misinterpret an offer or cite sources inaccurately; results are a screening aid, not a verdict.
- No caching, rate limiting or authentication yet.

## What I learned

- Designing a REST API with FastAPI for LLM-powered analysis.
- Using LangChain to structure prompts and parse responses.
- Integrating external data (company reviews) with LLM reasoning.
- Building a tool that solves a real problem I faced during my own job search.

## Future work

- Add authentication and user profiles with personal criteria.
- Add a lightweight frontend (React) for easier use.
- Cache company reputation results to avoid repeated web searches.
- Add support for multiple LLM providers (OpenAI, Anthropic, local models).