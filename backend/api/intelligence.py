from fastapi import APIRouter, HTTPException
from backend.database.models import AskAnalystRequest, AskAnalystResponse
from backend.services.ai_service import ai_service
from backend.database.queries import get_all_trends, get_pipeline_logs
from backend.database.supabase import db_manager

router = APIRouter(tags=["Intelligence"])

@router.post("/intelligence/ask", response_model=AskAnalystResponse, summary="Ask the AI Fashion Intelligence Analyst")
async def ask_intelligence(req: AskAnalystRequest):
    """
    Submits inquiry to the Fashion Analyst. Factually grounded against live database trends and sources.
    """
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    trends = await get_all_trends()
    data = db_manager.load_all()
    sources_raw = data.get("sources", [])
    all_sources = []
    if isinstance(sources_raw, list):
        all_sources = sources_raw
    elif isinstance(sources_raw, dict):
        for srcs in sources_raw.values():
            if isinstance(srcs, list):
                all_sources.extend(srcs)
            else:
                all_sources.append(srcs)

    response = await ai_service.answer_analyst_question(q, trends, all_sources)

    return AskAnalystResponse(**response)
