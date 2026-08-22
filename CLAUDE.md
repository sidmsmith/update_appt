# Update Appointment Date — Project Instructions

This project follows the global `AGENTS.md` and `SECURITY_BASELINE.md`.
The notes below cover only what's specific to this repository.

## Version identifiers

Three places, in sync at `v3.2.4`:

- `package.json` — the `version` field
- `index.html` — the `<title>`
- `api/index.py` — the `APP_VERSION` constant

## Local development

- `node server.js` — Express, serves `index.html` and proxies `/api/*`
  to the Flask backend (port 3000 by default, via `PORT` env var)
- `python api/index.py` — Flask backend, port 5000 (`app.run(port=5000,
  debug=True)`)

`api/index.py` seeds a default appointment list from the
`DEFAULT_APPOINTMENTS` env var (JSON string). `convert_appointments.py`
is a local one-off helper for converting a Python `APPOINTMENTS` list
into that JSON string for pasting into Vercel's env var config — not
part of the deployed app.
