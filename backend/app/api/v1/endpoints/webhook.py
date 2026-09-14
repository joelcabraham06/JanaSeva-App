import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserPreference
from app.models.conversation import ConversationLog
from app.services.whatsapp_service import whatsapp_service
from app.services.search_service import search_service
from app.services.ai_service import ai_service
from app.services.readiness_service import readiness_service
from app.core.guardrails import sanitize_ai_output
from app.schemas.webhook import WhatsAppSimulatorRequest, WhatsAppSimulatorResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/whatsapp")
def verify_whatsapp_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Meta WhatsApp Cloud API Webhook Verification Endpoint.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp Webhook verified successfully.")
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/whatsapp")
async def receive_whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Meta WhatsApp Cloud API Webhook Message Handler.
    """
    body = await request.json()
    logger.info(f"Incoming WhatsApp Webhook Payload: {body}")
    
    # Extract message entries
    entries = body.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])
            for msg in messages:
                from_phone = msg.get("from")
                msg_type = msg.get("type")
                
                text_body = ""
                if msg_type == "text":
                    text_body = msg.get("text", {}).get("body", "")
                elif msg_type == "interactive":
                    text_body = msg.get("interactive", {}).get("button_reply", {}).get("title", "")
                    
                if from_phone and text_body:
                    await _process_whatsapp_message(db, from_phone, text_body, msg_type)

    return {"status": "processed"}

@router.post("/simulator", response_model=WhatsAppSimulatorResponse)
async def process_simulator_message(payload: WhatsAppSimulatorRequest, db: Session = Depends(get_db)):
    """
    Local Interactive WhatsApp Simulator API Endpoint.
    Allows end-to-end testing of user conversation flows in real time.
    """
    phone = payload.phone_number
    user_input = payload.text_body or payload.button_payload or ""
    
    reply_text, buttons, lang = await _process_whatsapp_message(
        db, phone, user_input, payload.message_type
    )

    return WhatsAppSimulatorResponse(
        status="success",
        user_phone=phone,
        reply_text=reply_text,
        interactive_buttons=buttons,
        language=lang
    )

async def _process_whatsapp_message(db: Session, phone: str, message_text: str, msg_type: str):
    """
    Core conversation processor for both live WhatsApp & Simulator.
    """
    # 1. Fetch or create user
    user = db.query(User).filter(User.phone_number == phone).first()
    is_new = False
    if not user:
        user = User(phone_number=phone, preferred_language="ml")
        db.add(user)
        db.flush()
        db.add(UserPreference(user_id=user.id, session_state="SELECT_LANG"))
        db.commit()
        db.refresh(user)
        is_new = True

    pref = user.preferences
    if not pref:
        pref = UserPreference(user_id=user.id, session_state="IDLE")
        db.add(pref)
        db.commit()

    clean_text = message_text.strip().lower()

    # 2. Check for explicit Language Selection request or initial user greeting
    if is_new or clean_text in ["hi", "hello", "start", "menu", "ഭാഷ", "language", "change language"]:
        pref.session_state = "IDLE"
        db.commit()
        reply_text = (
            "🙏 *Janaseva - Government Service Assistant*\n"
            "ജനസേവ സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:\n\n"
            "Welcome! Choose your preferred language:"
        )
        buttons = [
            {"id": "lang_ml", "title": "മലയാളം (Malayalam)"},
            {"id": "lang_en", "title": "English"}
        ]
        await whatsapp_service.send_interactive_buttons(phone, "Janaseva Language", reply_text, buttons)
        return reply_text, buttons, user.preferred_language

    # Handle language choice selection button replies
    if clean_text in ["മലയാളം (malayalam)", "lang_ml", "1", "malayalam"]:
        user.preferred_language = "ml"
        db.commit()
        reply_text = (
            "✅ *ഭാഷ മലയാളമായി മാറ്റി.*\n\n"
            "ഏത് സർക്കാർ സേവനത്തെക്കുറിച്ചാണ് വിവരം വേണ്ടത്?\n"
            "ഉദാഹരണത്തിന്:\n"
            "• 'ലൈസൻസ് പുതുക്കണം'\n"
            "• 'പാസ്പോർട്ട് അപേക്ഷ'\n"
            "• 'റേഷൻ കാർഡ് തിരുത്തൽ'"
        )
        await whatsapp_service.send_text_message(phone, reply_text)
        return reply_text, [], "ml"

    if clean_text in ["english", "lang_en", "2"]:
        user.preferred_language = "en"
        db.commit()
        reply_text = (
            "✅ *Language updated to English.*\n\n"
            "Which government service do you need information about?\n"
            "Examples:\n"
            "• 'Renew Driving Licence'\n"
            "• 'Apply Passport'\n"
            "• 'Ration Card Correction'"
        )
        await whatsapp_service.send_text_message(phone, reply_text)
        return reply_text, [], "en"

    # 3. Handle Active Document Readiness Flow
    if pref.session_state == "READINESS_CHECK":
        if "yes" in clean_text or "ഉണ്ട്" in clean_text or "btn_yes" in clean_text:
            reply_text, buttons = readiness_service.process_answer(db, user, True)
        elif "no" in clean_text or "ഇല്ല" in clean_text or "btn_no" in clean_text:
            reply_text, buttons = readiness_service.process_answer(db, user, False)
        else:
            reply_text = "ദയവായി 'ഉണ്ട് (Yes)' അല്ലെങ്കിൽ 'ഇല്ല (No)' തിരഞ്ഞെടുക്കുക." if user.preferred_language == "ml" else "Please answer 'Yes' or 'No'."
            buttons = [{"id": "btn_yes", "title": "Yes"}, {"id": "btn_no", "title": "No"}]

        if buttons:
            await whatsapp_service.send_interactive_buttons(phone, "Readiness Check", reply_text, buttons)
        else:
            await whatsapp_service.send_text_message(phone, reply_text)

        return reply_text, buttons, user.preferred_language

    # 4. Handle Checklist Trigger for last active service
    if clean_text in ["checklist", "check", "രേഖകൾ", "readiness"]:
        if pref.active_service_id:
            service = db.query(Service).filter(Service.id == pref.active_service_id).first()
            if service:
                reply_text, buttons = readiness_service.start_readiness_check(db, user, service)
                await whatsapp_service.send_interactive_buttons(phone, "Document Readiness", reply_text, buttons)
                return reply_text, buttons, user.preferred_language

    # 5. Perform Service Search & Intent Resolution
    results, detected_lang, canonical_intent = search_service.search_services(
        db, message_text, lang_hint=user.preferred_language
    )

    buttons = []
    if results:
        top_service = results[0]
        pref.active_service_id = top_service.id
        db.commit()

        facts = sanitize_ai_output(top_service, lang=user.preferred_language)
        reply_text = ai_service.format_factual_response(facts, lang=user.preferred_language)

        buttons = [
            {"id": "btn_checklist", "title": "Checklist (രേഖകൾ)"},
            {"id": "btn_website", "title": "Official Link"}
        ]
        await whatsapp_service.send_text_message(phone, reply_text)
    else:
        is_ml = user.preferred_language == "ml"
        reply_text = (
            "ക്ഷമിക്കണം, താങ്കൾ ആവശ്യപ്പെട്ട സർക്കാർ സേവനം കണ്ടെത്താൻ കഴിഞ്ഞില്ല. ദയവായി മറ്റൊരു വാക്ക് ഉപയോഗിച്ച് തിരയുക."
            if is_ml else
            "Sorry, could not locate a matching government service. Please try searching with a different term."
        )
        await whatsapp_service.send_text_message(phone, reply_text)

    # 6. Log Conversation
    db.add(
        ConversationLog(
            user_id=user.id,
            input_type=msg_type,
            raw_input=message_text,
            detected_language=detected_lang,
            resolved_intent=canonical_intent,
            response_text=reply_text
        )
    )
    db.commit()

    return reply_text, buttons, user.preferred_language
