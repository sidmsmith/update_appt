# Update Appointment Date - Web Application

**Version 3.0.0** - Production Ready Release

Web version of the Appointment Date Updater tool, deployed on Vercel. This is a complete migration from the Python desktop application (`update_appointmentv19.py`) with enhanced features and improved user experience.

## Setup Instructions

### 1. Environment Variables in Vercel

Add the following environment variables in your Vercel project settings:

#### Required:
- `MANHATTAN_PASSWORD` - Manhattan API password
- `MANHATTAN_SECRET` - Manhattan API client secret
- `DEFAULT_APPOINTMENTS` - JSON string containing the default appointments array

#### Example `DEFAULT_APPOINTMENTS` format:
```json
[{"Asn-id": "ASN4100128", "Lpn01-id": "LPN4100128", "Lpn02-id": "LPN4200128", "Carrier-id": "SWFT", "Trailer-id": "TRL30103", "Appt-id": "APPT4191", "Day": "2025-08-26", "Time": "17:00:00"}, {"Asn-id": "ASN4100129", ...}]
```

**Note:** The JSON must be on a single line (minified) when pasting into Vercel's environment variable field.

### 2. Converting Python APPOINTMENTS to JSON

To convert the Python `APPOINTMENTS` list to JSON format:

1. Copy the APPOINTMENTS list from `update_appointmentv19.py` (lines 36-117)
2. Use Python to convert it:
   ```python
   import json
   # Paste your APPOINTMENTS list here
   APPOINTMENTS = [...]
   # Convert to JSON string
   json_str = json.dumps(APPOINTMENTS)
   print(json_str)
   ```
3. Copy the output and paste it into Vercel's `DEFAULT_APPOINTMENTS` environment variable

### 3. Local Development

1. Install dependencies:
   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. Set environment variables locally (create a `.env` file or export them):
   ```bash
   export MANHATTAN_PASSWORD="your_password"
   export MANHATTAN_SECRET="your_secret"
   export DEFAULT_APPOINTMENTS='[{"Asn-id": "...", ...}]'
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   vercel dev
   ```

### 4. Deployment

1. Connect your repository to Vercel
2. Add all environment variables in Vercel dashboard
3. Deploy!

## Features

### Core Functionality
- ✅ Authenticate with Manhattan API
- ✅ Validate appointments before updating
- ✅ Use default appointments (from environment variable)
- ✅ Add additional appointments via text input
- ✅ Upload CSV or Excel files (`.csv`, `.xls`, `.xlsx`) containing appointment IDs
- ✅ Real-time progress updates
- ✅ Results displayed as they complete
- ✅ Time tracking (elapsed/remaining)

### Validation & Error Handling
- ✅ Past date/time validation (prevents updating to dates in the past)
- ✅ Comprehensive error message extraction from API responses
- ✅ User-friendly error messages with full descriptions
- ✅ Singular/plural handling for missing appointments

### User Experience
- ✅ Modern dark theme UI
- ✅ Inline Authenticate button (prevents UI drift)
- ✅ Detailed logging for debugging
- ✅ Flexible column name matching in CSV/Excel files

## API Endpoints

- `POST /api/app_opened` - Track app open event
- `POST /api/auth` - Authenticate with Manhattan API
- `POST /api/get_default_appointments` - Get default appointments list
- `POST /api/validate` - Validate appointment IDs exist
- `POST /api/fetch_details` - Fetch full appointment details for IDs
- `POST /api/update` - Update appointment dates

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and release notes.

**Current Version:** 3.0.0 (Major Release)

## Project Structure

```
update_appt/
├── api/
│   ├── index.py          # Flask API endpoints
│   └── vercel.json       # Vercel configuration
├── index.html            # Frontend UI
├── server.js             # Express server (for local dev)
├── package.json          # Node.js dependencies
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── CHANGELOG.md         # Version history and release notes
```

