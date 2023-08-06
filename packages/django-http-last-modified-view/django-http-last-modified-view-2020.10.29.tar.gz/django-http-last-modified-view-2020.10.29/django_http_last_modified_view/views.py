__all__ = ['HttpLastModifiedMixin']


from datetime import date, datetime
from django.utils.http import http_date


class HttpLastModifiedMixin:
    http_last_modified = None

    def get_http_last_modified(self):
        return self.http_last_modified

    def get_http_last_modified_http_date(self):
        last_modified = self.get_http_last_modified()
        if not last_modified:
            return
        if isinstance(last_modified, datetime):
            return http_date(last_modified.timestamp())
        if isinstance(last_modified, date):
            return http_date(datetime.combine(last_modified, datetime.min.time()))
        if isinstance(last_modified, int):
            return http_date(last_modified)

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        if response.status_code in [200, 304]:
            last_modified = self.get_http_last_modified_http_date()
            if last_modified:
                response['Last-Modified'] = last_modified
        return response
