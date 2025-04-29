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
from app.models import RSAPublicKey, RSAPairs

file_path = pathlib.Path(__file__).resolve()

NUM_KEYS_THRESHOLD = 50
KEYS_TO_GENERATE = 10


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Journalist DB session (full key pairs)
    with db_manager.get_journalist_session() as journalist_session:
        result = journalist_session.execute(
            select(RSAPairs).where(RSAPairs.is_used == False)
        )
        unused_keypairs = result.scalars().all()

        if len(unused_keypairs) < NUM_KEYS_THRESHOLD:
            keys_to_generate = KEYS_TO_GENERATE - len(unused_keypairs)
            print(f"Generating {keys_to_generate} new RSA key pairs...")

            for i in range(keys_to_generate):
                public_key, private_key = generate_rsa_keypair()

                rsa_pair = RSAPairs(
                    public_key_pem=public_key.encode(),
                    private_key_pem=private_key.encode(),
                    is_used=False,
                )
                journalist_session.add(rsa_pair)
                print(f"Generated RSA key pair {i + 1}")

            journalist_session.commit()

        # Reload unused key pairs after potential generation
        result = journalist_session.execute(
            select(RSAPairs).where(RSAPairs.is_used == False)
        )
        unused_keypairs = result.scalars().all()

    # WhistleDrop DB session (only public keys)
    with db_manager.get_whistle_session() as whistle_session:
        # Load public keys already present
        existing_pubkeys = whistle_session.execute(select(RSAPublicKey))
        existing_pems = {r.public_key_pem for r in existing_pubkeys.scalars().all()}

        new_pubkeys = 0
        for pair in unused_keypairs:
            if pair.public_key_pem not in existing_pems:
                whistle_session.add(RSAPublicKey(public_key_pem=pair.public_key_pem))
                new_pubkeys += 1

        if new_pubkeys:
            print(f"Added {new_pubkeys} new public keys to WhistleDrop DB.")
            whistle_session.commit()

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
