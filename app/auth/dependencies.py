from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from app.auth.dao import UserDaoMgr
from app.exceptions import AuthError
from app.security import auth_manager
from app.config import LOGIN_URL


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):

    async def __call__(self, request: Request):
        payload = await auth_manager._auth_required(request)
        user_id = payload.sub
        user = await UserDaoMgr.find(int(user_id))
        if user:
            request.state.user = user
        else:
            raise AuthError('登录用户无效')


oauth2_authentication = CustomOAuth2PasswordBearer(tokenUrl=LOGIN_URL)
