"""Aplica uma política fail-closed ao plano binário de Terraform do RDS."""

import json
import subprocess
import sys
from pathlib import Path

PROTECTED_RDS_ATTRIBUTES = {
    "identifier",
    "backup_retention_period",
    "skip_final_snapshot",
    "final_snapshot_identifier",
    "deletion_protection",
}


def validate_plan(plan):
    """Rejeita exclusões/replace e alterações em identidade/backup do RDS."""
    deletions = [
        resource.get("address", "recurso sem endereço")
        for resource in plan.get("resource_changes", [])
        if "delete" in resource.get("change", {}).get("actions", [])
    ]
    protected_changes = []
    for resource in plan.get("resource_changes", []):
        if resource.get("type") != "aws_db_instance":
            continue
        change = resource.get("change", {})
        before = change.get("before") or {}
        after = change.get("after") or {}
        protected_changes.extend(
            f"{resource.get('address', 'RDS')}.{attribute}"
            for attribute in PROTECTED_RDS_ATTRIBUTES
            if before.get(attribute) != after.get(attribute)
        )
    if deletions or protected_changes:
        raise ValueError("Plano bloqueado: contém exclusão/substituição de recursos.")
    return len(plan.get("resource_changes", []))


def read_plan(path):
    if not Path(path).is_file():
        raise FileNotFoundError("Arquivo de plano Terraform não encontrado.")
    result = subprocess.run(
        ["terraform", "show", "-json", path],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main():
    if len(sys.argv) != 2:
        print("Uso: python review_rds_plan.py <arquivo.tfplan>", file=sys.stderr)
        return 2
    try:
        count = validate_plan(read_plan(sys.argv[1]))
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, ValueError):
        print("Plano Terraform inválido ou bloqueado pela política de segurança.", file=sys.stderr)
        return 1
    if count == 0:
        print("Plano aprovado: No changes.")
    else:
        print("Plano aprovado: nenhuma exclusão ou substituição detectada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
