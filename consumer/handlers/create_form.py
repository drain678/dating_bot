import logging.config
from typing import Any, Dict

from sqlalchemy.exc import SQLAlchemyError

from consumer.logger import LOGGING_CONFIG, logger
from src.model.model import GenderEnum, User
from src.storage.db import async_session


async def create_form(body: Dict[str, Any]) -> None:
    async with async_session() as db:
        logging.config.dictConfig(LOGGING_CONFIG)
        logger.info("Прием запроса", body)
        try:
            interests = ", ".join(body.get("interests", []))
            user = User(
                id=body.get("id"),
                name=body.get("name"),
                age=body.get("age"),
                gender=GenderEnum(body.get("preferred_gender")),
                city=body.get("city"),
                interests=interests,
                photo=body.get("photo"),
                preferred_gender=GenderEnum(body.get("preferred_gender")),
                preferred_age_min=body.get("preferred_age_min"),
                preferred_age_max=body.get("preferred_age_max"),
                preferred_city=body.get("preferred_city"),
            )

            db.add(user)
            await db.commit()
        except SQLAlchemyError as err:
            logger.error(err)
