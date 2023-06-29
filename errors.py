class InvalidSongError(Exception):
    """The song is invalid somehow"""
    pass


class UserCancelsLoadingError(Exception):
    """User cancels the loading screen"""
    pass
