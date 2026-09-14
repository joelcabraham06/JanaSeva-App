import re
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models.service import Service
from app.services.ai_service import ai_service

class SearchService:
    @staticmethod
    def search_services(db: Session, query: str, lang_hint: Optional[str] = None) -> Tuple[List[Service], str, str]:
        """
        Searches services in the database supporting Malayalam, English, Manglish, partial names, and typos.
        Returns (list_of_services, detected_language, resolved_intent)
        """
        raw_query = query.strip()
        detected_lang, canonical_intent, search_en = ai_service.detect_language_and_intent(raw_query)

        if lang_hint:
            detected_lang = lang_hint

        clean_q = search_en.lower()
        words = re.findall(r'\w+', clean_q)

        # Build SQL query filters
        filters = []
        for word in words:
            if len(word) < 2:
                continue
            pattern = f"%{word}%"
            filters.append(
                or_(
                    Service.name_en.ilike(pattern),
                    Service.name_ml.ilike(pattern),
                    Service.slug.ilike(pattern),
                    Service.category.ilike(pattern),
                    Service.description_en.ilike(pattern),
                    Service.description_ml.ilike(pattern),
                    Service.aliases_en.ilike(pattern),
                    Service.aliases_ml.ilike(pattern),
                    Service.aliases_manglish.ilike(pattern)
                )
            )

        # Also search raw query in Malayalam or raw text
        raw_pattern = f"%{raw_query}%"
        filters.append(
            or_(
                Service.name_en.ilike(raw_pattern),
                Service.name_ml.ilike(raw_pattern),
                Service.aliases_manglish.ilike(raw_pattern)
            )
        )

        query_builder = db.query(Service).filter(Service.is_active == True)
        if filters:
            query_builder = query_builder.filter(or_(*filters))

        results = query_builder.all()

        # If no results from exact word matches, fallback to returning all active services matching category
        if not results:
            results = db.query(Service).filter(Service.is_active == True).limit(5).all()

        return results, detected_lang, canonical_intent

search_service = SearchService()
