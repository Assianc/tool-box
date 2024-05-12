addEventListener('scheduled', event => {
  event.waitUntil(handleScheduledEvent(event))
})

async function handleScheduledEvent(event) {
  const url = 'https://open.feishu.cn/open-apis/bot/v2/hook/90a0axxxxxxxxx922-8029xxxxxxxx60c';
  const data = {
    "msg_type": "interactive",
    "card": {
      "type": "template",
      "data": {
        "template_id": "AAq3OTs48BADR",
        "template_version_name": "1.0.2",
        "template_variable": {
          "Title": "Linuxdo新帖推送到TG？不！推送飞书！！",
          "Author": "是丸子！",
          "Description": "平时一直在用tg看linuxdo的新帖推送，但是tg感觉又诸多不便。因为我平时就在使用飞书，So，那就来一个“将Linuxdo最新的主题，推送至飞书群组！”",
          "Category": "软件分享",
          "Time": "Sat, 11 May 2024 16:57:28",
          "Link": {
            "pc_url": "",
            "android_url": "",
            "ios_url": "",
            "url": "https://linux.do/t/topic/83421"
          }
        }
      }
    }
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });

  return response;
}