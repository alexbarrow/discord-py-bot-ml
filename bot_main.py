import discord

from data_dict import cf2_list, cf3_list
from data_dict import get_str_from_dict, fplot_url

from data_handler import data_show_stat, data_show_stat_ext, data_add, content_check, data_size, get_dist

from ml_module import ml_rf_acc, ml_rf_pred

from discord.ext import commands

prefix, prefix_add = '!', '#'

ch_name = 'general'
Bot = commands.Bot(command_prefix=prefix)

Bot.remove_command('help')


@Bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="the Abyss")
    await Bot.change_presence(activity=activity)
    print('Bot is ready!')


@Bot.command()
async def helpstat(ctx):
    if ctx.message.channel.name == ch_name:
        emb = discord.Embed(title='This is what i can do:', colour=0x39d0d6,
                            description='To add new entry to database, enter #stat and put the features'
                                        ' in the special order.\n For example:\n\n #stat 2 1 1 m x2 y6 5 1.')
        emb.add_field(name='{}stat'.format(prefix_add), value='Add new entry to database '
                                                              '(input in the format: 2 1 1 (m) x2 y6 5 1).')
        emb.add_field(name='{}pred'.format(prefix_add), value='Predict match result'
                                                              ' (input in the format: 2 1 1 (m) x2 y6).')

        emb.add_field(name='{}acc'.format(prefix), value='Accuracy.')
        emb.add_field(name='{}stat'.format(prefix), value='General stat.')
        emb.add_field(name='{}fstat'.format(prefix), value='Stat on cat_feat2.')
        emb.add_field(name='{}fplot'.format(prefix), value='Count plot for cat_feat2.')
        emb.add_field(name='{}updplot'.format(prefix), value='Update count plot.')
        emb.add_field(name='{}tags'.format(prefix), value='All tags for cat_feat2 and cat_feat3.')

        await ctx.send(embed=emb)


# SIMPLE COMMANDS
@Bot.command()
async def tags(ctx):
    if ctx.message.channel.name == ch_name:
        emb = discord.Embed(title='Tags.', colour=0x39d0d6, description='The tags for cat_feat2 and cat_feat3.')
        emb.add_field(name='Cat_feat2', value=get_str_from_dict(cf2_list), inline=True)
        emb.add_field(name='Cat_feat3', value=get_str_from_dict(cf3_list), inline=True)
        await ctx.send(embed=emb)


@Bot.command()
async def stat(ctx):
    if ctx.message.channel.name == ch_name:
        w, g, e = data_show_stat()
        s = data_size()
        kc, mc = len(cf2_list), len(cf3_list)
        await ctx.send('Games: {},\nWins: {:.0f}%,\nNum_feat4 mean: {:.1f},'
                       '\nRatio num_feat5: {:.0f}%,\nNumber of cat_feat2: {},\nNumber of cat_feat3: {}.'
                       .format(s, w, g, e*100, kc, mc))


@Bot.command()
async def fstat(ctx):
    if ctx.message.channel.name == ch_name:
        emb = discord.Embed(title='Stat on cat_feat2.', colour=0x39d0d6)
        kdf = data_show_stat_ext('cat_feat2')

        for item, row in kdf.iterrows():
            emb.add_field(name=cf2_list[item], value='Games: {:.0f}, Wins: {:.0f}%, num_feat4_mean:: {:.1f},'
                                                     ' Ratio num_feat5: {:.0f}%'
                          .format(row['count'], row['Result']*100, row['num_feat4'], row['mean_value']*100))
        await ctx.send(embed=emb)


@Bot.command()
async def fplot(ctx):
    if ctx.message.channel.name == ch_name:
        url = fplot_url + '.png'
        await ctx.channel.send(file=discord.File(url))


@Bot.command()
async def updplot(ctx):
    if ctx.message.channel.name == ch_name:
        get_dist('cat_feat2', fplot_url)
        await ctx.send('Plot is updated!')


@Bot.command()
async def acc(ctx):
    if ctx.message.channel.name == ch_name:
        a = ml_rf_acc()
        await ctx.send('The accuracy is {:.0f}%.'.format(a*100))


# LISTEN COMMANDS
@Bot.listen()
async def on_message(message):
    if message.channel.name == ch_name:
        if message.content.startswith('#stat'):
            content, channel = message.content.split()[1:], message.channel

            res = content_check(content, mode='a')
            if res == 'len':
                await channel.send('Wrong the input len.')
            elif res == 'err':
                await channel.send('Input error.')
            elif res == 'cf2':
                await channel.send('Wrong cat_feat2 value. Check !tags command.')
            elif res == 'cf3':
                await channel.send('Wrong cat_feat3 value. Check !tags command.')
            else:
                data_add(res)
                await channel.send('Completed.')


@Bot.listen()
async def on_message(message):
    if message.channel.name == ch_name:
        if message.content.startswith('#pred'):
            content, channel = message.content.split()[1:], message.channel

            res = content_check(content, mode='p')
            if res == 'len':
                await channel.send('Wrong the input len.')
            elif res == 'err':
                await channel.send('Input error.')
            elif res == 'cf2':
                await channel.send('Wrong cat_feat2 value. Check !tags command.')
            elif res == 'cf3':
                await channel.send('Wrong cat_feat3 value. Check !tags command.')
            else:
                prob, pred = ml_rf_pred(res)
                if pred > 0:
                    ans = 'win'
                else:
                    ans = 'lose'
                await channel.send('With probability of {:.0f}%, you will {}.'
                                   .format(prob*100, ans))

try:
    Bot.run(open('bot_token.txt', 'r').readline())
except discord.errors.LoginFailure as err:
    print(err)
