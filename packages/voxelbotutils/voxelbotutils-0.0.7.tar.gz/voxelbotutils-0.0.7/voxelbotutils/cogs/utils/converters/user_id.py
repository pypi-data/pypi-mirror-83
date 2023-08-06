from discord.ext import commands


class UserID(int):
    """
    A conveter that takes the given value and tries to grab the ID from it.
    When used, this would provide the ID of the user.
    """

    @classmethod
    async def convert(cls, ctx:commands.Context, value:str) -> int:
        """
        Converts the given value to a valid user ID.
        """

        commands.IDConverter
        match = commands.IDConverter()._get_id_match(value)
        if match is not None:
            return int(match.group(1))
        raise commands.BadArgument()
