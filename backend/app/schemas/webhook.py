from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class WhatsAppSimulatorRequest(BaseModel):
    phone_number: str = "919876543210"
    message_type: str = "text" # 'text', 'button_reply', 'interactive', 'voice'
    text_body: Optional[str] = None
    button_payload: Optional[str] = None
    voice_base64: Optional[str] = None

class WhatsAppSimulatorResponse(BaseModel):
    status: str = "success"
    user_phone: str
    reply_text: str
    interactive_buttons: Optional[List[Dict[str, str]]] = None
    language: str
