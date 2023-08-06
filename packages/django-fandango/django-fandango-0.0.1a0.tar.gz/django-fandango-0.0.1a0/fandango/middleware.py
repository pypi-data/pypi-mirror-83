import hashlib
from time import time
from re import compile
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from ipware import get_client_ip

from fandango.logging.log import get_logger
from fandango.utils.humanize import get_humanized_memory_usage


class BaseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)


class LoggingMiddleware(BaseMiddleware):
    logger = get_logger("access")

    def __call__(self, request):
        self.start_time = time()
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_response(self, request, response):
        db_stats = self.get_db_stats(response)
        total_time = self.get_total_time()
        ip, routable = get_client_ip(request)

        log_msg = "- %s - %s - %s - %s ms - %s - Session: %s - User: %s - Header hash: %s - Ref: %s " \
                  "- User agent type: %s - Mem usage: %s" \
                  % (ip,
                    request.get_full_path(),
                    response.status_code,
                    total_time,
                    request.user_agent.ua_string,
                    self.has_session(request),
                    self.get_username(request),
                    self.get_header_hash(request),
                    self.get_referer(request),
                    self.get_agent_type(request),
                    get_humanized_memory_usage())

        if db_stats["db_time"] or db_stats["db_queries"]:
            log_msg += " - DB-time: %s ms - Queries: %s" % (db_stats["db_time"], db_stats["db_queries"])

        self.logger.info(log_msg)
        return response

    def get_agent_type(self, request):
        if request.user_agent.is_mobile:
            return "MOBILE"
        if request.user_agent.is_tablet:
            return "TABLET"
        if request.user_agent.is_pc:
            return "PC"
        if request.user_agent.is_bot:
            return "BOT"

        return "UNKNOWN"

    def get_username(self, request):
        if hasattr(request, "user") and request.user.username:
            return request.user.username

        return "none"

    def get_referer(self, request):
        if "HTTP_REFERER" in request.META:
            return request.META["HTTP_REFERER"]

        return "none"

    def has_session(self, request):
        if request.COOKIES.get("sessionid"):
            return True

        return False

    def get_total_time(self):
        if hasattr(self, "start_time"):
            total_time = time() - self.start_time
            return int(total_time * 1000)
        else:
            return "Unknown time"

    def get_header_hash(self, request):
        fields_to_include = ["HTTP_USER_AGENT", "HTTP_ACCEPT_LANGUAGE", "HTTP_DNT"]
        headers = ""
        for field in fields_to_include:
            if field in request.META:
                headers += request.META[field] + "|"

        if headers:
            return hashlib.md5(headers.encode("UTF-8")).hexdigest()
        else:
            return "no-hash"

    def get_db_stats(self, response):
        total_time = 0
        if response.status_code == 200:
            for query in connection.queries:
                query_time = query.get('time')
                if query_time is None:
                    query_time = query.get('duration', 0) / 1000
                total_time += float(query_time)

        total_time = int(total_time * 1000)

        return {
            'db_time': total_time,
            'db_queries': len(connection.queries),
        }


EXEMPT_URLS = [
    # some hardcoded-ish URLs in here :(
    compile('/password/reset/.*'),
    compile('/reset/.*'),
    compile(str(reverse("login"))),
]


class LoginMiddleware(BaseMiddleware):

    def process_request(self, request):
        path = request.path_info
        # redirect logged in users to index
        if path == reverse("login") and request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        if not request.user.is_authenticated:
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(reverse("login"))
