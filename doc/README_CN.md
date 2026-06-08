# HACS Proxy
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[English](../README.md) | [简体中文](./doc/README_CN.md)

HACS Proxy 是为 [HACS](https://hacs.xyz) 配置自定义代理的集成。

## 安装

### 手动安装

下载 [hacs_proxy.zip](https://github.com/XaoflySho/hacs-proxy/releases/latest/download/hacs_proxy.zip) 文件解压到 Home Assistant 的 config/custom_components 文件夹下。

### HACS

使用 HACS 更新 HACS Proxy。

HACS > Overflow Menu > Custom repositories > Repository: https://github.com/XaoflySho/hacs-proxy.git & Category: Integration > ADD

## 配置

设置 > 设备与服务 > 添加集成 > 搜索”HACS Proxy” > 填写”代理地址”（必填），以及可选的”代理用户名”和”代理密码” > 提交

如需修改代理配置，进入集成条目点击”配置”即可。

## 开关实体

安装完成后会创建一个 **HACS Proxy** 开关实体，可在界面中手动切换或通过自动化控制，无需重启 Home Assistant 即可启用/禁用代理。开关状态在重启后保持。

