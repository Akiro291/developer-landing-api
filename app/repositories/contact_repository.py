from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.contact import Contact
from app.schemas.contact import ContactCreate
from app.services.ai_service import ai_service
from app.services.email_service import email_service
import logging

logger = logging.getLogger(__name__)

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        comment=contact.comment,
        ai_category=None,
        ai_sentiment=None,
        ai_response=None,
        created_at=datetime.utcnow()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    logger.info(f"Contact created: {db_contact.id}")
    return db_contact

async def create_contact_with_ai(db: Session, contact: ContactCreate) -> Contact:
    try:
        db_contact = create_contact(db, contact)
        
        ai_analysis = await ai_service.analyze_comment(contact.comment)
        
        if ai_analysis:
            db_contact.ai_category = ai_analysis.get("category")
            db_contact.ai_sentiment = ai_analysis.get("sentiment")
            db_contact.ai_response = ai_analysis.get("response")
            db.commit()
            db.refresh(db_contact)
        
        try:
            await email_service.send_owner_notification(contact)
        except Exception as e:
            logger.error(f"Failed to send owner notification: {e}")
        
        try:
            await email_service.send_user_confirmation(contact)
        except Exception as e:
            logger.error(f"Failed to send user confirmation: {e}")
        
        logger.info(f"Contact {db_contact.id} processed with AI")
        return db_contact
        
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise

def get_contact_by_id(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_all_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def update_contact_ai_data(db: Session, contact_id: int, ai_category: str, ai_sentiment: str, ai_response: str) -> Optional[Contact]:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.ai_category = ai_category
        contact.ai_sentiment = ai_sentiment
        contact.ai_response = ai_response
        db.commit()
        db.refresh(contact)
        logger.info(f"Updated AI data for contact: {contact_id}")
    return contact
