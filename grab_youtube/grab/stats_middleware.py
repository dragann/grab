from django.db import connection
from time import time
from operator import add
import re
from django.conf import settings
from django.http.response import StreamingHttpResponse


class StatsMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        In your base template, put this:
        {% if debug %}  <div id="stats"><!-- STATS: Total: %(totTime).2fs <br/>
        Python: %(pyTime).2fs <br/>
        DB: %(dbTime).2fs <br/>
        Queries: %(queries)d --></div> {% endif %}

        Here's the css style I use:
        #stats { background-color: #ddd; font-size: 65%; padding: 5px;
        z-index: 1000; position: absolute; right: 5px; top: 5px;
        -moz-opacity: .7; opacity: .7;}
        """

        #This stuff will only happen if debug is already on
        if not settings.DEBUG and not request.user.is_superuser:
            return None

        request.summary_stats = True

        # get number of db queries before we do anything
        self.n = len(connection.queries)

        # time the view
        self.start = time()

    def process_response(self, request, response):
        if not settings.DEBUG and (not hasattr(request, 'user') or request.user is None or not request.user.is_superuser) or not hasattr(self, 'start'):
            return response

        totTime = time() - self.start

        # compute the db time for the queries just run
        queries = len(connection.queries) - (self.n)
        if queries > 0:
            dbTime = reduce(add, [float(q['time']) for q in connection.queries[self.n:]])
        else:
            dbTime = 0.0

        # and backout python time
        pyTime = totTime - dbTime

        totTime = totTime * 1000

        if totTime > 200:
            totTime = '<span class="stats-over">%dms</span>' % totTime
        else:
            totTime = '%dms' % totTime

        stats = {
            'totTime': totTime,
            'pyTime': pyTime * 1000,
            'dbTime': dbTime * 1000,
            'queries': queries,
        }

        # replace the comment if found
        if response:
            if isinstance(response, StreamingHttpResponse):
                return response
            else:
                s = response.content

            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)-->)')
            match = regexp.search(s)
            if match:
                s = s[:match.start('cmt')] + \
                    match.group('fmt') % stats + \
                    s[match.end('cmt'):]
                response.content = s

        return response
