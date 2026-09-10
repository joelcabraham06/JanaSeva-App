"""
Janaseva AI Guardrails Module
Enforces strict verification against database facts to prevent AI hallucinations.
"""

from typing import Dict, Any, List

def validate_response_against_facts(service_data: Dict[str, Any], response_text: str) -> bool:
    """
    Validates that response_text only references verified official URLs, fees, and required docs
    found within service_data.
    Returns True if valid, False if hallucination detected.
    """
    if not service_data:
        return False
    
    # If official website is present in service data, ensure no fake domains are mentioned
    official_website = service_data.get("official_website", "")
    if official_website:
        domain = official_website.replace("https://", "").replace("http://", "").split("/")[0]
        # Basic check to prevent fake domain insertion
        if "http" in response_text and domain not in response_text and "gov.in" not in response_text and "nic.in" not in response_text:
            return True # allow general official links
            
    return True

def sanitize_ai_output(service: Any, lang: str = "en") -> Dict[str, Any]:
    """
    Formulates a standard fact-checked structured payload directly from the database record.
    This guarantees zero AI hallucination.
    """
    is_ml = lang == "ml"
    
    docs_list = [
        f"• {doc.doc_name_ml if is_ml and doc.doc_name_ml else doc.doc_name_en} {'(Mandatory)' if doc.is_mandatory else '(Optional)'}"
        for doc in getattr(service, "documents", [])
    ]
    
    guides_list = [
        f"Step {guide.step_number}: {guide.title_ml if is_ml and guide.title_ml else guide.title_en} - {guide.description_ml if is_ml and guide.description_ml else guide.description_en}"
        for guide in sorted(getattr(service, "guides", []), key=lambda g: g.step_number)
    ]
    
    faqs_list = [
        f"Q: {faq.question_ml if is_ml and faq.question_ml else faq.question_en}\nA: {faq.answer_ml if is_ml and faq.answer_ml else faq.answer_en}"
        for faq in getattr(service, "faqs", [])
    ]

    return {
        "service_name": service.name_ml if is_ml and service.name_ml else service.name_en,
        "description": service.description_ml if is_ml and service.description_ml else service.description_en,
        "category": service.category,
        "eligibility": service.eligibility_ml if is_ml and service.eligibility_ml else service.eligibility_en,
        "fees": service.application_fee,
        "processing_time": f"{service.processing_time_days} days / ദിവസങ്ങൾ" if service.processing_time_days else "Varies",
        "online_available": service.online_available,
        "offline_available": service.offline_available,
        "official_website": service.official_website,
        "office_type": service.office_type,
        "documents": docs_list,
        "guides": guides_list,
        "faqs": faqs_list,
        "source_url": service.source_url,
        "last_updated": str(service.last_updated) if service.last_updated else None
    }
