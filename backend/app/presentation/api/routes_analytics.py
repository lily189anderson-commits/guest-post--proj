from fastapi import APIRouter, Depends

from app.application.services.analytics_service import AnalyticsService
from app.presentation.api.deps import get_analytics_service, get_current_username
from app.presentation.schemas.analytics_schema import AnalyticsSummaryResponse, ClientRevenueResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"], dependencies=[Depends(get_current_username)])


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_summary(service: AnalyticsService = Depends(get_analytics_service)):
    summary = service.summary()
    return AnalyticsSummaryResponse(
        total_revenue_collected=summary.total_revenue_collected,
        total_revenue_expected=summary.total_revenue_expected,
        total_pending=summary.total_pending,
        total_orders=summary.total_orders,
        per_client=[
            ClientRevenueResponse(
                client_id=c.client_id, client_name=c.client_name,
                total_orders=c.total_orders, total_earned=c.total_earned,
                total_pending=c.total_pending,
            )
            for c in summary.per_client
        ],
    )
