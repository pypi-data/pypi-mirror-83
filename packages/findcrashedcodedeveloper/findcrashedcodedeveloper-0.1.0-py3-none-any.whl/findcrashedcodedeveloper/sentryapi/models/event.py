from .stacktrace import SentryStackTrace, SentryStackTraceLine


class SentryEvent:
    """A class to represent an event of Sentry"""

    def __init__(self, data):
        """
        Parameters
        ----------
        data : dict
            information return by sentry event API
        """
        self.data = data
        self.id = data['id']
        self.metadata = data['metadata']
        self.dateCreated = data['dateCreated']
        self.title = data['title']
        self.type = data['type']
        self.user = data['user']

        # others
        self.filename = self.metadata['filename']

    def _get_error_data(self):
        return self.data['entries'][0]['data']['values'][0]['stacktrace']['frames'][-1]

    def get_file_full_path(self):
        """Get crashed code file absolute path

        Returns
        -------
        str
            absolute path of crashed code file
        """
        error_data = self._get_error_data()
        return error_data['absPath']

    def get_crashed_line_number(self):
        """Get crashed code line number

        Returns
        -------
        int
            line number of crashed code
        """
        error_data = self._get_error_data()
        return error_data['lineNo']

    def _get_context_lines(self):
        error_data = self._get_error_data()
        return error_data['context']

    def get_crashed_line_code(self):
        """Get code of crashed line

        Returns
        -------
        str
            code of crashed line
        """
        context = self._get_context_lines()
        crashed_line_number = self.get_crashed_line_number()
        for c in context:
            if c[0] == crashed_line_number:
                return ''.join(c[1:])

    def get_crashed_context_code(self):
        """Get code around crashed code

        Returns
        -------
        str
            newline separated code around crashed code
        """
        context = self._get_context_lines()
        return '\n'.join(
            ''.join(c[1:])
            for c in context
        )

    def get_stack_trace(self):
        """Get stack trace of this event

        Returns
        -------
        SentryStackTrace
            stack trace of this event
        """
        trace_lines = []
        for trace_data in reversed(self.data['entries'][0]['data']['values'][0]['stacktrace']['frames']):
            crashed_line = None
            for line_data in trace_data['context']:
                if line_data[0] == trace_data['lineNo']:
                    crashed_line = ''.join(line_data[1:])
                    break

            trace_lines.append(
                SentryStackTraceLine(
                    absolute_filepath=trace_data['absPath'],
                    crashed_line_number=trace_data['lineNo'],
                    crashed_line_code=crashed_line,
                    crashed_line_context=[
                        {
                            'lineNo': line_data[0],
                            'code': ''.join(line_data[1:])
                        }
                        for line_data in trace_data['context']
                    ]
                )
            )
        return SentryStackTrace(trace_lines)
