# cloopy

Cloopy是一款用来集成企业微信发通知的软件，用Go语言开发，轻量高效。

代码来源于 https://github.com/liozzazhang/message-transfer

目前主要用于和 Grafan 的集成

```
FROM alpine
add cloopy /
EXPOSE 12345
CMD ["/cloopy"]
```