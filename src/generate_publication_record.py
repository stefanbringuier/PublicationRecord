import os
import requests
from datetime import datetime

def get_access_token(client_id, client_secret):
    """First need to obtain an ORCID access token.
    See ORCID API Developer Docs.
    """
    url = "https://orcid.org/oauth/token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "/read-public",
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def fetch_publications(orcid_id, access_token):
    """Fetch works/publications from ORCID and extract DOIs."""
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {
        "Accept": "application/vnd.orcid+json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    publications = response.json()

    dois = []
    for work in publications.get("group", []):
        work_summary = work.get("work-summary", [])[0]
        doi = next(
            (
                ext_id["external-id-value"]
                for ext_id in work_summary.get("external-ids", {}).get("external-id", [])
                if ext_id.get("external-id-type", "").lower() == "doi"
            ),
            None,
        )
        if doi:
            dois.append(doi)
    return dois

def fetch_bibtex_for_doi(doi):
    """For a given DOI fetch BibTeX entry."""
    url = f"https://dx.doi.org/{doi}"
    headers = {"Accept": "text/bibliography; style=bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Warning: Failed to retrieve BibTeX for DOI {doi}")
        return None

def write_bibtex_file(dois, filename):
    """Fetch and write BibTeX entries for all DOIs to a .bib file."""
    with open(filename, "w", encoding="utf-8") as bibfile:
        for doi in dois:
            bibtex_entry = fetch_bibtex_for_doi(doi)
            if bibtex_entry:
                bibfile.write(bibtex_entry + "\n")

if __name__ == "__main__":
    # Set these in your Github Repo settings
    client_id = os.environ.get("ORCID_CLIENT_ID")
    client_secret = os.environ.get("ORCID_CLIENT_SECRET")
    orcid_id = os.environ.get("ORCID_ID")

    if not client_id or not client_secret or not orcid_id:
        raise ValueError("Missing ORCID credentials or ORCID_ID. Please set the environment variables.")

    access_token = get_access_token(client_id, client_secret)
    dois = fetch_publications(orcid_id, access_token)
    date_str = datetime.now().strftime("%d%b%Y")  # e.g., 10Oct2024
    filename = f"PublicationRecord_{date_str}.bib"
    write_bibtex_file(dois, filename)
