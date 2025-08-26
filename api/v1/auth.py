import jwt
import os
import time

from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

load_dotenv()

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    client_kwargs={"scope": "openid email profile"},
)

JWT_SECRET = os.environ["JWT_SECRET"]

def issue_jwt(userinfo: dict) -> str:
    payload = {
        "sub": userinfo["sub"],           # стабильный Google user id
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture"),
        "exp": int(time.time()) + 60 * 60,  # 1 час
        "iat": int(time.time()),
        "iss": "your-app"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


FRONTEND_REDIRECT_URL = os.getenv("FRONTEND_REDIRECT_URL", "http://127.0.0.1:5173/")

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {e.error}")

    # Получаем профиль пользователя (через id_token или userinfo endpoint)
    userinfo = token.get("userinfo")
    if not userinfo:
        # parse_id_token валидирует подпись Google и вернет claims
        userinfo = await oauth.google.parse_id_token(request, token)

    if not userinfo or not userinfo.get("email"):
        raise HTTPException(status_code=400, detail="Не удалось получить профиль пользователя")

    # TODO: здесь get_or_create пользователя в вашей БД по email или sub (Google ID)
    # user = await get_or_create_user(session, google_sub=userinfo["sub"], email=userinfo["email"], ...)

    # Выдаем свой JWT (или создаем серверную сессию)
    app_jwt = issue_jwt(userinfo)

    # Вариант 1: положить JWT в httpOnly cookie
    resp = RedirectResponse(url=FRONTEND_REDIRECT_URL)
    resp.set_cookie(
        key="access_token",
        value=app_jwt,
        httponly=True,
        secure=False, # в проде True
        samesite="lax",
        max_age=3600,
        path="/"
    )
    return resp
