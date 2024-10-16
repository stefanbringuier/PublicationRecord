## ORCID Publication Record Generator

Automates the process of fetching ORCID publications and generating a BibTeX file via GitHub Actions.

### Reuse
1. Fork & Clone[^a]: `git clone https://github.com/stefanbringuier/PublicationRecord`
2. Get ORCID API Credentials
   - [Register a developer app on ORCID](https://info.orcid.org/documentation/integration-guide/registering-a-public-api-client)[^b] to get a `client_id` and `client_secret`.
   - Set GitHub `Secrets & Variables` in repo settings:
     - Secrets:
       - `ORCID_CLIENT_ID: Your ORCID Client ID`
       - `ORCID_CLIENT_SECRET: Your ORCID Client Secret`
     - Variable:
       - `ORCID_ID: Your ORCID ID (e.g., 0000-0001-6753-1437)`
      
[^a]: Be sure to enable read/write permissions for actions to allow for releases.
[^b]: In the app details setting of the developer tools for the name, url, and redirect you can just put anything (ex. https://github.com), I've found this works.
