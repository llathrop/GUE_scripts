CI Explanation and Removal
=========================

This repository includes a small, intentionally-visible GitHub Actions workflow at
`.github/workflows/ci.yml` that runs the project's pytest suite on push and pull
requests against Python 3.11 and 3.12. The workflow is minimal by design so that
it's easy to understand and remove if desired.

Files added for CI:

- `.github/workflows/ci.yml` - GitHub Actions workflow that checks out the repo,
  sets up Python, installs `requirements.txt` if present, and runs `pytest -q`.
- `requirements.txt` - Minimal dependency list used by the workflow. Add any
  other test/runtime deps here if needed.

How to remove or disable CI
---------------------------

1. To temporarily disable CI, create a new branch and delete `.github/workflows/ci.yml` in that branch and push it. GitHub will stop running the workflow for future pushes.
2. To remove it permanently, delete the file from the default branch (usually `main` or `master`).
3. Alternatively, you can edit `ci.yml` to change triggers (for example, remove `push`) or reduce the matrix.

Notes
-----
- The workflow intentionally uses `pip install -r requirements.txt` so you can
  control what's installed. If your project uses a different environment
  mechanism (conda, poetry), update the workflow accordingly.
- The workflow is designed to be short and well-commented to make maintenance easy.
