from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.search_service import search_service
from app.services.ai_service import ai_service
from app.core.guardrails import sanitize_ai_output
from app.schemas.search import SearchQueryRequest, SearchQueryResponse, SearchResultItem
from app.models.analytics import ServiceRequestStat, FailedSearchLog, DailyMetric
from datetime import date

router = APIRouter()

@router.post("/query", response_model=SearchQueryResponse)
def execute_search_query(payload: SearchQueryRequest, db: Session = Depends(get_db)):
    results, detected_lang, resolved_intent = search_service.search_services(
        db, payload.query, lang_hint=payload.language
    )

    items = []
    for s in results:
        items.append(
            SearchResultItem(
                id=s.id,
                slug=s.slug,
                category=s.category,
                name_en=s.name_en,
                name_ml=s.name_ml,
                description_en=s.description_en,
                description_ml=s.description_ml,
                score=1.0
            )
        )

    # Format factual response for top result if found
    if results:
        top_service = results[0]
        facts = sanitize_ai_output(top_service, lang=detected_lang)
        formatted_answer = ai_service.format_factual_response(facts, lang=detected_lang)

        # Track request stat
        stat = db.query(ServiceRequestStat).filter(ServiceRequestStat.service_id == top_service.id).first()
        if stat:
            stat.request_count += 1
        else:
            db.add(ServiceRequestStat(service_id=top_service.id, request_count=1))
    else:
        is_ml = detected_lang == "ml"
        formatted_answer = (
            "ക്ഷമിക്കണം, നിങ്ങൾ തിരഞ്ഞ സേവനം കണ്ടെത്താൻ സാധിച്ചില്ല. ദയവായി സേവനത്തിന്റെ പേര് കൃത്യമായി നൽകുക."
            if is_ml else
            "Sorry, could not find matching government service. Please try searching with a different keyword."
        )
        # Log failed search
        failed = db.query(FailedSearchLog).filter(FailedSearchLog.query_text == payload.query).first()
        if failed:
            failed.occurrence_count += 1
        else:
            db.add(FailedSearchLog(query_text=payload.query, user_language=detected_lang, occurrence_count=1))

    # Update daily metric
    daily = db.query(DailyMetric).filter(DailyMetric.metric_date == date.today()).first()
    if daily:
        daily.total_requests += 1
        if detected_lang == "ml":
            daily.malayalam_queries += 1
        elif detected_lang == "manglish":
            daily.manglish_queries += 1
        else:
            daily.english_queries += 1
    else:
        db.add(
            DailyMetric(
                metric_date=date.today(),
                total_requests=1,
                malayalam_queries=1 if detected_lang == "ml" else 0,
                manglish_queries=1 if detected_lang == "manglish" else 0,
                english_queries=1 if detected_lang == "en" else 0
            )
        )

    db.commit()

    return SearchQueryResponse(
        query=payload.query,
        detected_language=detected_lang,
        resolved_intent=resolved_intent,
        matched_services=items,
        formatted_answer=formatted_answer
    )
