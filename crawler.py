import requests
import pandas as pd
import base64
import json
import time



GITHUB_API = "https://api.github.com/search/repositories"
GITHUB_TOKEN = "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"   

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

SEARCH_QUERY = "ui test OR selenium OR playwright OR end-to-end OR e2e in:readme"


GUIDELINE_FILES = [
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug_report.md"
]


DOC_FILES = [
    "README.md", "TESTING.md", "CONTRIBUTING.md", "docs/testing.md", "package.json"
]


KEYWORDS = {
    "technologies": [
        "react", "angular", "vue", "svelte", "django", "spring boot", "next.js", "flask",
        "express", "rails", "laravel", "dotnet", ".net", "nuxt", "astro", "typescript",
        "javascript", "python", "java", "php", "ruby", "c#", "node.js"
    ],
    "ui_testing_tools": [
        "cypress", "selenium", "playwright", "puppeteer", "webdriverio", "robot framework",
        "testcafe", "karma", "nightwatch", "jest", "mocha", "junit", "nunit", "rspec"
    ],
    "patterns": [
        "page object", "page-object", "test pyramid", "screenplay pattern", "robot pattern",
        "layered test", "component test", "modular test", "arrange act assert",
        "given when then", "fixture pattern", "factory pattern", "builder pattern"
    ],
    "paradigms": [
        "test driven development", "tdd", "test first", "test-first",
        "behavior driven development", "bdd", "specification by example",
        "acceptance test driven development", "atdd", "exploratory testing",
        "property based testing", "contract testing"
    ],
    "best_practices": [
        "flaky test", "ci/cd", "test isolation", "visual testing", "cross-browser testing",
        "test coverage", "test reliability", "test maintainability", "shift-left testing",
        "test automation pyramid", "self-healing tests", "mocking", "stubbing",
        "test data management", "parallel testing", "headless testing"
    ],
    "principles": [
        "single responsibility", "open/closed principle", "liskov substitution",
        "interface segregation", "dependency inversion", "solid principles",
        "clean code", "testability", "loose coupling", "separation of concerns"
    ]
}



def fetch_file_content(full_name, filename):
    url = f"https://api.github.com/repos/{full_name}/contents/{filename}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        try:
            return base64.b64decode(r.json()["content"]).decode("utf-8").lower()
        except Exception:
            return ""
    return ""

def fetch_all_text(full_name):
    combined = ""
    for file in DOC_FILES:
        combined += fetch_file_content(full_name, file) + "\n"
    return combined

def check_guidelines(full_name):
    presence = {}
    for file in GUIDELINE_FILES:
        url = f"https://api.github.com/repos/{full_name}/contents/{file}"
        resp = requests.get(url, headers=HEADERS)
        presence[file] = "yes" if resp.status_code == 200 else "no"
    return presence

def analyze(text):
    results = {}
    for cat, terms in KEYWORDS.items():
        matches = [term for term in terms if term in text]
        results[cat] = ", ".join(matches)
    return results

def search_repos(query, pages=10):
    all_data = []
    for page in range(1, pages + 1):
        params = {"q": query, "per_page": 10, "page": page}
        res = requests.get(GITHUB_API, headers=HEADERS, params=params)
        if res.status_code != 200:
            print("Error:", res.status_code)
            break
        for item in res.json().get("items", []):
            print("Analyzing:", item["full_name"])
            row = {
                "name": item["name"],
                "url": item["html_url"],
                "language": item["language"],
                "description": item["description"],
                "stars": item["stargazers_count"]
            }
            text = fetch_all_text(item["full_name"])
            row.update(analyze(text))
            row.update(check_guidelines(item["full_name"]))
            all_data.append(row)
        time.sleep(1)
    return all_data



if __name__ == "__main__":
    repos = search_repos(SEARCH_QUERY)
    pd.DataFrame(repos).to_csv("ui_testing_repos_detailed.csv", index=False)
    print("✅ Saved data to ui_testing_repos_detailed.csv")