| Key        | Example value | Description                         |
| :--------- | :------------ | :---------------------------------- |
| `message ` | `Hello`       | Message to be sent out to recipient |

configuration.yaml

```
notify:
  - name: zulip_notification
    platform: notify_zulip
    site: 'PASTE_YOUR_ZULIP_URL_HERE'
    email: 'PASTE_YOUR_BOT_EMAIL_HERE'
    key: 'PASTE_YOUR_BOT_key_HERE'
    channel: 'PASTE_THE_CHANNEL_YOU_WANT_BOT_NOTIFY_HERE'
```
