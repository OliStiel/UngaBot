import os
import logging

import disnake
import requests
from disnake.ext import commands


REQUEST_FORMAT = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a man with 20IQ. Incredibly dumb. Neanderthal"}
        ],
        "temperature": 0.7
}
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MESSAGE_SUFFIX = """
Your name is UngaBot. Respond as though you are a man with 20IQ and a Neanderthal.
"""


class UngaCommand(commands.Cog):
    """This will be for a ping command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command()
    async def ug(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @ug.sub_command()
    async def unga(self, inter: disnake.ApplicationCommandInteraction, *, question: str):
        """
        Release the ungabot.
        """

        logging.info(
            msg=f"USER: {inter.author.display_name} ASKED QUESTION: {question}"
        )

        # TODO: really I need to scrap and rewrite all of this, but oh well

        # defer it while we compute some things
        await inter.response.defer()

        # take a copy of the payload to avoid any shenanigans
        payload = REQUEST_FORMAT.copy()

        # sanitize it slightly
        question = question.rstrip().lstrip()

        # format our user's question with the pre-requisite unga
        message = f"'{question}' {MESSAGE_SUFFIX}"

        # attach it to our payload
        payload['messages'].append(
            {"role": "assistant", "content": message}
        )

        # post it to the OpenAI API
        response = requests.post(
            url=OPENAI_URL,
            json=payload,
            headers={
                'Content-Type': "application/json",
                'Authorization': f"Bearer {os.environ['OPENAI_TOKEN']}"
            }
        )

        # get the response from OpenAPI
        if response.status_code == 200:
            response_message: str = response.json()['choices'][0]['message']['content']

            # seems like there's sometimes a massive number of leading spaces maybe?
            response_message = response_message.lstrip().replace(
                MESSAGE_SUFFIX, ""
            )

            # TODO: some response sanitisation as right now that response could be an error

            await inter.followup.send(f"**{inter.author.display_name}** asked: '{question}' "
                                      f"**Ungabot**: 💪 {response_message} 💪")
        else:
            print(response.text)
            print(response.status_code)
            await inter.response.send_message("*Fart Noise*")


def setup(bot: commands.Bot):
    bot.add_cog(UngaCommand(bot))
