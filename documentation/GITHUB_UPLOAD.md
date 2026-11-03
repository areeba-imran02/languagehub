# Upload LanguageHub to GitHub

1. Download and extract `LanguageHub-Complete-Source-Code.zip`.
2. Open the extracted `LanguageHub` folder. The folder itself contains `README.md`, `apps/`, `backend/`, `ai_engine/`, `curriculum/`, and `.gitignore`.
3. On GitHub, create a new empty repository named `LanguageHub`. Do not add a README, license, or .gitignore during creation because those are already in this project.
4. Upload the **contents** of the extracted `LanguageHub` folder, not the ZIP archive and not an extra nested folder.
5. Confirm `.env` files with real credentials are not uploaded. Only `.env.example` files belong in the repository.
6. GitHub's browser uploader has file/size limits. If it refuses a folder or many files, use GitHub Desktop: add the extracted folder as a local repository, commit, then publish to GitHub.

The included `.github/workflows/ci.yml` runs backend tests and a web TypeScript check on pushes and pull requests. The web CI job installs dependencies from the npm registry; its success must be checked on the GitHub Actions tab after the first push.
