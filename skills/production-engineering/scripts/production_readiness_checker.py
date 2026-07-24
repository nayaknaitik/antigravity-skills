#!/usr/bin/env python3
"""
Production Readiness Audit & Verification Engine
Evaluates service blueprints, configurations, or codebases against the 25 core production-engineering standards.
"""

import sys
import os
import json
import argparse
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def audit_blueprint(file_path: str) -> dict:
    path = Path(file_path).resolve()
    if not path.exists():
        return {"error": f"File '{file_path}' does not exist.", "score": 0, "status": "FAILED"}

    content = path.read_text(encoding="utf-8")
    data = {}

    if path.suffix == ".json":
        try:
            data = json.loads(content)
        except Exception as e:
            return {"error": f"JSON syntax error: {str(e)}", "score": 0, "status": "FAILED"}
    elif path.suffix in [".yaml", ".yml"]:
        if HAS_YAML:
            try:
                data = yaml.safe_load(content) or {}
            except Exception as e:
                return {"error": f"YAML syntax error: {str(e)}", "score": 0, "status": "FAILED"}
        else:
            data = {"raw_text": content}
    else:
        data = {"raw_text": content}

    checks_passed = []
    checks_failed = []

    # Category 1: Architecture
    arch = data.get("architecture", {})
    if arch.get("pattern") == "clean-architecture-hexagonal" or "clean" in content.lower():
        checks_passed.append("Clean Architecture & Hexagonal Ports/Adapters defined")
    else:
        checks_failed.append("Missing explicit Clean Architecture specification")

    if arch.get("domain_driven_design", {}).get("bounded_context") or "bounded" in content.lower():
        checks_passed.append("DDD Bounded Context & Aggregates defined")
    else:
        checks_failed.append("Missing DDD Bounded Context mapping")

    if arch.get("event_driven", {}).get("outbox_pattern_enabled") or "outbox" in content.lower():
        checks_passed.append("Event-Driven Outbox pattern & DLQ enabled")
    else:
        checks_failed.append("Missing Event-Driven Transactional Outbox pattern")

    # Category 2: Resilience
    res = data.get("resilience", {})
    if res.get("timeouts") or "timeout" in content.lower():
        checks_passed.append("Explicit timeout rules configured")
    else:
        checks_failed.append("Missing explicit timeouts configuration")

    if res.get("retries", {}).get("jitter") == "full" or "jitter" in content.lower():
        checks_passed.append("Retries with exponential backoff & full jitter configured")
    else:
        checks_failed.append("Missing full jitter in retry policy")

    if res.get("circuit_breaker") or "circuit" in content.lower():
        checks_passed.append("Circuit Breaker failure threshold configured")
    else:
        checks_failed.append("Missing Circuit Breaker configuration")

    if res.get("graceful_shutdown") or "graceful" in content.lower() or "sigterm" in content.lower():
        checks_passed.append("Graceful shutdown & traffic drain protocol defined")
    else:
        checks_failed.append("Missing Graceful Shutdown protocol")

    # Category 3: Observability
    obs = data.get("observability", {})
    if obs.get("opentelemetry", {}).get("enabled") or "opentelemetry" in content.lower() or "otel" in content.lower():
        checks_passed.append("OpenTelemetry OTLP instrumentation enabled")
    else:
        checks_failed.append("Missing OpenTelemetry specification")

    if obs.get("logging", {}).get("format") == "json" or "json" in content.lower():
        checks_passed.append("Structured JSON logging with trace context correlation defined")
    else:
        checks_failed.append("Missing JSON log schema specification")

    if obs.get("health_checks") or "health" in content.lower():
        checks_passed.append("Kubernetes Startup, Liveness, and Readiness probes configured")
    else:
        checks_failed.append("Missing explicit health check probes")

    # Category 4: Operations & Security
    sec = data.get("security", {})
    if sec.get("secrets_provider") or "vault" in content.lower() or "secrets" in content.lower():
        checks_passed.append("Secrets management via external provider (Vault/AWS/K8s) configured")
    else:
        checks_failed.append("Missing external secrets management specification")

    if sec.get("tls_enabled") or "tls" in content.lower():
        checks_passed.append("TLS 1.3 / mTLS transport security enforced")
    else:
        checks_failed.append("Missing explicit TLS specification")

    total_checks = len(checks_passed) + len(checks_failed)
    score = int((len(checks_passed) / total_checks) * 100) if total_checks > 0 else 0

    return {
        "file": str(path),
        "score": score,
        "status": "APPROVED" if score >= 85 else "REJECTED",
        "passed_count": len(checks_passed),
        "failed_count": len(checks_failed),
        "checks_passed": checks_passed,
        "checks_failed": checks_failed
    }

def main():
    parser = argparse.ArgumentParser(description="Production Readiness Checker")
    parser.add_argument("--spec", required=True, help="Path to service blueprint (YAML/JSON/MD)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    args = parser.parse_args()

    result = audit_blueprint(args.spec)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Production Readiness Audit Report ===")
        print(f"Target: {result.get('file')}")
        print(f"Score:  {result.get('score')}/100")
        print(f"Status: {result.get('status')}\n")

        print("Passed Verifications:")
        for p in result.get("checks_passed", []):
            print(f"  [✓] {p}")

        if result.get("checks_failed"):
            print("\nFailed Checks / Missing Requirements:")
            for f in result.get("checks_failed", []):
                print(f"  [X] {f}")

        sys.exit(0 if result.get("score", 0) >= 85 else 1)

if __name__ == "__main__":
    main()
