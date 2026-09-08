import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_consultancy_returns_false():
    """Consultancy-like offer should return should_apply: false"""
    response = client.post(
        "/api/v1/analyze",
        json={
            "offer_text": "Umbrella Corporation is hiring a remote Python Engineer. Culture of Relentless Performance with 99% project success rate. Top global clients. Relocation program available. Work From Anywhere Culture."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["should_apply"] == False
    assert len(data["red_flags"]) > 0


def test_analyze_good_offer_returns_true():
    """Good product company offer should return should_apply: true"""
    response = client.post(
        "/api/v1/analyze",
        json={
            "offer_text": "Stark Industries is a SaaS product company, no clients. 100% Remote Europe. Salary 75000-90000 EUR per year. Permanent contract. Requirements: 5+ years Python backend, FastAPI, PostgreSQL, Redis, Docker, CI/CD. 30 days vacation, private health insurance."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["should_apply"] == True


def test_analyze_returns_required_fields():
    """Response must contain all required fields"""
    response = client.post(
        "/api/v1/analyze",
        json={"offer_text": "Python developer position remote Europe salary 50000 EUR"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "should_apply" in data
    assert "reasons" in data
    assert "summary" in data
    assert "red_flags" in data


def test_company_endpoint_returns_required_fields():
    """Company analysis must contain all required fields"""
    response = client.post(
        "/api/v1/company",
        json={"company_name": "Wayne Enterprises"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "company_name" in data
    assert "reputation_score" in data
    assert "summary" in data
    assert "red_flags" in data
    assert "positive_signals" in data