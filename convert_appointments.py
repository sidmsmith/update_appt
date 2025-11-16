#!/usr/bin/env python3
"""
Helper script to convert Python APPOINTMENTS list to JSON format
for use in Vercel environment variable DEFAULT_APPOINTMENTS.

Usage:
1. Copy the APPOINTMENTS list from update_appointmentv19.py (lines 36-117)
2. Paste it below, replacing the example
3. Run: python convert_appointments.py
4. Copy the output and paste into Vercel's DEFAULT_APPOINTMENTS environment variable
"""

import json

# Paste your APPOINTMENTS list here (from update_appointmentv19.py)
APPOINTMENTS = [

    {"Asn-id": "ASN4100128", "Lpn01-id": "LPN4100128", "Lpn02-id": "LPN4200128", "Carrier-id": "SWFT", "Trailer-id": "TRL30103", "Appt-id": "APPT4191", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100129", "Lpn01-id": "LPN4100129", "Lpn02-id": "LPN4200129", "Carrier-id": "SWFT", "Trailer-id": "TRL30104", "Appt-id": "APPT4192", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100130", "Lpn01-id": "LPN4100130", "Lpn02-id": "LPN4200130", "Carrier-id": "SWFT", "Trailer-id": "TRL30105", "Appt-id": "APPT4193", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100131", "Lpn01-id": "LPN4100131", "Lpn02-id": "LPN4200131", "Carrier-id": "SWFT", "Trailer-id": "TRL30106", "Appt-id": "APPT4194", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100132", "Lpn01-id": "LPN4100132", "Lpn02-id": "LPN4200132", "Carrier-id": "SWFT", "Trailer-id": "TRL30107", "Appt-id": "APPT4195", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100133", "Lpn01-id": "LPN4100133", "Lpn02-id": "LPN4200133", "Carrier-id": "SWFT", "Trailer-id": "TRL30108", "Appt-id": "APPT4196", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100134", "Lpn01-id": "LPN4100134", "Lpn02-id": "LPN4200134", "Carrier-id": "SWFT", "Trailer-id": "TRL30109", "Appt-id": "APPT4197", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100135", "Lpn01-id": "LPN4100135", "Lpn02-id": "LPN4200135", "Carrier-id": "SWFT", "Trailer-id": "TRL30110", "Appt-id": "APPT4198", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100136", "Lpn01-id": "LPN4100136", "Lpn02-id": "LPN4200136", "Carrier-id": "SWFT", "Trailer-id": "TRL30111", "Appt-id": "APPT4199", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100137", "Lpn01-id": "LPN4100137", "Lpn02-id": "LPN4200137", "Carrier-id": "SWFT", "Trailer-id": "TRL30112", "Appt-id": "APPT4200", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100138", "Lpn01-id": "LPN4100138", "Lpn02-id": "LPN4200138", "Carrier-id": "SWFT", "Trailer-id": "TRL30113", "Appt-id": "APPT4201", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100139", "Lpn01-id": "LPN4100139", "Lpn02-id": "LPN4200139", "Carrier-id": "SWFT", "Trailer-id": "TRL30114", "Appt-id": "APPT4202", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100140", "Lpn01-id": "LPN4100140", "Lpn02-id": "LPN4200140", "Carrier-id": "SWFT", "Trailer-id": "TRL30115", "Appt-id": "APPT4203", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100141", "Lpn01-id": "LPN4100141", "Lpn02-id": "LPN4200141", "Carrier-id": "SWFT", "Trailer-id": "TRL30116", "Appt-id": "APPT4204", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100142", "Lpn01-id": "LPN4100142", "Lpn02-id": "LPN4200142", "Carrier-id": "SWFT", "Trailer-id": "TRL30117", "Appt-id": "APPT4205", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100143", "Lpn01-id": "LPN4100143", "Lpn02-id": "LPN4200143", "Carrier-id": "SWFT", "Trailer-id": "TRL30118", "Appt-id": "APPT4206", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100144", "Lpn01-id": "LPN4100144", "Lpn02-id": "LPN4200144", "Carrier-id": "SWFT", "Trailer-id": "TRL30119", "Appt-id": "APPT4207", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100145", "Lpn01-id": "LPN4100145", "Lpn02-id": "LPN4200145", "Carrier-id": "SWFT", "Trailer-id": "TRL30120", "Appt-id": "APPT4208", "Day": "2025-08-26", "Time": "21:00:00"},
    {"Asn-id": "ASN4100146", "Lpn01-id": "LPN4100146", "Lpn02-id": "LPN4200146", "Carrier-id": "SWFT", "Trailer-id": "TRL30121", "Appt-id": "APPT4209", "Day": "2025-08-26", "Time": "21:00:00"},
    {"Asn-id": "ASN4100147", "Lpn01-id": "LPN4100147", "Lpn02-id": "LPN4200147", "Carrier-id": "SWFT", "Trailer-id": "TRL30122", "Appt-id": "APPT4210", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100148", "Lpn01-id": "LPN4100148", "Lpn02-id": "LPN4200148", "Carrier-id": "SWFT", "Trailer-id": "TRL30123", "Appt-id": "APPT4211", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100149", "Lpn01-id": "LPN4100149", "Lpn02-id": "LPN4200149", "Carrier-id": "SWFT", "Trailer-id": "TRL30124", "Appt-id": "APPT4212", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100150", "Lpn01-id": "LPN4100150", "Lpn02-id": "LPN4200150", "Carrier-id": "SWFT", "Trailer-id": "TRL30125", "Appt-id": "APPT4213", "Day": "2025-08-26", "Time": "23:00:00"},
    {"Asn-id": "ASN4100151", "Lpn01-id": "LPN4100151", "Lpn02-id": "LPN4200151", "Carrier-id": "SWFT", "Trailer-id": "TRL30126", "Appt-id": "APPT4214", "Day": "2025-08-26", "Time": "23:00:00"},
    {"Asn-id": "ASN4100152", "Lpn01-id": "LPN4100152", "Lpn02-id": "LPN4200152", "Carrier-id": "SWFT", "Trailer-id": "TRL30127", "Appt-id": "APPT4215", "Day": "2025-08-26", "Time": "16:00:00"},
    {"Asn-id": "ASN4100153", "Lpn01-id": "LPN4100153", "Lpn02-id": "LPN4200153", "Carrier-id": "SWFT", "Trailer-id": "TRL30128", "Appt-id": "APPT4216", "Day": "2025-08-26", "Time": "16:00:00"},
    {"Asn-id": "ASN4100154", "Lpn01-id": "LPN4100154", "Lpn02-id": "LPN4200154", "Carrier-id": "SWFT", "Trailer-id": "TRL30129", "Appt-id": "APPT4217", "Day": "2025-08-26", "Time": "16:00:00"},
    {"Asn-id": "ASN4100155", "Lpn01-id": "LPN4100155", "Lpn02-id": "LPN4200155", "Carrier-id": "SWFT", "Trailer-id": "TRL30130", "Appt-id": "APPT4218", "Day": "2025-08-26", "Time": "15:00:00"},
    {"Asn-id": "ASN4100156", "Lpn01-id": "LPN4100156", "Lpn02-id": "LPN4200156", "Carrier-id": "SWFT", "Trailer-id": "TRL30131", "Appt-id": "APPT4219", "Day": "2025-08-26", "Time": "15:00:00"},
    {"Asn-id": "ASN4100157", "Lpn01-id": "LPN4100157", "Lpn02-id": "LPN4200157", "Carrier-id": "SWFT", "Trailer-id": "TRL30132", "Appt-id": "APPT4220", "Day": "2025-08-26", "Time": "15:00:00"},
    {"Asn-id": "ASN4100158", "Lpn01-id": "LPN4100158", "Lpn02-id": "LPN4200158", "Carrier-id": "SWFT", "Trailer-id": "TRL30133", "Appt-id": "APPT4221", "Day": "2025-08-26", "Time": "15:00:00"},
    {"Asn-id": "ASN4100159", "Lpn01-id": "LPN4100159", "Lpn02-id": "LPN4200159", "Carrier-id": "SWFT", "Trailer-id": "TRL30134", "Appt-id": "APPT4222", "Day": "2025-08-26", "Time": "15:00:00"},
    {"Asn-id": "ASN4100160", "Lpn01-id": "LPN4100160", "Lpn02-id": "LPN4200160", "Carrier-id": "SWFT", "Trailer-id": "TRL30135", "Appt-id": "APPT4223", "Day": "2025-08-26", "Time": "14:00:00"},
    {"Asn-id": "ASN4100161", "Lpn01-id": "LPN4100161", "Lpn02-id": "LPN4200161", "Carrier-id": "SWFT", "Trailer-id": "TRL30136", "Appt-id": "APPT4224", "Day": "2025-08-26", "Time": "14:00:00"},
    {"Asn-id": "ASN4100162", "Lpn01-id": "LPN4100162", "Lpn02-id": "LPN4200162", "Carrier-id": "SWFT", "Trailer-id": "TRL30137", "Appt-id": "APPT4225", "Day": "2025-08-26", "Time": "14:00:00"},
    {"Asn-id": "ASN4100163", "Lpn01-id": "LPN4100163", "Lpn02-id": "LPN4200163", "Carrier-id": "SWFT", "Trailer-id": "TRL30138", "Appt-id": "APPT4226", "Day": "2025-08-26", "Time": "14:00:00"},
    {"Asn-id": "ASN4100164", "Lpn01-id": "LPN4100164", "Lpn02-id": "LPN4200164", "Carrier-id": "SWFT", "Trailer-id": "TRL30139", "Appt-id": "APPT4227", "Day": "2025-08-26", "Time": "13:00:00"},
    {"Asn-id": "ASN4100165", "Lpn01-id": "LPN4100165", "Lpn02-id": "LPN4200165", "Carrier-id": "SWFT", "Trailer-id": "TRL30140", "Appt-id": "APPT4228", "Day": "2025-08-26", "Time": "13:00:00"},
    {"Asn-id": "ASN4100166", "Lpn01-id": "LPN4100166", "Lpn02-id": "LPN4200166", "Carrier-id": "SWFT", "Trailer-id": "TRL30141", "Appt-id": "APPT4229", "Day": "2025-08-26", "Time": "13:00:00"},
    {"Asn-id": "ASN4100167", "Lpn01-id": "LPN4100167", "Lpn02-id": "LPN4200167", "Carrier-id": "SWFT", "Trailer-id": "TRL30142", "Appt-id": "APPT4230", "Day": "2025-08-26", "Time": "13:00:00"},
    {"Asn-id": "ASN4100168", "Lpn01-id": "LPN4100168", "Lpn02-id": "LPN4200168", "Carrier-id": "SWFT", "Trailer-id": "TRL30143", "Appt-id": "APPT4231", "Day": "2025-08-26", "Time": "12:00:00"},
    {"Asn-id": "ASN4100169", "Lpn01-id": "LPN4100169", "Lpn02-id": "LPN4200169", "Carrier-id": "SWFT", "Trailer-id": "TRL30144", "Appt-id": "APPT4232", "Day": "2025-08-26", "Time": "12:00:00"},
    {"Asn-id": "ASN4100170", "Lpn01-id": "LPN4100170", "Lpn02-id": "LPN4200170", "Carrier-id": "SWFT", "Trailer-id": "TRL30145", "Appt-id": "APPT4233", "Day": "2025-08-26", "Time": "12:00:00"},
    {"Asn-id": "ASN4100171", "Lpn01-id": "LPN4100171", "Lpn02-id": "LPN4200171", "Carrier-id": "SWFT", "Trailer-id": "TRL30146", "Appt-id": "APPT4234", "Day": "2025-08-26", "Time": "12:00:00"},
    {"Asn-id": "ASN4100172", "Lpn01-id": "LPN4100172", "Lpn02-id": "LPN4200172", "Carrier-id": "SWFT", "Trailer-id": "TRL30147", "Appt-id": "APPT4235", "Day": "2025-08-26", "Time": "12:00:00"},
    {"Asn-id": "ASN4100173", "Lpn01-id": "LPN4100173", "Lpn02-id": "LPN4200173", "Carrier-id": "SWFT", "Trailer-id": "TRL30148", "Appt-id": "APPT4236", "Day": "2025-08-26", "Time": "11:00:00"},
    {"Asn-id": "ASN4100174", "Lpn01-id": "LPN4100174", "Lpn02-id": "LPN4200174", "Carrier-id": "SWFT", "Trailer-id": "TRL30149", "Appt-id": "APPT4237", "Day": "2025-08-26", "Time": "11:00:00"},
    {"Asn-id": "ASN4100175", "Lpn01-id": "LPN4100175", "Lpn02-id": "LPN4200175", "Carrier-id": "SWFT", "Trailer-id": "TRL30150", "Appt-id": "APPT4238", "Day": "2025-08-26", "Time": "11:00:00"},
    {"Asn-id": "ASN4100176", "Lpn01-id": "LPN4100176", "Lpn02-id": "LPN4200176", "Carrier-id": "SWFT", "Trailer-id": "TRL30151", "Appt-id": "APPT4239", "Day": "2025-08-26", "Time": "11:00:00"},
    {"Asn-id": "ASN4100177", "Lpn01-id": "LPN4100177", "Lpn02-id": "LPN4200177", "Carrier-id": "SWFT", "Trailer-id": "TRL30152", "Appt-id": "APPT4240", "Day": "2025-08-26", "Time": "10:00:00"},
    {"Asn-id": "ASN4100178", "Lpn01-id": "LPN4100178", "Lpn02-id": "LPN4200178", "Carrier-id": "SWFT", "Trailer-id": "TRL30153", "Appt-id": "APPT4241", "Day": "2025-08-26", "Time": "16:00:00"},
    {"Asn-id": "ASN4100179", "Lpn01-id": "LPN4100179", "Lpn02-id": "LPN4200179", "Carrier-id": "PFLT", "Trailer-id": "TRL30154", "Appt-id": "APPT4242", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100180", "Lpn01-id": "LPN4100180", "Lpn02-id": "LPN4200180", "Carrier-id": "HJBT", "Trailer-id": "TRL30155", "Appt-id": "APPT4243", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100181", "Lpn01-id": "LPN4100181", "Lpn02-id": "LPN4200181", "Carrier-id": "CNWY", "Trailer-id": "TRL30156", "Appt-id": "APPT4244", "Day": "2025-08-26", "Time": "17:00:00"},
    {"Asn-id": "ASN4100182", "Lpn01-id": "LPN4100182", "Lpn02-id": "LPN4200182", "Carrier-id": "HJBT", "Trailer-id": "TRL30157", "Appt-id": "APPT4245", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100183", "Lpn01-id": "LPN4100183", "Lpn02-id": "LPN4200183", "Carrier-id": "CNWY", "Trailer-id": "TRL30158", "Appt-id": "APPT4246", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100184", "Lpn01-id": "LPN4100184", "Lpn02-id": "LPN4200184", "Carrier-id": "PFLT", "Trailer-id": "TRL30159", "Appt-id": "APPT4247", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100185", "Lpn01-id": "LPN4100185", "Lpn02-id": "LPN4200185", "Carrier-id": "HJBT", "Trailer-id": "TRL30160", "Appt-id": "APPT4248", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100186", "Lpn01-id": "LPN4100186", "Lpn02-id": "LPN4200186", "Carrier-id": "CNWY", "Trailer-id": "TRL30161", "Appt-id": "APPT4249", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100187", "Lpn01-id": "LPN4100187", "Lpn02-id": "LPN4200187", "Carrier-id": "PFLT", "Trailer-id": "TRL30162", "Appt-id": "APPT4250", "Day": "2025-08-26", "Time": "18:00:00"},
    {"Asn-id": "ASN4100188", "Lpn01-id": "LPN4100188", "Lpn02-id": "LPN4200188", "Carrier-id": "PFLT", "Trailer-id": "TRL30163", "Appt-id": "APPT4251", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100189", "Lpn01-id": "LPN4100189", "Lpn02-id": "LPN4200189", "Carrier-id": "HJBT", "Trailer-id": "TRL30164", "Appt-id": "APPT4252", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100190", "Lpn01-id": "LPN4100190", "Lpn02-id": "LPN4200190", "Carrier-id": "CNWY", "Trailer-id": "TRL30165", "Appt-id": "APPT4253", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100191", "Lpn01-id": "LPN4100191", "Lpn02-id": "LPN4200191", "Carrier-id": "PFLT", "Trailer-id": "TRL30166", "Appt-id": "APPT4254", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100192", "Lpn01-id": "LPN4100192", "Lpn02-id": "LPN4200192", "Carrier-id": "PFLT", "Trailer-id": "TRL30167", "Appt-id": "APPT4255", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100193", "Lpn01-id": "LPN4100193", "Lpn02-id": "LPN4200193", "Carrier-id": "HJBT", "Trailer-id": "TRL30168", "Appt-id": "APPT4256", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100194", "Lpn01-id": "LPN4100194", "Lpn02-id": "LPN4200194", "Carrier-id": "CNWY", "Trailer-id": "TRL30169", "Appt-id": "APPT4257", "Day": "2025-08-26", "Time": "19:00:00"},
    {"Asn-id": "ASN4100195", "Lpn01-id": "LPN4100195", "Lpn02-id": "LPN4200195", "Carrier-id": "PFLT", "Trailer-id": "TRL30170", "Appt-id": "APPT4258", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100196", "Lpn01-id": "LPN4100196", "Lpn02-id": "LPN4200196", "Carrier-id": "PFLT", "Trailer-id": "TRL30171", "Appt-id": "APPT4259", "Day": "2025-08-26", "Time": "20:00:00"},
    {"Asn-id": "ASN4100197", "Lpn01-id": "LPN4100197", "Lpn02-id": "LPN4200197", "Carrier-id": "HJBT", "Trailer-id": "TRL30172", "Appt-id": "APPT4260", "Day": "2025-08-26", "Time": "21:00:00"},
    {"Asn-id": "ASN4100198", "Lpn01-id": "LPN4100198", "Lpn02-id": "LPN4200198", "Carrier-id": "CNWY", "Trailer-id": "TRL30173", "Appt-id": "APPT4261", "Day": "2025-08-26", "Time": "21:00:00"},
    {"Asn-id": "ASN4100199", "Lpn01-id": "LPN4100199", "Lpn02-id": "LPN4200199", "Carrier-id": "PFLT", "Trailer-id": "TRL30174", "Appt-id": "APPT4262", "Day": "2025-08-26", "Time": "21:00:00"},
    {"Asn-id": "ASN4100200", "Lpn01-id": "LPN4100200", "Lpn02-id": "LPN4200200", "Carrier-id": "PFLT", "Trailer-id": "TRL30175", "Appt-id": "APPT4263", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100201", "Lpn01-id": "LPN4100201", "Lpn02-id": "LPN4200201", "Carrier-id": "HJBT", "Trailer-id": "TRL30176", "Appt-id": "APPT4264", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100202", "Lpn01-id": "LPN4100202", "Lpn02-id": "LPN4200202", "Carrier-id": "CNWY", "Trailer-id": "TRL30177", "Appt-id": "APPT4265", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100203", "Lpn01-id": "LPN4100203", "Lpn02-id": "LPN4200203", "Carrier-id": "PFLT", "Trailer-id": "TRL30178", "Appt-id": "APPT4266", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100204", "Lpn01-id": "LPN4100204", "Lpn02-id": "LPN4200204", "Carrier-id": "PFLT", "Trailer-id": "TRL30179", "Appt-id": "APPT4267", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100205", "Lpn01-id": "LPN4100205", "Lpn02-id": "LPN4200205", "Carrier-id": "PFLT", "Trailer-id": "TRL30180", "Appt-id": "APPT4268", "Day": "2025-08-26", "Time": "22:00:00"},
    {"Asn-id": "ASN4100206", "Lpn01-id": "LPN4100206", "Lpn02-id": "LPN4200206", "Carrier-id": "PFLT", "Trailer-id": "TRL30181", "Appt-id": "APPT4269", "Day": "2025-08-26", "Time": "23:00:00"},
    {"Asn-id": "ASN4100207", "Lpn01-id": "LPN4100207", "Lpn02-id": "LPN4200207", "Carrier-id": "PFLT", "Trailer-id": "TRL30182", "Appt-id": "APPT4270", "Day": "2025-08-26", "Time": "19:00:00"}
]

if __name__ == "__main__":
    # Convert to JSON string (minified, single line)
    json_str = json.dumps(APPOINTMENTS, separators=(',', ':'))
    print("\n" + "="*80)
    print("Copy the following JSON string to Vercel's DEFAULT_APPOINTMENTS variable:")
    print("="*80)
    print(json_str)
    print("="*80)
    print(f"\nTotal appointments: {len(APPOINTMENTS)}")
    print("="*80 + "\n")

