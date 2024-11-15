import discord
import os
from discord.ext import commands

# 環境変数からトークンを取得
TOKEN = os.getenv("DISCORD_TOKEN")

# Intentの設定
intents = discord.Intents.default()
intents.messages = True  # メッセージイベントを有効化
intents.message_content = True  # メッセージ内容Intent（重要）

# BOT設定
bot = commands.Bot(command_prefix="/", intents=intents)

# Tree（スラッシュコマンドの登録用オブジェクト）
tree = bot.tree

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')
    try:
        synced = await tree.sync()  # スラッシュコマンドを同期
        print(f"スラッシュコマンドを {len(synced)} 個同期しました")
    except Exception as e:
        print(f"コマンドの同期中にエラーが発生しました: {e}")

# スラッシュコマンドを定義
@tree.command(name="verify", description="認証を行いロールを付与します")
async def verify(interaction: discord.Interaction):
    guild = interaction.guild
    member = interaction.user
    role_name = "Verified"

    # ロールを検索
    role = discord.utils.get(guild.roles, name=role_name)

    # ユーザーがすでにロールを持っているか確認
    if role in member.roles:
        await interaction.response.send_message("⚠️すでに認証済みです。", ephemeral=False)
        return

    # ロールがない場合、自動作成
    if not role:
        try:
            role = await guild.create_role(
                name=role_name,
                colour=discord.Colour.green(),  # 緑色
                permissions=discord.Permissions(send_messages=True)  # 必要な権限を設定
            )
            await interaction.response.send_message(f"✅ ロール '{role_name}' を作成しました！", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ BOTにロールを作成する権限がありません。管理者に確認してください。", ephemeral=False)
            return
        except Exception as e:
            await interaction.response.send_message(f"⚠️ ロールの作成中にエラーが発生しました: {e}", ephemeral=False)
            return

    # ロールをユーザーに付与
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ {member.mention} さんにロール '{role_name}' を付与しました！", ephemeral=False)
    except discord.Forbidden:
        await interaction.response.send_message("⚠️ BOTにロールを付与する権限がありません。管理者に確認してください。", ephemeral=False)
    except Exception as e:
        await interaction.response.send_message(f"⚠️ ロール付与中にエラーが発生しました: {e}", ephemeral=False)

# BOT起動
bot.run(TOKEN)  # 環境変数からボットトークンを使う
