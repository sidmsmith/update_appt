# Changelog

All notable changes to the Update Appointment Date web application will be documented in this file.

## [3.0.0] - 2025-01-XX

### Major Release - Production Ready

This is the first major release (v3.0.0) of the web application, representing a complete migration from the Python desktop application with significant enhancements.

### Added
- **CSV/Excel File Upload Support**: Users can now upload CSV or Excel files (`.csv`, `.xls`, `.xlsx`) containing appointment IDs for bulk validation and updates
- **Past Date/Time Validation**: Comprehensive validation to prevent updating appointments to dates/times in the past
  - Validation occurs in both Validate and Update workflows
  - Early detection prevents unnecessary API calls
- **Enhanced Error Messages**: 
  - Extracts detailed error descriptions from Manhattan API responses
  - Displays user-friendly error messages (e.g., "APT::213 Appointment Occurs in Past")
  - Proper singular/plural handling for missing appointments
- **Improved UI Layout**: 
  - Authenticate button positioned inline with ORG input field
  - Better visual hierarchy and spacing
- **Comprehensive Logging**: 
  - Detailed API call logging for both validation and update operations
  - Request/response details for debugging
  - Logs include headers, payloads, and raw JSON responses

### Changed
- **Environment Variable Configuration**: Default appointments list moved from hardcoded Python variable to Vercel environment variable (`DEFAULT_APPOINTMENTS`)
- **Validation Logic**: Unified validation approach between Validate button and Update workflow
- **Error Handling**: Improved error extraction and display from API responses

### Fixed
- Fixed bug where Validate button would pass invalid appointments when default checkbox was unchecked
- Fixed UI not hiding after failed authentication attempts
- Fixed CSV parsing to handle quoted values and flexible column name matching
- Fixed error message display to show full API error descriptions instead of generic HTTP errors

### Technical Details
- **Frontend**: HTML/JavaScript with Bootstrap 5.3.3
- **Backend**: Flask API deployed on Vercel serverless functions
- **File Processing**: Client-side CSV/Excel parsing using SheetJS (XLSX.js)
- **API Integration**: Manhattan WMS Appointment API

---

## [2.10] - 2025-01-XX

### Added
- Past date/time validation in Validate button
- Enhanced error message extraction from API responses
- Inline Authenticate button layout

## [2.9] - 2025-01-XX

### Added
- Past date/time validation before update operations
- Improved error message formatting

## [2.8] - 2025-01-XX

### Added
- Detailed logging for update API calls
- Enhanced error handling and reporting

## [2.7] - 2025-01-XX

### Added
- CSV/Excel file upload support
- Client-side file parsing
- Flexible column name matching

## [2.6] - 2025-01-XX

### Added
- Detailed API logging for validation calls
- Improved validation success/error messaging

## [2.0-2.5] - 2025-01-XX

### Initial Development
- Migration from Python desktop application
- Basic authentication and validation
- Appointment update functionality
- Default appointments support
- Additional appointments input
- Real-time progress tracking

