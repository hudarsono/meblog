def log_traceback(exception, args):
    import sys, traceback, logging
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    logging.debug(exception)
    logging.debug(args)
    for tb in traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback):
        logging.debug(tb)