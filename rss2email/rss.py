#  订阅RSS源，发送到电子邮箱

import os
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup


def get_feeds(script_dir):
    feed_file_path = os.path.join(script_dir, 'feed.txt')
    # 从文件中读取订阅源
    with open(feed_file_path, 'r') as file:
        feeds = file.read().splitlines()

    return feeds


def get_content(feeds, sent_titles):
    # 遍历每个订阅源
    for feed in feeds:
        # 获取RSS内容
        feed = feedparser.parse(feed)

        entries = feed.entries
        for entry in entries:
            title = entry.title
            link = entry.link

            # 获取文章内容
            try:
                content = entry.content[0].value
            except (KeyError, AttributeError, IndexError):
                content = entry.summary

            # 删除 <p> 标签
            content = remove_html_tags(content)

            if title not in sent_titles:
                send_email(title, link, content)
                sent_titles.add(title)


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def send_email(title, link, content):
    # 电子邮件配置
    sender_email = 'pinhsin@163.com'
    sender_password = 'KNFEGCBHLFTUKMLN'
    receiver_email = 'rss@bxin.top'

    # 构建邮件内容
    article_content = f"\nTitle: {title}\nLink: {link}\n\nContent:\n{content}\n\n"

    # 创建MIMEText对象
    msg = MIMEMultipart()
    msg.attach(MIMEText(article_content, 'plain'))

    # 设置发件人和收件人
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'{title} by rss2email'

    # 连接到SMTP服务器并发送邮件
    with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f'文章 {title} 发送成功')


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    articles_file_path = os.path.join(script_dir, 'sent_articles.txt')

    feeds = get_feeds(script_dir)

    # 用一个集合来记录已发送的文章标题
    sent_titles = set()

    # 在每次运行时检查已发送的文章，以防止重复发送
    try:
        with open(articles_file_path, 'r') as file:
            sent_titles.update(file.read().splitlines())
    except FileNotFoundError:
        pass

    get_content(feeds, sent_titles)

    # 在每次运行后更新已发送的文章记录
    with open(articles_file_path, 'w') as file:
        file.write('\n'.join(sent_titles))

    print("运行结束")
    input()


if __name__ == '__main__':
    main()
