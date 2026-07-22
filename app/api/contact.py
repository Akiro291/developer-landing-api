from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.contact import ContactCreate, ContactResponse
from app.database.database import get_db
from app.repositories.contact_repository import create_contact_with_ai
from app.services.ai_service import ai_service
from app.services.email_service import email_service
from app.models.contact import Contact
import logging
from app.services.rate_limiter import rate_limiter
from app.services.metrics_service import metrics_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_endpoint(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    from fastapi import Request
    
    try:
        if not await rate_limiter.check_rate_limit():
            metrics_service.record_request(success=False)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        db_contact = await create_contact_with_ai(db, contact)
        
        metrics_service.record_request(success=True, ai_processed=True)
        
        logger.info(f"Contact created: {db_contact.id}")
        
        return db_contact
        
    except HTTPException:
        raise
    except Exception as e:
        metrics_service.record_request(success=False)
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create contact")

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        metrics_service.record_request(success=False)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact
