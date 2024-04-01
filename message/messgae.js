const MESSAGE_COUNT_KEY = 'message_count';
export default {
    async fetch(request, env) {
        // 初始化KV存储
        const store = env.QYAPI_KY;

        // 检查请求方法是否为GET
        if (request.method === 'GET') {
            // 从KV存储中获取消息数量
            const messageCount = await store.get(MESSAGE_COUNT_KEY);
            const count = messageCount ? parseInt(messageCount, 10) : 0;

            // 返回包含消息数量的页面内容
            const htmlContent = `<h1>API is running normally</h1><p>Messages sent: ${count}</p>`;
            return new Response(htmlContent, {status: 200, headers: {'Content-Type': 'text/html'}});
        }

        // 检查请求方法是否为POST
        if (request.method !== 'POST') {
            return new Response('Method Not Allowed', {status: 405});
        }

        // 从请求中获取消息数据
        const requestData = await request.json();
        const {type, message} = requestData;

        // 根据type类型选择不同的webhook地址
        let webhookUrl;
        if (type === 'default') {
            webhookUrl = env.WEBHOOK_URL;
        } else if (type === 'course') {
            webhookUrl = env.COURSE;
        } else {
            return new Response('Invalid type', {status: 400});
        }

        try {
            // 发送POST请求到选择的webhook地址
            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    msgtype: 'text',
                    text: {
                        content: message,
                    },
                }),
            });

            // 更新消息数量统计并保存到KV存储
            if (response.ok) {
                let messageCount = await store.get(MESSAGE_COUNT_KEY);
                messageCount = messageCount ? parseInt(messageCount, 10) + 1 : 1;
                await store.put(MESSAGE_COUNT_KEY, messageCount.toString());
            }

            // 返回消息发送结果
            if (response.ok) {
                return new Response('Message sent successfully', {status: 200});
            } else {
                return new Response('Failed to send message', {status: 500});
            }
        } catch (error) {
            console.error('Error sending message:', error);
            return new Response('Error sending message', {status: 500});
        }
    },
};
