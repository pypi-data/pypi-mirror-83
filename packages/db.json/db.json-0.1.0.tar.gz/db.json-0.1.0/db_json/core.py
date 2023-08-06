import json
from pathlib import Path

import typer

from db_json.data_structures import RoutesMap, RouteModel


class Core:
    def __init__(self, path_to_db_file: str):
        self.routes_map = self.load_data(path_to_db_file)

    @staticmethod
    def check_db_file(path_to_db_file: str) -> Path:
        db_file = Path(path_to_db_file)
        if not db_file.exists():
            typer.echo(f"File({path_to_db_file}) not found!")
            raise typer.Exit(1)
        elif not db_file.is_file():
            typer.echo(f"`{path_to_db_file}` must be file!")
            raise typer.Exit(1)
        return db_file

    def load_data(self, path_to_db_file: str) -> RoutesMap:
        db_file = self.check_db_file(path_to_db_file)
        with db_file.open() as f:
            try:
                data = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                typer.echo(f"Not valid json file({db_file.resolve()})!")
                raise typer.Exit(1)
            else:
                success_msg = typer.style("Success!", fg=typer.colors.GREEN)
                typer.echo(f"{success_msg} DB file path={db_file.resolve()}")

        return RoutesMap(
            routes=[
                RouteModel(
                    path=path,
                    response=response,
                )
                for path, response in data.items()
            ]
        )
