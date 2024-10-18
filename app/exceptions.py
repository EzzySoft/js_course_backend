class InvalidSessionError(ValueError):
    def __init__(self):
        super().__init__("Invalid session ID")


class InvalidCredentialsError(ValueError):
    def __init__(self):
        super().__init__("Invalid credentials")


class UsernameInUseError(ValueError):
    def __init__(self):
        super().__init__("The username is already taken")


class EmailInUseError(ValueError):
    def __init__(self):
        super().__init__("The email is already taken")


class UserNotFoundError(ValueError):
    def __init__(self):
        super().__init__("User not found")


class TripNotFoundError(ValueError):
    def __init__(self):
        super().__init__("Trip not found")


class UserTripNotFoundError(ValueError):
    def __init__(self, user_id, trip_id):
        super().__init__(f"User {user_id} do not have trip {trip_id}")


class UserNotAllowedError(ValueError):
    def __init__(self: str):
        super().__init__("This operation is not allowed for user")


exceptions_list = (TripNotFoundError,
                   UserNotFoundError,
                   EmailInUseError,
                   UsernameInUseError,
                   InvalidCredentialsError,
                   InvalidSessionError,
                   UserTripNotFoundError,
                   UserNotAllowedError,
                   )
