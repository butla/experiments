from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_host: str = 'localhost'
    postgres_password: str = 'postgres'
    postgres_database: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_port: int = 5432

    @property
    def postgres_url(self) -> str:
        return (f'postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@'
                f'{self.postgres_host}:{self.postgres_port}/'
                f'{self.postgres_database}')
