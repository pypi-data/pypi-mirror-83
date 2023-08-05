import requests
from functools import wraps

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .CurrentUser import CurrentUser

from magicapi import g
import firebase_admin
from firebase_admin import auth

from .errors import DoormanAuthException
from magicapi.Decorators.firestore import need_firestore
from magicapi.FieldTypes import PhoneNumber

# from magicapi import settings
from magicapi import g
from magicapi.RouteClasses import MagicCallLogger

LOCATION, PROJECT_ID, DOORMAN_ID = (
    g.settings.cloud_function_location or "us-central1",
    g.settings.firebase_project_id,
    g.settings.doorman_public_project_id,
)

ID_TOKEN_ENDPOINT: str = f"https://{LOCATION}-{PROJECT_ID}.cloudfunctions.net/getIdToken"
DOORMAN_BACKEND_ENDPOINT: str = "https://sending-messages-for-doorman.herokuapp.com/phoneLogic"

doorman_prefix = "/doorman"
bare_token_path = f"{doorman_prefix}/token"
token_url = (
    bare_token_path if g.settings.local else f"/{g.settings.stage}{bare_token_path}"
)
oath2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

doorman_router = APIRouter(route_class=MagicCallLogger)


def need_doorman_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        doorman_vars = [LOCATION, PROJECT_ID, DOORMAN_ID]
        if None in doorman_vars:
            raise DoormanAuthException(
                message="Not all Doorman credentials found in .env file. Need DOORMAN_PUBLIC_PROJECT_ID, "
                "FIREBASE_PROJECT_ID, and CLOUD_FUNCTION_LOCATION"
            )
        return f(*args, **kwargs)

    return wrapper


@doorman_router.post("/login_with_phone")
@need_doorman_vars
def login_with_phone(phone_number: PhoneNumber):
    body = {
        "action": "loginWithPhone",
        "phoneNumber": phone_number,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    return resp


def sign_in_with_magic_link(form_data):
    body = {"email": form_data.username, "magicLink": form_data.password}

    magic_link_id_token_endpoint = ID_TOKEN_ENDPOINT.replace(
        "getIdToken", "getIdTokenFromMagicLink"
    )

    id_resp = requests.post(magic_link_id_token_endpoint, json=body).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        raise DoormanAuthException(message=str(id_resp))

    return {"access_token": id_token, "token_type": "bearer"}


@doorman_router.post("/token")
@need_doorman_vars
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if "@" in form_data.username:
        return sign_in_with_magic_link(form_data)
    body = {
        "action": "verifyCode",
        "phoneNumber": form_data.username,
        "code": form_data.password,
        "publicProjectId": DOORMAN_ID,
    }
    resp = requests.post(DOORMAN_BACKEND_ENDPOINT, json=body).json()
    backend_token = resp.get("token")
    if not backend_token:
        print(resp)
        raise DoormanAuthException(message=str(resp))

    id_resp = requests.post(ID_TOKEN_ENDPOINT, json={"token": backend_token}).json()
    id_token = id_resp.get("idToken")
    if not id_token:
        print(id_resp)
        raise DoormanAuthException(message=str(id_resp))

    return {"access_token": id_token, "token_type": "bearer"}


@need_firestore
def get_current_user(token: str = Depends(oath2_scheme)):
    try:
        decoded = auth.verify_id_token(token)
        current_user = CurrentUser(**decoded)
        return current_user
    except firebase_admin._token_gen.ExpiredIdTokenError as e:
        raise DoormanAuthException(message=e)


@need_firestore
def get_current_user_raw(token: str = Depends(oath2_scheme)):
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except firebase_admin._token_gen.ExpiredIdTokenError as e:
        raise DoormanAuthException(message=e)


GET_USER = Depends(get_current_user)

g.app.include_router(doorman_router, prefix=doorman_prefix, tags=["Doorman"])
