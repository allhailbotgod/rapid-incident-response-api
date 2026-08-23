from fastapi import Depends, HTTPException, status

from app.auth.oauth2 import get_current_user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )

    return current_user


def require_dispatch(current_user=Depends(get_current_user)):
    if current_user.role.name != "dispatcher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )

    return current_user
