# api/index.py
from flask import Flask, request, jsonify, send_from_directory
import json
import re
import os
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# === SECURE CONFIG (from Vercel Environment Variables) ===
HA_WEBHOOK_URL = "http://sidmsmith.zapto.org:8123/api/webhook/manhattan_appt_update"
HA_HEADERS = {"Content-Type": "application/json"}

AUTH_HOST = "salep-auth.sce.manh.com"
API_HOST = "salep.sce.manh.com"
USERNAME_BASE = "sdtadmin@"
PASSWORD = os.getenv("MANHATTAN_PASSWORD")
CLIENT_ID = "omnicomponent.1.0.0"
CLIENT_SECRET = os.getenv("MANHATTAN_SECRET")

# Load APPOINTMENTS from environment variable (JSON string)
APPOINTMENTS_JSON = os.getenv("DEFAULT_APPOINTMENTS", "[]")
try:
    APPOINTMENTS = json.loads(APPOINTMENTS_JSON) if APPOINTMENTS_JSON else []
except json.JSONDecodeError:
    APPOINTMENTS = []
    print("[WARNING] Failed to parse DEFAULT_APPOINTMENTS environment variable. Using empty list.")

# Critical: Fail fast if secrets missing
if not PASSWORD or not CLIENT_SECRET:
    raise Exception("Missing MANHATTAN_PASSWORD or MANHATTAN_SECRET environment variables")

# === HELPERS ===
def send_ha_message(payload):
    try:
        requests.post(HA_WEBHOOK_URL, json=payload, headers=HA_HEADERS, timeout=5)
    except:
        pass

def get_manhattan_token(org):
    url = f"https://{AUTH_HOST}/oauth/token"
    username = f"{USERNAME_BASE}{org.lower()}"
    data = {
        "grant_type": "password",
        "username": username,
        "password": PASSWORD,
    }
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    try:
        r = requests.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=auth,
            timeout=30,
            verify=False,
        )
        r.raise_for_status()
        return r.json().get("access_token")
    except Exception as e:
        print(f"[AUTH] {e}")
        return None

def validate_appointments(base_headers, org, appt_ids):
    url = f"https://{API_HOST}/appointment/api/appointment/appointment/search"
    headers = base_headers.copy()
    headers["Content-Type"] = "application/json"
    headers["selectedOrganization"] = org
    headers["selectedLocation"] = f"{org}-DM1"

    if not appt_ids:
        return []

    query = " OR ".join(f"AppointmentId = '{id}'" for id in appt_ids)
    payload = {
        "Query": f"({query})",
        "Size": len(appt_ids),
        "Page": 0
    }

    # Detailed logging
    print("=" * 80)
    print("[VALIDATE] API Call Details")
    print("=" * 80)
    print(f"[VALIDATE] URL: {url}")
    print(f"[VALIDATE] Headers:")
    for key, value in headers.items():
        if key == "Authorization":
            print(f"  {key}: Bearer [REDACTED]")
        else:
            print(f"  {key}: {value}")
    print("-" * 80)
    print(f"[VALIDATE] EXACT QUERY STRING:")
    print(f"  {query}")
    print("-" * 80)
    print(f"[VALIDATE] Request Body (Payload):")
    print(f"  {json.dumps(payload, indent=2)}")
    print("-" * 80)
    print(f"[VALIDATE] Requested Appointment IDs ({len(appt_ids)}): {appt_ids}")
    print("-" * 80)

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
        
        print(f"[VALIDATE] Response Status: {r.status_code}")
        print(f"[VALIDATE] Response Headers:")
        for key, value in r.headers.items():
            print(f"  {key}: {value}")
        
        r.raise_for_status()
        response_json = r.json()
        
        print(f"[VALIDATE] Raw JSON Response:")
        print(json.dumps(response_json, indent=2))
        
        data = response_json.get("data", [])
        print(f"[VALIDATE] Data array length: {len(data)}")
        
        # Extract existing appointment IDs from the response
        existing_ids = [item.get("AppointmentId") for item in data if item.get("AppointmentId")]
        print(f"[VALIDATE] Existing Appointment IDs found ({len(existing_ids)}): {existing_ids}")
        
        # Find missing appointments (requested IDs that don't exist in the response)
        missing = [id for id in appt_ids if id not in existing_ids]
        print(f"[VALIDATE] Missing Appointment IDs ({len(missing)}): {missing}")
        print("=" * 80)
        
        return missing
    except requests.exceptions.HTTPError as e:
        print(f"[VALIDATE] HTTP Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[VALIDATE] Response Status: {e.response.status_code}")
            print(f"[VALIDATE] Response Text: {e.response.text}")
        print("=" * 80)
        return None
    except Exception as e:
        print(f"[VALIDATE] Exception: {type(e).__name__}: {e}")
        import traceback
        print(f"[VALIDATE] Traceback: {traceback.format_exc()}")
        print("=" * 80)
        return None

def fetch_appointment_details(base_headers, org, appt_ids):
    """Fetch full appointment details from API and convert to format needed for update."""
    url = f"https://{API_HOST}/appointment/api/appointment/appointment/search"
    headers = base_headers.copy()
    headers["Content-Type"] = "application/json"
    headers["selectedOrganization"] = org
    headers["selectedLocation"] = f"{org}-DM1"

    if not appt_ids:
        return []

    query = " OR ".join(f"AppointmentId = '{id}'" for id in appt_ids)
    payload = {
        "Query": f"({query})",
        "Size": len(appt_ids),
        "Page": 0
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
        r.raise_for_status()
        data = r.json().get("data", [])
        
        appointments = []
        for item in data:
            # Extract time from PreferredDateTime or ArrivalDateTime
            datetime_str = item.get("PreferredDateTime") or item.get("ArrivalDateTime") or ""
            time_part = ""
            if datetime_str and "T" in datetime_str:
                time_part = datetime_str.split("T")[1].split(".")[0]  # Extract HH:MM:SS
            
            # Extract ASN from AppointmentContents or Asn
            asn_id = ""
            appointment_contents = item.get("AppointmentContents", [])
            if appointment_contents and len(appointment_contents) > 0:
                asn_id = appointment_contents[0].get("Asn", "")
            if not asn_id:
                asn_list = item.get("Asn", [])
                if asn_list and len(asn_list) > 0:
                    asn_id = asn_list[0].get("AsnId", "")
            
            appt_dict = {
                "Appt-id": item.get("AppointmentId", ""),
                "Asn-id": asn_id,
                "Carrier-id": item.get("CarrierId", ""),
                "Trailer-id": item.get("TrailerId", ""),
                "Time": time_part or "00:00:00",  # Default if not found
            }
            appointments.append(appt_dict)
        
        return appointments
    except Exception as e:
        print(f"[API] Fetch error: {e}")
        return None

def update_appointment(appt, new_date, base_headers, org):
    url = f"https://{API_HOST}/appointment/api/appointment/editAppointment"
    headers = base_headers.copy()
    headers["Content-Type"] = "application/json"
    headers["selectedOrganization"] = org
    headers["selectedLocation"] = f"{org}-DM1"

    original_time = appt["Time"]
    new_datetime = f"{new_date}T{original_time}"
    appt_id = appt.get("Appt-id", "Unknown")

    # Only update dates - conditionally include ASN, Carrier, and Trailer only if they have values
    # Get values, convert to string, strip whitespace - only include in payload if non-empty
    asn_id = str(appt.get("Asn-id", "")).strip()
    carrier_id = str(appt.get("Carrier-id", "")).strip()
    trailer_id = str(appt.get("Trailer-id", "")).strip()
    
    # Build base payload with required fields
    payload = {
        "AppointmentId": appt_id,
        "AppointmentTypeId": "DROP_UNLOAD",
        "UserLoadInformation": [],
        "EquipmentTypeId": "48FT",
        "PreferredDateTime": new_datetime,
        "ArrivalDateTime": new_datetime,
        "Duration": 60,
        "AppointmentStatusId": "3000"
    }
    
    # Only include Carrier if it has a value
    if carrier_id:
        payload["CarrierId"] = carrier_id
    
    # Only include Trailer if it has a value
    if trailer_id:
        payload["TrailerId"] = trailer_id
    
    # Only include ASN if it has a value
    if asn_id:
        payload["AppointmentContents"] = [{"Asn": asn_id}]
        payload["Asn"] = [{"AsnId": asn_id, "DestinationFacilityId": f"{org}-DM1"}]

    # Detailed logging
    print("=" * 80)
    print(f"[UPDATE] API Call Details for Appointment: {appt_id}")
    print("=" * 80)
    print(f"[UPDATE] URL: {url}")
    print(f"[UPDATE] Headers:")
    for key, value in headers.items():
        if key == "Authorization":
            print(f"  {key}: Bearer [REDACTED]")
        else:
            print(f"  {key}: {value}")
    print(f"[UPDATE] Request Body (Payload):")
    print(f"  {json.dumps(payload, indent=2)}")
    print(f"[UPDATE] Appointment Data:")
    print(f"  Appt-id: {appt_id}")
    print(f"  Asn-id: {appt.get('Asn-id', 'N/A')}")
    print(f"  Carrier-id: {appt.get('Carrier-id', 'N/A')}")
    print(f"  Trailer-id: {appt.get('Trailer-id', 'N/A')}")
    print(f"  Original Time: {original_time}")
    print(f"  New Date: {new_date}")
    print(f"  New DateTime: {new_datetime}")
    print("-" * 80)

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
        
        print(f"[UPDATE] Response Status: {r.status_code}")
        print(f"[UPDATE] Response Headers:")
        for key, value in r.headers.items():
            print(f"  {key}: {value}")
        
        r.raise_for_status()
        response_json = r.json()
        
        print(f"[UPDATE] Raw JSON Response:")
        print(json.dumps(response_json, indent=2))
        print(f"[UPDATE] Result: SUCCESS")
        print("=" * 80)
        
        return {"success": True, "message": "Success"}
    except requests.exceptions.HTTPError as e:
        print(f"[UPDATE] HTTP Error: {e}")
        error_message = str(e)
        found_good_message = False
        
        if hasattr(e, 'response') and e.response is not None:
            print(f"[UPDATE] Response Status: {e.response.status_code}")
            try:
                error_response = e.response.json()
                print(f"[UPDATE] Error Response JSON:")
                print(json.dumps(error_response, indent=2))
                
                # Try to extract meaningful error message from response
                if isinstance(error_response, dict):
                    # First check for messages.Message array (Manhattan API format)
                    if "messages" in error_response and isinstance(error_response["messages"], dict):
                        messages = error_response["messages"].get("Message", [])
                        if isinstance(messages, list) and len(messages) > 0:
                            msg_obj = messages[0]
                            if isinstance(msg_obj, dict):
                                code = msg_obj.get("Code", "")
                                description = msg_obj.get("Description", "")
                                if code and description:
                                    error_message = f"{code} {description}"
                                    found_good_message = True
                                elif description:
                                    error_message = description
                                    found_good_message = True
                                elif code:
                                    error_message = code
                                    found_good_message = True
                    
                    # Fallback to other common error message fields
                    if not found_good_message:
                        if "message" in error_response:
                            error_message = error_response["message"]
                            found_good_message = True
                        elif "error" in error_response:
                            error_message = error_response["error"]
                            found_good_message = True
                        elif "errors" in error_response:
                            errors = error_response["errors"]
                            if isinstance(errors, list) and len(errors) > 0:
                                if isinstance(errors[0], dict):
                                    error_message = errors[0].get("message", errors[0].get("description", str(errors[0])))
                                else:
                                    error_message = str(errors[0])
                                found_good_message = True
                            elif isinstance(errors, dict):
                                error_message = errors.get("message", errors.get("description", str(errors)))
                                found_good_message = True
                        elif "exceptions" in error_response:
                            exceptions = error_response["exceptions"]
                            if isinstance(exceptions, list) and len(exceptions) > 0:
                                if isinstance(exceptions[0], dict):
                                    error_message = exceptions[0].get("message", exceptions[0].get("description", str(exceptions[0])))
                                else:
                                    error_message = str(exceptions[0])
                                found_good_message = True
                        elif "Message" in error_response:
                            error_message = error_response["Message"]
                            found_good_message = True
                        elif "Error" in error_response:
                            error_message = error_response["Error"]
                            found_good_message = True
            except:
                response_text = e.response.text[:1000] if hasattr(e.response, 'text') else str(e.response)
                print(f"[UPDATE] Response Text: {response_text}")
                # Try to extract error from text if JSON parsing failed
                if "Appointment Occurs in Past" in response_text:
                    error_message = "Appointment Occurs in Past"
                elif response_text and len(response_text) < 200:
                    error_message = response_text
        print(f"[UPDATE] Result: FAILED - {error_message}")
        print("=" * 80)
        return {"success": False, "error": error_message}
    except Exception as e:
        print(f"[UPDATE] Exception: {type(e).__name__}: {e}")
        import traceback
        print(f"[UPDATE] Traceback: {traceback.format_exc()}")
        print(f"[UPDATE] Result: FAILED")
        print("=" * 80)
        return {"success": False, "error": str(e)}

# === API ROUTES ===
@app.route('/api/app_opened', methods=['POST'])
def app_opened():
    send_ha_message({"event": "manhattan_appt_update_open", "org": request.json.get("org", "")})
    return jsonify({"success": True})

@app.route('/api/auth', methods=['POST'])
def auth():
    org = request.json.get('org', '').strip()
    if not org:
        return jsonify({"success": False, "error": "ORG required"})
    token = get_manhattan_token(org)
    if token:
        send_ha_message({"event": "manhattan_appt_update_auth", "org": org, "success": True})
        return jsonify({"success": True, "token": token})
    send_ha_message({"event": "manhattan_appt_update_auth", "org": org, "success": False})
    return jsonify({"success": False, "error": "Auth failed"})

@app.route('/api/get_default_appointments', methods=['POST'])
def get_default_appointments():
    """Return the default appointments list."""
    return jsonify({"success": True, "appointments": APPOINTMENTS})

@app.route('/api/validate', methods=['POST'])
def validate():
    request_data = request.json
    org = request_data.get('org')
    token = request_data.get('token')
    # Frontend sends 'useDefault' (camelCase), accept both for compatibility
    use_default = request_data.get('useDefault', request_data.get('use_default', False))
    csv_ids = request_data.get('csvIds', []) or []
    additional_ids_raw = request_data.get('additionalIds', request_data.get('additional_ids', ''))
    new_date = request_data.get('new_date')  # Optional date for past-date validation
    
    print("=" * 80)
    print("[VALIDATE ENDPOINT] Received Request")
    print("=" * 80)
    print(f"[VALIDATE ENDPOINT] Request Body: {json.dumps(request_data, indent=2)}")
    print(f"[VALIDATE ENDPOINT] org: {org}")
    print(f"[VALIDATE ENDPOINT] useDefault from request: {request_data.get('useDefault')}")
    print(f"[VALIDATE ENDPOINT] use_default from request: {request_data.get('use_default')}")
    print(f"[VALIDATE ENDPOINT] Final use_default value: {use_default} (type: {type(use_default).__name__})")
    print(f"[VALIDATE ENDPOINT] csvIds from request: {csv_ids}")
    print(f"[VALIDATE ENDPOINT] additionalIds from request: {request_data.get('additionalIds')}")
    print(f"[VALIDATE ENDPOINT] additional_ids_raw: '{additional_ids_raw}'")
    print(f"[VALIDATE ENDPOINT] new_date: {new_date}")
    print("-" * 80)
    
    if not all([org, token]):
        print("[VALIDATE ENDPOINT] ERROR: Missing org or token")
        print("=" * 80)
        return jsonify({"success": False, "error": "Missing org or token"})
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Collect appointment IDs
    appt_ids = []
    if use_default:
        default_ids = [appt["Appt-id"] for appt in APPOINTMENTS]
        appt_ids.extend(default_ids)
        print(f"[VALIDATE ENDPOINT] Added {len(default_ids)} default appointment IDs")
    
    if csv_ids:
        appt_ids.extend(csv_ids)
        print(f"[VALIDATE ENDPOINT] Added {len(csv_ids)} CSV appointment IDs: {csv_ids}")
    
    if additional_ids_raw:
        tokens = [t.strip() for t in re.split(r'[,\s;]+', additional_ids_raw) if t.strip()]
        appt_ids.extend(tokens)
        print(f"[VALIDATE ENDPOINT] Added {len(tokens)} additional appointment IDs: {tokens}")
    
    # Deduplicate
    appt_ids = list(dict.fromkeys(appt_ids))
    print(f"[VALIDATE ENDPOINT] Total unique appointment IDs to validate: {len(appt_ids)}")
    print(f"[VALIDATE ENDPOINT] Appointment IDs: {appt_ids}")
    print("-" * 80)
    
    if not appt_ids:
        print("[VALIDATE ENDPOINT] ERROR: No appointments to validate")
        print("=" * 80)
        return jsonify({"success": False, "error": "No appointments to validate"})
    
    # Validate appointments - returns list of missing IDs, or None on error
    missing = validate_appointments(headers, org, appt_ids)
    
    print("[VALIDATE ENDPOINT] Validation Result:")
    print(f"  missing = {missing}")
    print(f"  missing is None: {missing is None}")
    print(f"  len(missing) if not None: {len(missing) if missing is not None else 'N/A'}")
    print("-" * 80)
    
    # Handle error case
    if missing is None:
        print("[VALIDATE ENDPOINT] Returning: Validation failed")
        print("=" * 80)
        return jsonify({"success": False, "error": "Validation failed"})
    
    # Handle missing appointments case (missing is a non-empty list)
    if missing and len(missing) > 0:
        missing_count = len(missing)
        if missing_count == 1:
            error_msg = f"Missing appointment: {', '.join(missing)}"
        else:
            error_msg = f"Missing appointments: {', '.join(missing)}"
        print(f"[VALIDATE ENDPOINT] Returning: {error_msg}")
        print("=" * 80)
        return jsonify({
            "success": False,
            "error": error_msg,
            "missing": missing
        })
    
    # If new_date is provided, check for past appointments
    if new_date:
        print(f"[VALIDATE ENDPOINT] Checking for past appointments with date: {new_date}")
        appointments = fetch_appointment_details(headers, org, appt_ids)
        if appointments is None:
            print("[VALIDATE ENDPOINT] ERROR: Failed to fetch appointment details for date validation")
            print("=" * 80)
            return jsonify({"success": False, "error": "Failed to fetch appointment details"})
        
        now = datetime.now()
        past_appointments = []
        
        for appt in appointments:
            appt_id = appt.get("Appt-id", "Unknown")
            appt_time = appt.get("Time", "00:00:00")
            new_datetime_str = f"{new_date}T{appt_time}"
            try:
                new_datetime = datetime.strptime(new_datetime_str, "%Y-%m-%dT%H:%M:%S")
                if new_datetime < now:
                    past_appointments.append(appt_id)
                    print(f"[VALIDATE ENDPOINT] Past appointment found: {appt_id} ({new_datetime_str})")
            except Exception as e:
                print(f"[VALIDATE ENDPOINT] Error parsing datetime for {appt_id}: {e}")
        
        if past_appointments:
            past_count = len(past_appointments)
            if past_count == 1:
                error_msg = f"{past_appointments[0]}: Appointment would occur in the past"
            else:
                error_msg = f"{', '.join(past_appointments)}: These appointments would occur in the past"
            print(f"[VALIDATE ENDPOINT] Returning: {error_msg}")
            print("=" * 80)
            return jsonify({
                "success": False,
                "error": error_msg,
                "past_appointments": past_appointments
            })
        print(f"[VALIDATE ENDPOINT] No past appointments found")
    
    # All appointments are valid (missing is empty list [])
    validated_count = len(appt_ids)
    success_msg = f"Successfully validated {validated_count} appointment{'s' if validated_count != 1 else ''}"
    print(f"[VALIDATE ENDPOINT] Returning: {success_msg}")
    print("=" * 80)
    return jsonify({"success": True, "message": success_msg})

@app.route('/api/search_by_date_range', methods=['POST'])
def search_by_date_range():
    """Search appointments by date range or ApptId range"""
    data = request.json
    org = data.get('org', '').strip()
    token = data.get('token', '').strip()
    filter_type = data.get('filter_type', 'date').strip()
    from_date = data.get('from_date', '').strip()
    to_date = data.get('to_date', '').strip()
    from_appt_id = data.get('from_appt_id', '').strip()
    to_appt_id = data.get('to_appt_id', '').strip()
    
    if not org or not token:
        return jsonify({"success": False, "error": "ORG and token required"}), 400
    
    base_headers = {
        "Authorization": f"Bearer {token}",
        "selectedOrganization": org,
        "selectedLocation": f"{org}-DM1"
    }
    
    url = f"https://{API_HOST}/appointment/api/appointment/appointment/search"
    headers = base_headers.copy()
    headers["Content-Type"] = "application/json"
    
    # Build query based on filter type
    if filter_type == 'apptId':
        if not from_appt_id or not to_appt_id:
            return jsonify({"success": False, "error": "From ApptId and To ApptId required"}), 400
        
        # Search by ApptId range - need to fetch all and filter
        # Since we can't do range queries on ApptId directly, we'll search for a broader set
        # and filter client-side, or use a pattern if the API supports it
        query = f"AppointmentId >= '{from_appt_id}' AND AppointmentId <= '{to_appt_id}'"
    else:
        # Date range
        if not from_date or not to_date:
            return jsonify({"success": False, "error": "From date and to date required"}), 400
        query = f"PreferredDateTime >= '{from_date}T00:00:00' AND PreferredDateTime <= '{to_date}T23:59:59'"
    
    payload = {
        "Query": query,
        "Size": 1000,  # Adjust as needed
        "Page": 0
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)
        r.raise_for_status()
        data = r.json().get("data", [])
        
        appointments = []
        for item in data:
            appt_id = item.get("AppointmentId", "")
            
            # For ApptId range, filter by ApptId comparison
            if filter_type == 'apptId':
                if not (from_appt_id <= appt_id <= to_appt_id):
                    continue
            
            # Extract time from PreferredDateTime or ArrivalDateTime (same logic as fetch_appointment_details)
            datetime_str = item.get("PreferredDateTime", "") or item.get("ArrivalDateTime", "")
            if not datetime_str:
                continue
            
            # Extract date part (YYYY-MM-DD)
            date_part = datetime_str.split('T')[0] if 'T' in datetime_str else datetime_str.split(' ')[0]
            # Extract time part (HH:MM:SS)
            time_part = ""
            if datetime_str and "T" in datetime_str:
                time_part = datetime_str.split("T")[1].split(".")[0]  # Extract HH:MM:SS
            if not time_part:
                time_part = "00:00:00"  # Default if not found
            
            # For date range, check if date is within range
            if filter_type == 'date':
                if not (from_date <= date_part <= to_date):
                    continue
            
            # Extract ASN from AppointmentContents or Asn (same logic as fetch_appointment_details)
            asn_id = ""
            appointment_contents = item.get("AppointmentContents", [])
            if appointment_contents and len(appointment_contents) > 0:
                asn_id = appointment_contents[0].get("Asn", "")
            if not asn_id:
                asn_list = item.get("Asn", [])
                if asn_list and len(asn_list) > 0:
                    asn_id = asn_list[0].get("AsnId", "")
            
            appointments.append({
                "Appt-id": appt_id,
                "Asn-id": asn_id,
                "Carrier-id": item.get("CarrierId", ""),
                "Trailer-id": item.get("TrailerId", ""),
                "Date": date_part,
                "Time": time_part
            })
        
        return jsonify({
            "success": True,
            "appointments": appointments,
            "count": len(appointments)
        })
    except Exception as e:
        print(f"[SEARCH_RANGE] Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/fetch_details', methods=['POST'])
def fetch_details():
    org = request.json.get('org')
    token = request.json.get('token')
    appt_ids = request.json.get('appt_ids', [])
    
    if not all([org, token, appt_ids]):
        return jsonify({"success": False, "error": "Missing data"})
    
    headers = {"Authorization": f"Bearer {token}"}
    appointments = fetch_appointment_details(headers, org, appt_ids)
    
    if appointments is None:
        return jsonify({"success": False, "error": "Failed to fetch appointment details"})
    
    return jsonify({"success": True, "appointments": appointments})

@app.route('/api/update', methods=['POST'])
def update():
    request_data = request.json
    org = request_data.get('org')
    token = request_data.get('token')
    appointments = request_data.get('appointments', [])
    new_date = request_data.get('new_date')
    
    print("=" * 80)
    print("[UPDATE ENDPOINT] Received Request")
    print("=" * 80)
    print(f"[UPDATE ENDPOINT] org: {org}")
    print(f"[UPDATE ENDPOINT] new_date: {new_date}")
    print(f"[UPDATE ENDPOINT] Number of appointments to update: {len(appointments)}")
    print(f"[UPDATE ENDPOINT] Appointment IDs: {[appt.get('Appt-id', 'Unknown') for appt in appointments]}")
    print("-" * 80)
    
    if not all([org, token, appointments, new_date]):
        print("[UPDATE ENDPOINT] ERROR: Missing required data")
        print("=" * 80)
        return jsonify({"success": False, "error": "Missing data"})
    
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    success_count = 0
    
    for idx, appt in enumerate(appointments):
        appt_id = appt.get("Appt-id", "Unknown")
        print(f"[UPDATE ENDPOINT] Processing appointment {idx + 1}/{len(appointments)}: {appt_id}")
        result = update_appointment(appt, new_date, headers, org)
        results.append({
            "appt_id": appt_id,
            "success": result["success"],
            "message": result.get("message", "Success") if result["success"] else result.get("error", "Unknown error")
        })
        if result["success"]:
            success_count += 1
        print(f"[UPDATE ENDPOINT] Appointment {appt_id}: {'SUCCESS' if result['success'] else 'FAILED'}")
        if not result["success"]:
            print(f"[UPDATE ENDPOINT] Error for {appt_id}: {result.get('error', 'Unknown error')}")
    
    total = len(appointments)
    fail_count = total - success_count
    
    print("-" * 80)
    print(f"[UPDATE ENDPOINT] Summary:")
    print(f"  Total: {total}")
    print(f"  Success: {success_count}")
    print(f"  Failed: {fail_count}")
    print("=" * 80)
    
    send_ha_message({
        "event": "manhattan_appt_update",
        "org": org,
        "success_count": success_count,
        "total_count": total,
    })
    
    return jsonify({
        "success": True,
        "results": results,
        "summary": f"Finished: {total} appointments. {success_count} passed, {fail_count} failed",
        "success_count": success_count,
        "fail_count": fail_count,
        "total_count": total
    })

# === FALLBACK: Serve index.html for SPA (Critical for Vercel) ===
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        return "API route not found", 404
    try:
        return send_from_directory('..', 'index.html')
    except:
        return "File not found", 404

# === DEV SERVER ===
if __name__ == '__main__':
    app.run(port=5000, debug=True)

