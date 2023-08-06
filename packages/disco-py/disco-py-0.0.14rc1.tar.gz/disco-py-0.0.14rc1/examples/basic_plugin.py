from __future__ import print_function

from disco.bot import Plugin
from disco.util.sanitize import S


class BasicPlugin(Plugin):
    @Plugin.command('auditme')
    def on_auditme(self, event):
        invite = event.channel.create_invite(reason='TEST AUDIT')
        invite.delete(reason='TEST AUDIT 2')
        channel = event.guild.create_channel('audit-log-test', 'text', reason='TEST CREATE')
        channel.delete(reason='TEST AUDIT 2')

    @Plugin.command('create-some-channels')
    def on_create_some_channels(self, event):
        category = event.guild.create_category('My Category')
        category.create_text_channel('text-channel')
        category.create_voice_channel('voice-channel')
        event.msg.reply('Ok, created some channels')

    @Plugin.command('ratelimitme')
    def on_ratelimitme(self, event):
        msg = event.msg.reply('Hi!')

        with self.client.api.capture() as requests:
            for i in range(6):
                msg.edit('Hi {}!'.format(i))

        print('Rate limited {} for {}'.format(
            requests.rate_limited,
            requests.rate_limited_duration(),
        ))

    @Plugin.command('ban', '<user:snowflake> <reason:str...>')
    def on_ban(self, event, user, reason):
        event.guild.create_ban(user, reason=reason + u'\U0001F4BF')

    @Plugin.command('ping')
    def on_ping_command(self, event):
        # Generally all the functionality you need to interact with is contained
        #  within the event object passed to command and event handlers.
        event.msg.reply('Pong!')

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        # All of Discord's events can be listened too and handled easily
        self.log.info(u'{}: {}'.format(event.author, event.content))

    @Plugin.command('test')
    @Plugin.command('echo', '<content:str...>')
    def on_echo_command(self, event, content):
        # Commands can take a set of arguments that are validated by Disco itself
        #  and content sent via messages can be automatically sanitized to avoid
        #  mentions/etc.
        event.msg.reply(content, santize=True)

    @Plugin.command('add', '<a:int> <b:int>', group='math')
    def on_math_add_command(self, event, a, b):
        # Commands can be grouped together for a cleaner user-facing interface.
        event.msg.reply('{}'.format(a + b))

    @Plugin.command('sub', '<a:int> <b:int>', group='math')
    def on_math_sub_command(self, event, a, b):
        event.msg.reply('{}'.format(a - b))

    @Plugin.command('test', parser=True)
    @Plugin.parser.add_argument('-a', '--asdf', help='wow')
    @Plugin.parser.add_argument('--help', action='store_true')
    def on_test(self, event, args):
        # Disco supports using an argparse.ArgumentParser for parsing commands as
        #  well, which helps for large complex commands with many options or flags.
        if args.help:
            return event.msg.reply(event.parser.format_help())
        event.msg.reply(args.asdf)
        
    # You can use a listener to react to events, like someone joining your guild
    @Plugin.listen('GuildMemberAdd')
    def send_welcome_dm(self, event):
        # Send the user a direct message with a welcome greeting after they join.
        event.member.user.open_dm().send_message('Hi there! Welcome to our friendly community.')
