import requests
import os
from dotenv import load_dotenv

load_dotenv()

JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")


def fetch_jooble_jobs(search_query, location="India", row=20):
    url = "https://jooble.org/api/2"

    payload = {"keywords": search_query, "location": location, "pageSize": row}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data.get("jobs", []):
                jobs.append(
                    {
                        "title": job.get("title", "N/A"),
                        "companyName": job.get("company", "N/A"),
                        "location": job.get("location", "N/A"),
                        "link": job.get("link", "#"),
                        "snippet": job.get("snippet", ""),
                        "salary": job.get("salary", "Not disclosed"),
                    }
                )
            return jobs
        else:
            print(f"Jooble API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Jooble API exception: {e}")
        return []


def fetch_jsearch_jobs(search_query, location="India", row=20):
    if not JSEARCH_API_KEY:
        return []

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{search_query} jobs in {location}",
        "page": "1",
        "num_pages": "1",
        "date_posted": "all",
    }

    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data.get("data", [])[:row]:
                jobs.append(
                    {
                        "title": job.get("job_title", "N/A"),
                        "companyName": job.get("employer_name", "N/A"),
                        "location": job.get("job_city", "N/A")
                        + ", "
                        + job.get("job_country", "N/A"),
                        "link": job.get("job_apply_link", "#"),
                        "snippet": job.get("job_description", "")[:200],
                        "salary": job.get("job_salary_currency", "")
                        + " "
                        + str(job.get("job_min_salary", ""))
                        + " - "
                        + str(job.get("job_max_salary", "")),
                        "posted": job.get("job_posted_at_datetime_utc", "N/A"),
                    }
                )
            return jobs
        else:
            print(f"JSearch API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"JSearch API exception: {e}")
        return []


def fetch_linkedin_jobs(search_query, location="India", row=60):
    from apify_client import ApifyClient

    apify_client = ApifyClient(token=os.getenv("APIFY_API_TOKEN"))

    run_input = {
        "title": search_query,
        "location": location,
        "row": min(row, 10),
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }

    try:
        run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
        jobs = apify_client.dataset(run["defaultDatasetId"]).list_items().items
        return jobs
    except Exception as e:
        print(f"LinkedIn API error: {str(e)[:100]}")
        return []


def fetch_joinrise_jobs(search_query, location="India", row=20):
    url = "https://api.joinrise.io/api/v1/jobs/public"

    try:
        response = requests.get(url, params={"page": 1, "limit": 100})
        if response.status_code == 200:
            data = response.json()
            jobs_data = data.get("result", {}).get("jobs", [])

            search_terms = search_query.lower().split()
            filtered_jobs = []

            for job in jobs_data:
                title = job.get("title", "").lower()
                desc = (
                    job.get("descriptionBreakdown", {})
                    .get("oneSentenceJobSummary", "")
                    .lower()
                )
                combined = title + " " + desc

                if any(term in combined for term in search_terms):
                    filtered_jobs.append(
                        {
                            "title": job.get("title", "N/A"),
                            "companyName": job.get("owner", {}).get(
                                "companyName", "N/A"
                            ),
                            "location": job.get("locationAddress", "N/A"),
                            "link": job.get("url", "#"),
                            "type": job.get("type", "N/A"),
                            "seniority": job.get("seniority", "N/A"),
                            "skills": job.get("skills_suggest", [])[:5],
                        }
                    )

                if len(filtered_jobs) >= row:
                    break

            return filtered_jobs
        else:
            print(f"JoinRise API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"JoinRise API exception: {e}")
        return []


def fetch_naukri_jobs(search_query, location="India", row=60):
    from apify_client import ApifyClient

    apify_client = ApifyClient(token=os.getenv("APIFY_API_TOKEN"))

    run_input = {
        "keywords": search_query,
        "maxJobs": min(row, 30),
        "freshness": "all",
        "sortby": "relevance",
        "experience": "all",
    }

    try:
        run = apify_client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)
        jobs = apify_client.dataset(run["defaultDatasetId"]).list_items().items
        return jobs
    except Exception as e:
        print(f"Naukri API error: {str(e)[:100]}")
        return []
