from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

adminRouter = APIRouter()
templates = Jinja2Templates(directory="templates")


@adminRouter.get("/", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@adminRouter.post("/", response_class=HTMLResponse, response_model=None)
def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})


@adminRouter.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
