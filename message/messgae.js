export default {
  async fetch(request, env) {
    // 检查请求方法是否为POST
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    // 从请求中获取消息数据
    const requestData = await request.json();
    const { type, message } = requestData;

    // 根据type类型选择不同的webhook地址
    let webhookUrl;
    if (type === 'default') {
      webhookUrl = env.WEBHOOK_URL;
    } else if (type === 'course') {
      webhookUrl = env.COURSE;
    }
    else {
      return new Response('Invalid type', { status: 400 });
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

      // 检查webhook响应状态码
      if (response.ok) {
        return new Response('Message sent successfully', { status: 200 });
      } else {
        return new Response('Failed to send message', { status: 500 });
      }
    } catch (error) {
      console.error('Error sending message:', error);
      return new Response('Error sending message', { status: 500 });
    }
  },
};
