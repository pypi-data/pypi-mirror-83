class InvalidLineNumberException(Exception):
    """Exception to raise when you pass invalid line number in a function"""
    def __init__(self, line_number, line_label='line_number'):
        msg = 'Invalid {}: {}'.format(line_label, line_number)
        super(InvalidLineNumberException, self).__init__(msg)