class MagpieDbError(Exception):
    def __init__(self, err):
        # TODO: Log "MAGPIE DB ERROR: %s" % err
        self.err = err
