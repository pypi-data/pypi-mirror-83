import typer
from db_json.server import Server
from db_json.core import Core

app = typer.Typer()


@app.command()
def db_file(
    path_to_db_file: str, host: str = "127.0.0.1", port: int = 8000
) -> None:
    server = Server(core=Core(path_to_db_file))
    server.run(host=host, port=port)
