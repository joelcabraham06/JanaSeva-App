from typing import Dict, Any, Tuple, List
from sqlalchemy.orm import Session

from app.models.user import User, UserPreference
from app.models.service import Service, ServiceDocument

class ReadinessService:
    @staticmethod
    def start_readiness_check(db: Session, user: User, service: Service) -> Tuple[str, List[Dict[str, str]]]:
        """
        Starts the document readiness checklist for a service.
        Returns (question_prompt, buttons_list).
        """
        pref = user.preferences
        if not pref:
            pref = UserPreference(user_id=user.id)
            db.add(pref)

        mandatory_docs = [d for d in service.documents if d.is_mandatory]

        if not mandatory_docs:
            is_ml = user.preferred_language == "ml"
            msg = "ഈ സേവനത്തിന് പ്രത്യേകം രേഖകൾ സമർപ്പിക്കേണ്ടതില്ല. നിങ്ങൾക്ക് നേരിട്ട് അപേക്ഷിക്കാം! 🚀" if is_ml else "No mandatory documents required for this service. You are ready to apply! 🚀"
            return msg, []

        pref.session_state = "READINESS_CHECK"
        pref.active_service_id = service.id
        pref.current_step_index = 0
        pref.readiness_answers = {}
        db.commit()

        first_doc = mandatory_docs[0]
        return ReadinessService._format_doc_question(first_doc, user.preferred_language, 1, len(mandatory_docs))

    @staticmethod
    def process_answer(db: Session, user: User, answer_yes: bool) -> Tuple[str, List[Dict[str, str]]]:
        """
        Processes the user's Yes/No response for the current document.
        Advances to the next document question or generates the final readiness verdict.
        """
        pref = user.preferences
        if not pref or pref.session_state != "READINESS_CHECK" or not pref.active_service_id:
            return "സേവനം ലഭ്യമല്ല. ദയവായി വീണ്ടും സേവനം തിരയുക.", []

        service = db.query(Service).filter(Service.id == pref.active_service_id).first()
        if not service:
            pref.session_state = "IDLE"
            db.commit()
            return "Service not found.", []

        mandatory_docs = [d for d in service.documents if d.is_mandatory]
        current_idx = pref.current_step_index or 0

        # Store answer
        current_doc = mandatory_docs[current_idx]
        answers = dict(pref.readiness_answers or {})
        answers[str(current_doc.id)] = answer_yes
        pref.readiness_answers = answers

        next_idx = current_idx + 1

        if next_idx < len(mandatory_docs):
            pref.current_step_index = next_idx
            db.commit()
            next_doc = mandatory_docs[next_idx]
            return ReadinessService._format_doc_question(next_doc, user.preferred_language, next_idx + 1, len(mandatory_docs))
        else:
            # Completed all checklist items
            pref.session_state = "IDLE"
            db.commit()
            return ReadinessService._generate_final_summary(service, mandatory_docs, answers, user.preferred_language)

    @staticmethod
    def _format_doc_question(doc: ServiceDocument, lang: str, current: int, total: int) -> Tuple[str, List[Dict[str, str]]]:
        is_ml = lang == "ml"
        doc_name = doc.doc_name_ml if is_ml and doc.doc_name_ml else doc.doc_name_en
        
        prompt = (
            f"📋 *Document Readiness Check ({current}/{total})*\n\n"
            f"{'നിങ്ങളുടെ പക്കൽ താഴെ പറയുന്ന രേഖയുണ്ടോ?' if is_ml else 'Do you have the following document?'}\n\n"
            f"👉 *{doc_name}*"
        )
        buttons = [
            {"id": "btn_yes", "title": "ഉണ്ട് (Yes)" if is_ml else "Yes"},
            {"id": "btn_no", "title": "ഇല്ല (No)" if is_ml else "No"}
        ]
        return prompt, buttons

    @staticmethod
    def _generate_final_summary(service: Service, docs: List[ServiceDocument], answers: Dict[str, bool], lang: str) -> Tuple[str, List[Dict[str, str]]]:
        is_ml = lang == "ml"
        missing_docs = []

        for doc in docs:
            has_doc = answers.get(str(doc.id), False)
            if not has_doc:
                missing_name = doc.doc_name_ml if is_ml and doc.doc_name_ml else doc.doc_name_en
                missing_docs.append(f"❌ {missing_name}")

        service_name = service.name_ml if is_ml and service.name_ml else service.name_en

        if not missing_docs:
            summary = (
                f"✅ *നിങ്ങൾ അപേക്ഷിക്കാൻ തയ്യാറാണ്! (Ready to Apply)*\n\n"
                f"🏛️ *{service_name}* അപേക്ഷിക്കുന്നതിന് ആവശ്യമായ എല്ലാ രേഖകളും നിങ്ങളുടെ പക്കലുണ്ട്.\n\n"
                f"🌐 ഔദ്യോഗിക വെബ്സൈറ്റ്: {service.official_website}\n"
                f"🏢 സമർപ്പിക്കേണ്ട ഓഫീസ്: {service.office_type}\n\n"
                f"💡 ഘട്ടം ഘട്ടമായുള്ള വഴികാട്ടി ലഭിക്കാൻ 'Guide' എന്ന് ടൈപ്പ് ചെയ്യുക."
            ) if is_ml else (
                f"✅ *You are ready to apply!*\n\n"
                f"You have all required mandatory documents for *{service_name}*.\n\n"
                f"🌐 Official Website: {service.official_website}\n"
                f"🏢 Submitting Office: {service.office_type}\n\n"
                f"💡 Type 'Guide' to see step-by-step application walkthrough."
            )
        else:
            missing_str = "\n".join(missing_docs)
            summary = (
                f"⚠️ *ചില രേഖകൾ അപൂർണ്ണമാണ് (Missing Documents)*\n\n"
                f"🏛️ *{service_name}* അപേക്ഷിക്കുന്നതിന് താഴെ പറയുന്ന രേഖകൾ കൂടെ ലഭ്യമാക്കേണ്ടതുണ്ട്:\n\n"
                f"{missing_str}\n\n"
                f"💡 രേഖകൾ സംഘടിപ്പിച്ച ശേഷം വീണ്ടും അപേക്ഷിക്കുക."
            ) if is_ml else (
                f"⚠️ *Missing Required Documents*\n\n"
                f"You are missing the following mandatory documents for *{service_name}*:\n\n"
                f"{missing_str}\n\n"
                f"Please obtain these documents before submitting your application."
            )

        return summary, []

readiness_service = ReadinessService()
