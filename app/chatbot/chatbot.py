from app.services.service import create_appointment, get_appointments
from app.chatbot.llm_parser import parse_message_with_llm
import re
from datetime import datetime, timedelta
from app.services.doctor_service import get_doctors_by_department, get_doctors_by_patient, get_all_doctors
from app.chatbot.doctor_agent import extract_department

conversation_state = {}


def contains_department(message, dept_keywords):
    return any(dept in message.lower() for dept in dept_keywords)


def is_date_like(value: str):
    if not value:
        return False
    v = value.lower().strip()
    if re.match(r"\d{4}-\d{2}-\d{2}", value):
        return True
    if re.match(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", value):
        return True
    if any(word in value.lower() for word in ["today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
        return True
    
    if re.match(r"\d{1,2}:\d{2}", v):
        return True
    if re.match(r"\d{1,2}(:\d{2})?\s?(am|pm)", v):
        return True
    if re.match(r"\b\d{1,2}\b", v):
        return True

    return False

def normalize_time(t):
    try:
        return datetime.strptime(t.strip(), "%H:%M").strftime("%H:%M")
    except:
        try:
            return datetime.strptime(t.strip(), "%I %p").strftime("%H:%M")
        except:
            try:
                return datetime.strptime(t.strip(), "%I:%M %p").strftime("%H:%M")
            except:
                return None

hospital_keywords = [
    "dentist", "cardiac", "checkup", "surgery", "consultation", "therapy", "treatment", "physio", "scan", "xray", "blood test", "lab", "medical",
]
# "doctor", "dentist", "cardiac", "checkup", "surgery", "consultation", "therapy", "treatment", "physio", "hospital", "clinic", "scan", "xray", "blood test", "lab", "medical", "health"


def process_message(message: str):
    global conversation_state
    message_lower = message.lower()
    words = re.findall(r"\b\w+\b", message_lower)
    
    greetings = ["hi", "hello", "hey", "gm", "morning", "afternoon", "evening"]
    if any(word in greetings for word in words):
        if conversation_state.get("intent") == "create":
            pass
        else:
            if "morning" in words or "gm" in words:
                return "Good morning. I am your appointment assistant. I can help you create or view bookings. How may I assist you today?"
            if "afternoon" in words:
                return "Good afternoon. I am your appointment assistant. I can help you create or view bookings. How may I assist you today?"
            if "evening" in words:
                return "Good evening. I am your appointment assistant. I can help you create or view bookings. How may I assist you today?"
            return "Hello. I am your appointment assistant. I can help you create or view bookings. How may I assist you today?"

    # Small talk handling
    small_talk_responses = {
        "how are you?": "I'm doing well, thank you. I can help you book or view hospital appointments. How may I assist you?",
        "how are you doing?": "I'm doing well, thank you. How can I assist you with appointments today?",
        "what can you do?": "I can help you book hospital appointments or view your existing bookings.",
        "help": "You can ask me to book an appointment or show your bookings."
    }
    if message_lower in small_talk_responses:
        return small_talk_responses[message_lower]

    if any(word in message_lower for word in ["thanks", "thank you"]):
        return "You're welcome. Let me know if you need help with appointments."
    if any(word in message_lower for word in ["bye", "goodbye"]):
        return "Goodbye. Feel free to come back anytime."

    parsed = parse_message_with_llm(message)
    
    parsed.setdefault("intent", None)
    parsed.setdefault("name", None)
    parsed.setdefault("date", None)
    parsed.setdefault("time", None)
    parsed.setdefault("start_date", None)
    parsed.setdefault("end_date", None)
    parsed.setdefault("description", None)

    if conversation_state.get("intent") == "create":
        parsed["description"] = parsed.get("description") if not conversation_state.get("description") else None


    print("Parsed:", parsed)
    # If parsing fails but conversation exists, continue using memory
    if not parsed:
        if conversation_state.get("intent") == "create":
            parsed = {}
        else:
            return "Could not understand input"

    intent = parsed.get("intent")

    # GET detection
    if any(word in words for word in ["show", "get", "list", "view", "bookings"]):
        intent = "get"
    # CREATE detection
    if any(word in words for word in ["create", "book", "schedule", "appointment", "meeting", "want"]):
        intent = "create"
    # Force CREATE if conversation in progress
    if conversation_state.get("intent") == "create":
        intent = "create"
        parsed["intent"] = "create"
    # GET doctor detection
    if any(word in message_lower for word in ["doctor", "doctors", "available", "which doctor"]):
        intent = "doctor"
    # Merge previous state
    if conversation_state:
        for key in ["name", "date"]:
            if parsed.get(key):
                conversation_state[key] = parsed[key]
            if not parsed.get(key):
                parsed[key] = conversation_state.get(key)

    # Extract values
    name = parsed.get("name")
    date = parsed.get("date")
    time = parsed.get("time")
    desc = parsed.get("description")


    # Follow-up handling (important fix)
    if conversation_state:
        if not conversation_state.get("description"):
            desc = message.strip().lower()
            parsed["description"] = desc

        elif not conversation_state.get("name"):
            parsed["name"] = message.strip()

        elif not conversation_state.get("date"):
            if not parsed.get("date"):
                parsed["date"] = message.strip()
            date = parsed["date"]
        
        elif not conversation_state.get("time"):
            parsed["time"] = message.strip()
            time = parsed["time"]

    # Clean description
    if desc and intent == "create":

        desc = desc.strip().lower()

        if desc in ["booking", "appointment", "schedule", "book"]:
            desc = None

        elif is_date_like(desc):
            desc = None

        elif len(desc.split()) > 6:
            desc = None

        elif not any(keyword in desc for keyword in hospital_keywords):
            conversation_state["description"] = None
            return (
                "I can only assist with hospital-related appointments. "
                "For example: dentist, doctor visit, checkup, surgery.\n"
                "What is the appointment about?"
            )

        if desc:
            conversation_state["description"] = desc


    # Clean name
    if name:
        name = name.strip()
        if is_date_like(name):
            name = None
        else: 
            conversation_state["name"] = name

    if not name:
        name = None

    # Validate date
    today = datetime.today()
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            try:
                parsed_date = datetime.strptime(date, "%d %B %Y")
                date = parsed_date.strftime("%Y-%m-%d")
            except:
                # HANDLE NATURAL DATES
                if "today" in date.lower():
                    date = today.strftime("%Y-%m-%d")

                elif "tomorrow" in date.lower():
                    date = (today + timedelta(days=1)).strftime("%Y-%m-%d")

                else:
                    date = None
        if date: 
            conversation_state["date"] = date

    # Validate time
    if time:
        try:
            datetime.strptime(time, "%H:%M")
        except:
            time = None
    if time:
        time = normalize_time(time)
        if time:
            conversation_state["time"] = time


    if intent == "create":
        conversation_state["intent"] = "create"
        if not conversation_state.get("name"):
            return "Who is it for?"
        if not conversation_state.get("date"):
            return "When is it?"
        if not conversation_state.get("time"):
            return "What time is the appointment?"
        if not conversation_state.get("description"):
            return "What is it about?"

        name = conversation_state["name"]
        date = conversation_state["date"]
        time = conversation_state["time"]
        desc = conversation_state["description"]

        conversation_state = {}

        datetime_str = f"{date} {time}"
        return create_appointment(name, datetime_str, desc)


    if intent == "get" and any(word in words for word in ["show", "get", "list", "view", "bookings", "appointments"]):
        conversation_state = {}
        name = parsed.get("name")
        desc = parsed.get("description")
        date = parsed.get("date")
        start_date = parsed.get("start_date")
        end_date = parsed.get("end_date")

        message_lower = message.lower()

        if "today" in message_lower:
            from datetime import date as dt
            today_date = dt.today().strftime("%Y-%m-%d")
            return get_appointments(date=today_date)
        if start_date and end_date:
            return get_appointments(start_date=start_date, end_date=end_date)
        if date:
            return get_appointments(date=date)
        if name:
            return get_appointments(name=name)
        if desc and desc.lower() in ["booking", "bookings", "appointment", "appointments"]:
            desc = None
        if desc:
            return get_appointments(description=desc)
        if any(word in message_lower for word in [
            "today", "tomorrow",
            "monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday"
        ]):
            from datetime import date as dt, timedelta
            today = dt.today()
            if "today" in message_lower:
                return get_appointments(date=today.strftime("%Y-%m-%d"))
            if "tomorrow" in message_lower:
                tomorrow = today + timedelta(days=1)
                return get_appointments(date=tomorrow.strftime("%Y-%m-%d"))
            weekdays = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6
            }
            for day, index in weekdays.items():
                if day in message_lower:
                    today_weekday = today.weekday()

                    days_ahead = index - today_weekday
                    if days_ahead <= 0:
                        days_ahead += 7 
                    target_date = today + timedelta(days=days_ahead)
                    return get_appointments(date=target_date.strftime("%Y-%m-%d"))
        return get_appointments()

    if intent == "doctor":
        conversation_state.clear()

        dept_keywords = {
            "dentist", "cardiac", "checkup", "surgery",
            "consultation", "therapy", "treatment", "physio",
            "scan", "xray", "blood test", "lab", "medical"
        }

        # ✅ STEP 0: handle ALL doctors
        if any(word in message_lower for word in ["all", "list", "every"]):
            return get_all_doctors()

        # ✅ STEP 1: RULE-BASED department detection (HIGH PRIORITY ✅)
        dept = None
        for d in dept_keywords:
            if d in message_lower:
                dept = d
                break

        # ✅ STEP 2: extract name
        stop_words = {
            "show", "doctor", "doctors", "for",
            "available", "which", "in", "department"
        }

        words = message_lower.split()
        filtered = [w for w in words if w not in stop_words]

        name = None
        if filtered:
            candidate = filtered[0]
            if candidate not in dept_keywords:
                name = candidate

        # ✅ CASE 1: patient name → PRIORITY
        if name:
            return get_doctors_by_patient(name)

        # ✅ CASE 2: department
        if dept:
            return get_doctors_by_department(dept)

        # ✅ STEP 3: ONLY NOW use LangChain (fallback)
        dept_llm = extract_department(message)
        if dept_llm:
            return get_doctors_by_department(dept_llm)

        # ✅ FINAL: return all
        return get_all_doctors()

    return "I am your appointment assistant. I can help you create or view bookings. How may I assist you today?"

# show bookings between 23 January 2021 and 27 September 2026
# show doctor for {department name}