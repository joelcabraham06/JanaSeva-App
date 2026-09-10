import json
import logging
from typing import Dict, Any, Tuple
from app.core.config import settings

logger = logging.getLogger(__name__)

# Pre-compiled comprehensive Manglish mapping dictionary for all 17 government services
MANGLISH_INTENT_MAP = {
    # 1. Driving Licence Renewal
    "license puthukkanam": "renew driving licence",
    "license puthukanam": "renew driving licence",
    "licence puthukkanam": "renew driving licence",
    "licence puthukanam": "renew driving licence",
    "licence puthukal": "renew driving licence",
    "laisenso puthukkanam": "renew driving licence",
    "laicense puthukkanam": "renew driving licence",
    "licens puthukanam": "renew driving licence",
    "dl renewal": "renew driving licence",
    "dl renew": "renew driving licence",
    "dl puthukkanam": "renew driving licence",
    "driving licence renewal": "renew driving licence",
    "driving license renewal": "renew driving licence",
    "licence navikarikkanam": "renew driving licence",

    # 2. New Driving Licence
    "license edukkanam": "driving licence",
    "licence edukkanam": "driving licence",
    "puthiya license": "driving licence",
    "new driving licence": "driving licence",
    "new driving license": "driving licence",
    "dl apply": "driving licence",

    # 3. Learner's Licence
    "learners license": "learner's licence",
    "learner license": "learner's licence",
    "learners test": "learner's licence",
    "learner test": "learner's licence",
    "learners licence": "learner's licence",
    "ll apply": "learner's licence",

    # 4. Aadhaar Card Update / Correction
    "aadhaar update": "aadhaar update",
    "adhar update": "aadhaar update",
    "aadhar update": "aadhaar update",
    "aadhaar correction": "aadhaar update",
    "adhar correction": "aadhaar update",
    "aadhar card change": "aadhaar update",
    "adhar name change": "aadhaar update",
    "adhar address change": "aadhaar update",
    "adhar phone link": "aadhaar update",
    "aadhaar thiruthanam": "aadhaar update",
    "adhaar card": "aadhaar update",

    # 5. PAN Card Application / Correction
    "pan card": "pan card",
    "pancard": "pan card",
    "pan edukkanam": "pan card",
    "new pan card": "pan card",
    "pan card apply": "pan card",
    "pan card correction": "pan card",

    # 6. Passport Application / Renewal
    "passport": "passport",
    "pasport": "passport",
    "pass port": "passport",
    "passport edukkanam": "passport",
    "pasport edukkanam": "passport",
    "new passport": "passport",
    "passport apply": "passport",
    "pasport apply": "passport",
    "passport renewal": "passport",
    "passport navikarikkanam": "passport",

    # 7. Birth Certificate
    "birth certificate": "birth certificate",
    "janana certificate": "birth certificate",
    "janma certificate": "birth certificate",
    "janana sarathifikat": "birth certificate",
    "janma sarathifikat": "birth certificate",
    "birth certificate apply": "birth certificate",

    # 8. Death Certificate
    "death certificate": "death certificate",
    "marana certificate": "death certificate",
    "marana sarathifikat": "death certificate",
    "death certificate apply": "death certificate",

    # 9. Income Certificate
    "income certificate": "income certificate",
    "varamana certificate": "income certificate",
    "varamana sarathifikat": "income certificate",
    "income certificate apply": "income certificate",
    "varamana certificate edukkanam": "income certificate",

    # 10. Community / Caste Certificate
    "community certificate": "community certificate",
    "caste certificate": "community certificate",
    "jaathi certificate": "community certificate",
    "jathi certificate": "community certificate",
    "jaathi sarathifikat": "community certificate",
    "community sarathifikat": "community certificate",

    # 11. Residence Certificate
    "residence certificate": "residence certificate",
    "thalamasam certificate": "residence certificate",
    "thamasasathram": "residence certificate",
    "residence sarathifikat": "residence certificate",
    "natavasi certificate": "residence certificate",

    # 12. Ration Card
    "ration card": "ration card",
    "rashan card": "ration card",
    "raashen card": "ration card",
    "ration card edukkanam": "ration card",
    "ration card maattanum": "ration card",
    "ration card name add": "ration card",
    "ration card thiruthanam": "ration card",

    # 13. Voter ID
    "voter id": "voter id",
    "vottar id": "voter id",
    "vote id": "voter id",
    "voter card": "voter id",
    "voter list": "voter id",
    "voter id apply": "voter id",

    # 14. Pension Schemes
    "pension": "pension schemes",
    "penshan": "pension schemes",
    "vayo pension": "pension schemes",
    "old age pension": "pension schemes",
    "disability pension": "pension schemes",
    "pension apply": "pension schemes",
    "kshama pension": "pension schemes",

    # 15. Welfare Schemes (Karunya / KSRTC)
    "welfare schemes": "welfare schemes",
    "ksrtc concession": "welfare schemes",
    "karunya": "welfare schemes",
    "karunya benevola": "welfare schemes",
    "welfare card": "welfare schemes",

    # 16. Vehicle Registration
    "vehicle registration": "vehicle registration",
    "vandi registration": "vehicle registration",
    "new rc": "vehicle registration",
    "rc book": "vehicle registration",

    # 17. Vehicle Transfer
    "vehicle transfer": "vehicle transfer",
    "vandi maattal": "vehicle transfer",
    "rc transfer": "vehicle transfer",
    "owner change": "vehicle transfer",
    "rc owner change": "vehicle transfer"
}

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client: {e}")

    def detect_language_and_intent(self, text_query: str) -> Tuple[str, str, str]:
        """
        Detects language ('ml', 'en', 'manglish'), standard intent, and translated English search query.
        Supports fuzzy matching across Manglish variations and misspellings.
        """
        clean_text = text_query.strip().lower()

        # Check Manglish dictionary first
        for key, intent in MANGLISH_INTENT_MAP.items():
            if key in clean_text:
                return "manglish", intent, intent

        # Unicode detection for Malayalam characters (\u0D00 to \u0D7F)
        has_malayalam = any("\u0d00" <= char <= "\u0d7f" for char in text_query)
        detected_lang = "ml" if has_malayalam else "en"

        # Try Gemini API if available
        if self.client:
            try:
                prompt = (
                    "You are an NLP analyzer for Indian & Kerala government service requests.\n"
                    f"Analyze query: '{text_query}'.\n"
                    "Return ONLY valid JSON with keys:\n"
                    "- language: 'ml', 'en', or 'manglish'\n"
                    "- canonical_intent: string short service name (e.g. 'passport', 'renew driving licence', 'income certificate')\n"
                    "- search_keywords_en: English query string\n"
                )
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                content = response.text.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                data = json.loads(content)
                return data.get("language", detected_lang), data.get("canonical_intent", text_query), data.get("search_keywords_en", text_query)
            except Exception as e:
                logger.warning(f"Gemini API intent resolution fallback triggered: {e}")

        return detected_lang, text_query, text_query

    def format_factual_response(self, service_facts: Dict[str, Any], lang: str = "en") -> str:
        """
        Formats structured database facts into a clear, natural WhatsApp markdown message in user's language.
        No facts are generated by AI.
        """
        is_ml = lang == "ml" or lang == "manglish"

        if is_ml:
            header = f"🏛️ *{service_facts['service_name']}*\n_{service_facts['description']}_\n"
            
            # Documents list with checkmarks
            docs_list = service_facts['documents']
            if docs_list:
                formatted_docs = "\n".join([f"  • {doc}" for doc in docs_list])
            else:
                formatted_docs = "  • പ്രത്യേക രേഖകൾ ആവശ്യമില്ല"
                
            # Guides with numbered steps
            guides_list = service_facts['guides']
            if guides_list:
                formatted_guides = "\n".join([f"{i+1}️⃣ {guide}" for i, guide in enumerate(guides_list)])
            else:
                formatted_guides = "ഘട്ടങ്ങൾ അക്ഷയ സെന്ററിൽ ലഭ്യമാണ്."
            
            body = (
                f"{header}\n"
                f"📋 *ആവശ്യമായ രേഖകൾ (Required Documents):*\n{formatted_docs}\n\n"
                f"💰 *അപേക്ഷാ ഫീസ് (Fees):* {service_facts['fees']}\n"
                f"⏱️ *പ്രോസസ്സിംഗ് സമയം (Time):* {service_facts['processing_time']}\n"
                f"🏢 *അപേക്ഷിക്കേണ്ട ഓഫീസ് (Office):* {service_facts['office_type']}\n"
                f"🌐 *ഔദ്യോഗിക വെബ്സൈറ്റ് (Website):* {service_facts['official_website']}\n\n"
                f"📝 *അപേക്ഷിക്കുന്ന ഘട്ടങ്ങൾ (Step-by-Step Guide):*\n{formatted_guides}\n\n"
                f"💡 കൂടുതൽ വിവരങ്ങൾക്ക് *'Checklist'* എന്ന് ടൈപ്പ് ചെയ്യുക."
            )
        else:
            header = f"🏛️ *{service_facts['service_name']}*\n_{service_facts['description']}_\n"
            
            # Documents list with checkmarks
            docs_list = service_facts['documents']
            if docs_list:
                formatted_docs = "\n".join([f"  • {doc}" for doc in docs_list])
            else:
                formatted_docs = "  • No special documents required"

            # Guides with numbered steps
            guides_list = service_facts['guides']
            if guides_list:
                formatted_guides = "\n".join([f"{i+1}️⃣ {guide}" for i, guide in enumerate(guides_list)])
            else:
                formatted_guides = "Steps available at nearest Akshaya Center."

            body = (
                f"{header}\n"
                f"📋 *Required Documents:*\n{formatted_docs}\n\n"
                f"💰 *Application Fee:* {service_facts['fees']}\n"
                f"⏱️ *Processing Time:* {service_facts['processing_time']}\n"
                f"🏢 *Office:* {service_facts['office_type']}\n"
                f"🌐 *Official Website:* {service_facts['official_website']}\n\n"
                f"📝 *Step-by-Step Guide:*\n{formatted_guides}\n\n"
                f"💡 Type *'Checklist'* to verify your document readiness."
            )

        return body

ai_service = AIService()
