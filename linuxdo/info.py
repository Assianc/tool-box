from telethon import events
from telethon.sync import TelegramClient
import requests
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont

api_id = ''
api_hash = ''
bot_token = ''


def get_info(username):
    url = f"https://linux.do/u/{username}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "user" in data:
            return data["user"]
    return None


def convert_to_shanghai_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_time = pytz.utc.localize(utc_time)
    shanghai_time = utc_time.astimezone(pytz.timezone("Asia/Shanghai"))
    return shanghai_time.strftime("%Y-%m-%d %H:%M:%S")


async def start(event):
    await event.respond('请输入要查询的用户名')


async def handle_message(event):
    message = event.raw_text
    if not message.startswith('q/'):
        return  # 如果消息不以'q/'开头，那么就不处理

    username = message[2:]  # 移除消息开头的'q/'，剩下的部分就是用户名
    user = get_info(username)
    if user is not None:
        keys_to_print = ["id", "username", "name", "last_posted_at", "last_seen_at", "created_at", "ignored", "muted",
                         "can_ignore_user", "can_mute_user", "can_send_private_messages",
                         "can_send_private_message_to_user", "trust_level", "moderator", "admin", "badge_count",
                         "time_read", "recent_time_read", "primary_group_id", "primary_group_name", "flair_group_id",
                         "featured_topic", "timezone", "can_edit", "can_edit_username", "can_edit_email",
                         "can_edit_name", "pending_count", "profile_view_count", "can_upload_profile_header",
                         "can_upload_user_card_background", "custom_avatar_upload_id", "can_chat_user",
                         "can_see_following", "can_see_followers", "can_see_network_tab", "can_follow", "is_followed",
                         "total_followers", "total_following", "notify_me_when_followed",
                         "notify_followed_user_when_followed", "notify_me_when_followed_replies",
                         "notify_me_when_followed_creates_topic", "allow_people_to_follow_me", "gamification_score",
                         "vote_count", "see_signatures", "accepted_answers", "featured_user_badge_ids"]
        chinese_keys = ["ID", "用户名", "名称", "最后发帖时间", "最后在线时间", "创建时间", "忽略", "静音",
                        "可以忽略用户", "可以静音用户", "可以发送私人消息", "可以向用户发送私人消息", "信任等级",
                        "版主", "管理员", "徽章数量", "阅读时间", "最近阅读时间", "主要组ID", "主要组名称", "标签组ID",
                        "特色主题", "时区", "可以编辑", "可以编辑用户名", "可以编辑电子邮件", "可以编辑名称",
                        "待处理数量", "个人资料查看次数", "可以上传个人资料头部", "可以上传用户卡背景",
                        "自定义头像上传ID", "可以与用户聊天", "可以查看关注者", "可以查看粉丝", "可以查看网络标签",
                        "可以关注", "被关注", "总粉丝数", "总关注数", "当被关注时通知我",
                        "当被关注的用户被关注时通知我", "当被关注的用户回复时通知我", "当被关注的用户创建主题时通知我",
                        "允许人们关注我", "游戏化分数", "投票数", "查看签名", "接受的答案", "特色用户徽章ID"]

        result = ""
        for key, chinese_key in zip(keys_to_print, chinese_keys):
            if key in user and user[key] not in [None, False, True]:  # 检查键值的值是否为None，False或True
                if key in ["last_posted_at", "last_seen_at", "created_at"]:
                    result += f"{chinese_key}: {convert_to_shanghai_time(user[key])}\n"
                else:
                    result += f"{chinese_key}: {user[key]}\n"

        # 打开背景图片
        img = Image.open('test.jpg')  # 背景图
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('wr.ttf', 30)  # 使用你的字体文件路径
        d.text((10, 10), result, font=fnt, fill=(0, 0, 0))  # 字体颜色

        # 保存图片为JPEG格式
        img.save('result.jpg', 'JPEG')

        # 发送图片
        await event.respond(file='result.jpg')

        # 获取用户ID
        user_id = event.sender_id

        # 使用用户ID发送消息
        await client.send_message(user_id, "这是你请求的信息")
    else:
        await event.respond("获取信息失败")


with TelegramClient('bot', api_id, api_hash) as client:
    client.add_event_handler(start, events.NewMessage(pattern='/start'))
    client.add_event_handler(handle_message, events.NewMessage())
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
