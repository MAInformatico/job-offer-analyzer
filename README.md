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
2. The service uses an LLM (LangChain) to extract key signals.
3. A company reputation module searches the web for reviews and signals.
4. The result is combined into a final recommendation.

## Technologies

- Python
- FastAPI
- LangChain
- OpenAI / LLM APIs
- Pydantic
- Docker
- (pendiente: frontend ligero)

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
  "reasons": ["company type does not match preferred criteria"],
  "summary": "Remote Python role at a global services company",
  "red_flags": ["top global clients", "project success rate"],
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
  "reputation_score": "negative",
  "summary": "Mixed reputation with concerns about culture and leadership",
  "red_flags": ["poor culture ratings", "low career opportunities"],
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
  "offer_analysis": { ... },
  "company_analysis": { ... },
  "final_recommendation": "Not recommended to apply"
}
```

## How to run it

```bash
docker-compose up --build
```

Or in local:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

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