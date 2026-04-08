import typer
import os
from typing_extensions import Annotated
from juniorfetch.core.crawler import JuniorFetchCrawler

app = typer.Typer()

@app.command()
def index(
    path: Annotated[str, typer.Argument(help="Target directory to index")] = "~/Documents",
    max_files: Annotated[int, typer.Option(help="Maximum number of files to process")] = 100000
):
    typer.echo(f"Initializing JuniorFetch crawler on {path}...")
    crawler = JuniorFetchCrawler()
    crawler.index(path, max_files)

@app.command()
def dashboard():
    typer.echo("Booting JuniorFetch Workspace...")
    os.system("streamlit run juniorfetch/playground/app.py")

if __name__ == "__main__":
    app()