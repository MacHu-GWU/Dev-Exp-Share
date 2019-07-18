IOT (Internet of Things)
==============================================================================

- Authentication
- Registry
- Device Shadow Service?
- Job Service
- Message Broker
- Rule Engine?
- Device Gateway?


Concept
------------------------------------------------------------------------------

- **Device Shadow**: 是一个 JSON Document, 记录了 Device 的当前状态. 官方原话: Device Shadow is a JSON Document used to store and retrieve current state information for a device. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.
- **Device Shadow Service**: 是一个服务, 维护所有 Device Shadow (相当于一个数据库). Device Shadow Service Provides persistent representation of your devices. https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html.


Device Register Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Docs: https://docs.aws.amazon.com/iot/latest/developerguide/register-device.html
- 什么是 Device Register Service: 用于管理 AWS Resource 和 Device 之间的联系. Shadow Service 相当于一个数据库, 管理 Device 的状态和数据. 而 Device Register Service 负责 Device 注册.