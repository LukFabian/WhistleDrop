import pathlib
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from sqlalchemy import select
from app.api.deps import db_manager

from app.api.enryption_utils import generate_rsa_keypair
from app.api.main import api_router
from app.core.config import settings
from app.models import RSAPublicKey

file_path = pathlib.Path(__file__).resolve()

NUM_KEYS_THRESHOLD = 50
KEYS_TO_GENERATE = 10


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    with db_manager.get_session() as session:
        result = session.execute(
            select(RSAPublicKey).where(RSAPublicKey.is_used == False)
        )
        unused_keys = result.scalars().all()

        if len(unused_keys) < NUM_KEYS_THRESHOLD:
            remaining_keys = KEYS_TO_GENERATE - len(unused_keys)
            print(f"Generating {remaining_keys} new RSA keys...")

            for i in range(remaining_keys):
                public_key, private_key = generate_rsa_keypair()
                # Save public key to DB
                session.add(RSAPublicKey(public_key_pem=str.encode(public_key)))
                print(f"Generated RSA key number: {i + 1}")
            session.commit()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",  # Vite dev server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(api_router)
