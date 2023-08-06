# Support Python 2
from __future__ import print_function


def print_sentry_stack_trace(stack_trace, heading='Stack Trace:'):
    """Print Sentry stack trace information

    Parameters
    ----------
    stack_trace : SentryStackTrace
    heading : str
    """
    print(heading)
    for trace_line in stack_trace.get_trace_lines():
        print('file:', trace_line.get_absolute_filepath())
        message = '{}:{}'.format(
            trace_line.get_crashed_line_number(),
            trace_line.get_crashed_line_code()
        )
        print(message)
