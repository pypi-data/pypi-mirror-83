import royalnet.commands as rc
from ..tables import User


class RoyalnetrolesCommand(rc.Command):
    name: str = "royalnetroles"

    description: str = "Display your Royalnet roles."

    syntax: str = ""

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if name := args.optional(0) is not None:
            async with data.session_acm() as session:
                user = await User.find(alchemy=self.alchemy, session=session, identifier=name)
        else:
            user = await data.get_author(error_if_none=True)

        msg = [
            "👤 You currently have these roles:",
            *list(map(lambda r: f"- {r}", user.roles))
        ]

        await data.reply("\n".join(msg))
