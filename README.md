<h1 align="center">
  <a href="https://github.com/XYCode-Kerman/ItsWA">
    <img src="https://raw.githubusercontent.com/XYCode-Kerman/ItsWA/docs/logo.svg" alt="Logo" width="100" height="100">
  </a>
</h1>


<div align="center">
  ItsWA
  <br />
  <a href="#about"><strong>查看使用效果</strong></a>
  <br />
  <br />
  <a href="https://github.com/XYCode-Kerman/ItsWA/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/XYCode-Kerman/ItsWA/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/XYCode-Kerman/ItsWA/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

![GitHub License](https://img.shields.io/github/license/XYCode-Kerman/ItsWA?style=flat-square) [![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white&style=flat-square)](https://conventionalcommits.org)

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/XYCode-Kerman/ItsWA/master?style=flat-square&label=Last%20Commit%20on%20Master) ![Codecov (with branch)](https://img.shields.io/codecov/c/github/XYCode-Kerman/ItsWA/master?style=flat-square&label=Coverage%20on%20Master)

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/XYCode-Kerman/ItsWA/develop?style=flat-square&label=Last%20Commit%20on%20Develop) ![Codecov (with branch)](https://img.shields.io/codecov/c/github/XYCode-Kerman/ItsWA/develop?style=flat-square&label=Coverage%20on%20Develop)

</div>

---

## 关于

ItsWA是一个基于Python实现的代码评测系统，使用`Lrun`提供安全运行时。并且所有比赛信息均存储在`ccf.json`中，方便在各个计算机间的移动。

作为ItsWA的姊妹项目，[ItsWA-Editor](https://github.com/XYCode-Kerman/ItsWA-Editor/)（简称ITED）实现了一个在**前端**的GUI，通过访问ItsWA-API的方式实现了对比赛的远程管理（即可以远程操作评测机进行评测）。

|                          ITED的首页                          |                         ITED评测结果                         |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![image-20240415134229646](https://github.com/XYCode-Kerman/ItsWA/blob/docs/images/image-20240415134229646.png?raw=true) | ![image-20240415134359382](https://github.com/XYCode-Kerman/ItsWA/blob/docs/images/image-20240415134359382.png?raw=true) |

### 技术栈

* Python
  * Pydantic
  * AsyncIO
  * FastAPI
* Linux
  * Lrun（WIP）

## 开始

查看[Getting Started - ItsWA Online Documents](https://docs.itswa.xycode.club/)。

## 使用

查看[安装 - ItsWA Online Documents](https://docs.itswa.xycode.club/how-to-use/install/)。

## 开发路线图

在 [open issues](https://github.com/XYCode-Kerman/ItsWA/issues) 中列出了我们将会修复的bug和将会新增的功能。

## 寻求帮助

通过如下方式，可以向我们寻求帮助

- 查看已解决的 Issue。
- 发起一个新的 Github Issue。

## 帮助开发

为了帮助我们的开发，您可以做以下几件事：

- 给我们的项目点一个 [Star](https://github.com/XYCode-Kerman/ItsWA)。
- 向其他OIer、教练或非正式赛事组织方推荐ItsWA。
- 在[Issue](https://github.com/XYCode-Kerman/ItsWA/issues)中向我们提起新功能建议或报告已知的Bug。
- 根据[开发规范](https://docs.itswa.xycode.club/develop/rules/)编写贡献代码，并提起[Pull Request](https://github.com/XYCode-Kerman/ItsWA/pulls)，将其合并到我们的项目中。

## 开发者

本项目目前由 [XYCode Kerman](https://github.com/XYCode-Kerman) 一个人**独立制作**完成。

在 [the contributors page](https://github.com/XYCode-Kerman/ItsWA/contributors) 查看所有的贡献者。

## 安全

ItsWA无法保证我们的代码中没有安全漏洞，因此请您自行做好安全措施，包括但不限于以下几点：

1. 不要将ItsWA Management API暴露到公网中。
2. 不要直接将ItsWA Online Judge API暴露到公网中，使用Zerotier等服务实现有限的服务共享。
3. 不要用ItsWA Built-in Online Judge来搭建公共OJ。
4. 确保你可以在线下找到所有选手，如果他们的代码损坏了评测机，请**立即**要求他们进行赔偿！

如果您在Review Code过程中发现了任何安全问题，**请勿**擅自将其公开，而应立即将安全问题发送到xycode-xyc@outlook.com以获取我们的技术支持。当您获得我们的允许后，方可公开该问题。

## 关于遥测

为了方便开发，ItsWA会向遥测服务上报一些不涉及隐私的基本信息，该遥测服务的源代码位于[XYCode-Kerman/ItsWA-Telemetering](https://github.com/XYCode-Kerman/ItsWA-Telemetering)。遥测服务只会收集ItsWA的开启、关闭等基本信息，访问[itte.api.xycode.club/docs](http://itte.api.xycode.club/docs)以获取ItsWA遥测服务的帮助（包括自己已有的遥测信息、删除遥测记录等）。

> 尽管ITTE的代码中包含了收集客户端的IP地址的逻辑-，但由于ITTE使用了Service + Ingress进行部署，**因此ITTE实际上收集到的IP地址实际上是集群内部的IP地址**。

**如果您不希望使用遥测服务，请打开`configs.py`并将其中的`TELEMETERING = True`修改为`TELEMETERING = False`。**

## 许可证

本项目的许可证是 **GPL v3**。

> GNU 通用公共许可证是传染性协议，这意味着所有使用到 ItsWA 或基于 ItsWA 修改的程序应当 使用相同的许可证并开放源代码。
>
> 但是根据本软件作者的意愿，如果您有修改本软件并闭源的需求，请依照下方的模板，发送一份申请到 [xycode-xyc@outlook.com](mailto:xycode-xyc@outlook.com)，获得许可后您可无视 GNU 通用公共许可证中的条款来对本软件的某一版 本进行修改和再分发。（详情请见用户手册）
