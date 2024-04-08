# ItsWA

![GitHub License](https://img.shields.io/github/license/XYCode-Kerman/ItsWA?style=flat-square) [![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/XYCode-Kerman/ItsWA/master?style=flat-square&label=Last%20Commit%20on%20Master) ![Codecov (with branch)](https://img.shields.io/codecov/c/github/XYCode-Kerman/ItsWA/master?style=flat-square&label=Coverage%20on%20Master)

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/XYCode-Kerman/ItsWA/develop?style=flat-square&label=Last%20Commit%20on%20Develop) ![Codecov (with branch)](https://img.shields.io/codecov/c/github/XYCode-Kerman/ItsWA/develop?style=flat-square&label=Coverage%20on%20Develop)

ItsWA是一个基于`Python`搭建，使用`Lrun`提供安全运行时的`Linux`下的竞赛代码评测系统。

## 使用教程

ItsWA提供一个基于Latex编写的用户手册，在本项目的`docs/`中。

> ItsWA在目前不会考虑使用例如Markdown等**难以印刷**的排版语言编写文档，ItsWA的文档设计始终以**可印刷性、易读性**为宗旨。也许在以后我们会基于`Mkdocs`提供一个在线文档？

## 关于CCF

在本程序语境下，CCF指的是`Contest Config File`（比赛配置文件）而非**中国计算机学会**，本软件及其开发者与**中国计算机学会**之间没有任何关联！

## 许可证声明

GNU 通用公共许可证是传染性协议，这意味着所有使用到 ItsWA 或基于 ItsWA 修改的程序应当
使用相同的许可证并开放源代码。

但是根据本软件作者的意愿，如果您有修改本软件并闭源的需求，请依照下方的模板，发送一份申请到
xycode-xyc@outlook.com，获得许可后您可无视 GNU 通用公共许可证中的条款来对本软件的某一版
本进行修改和再分发。（详情请见用户手册）

## 关于开发

### 提交规范

本项目自2024年4月8日起采用[**约定式提交 v1.0.0**](https://www.conventionalcommits.org/zh-hans/v1.0.0/)作为提交的格式规范，语言为**中文**，不符合提交规范的代码将会被拒绝！

### 测试结果（来自CodeCov）

![codecov.io/gh/XYCode-Kerman/ItsWA/graphs/icicle.svg?token=8knjccNoca](https://codecov.io/gh/XYCode-Kerman/ItsWA/graphs/icicle.svg?token=8knjccNoca)

### Work-In-Progress

本项目正处于开发状态，请勿将其用于正式比赛的评测！我们不保证评测结果始终是正确的。

以下是本项目已经完成的功能。

- [x] CCF的解析器
- [ ] CCF的UI编辑器
- [x] 不良代码过滤器
  - [x] CPP支持
  - [ ] C支持
- [x] 评测
  - [ ] 语言
    - [x] CPP
    - [ ] C
  - [x] 测试点
    - [x] STDIN/STDOUT
    - [x] FILE
  - [ ] 测试点状态支持
    - [x] AC
    - [x] CE
    - [x] WA
    - [x] RE
    - [x] TLE
    - [ ] MLE
    - [ ] OLE
  - [ ] 安全防护
    - [x] 代码过滤
    - [ ] 系统调用防护

