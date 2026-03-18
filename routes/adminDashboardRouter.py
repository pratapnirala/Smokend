# from fastapi import APIRouter, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
#
# adminDashboard = APIRouter()
# templates = Jinja2Templates(directory="templates")
#
#
# @adminDashboard.post("/admin/dashboard", response_class=HTMLResponse)
# async def admin_login_form(request: Request):
#     return templates.TemplateResponse("dashboard.html", {"request": request})
