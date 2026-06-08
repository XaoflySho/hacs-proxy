# HACS Proxy
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[English](./README.md) | [简体中文](./doc/README_CN.md)

HACS Proxy is an integration that provides custom proxy for [HACS](https://hacs.xyz)

## Installation

### Manual

Download the [hacs_proxy.zip](https://github.com/XaoflySho/hacs-proxy/releases/latest/download/hacs_proxy.zip) file and extract it to the `config/custom_components` folder of Home Assistant.

### HACS

Use HACS to update HACS Proxy.

HACS > Overflow Menu > Custom repositories > Repository: https://github.com/XaoflySho/hacs-proxy.git & Category: Integration > ADD

## Configuration

Configuration > Devices & Services > Add Integration > Search for "HACS Proxy" > Fill in "Proxy URL" (required) and optionally "Proxy Username" & "Proxy Password" > Submit

To update proxy settings later, go to the integration entry and click "Configure".

## Switch Entity

After setup, a **HACS Proxy** switch entity is created. You can toggle it in the UI or via automations to enable/disable the proxy at runtime without restarting Home Assistant. The switch state is persisted across restarts.

