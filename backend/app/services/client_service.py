from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    @staticmethod
    def list_clients(database: Session) -> list[Client]:
        return list(database.scalars(select(Client).order_by(Client.created_at.desc())))

    @staticmethod
    def get_client(database: Session, client_id: int) -> Client | None:
        return database.get(Client, client_id)

    @staticmethod
    def create_client(database: Session, payload: ClientCreate) -> Client:
        client = Client(**payload.model_dump())
        database.add(client)
        ClientService._commit(database)
        database.refresh(client)
        return client

    @staticmethod
    def update_client(database: Session, client: Client, payload: ClientUpdate) -> Client:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(client, field, value)
        ClientService._commit(database)
        database.refresh(client)
        return client

    @staticmethod
    def delete_client(database: Session, client: Client) -> None:
        database.delete(client)
        database.commit()

    @staticmethod
    def _commit(database: Session) -> None:
        try:
            database.commit()
        except IntegrityError as error:
            database.rollback()
            raise ValueError("A client with this email already exists.") from error
