## Github Action 运行

首先 fork 仓库[https://github.com/ZhouBinxin/tool-box](https://github.com/ZhouBinxin/tool-box)

点击 Actions 按钮，启用 Workflow `I understand my workflows, go ahead and enable them`

点击 Settings -> Secrets and variables -> actions -> Newrepository ssecret

选择使用邮箱接收，添加以下变量
SENDER_EMAIL 163邮箱
SENDER_PASSWORD 163邮箱密码

选择使用R2存储桶接收，添加以下变量
ACCESS_KEY_ID 访问密钥ID
SECRET_ACCESS_KEY 机密访问密钥
ACCOUNT_ID 为 S3 客户端使用管辖权地特定的终结点
