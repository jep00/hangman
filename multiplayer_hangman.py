from hangman import Hangman


class MultiPlayerHangman(Hangman):
    def set_up_users(self, user_one: str, user_two: str):
        """ """
        if user_one == user_two:
            raise ValueError("Users cannot have the same name.")
        print(f"{user_one} v {user_two}")
