from django.conf import settings


class ConsoleExceptionMiddleware:
    def process_exception(self, request, exception):
        if not settings.DEBUG:
            return
        import traceback
        import sys
        exc_info = sys.exc_info()
        print "######################## Exception #############################"
        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        print "################################################################"
        #print repr(request)
        #print "################################################################"
