
import typer
import uvicorn

from imghst.app.app import app
from imghst.app.configuration.configuration import Configuration

cli_app = typer.Typer()



@cli_app.command()
def run(portNumber: int = Configuration.port_number_to_run_on):
    uvicorn.run(app, port=portNumber)


if __name__ == "__main__":
    cli_app()
