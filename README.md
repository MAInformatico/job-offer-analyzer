## API Endpoints

### Analyze a job offer
`POST /api/v1/analyze`

Returns whether a job offer is worth applying to based on your personal criteria.

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

---

### Analyze a company's reputation
`POST /api/v1/company`

Searches the web for reviews and signals about a company's culture, reputation, and red flags.

**Request:**
```json
{
  "company_name": "Mozilla"
}
```

**Response:**
```json
{
  "company_name": "Mozilla",
  "reputation_score": "negative",
  "summary": "Mixed reputation with concerns about culture and leadership",
  "red_flags": ["poor culture ratings", "low career opportunities"],
  "positive_signals": ["interesting projects", "flexible schedule"],
  "sources_consulted": ["https://glassdoor.com/..."]
}
```

---

### Full analysis (offer + company)
`POST /api/v1/analyze/full`

Combines offer analysis and company reputation into a single recommendation.

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