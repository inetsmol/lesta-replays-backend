@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
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
    resp = RedirectResponse(url="/me")
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

@app.get("/me")
async def me(request: Request):
    # Достаем JWT из куки
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Не авторизован"})

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Токен недействителен"})

    return {"user": {"email": payload.get("email"), "name": payload.get("name"), "picture": payload.get("picture")}}