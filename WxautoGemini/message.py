import os

from wxauto import WeChat
import time
from GeminiProProxy import gemini

# 实例化微信自动化对象
wechat = WeChat()


# 监听消息并回复
def listen_and_reply():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'allow.txt')
    # 初始化允许回复的聊天对象列表
    allowed_chat_objects = []

    # 从文件中读取允许回复的聊天对象列表并添加到列表中
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            allowed_chat_objects.append(line.strip())

    while True:
        # 获取所有新消息
        new_list = wechat.GetSessionList(reset=True, newmessage=True)
        # 遍历所有键
        for username in new_list.keys():
            if username in allowed_chat_objects:
                wechat.ChatWith(username)
                msg = wechat.GetLatestMessage()
                if "结束对话" in msg[1]:
                    allowed_chat_objects.remove(username)
                    # 将更新后的列表写回到文件中
                    with open(file_path, 'w',encoding="utf-8") as file:
                        for user in allowed_chat_objects:
                            file.write(user + '\n')
                    wechat.SendMsg("你好，已结束对话。如果希望重新开始对话，请输入‘小周，开始对话’", who=username)
                # 如果消息内容以"小周"开头
                if msg[1].startswith("小周"):
                    # 截取小周后面的内容
                    content = msg[1][2:]
                    print(content)
                    reply = gemini(content)
                    # 回复收到
                    wechat.SendMsg(reply, who=username)
            else:
                wechat.ChatWith(username)
                msg = wechat.GetLatestMessage()
                # 如果消息内容以"小周"开头
                if msg[1].startswith("小周"):
                    if "开始对话" in msg[1]:
                        allowed_chat_objects.append(username)
                        # 将更新后的列表写回到文件中
                        with open(file_path, 'w',encoding="utf-8") as file:
                            for user in allowed_chat_objects:
                                file.write(user + '\n')
                        wechat.SendMsg("你好，已开启对话。如果希望结束对话，请输入‘结束对话’", who=username)

        # 每隔一秒检查一次新消息
        time.sleep(1)


def main():
    listen_and_reply()


# 启动监听并回复消息
if __name__ == "__main__":
    main()
