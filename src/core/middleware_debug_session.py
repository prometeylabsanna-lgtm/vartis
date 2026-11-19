"""Тимчасові логи сесії адмінки (debug)."""

from __future__ import annotations

import json
import os
import time

_LOG = '/Users/olegbonislavskyi/Sites/Vartis/.cursor/debug-12d06c.log'


def _dbg(hypothesis_id, location, message, data):
    # #region agent log
    payload = {
        'sessionId': '12d06c',
        'runId': 'pre-fix',
        'hypothesisId': hypothesis_id,
        'location': location,
        'message': message,
        'data': data,
        'timestamp': int(time.time() * 1000),
    }
    try:
        with open(_LOG, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(payload, ensure_ascii=True) + '\n')
    except OSError:
        try:
            with open('/tmp/debug-12d06c.log', 'a', encoding='utf-8') as fh:
                fh.write(json.dumps(payload, ensure_ascii=True) + '\n')
        except OSError:
            pass
    # #endregion


class DebugAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/'):
            return self.get_response(request)

        session_cookie = request.COOKIES.get('sessionid', '')
        csrf_cookie = request.COOKIES.get('csrftoken', '')
        user = getattr(request, 'user', None)
        session = getattr(request, 'session', None)
        keys = list(session.keys()) if session is not None else []
        user_count = None
        try:
            from django.contrib.auth import get_user_model

            user_count = get_user_model().objects.count()
        except Exception as exc:
            user_count = type(exc).__name__
        # #region agent log
        _dbg(
            'A',
            'middleware_debug_session.py:request',
            'admin request session',
            {
                'path': request.path,
                'query': request.META.get('QUERY_STRING', '')[:200],
                'method': request.method,
                'vercel': bool(os.environ.get('VERCEL')),
                'engine': str(__import__('django.conf', fromlist=['settings']).settings.SESSION_ENGINE),
                'secure': request.is_secure(),
                'xfp': request.META.get('HTTP_X_FORWARDED_PROTO', ''),
                'cookie_session_len': len(session_cookie),
                'cookie_csrf_len': len(csrf_cookie),
                'auth': bool(getattr(user, 'is_authenticated', False)),
                'user_pk': getattr(user, 'pk', None) if getattr(user, 'is_authenticated', False) else None,
                'session_keys': keys,
                'has_auth_hash': '_auth_user_hash' in keys,
                'user_count': user_count,
            },
        )
        # #endregion
        response = self.get_response(request)
        set_cookie = response.get('Set-Cookie', '') or ''
        # #region agent log
        _dbg(
            'B',
            'middleware_debug_session.py:response',
            'admin response session',
            {
                'path': request.path,
                'status': response.status_code,
                'location': (response.get('Location') or '')[:200],
                'set_cookie_len': len(set_cookie),
                'set_cookie_has_session': 'sessionid=' in set_cookie.lower(),
                'auth_after': bool(getattr(getattr(request, 'user', None), 'is_authenticated', False)),
            },
        )
        # #endregion
        return response
