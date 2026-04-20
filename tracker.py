#!/usr/bin/env python3
"""macro-tracker-ma — Moroccan product macro tracker."""

import json
import click
from rich.console import Console
from rich.table import Table

console = Console()


def load_products():
    with open("data/marques.json") as f:
        return json.load(f)["produits"]


@click.group()
def cli():
    """Moroccan macro tracker."""
    pass


@cli.command()
@click.argument("query")
def search(query):
    """Search products by name."""
    products = load_products()
    table = Table(title=f"Results for: {query}")
    table.add_column("Nom", style="cyan")
    table.add_column("Protéines (g)", justify="right")
    table.add_column("Sans lactose")
    for p in products:
        if query.lower() in p["nom"].lower():
            table.add_row(
                p["nom"],
                str(p.get("proteines_g", "?")),
                "✓" if p.get("sans_lactose") else "✗"
            )
    console.print(table)


if __name__ == "__main__":
    cli()
