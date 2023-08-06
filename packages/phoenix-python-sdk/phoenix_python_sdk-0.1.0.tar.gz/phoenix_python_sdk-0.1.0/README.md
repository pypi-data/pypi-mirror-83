# phoenix python client

### 安装
```shell script
pip install phoenix-python-sdk
```

### 使用
```python


from phoenix-python-sdk.client import Client
# 当前应用名称
app = "console-end"
# phoenix api 地址
api_url = "http://127.0.0.1:8889"
client = Client(api_url=api_url, app=app)
client.init_config()



# 发送单个任务
from phoenix-python-sdk.client import Receiver
# 注册的方法
service = "hello"
callback_url = "回调地址"
# 参数
params = {}
receiver = Receiver(app=app, service=service)
client.send_task(params=params, receiver=receiver, callback_url=callback_url)

#发送任务流
workflow_name = "createVm"
client.send_workflow(params=params, workflow_name=workflow_name, callback_url=callback_url)
```