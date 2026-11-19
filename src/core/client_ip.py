"""IP клієнта за reverse proxy (Vercel, пізніше DigitalOcean)."""

from __future__ import annotations

import ipaddress

from django.http import HttpRequest


def client_ip(request: HttpRequest) -> str:
    """
    X-Real-IP, якщо проксі його виставив.
    Інакше правий адрес у X-Forwarded-For — його дописує найближчий проксі.
    Без цих заголовків лишається REMOTE_ADDR.
    """
    candidates = []
    real_ip = (request.META.get('HTTP_X_REAL_IP') or '').strip()
    if real_ip:
        candidates.append(real_ip)
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    parts = [part.strip() for part in forwarded.split(',') if part.strip()]
    candidates.extend(reversed(parts))
    remote = (request.META.get('REMOTE_ADDR') or '').strip()
    if remote:
        candidates.append(remote)
    for raw in candidates:
        host = raw.split('%', 1)[0]
        try:
            return str(ipaddress.ip_address(host))
        except ValueError:
            continue
    return '127.0.0.1'
