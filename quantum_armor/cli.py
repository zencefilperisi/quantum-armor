import click
from .scanner import scan_directory

@click.group()
@click.version_option("0.1.0", prog_name="Quantum-Armor")
def cli():
    """Quantum-Armor – Post-quantum cryptography audit tool"""
    pass

@cli.command()
@click.argument("path", type=click.Path(exists=True), default=".")
def scan(path):
    """Scan a directory for quantum-vulnerable cryptography"""
    click.secho("Quantum-Armor  Scanning for quantum-vulnerable algorithms…\n", fg="cyan", bold=True)

    findings = scan_directory(path)

    if not findings:
        click.secho("No vulnerable cryptography found – you're quantum-ready!", fg="green", bold=True)
        return

    total = sum(len(v) for v in findings.values())
    click.secho(f"Found {total} vulnerable usage(s):\n", fg="red", bold=True)

    for file, issues in findings.items():
        click.echo(click.style(f"{file}", bold=True))
        for issue in issues:
            click.echo(f"   • Line {issue['line']}: {issue['algo']} → Migrate to {issue['replacement']}")
        click.echo("")

    click.secho("Start migrating today: https://github.com/zencefilperisi/quantum-armor", fg="bright_blue")

if __name__ == "__main__":
    cli()


@click.command()
@click.argument("path", type=click.Path(exists=True), default=".")
def migrate(path):
    """Automatically migrate RSA → Kyber (PQC)"""
    from quantum_armor.migrators.rsa_to_kyber import RSAToKyberMigrator
    migrator = RSAToKyberMigrator()
    migrator.migrate_project(path)

cli.add_command(migrate)