class InvalidSongError(Exception):
    """The song is invalid somehow"""
    pass


class UserCancelsLoadingError(Exception):
    """User cancels the loading screen"""
    pass


class MapLoadingFailureError(Exception):
    """The map fails to load (recurs function fails)"""
    pass
