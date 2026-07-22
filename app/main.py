from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.database import create_tables
from app.api.contact import router as contact_router
from app.core.config import settings
from app.core.config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    setup_logging()
    create_tables()

    yield

    # shutdown
    pass


def create_application() -> FastAPI:
    application = FastAPI(
        title="Developer Landing API",
        description="Backend API with AI integration",
        version="1.0.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        contact_router,
        prefix="/api",
    )

    return application


app = create_application()


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    from app.database.database import SessionLocal
    from app.models.contact import Contact

    db = SessionLocal()
    try:
        contacts = db.query(Contact).order_by(Contact.id.desc()).all()
    finally:
        db.close()

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #42b883;
                color: white;
                font-weight: 600;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .empty {
                text-align: center;
                padding: 40px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Панель администратора</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Имя</th>
                        <th>Email</th>
                        <th>Телефон</th>
                        <th>Комментарий</th>
                        <th>Категория</th>
                        <th>Сентимент</th>
                        <th>Создано</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    rows = ""
    if contacts:
        for contact in contacts:
            created_at = contact.created_at.strftime("%d.%m.%Y %H:%M:%S") if contact.created_at else "-"
            rows += f"""
                <tr>
                    <td>{contact.id}</td>
                    <td>{contact.name}</td>
                    <td>{contact.email}</td>
                    <td>{contact.phone or '-'}</td>
                    <td>{contact.comment}</td>
                    <td>{contact.ai_category or '-'}</td>
                    <td>{contact.ai_sentiment or '-'}</td>
                    <td>{created_at}</td>
                </tr>
            """
    else:
        rows = '<tr><td colspan="8" class="empty">Нет заявок</td></tr>'

    return HTMLResponse(content=html_content.replace("{rows}", rows))