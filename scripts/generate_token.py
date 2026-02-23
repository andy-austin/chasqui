#!/usr/bin/env python3
"""Generate a signed JWT for a Chasqui API client.

Usage:
    python scripts/generate_token.py <client_id> [--days N] [--secret SECRET]

Examples:
    python scripts/generate_token.py workshop-123
    python scripts/generate_token.py torke-backend --days 180
    JWT_SECRET=mysecret python scripts/generate_token.py workshop-456
"""

import argparse
import os
import sys
from datetime import UTC, datetime, timedelta

import jwt


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Chasqui API JWT")
    parser.add_argument("client_id", help="Client identifier (becomes the 'sub' claim)")
    parser.add_argument(
        "--days", type=int, default=90, help="Token validity in days (default: 90)"
    )
    parser.add_argument(
        "--secret", default=None, help="JWT secret (default: reads JWT_SECRET env var)"
    )
    parser.add_argument(
        "--algorithm", default="HS256", help="JWT algorithm (default: HS256)"
    )
    args = parser.parse_args()

    secret = args.secret or os.environ.get("JWT_SECRET")
    if not secret:
        print("Error: provide --secret or set the JWT_SECRET environment variable", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(UTC)
    payload = {
        "sub": args.client_id,
        "iat": now,
        "exp": now + timedelta(days=args.days),
    }

    token = jwt.encode(payload, secret, algorithm=args.algorithm)
    print(f"Client:  {args.client_id}")
    print(f"Expires: {payload['exp'].isoformat()}")
    print(f"Token:   {token}")


if __name__ == "__main__":
    main()
