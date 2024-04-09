# 开发规范

## 提交签名

为了防止恶意用户使用和贡献者相同的用户名和邮箱伪造提交，从 2024 年 3 月 29 日起 ItsWA 项目只会接收已签名 (Verified) 的提交。

## 提交描述

ItsWA的提交描述遵循[约定式提交 v1.0.0 (conventionalcommits.org)](https://www.conventionalcommits.org/zh-hans/v1.0.0/)，所有提交描述必须按照该标准撰写，不符合该规范的提交和PR将会被拒绝。

## 代码规范

除本项目另有规定，所有代码均需要符合 PEP8 规范。 建议本项目贡献者安装 autopep8 并设置为保存时自动格式化

## 程序测试

程序测试是一个程序可靠性的根本保障，因此我们要求 ItsWA 的测试覆盖率必须 ≥ 95%。 对于无法测试到的代码，应当使用`#pragma no cover`进行标记。

值得注意的是，如果您只是为了达到 覆盖率要求，而大量使用该标记，那么您的提交或 PR 将会被拒绝。 ItsWA 使用 Pytest 作为测试框架，使用 `pytest-cov` 生成测试率报告，只需执行`pytest –cov –cov-report=html -v -n auto`即可自动进行多线程测试并生成 html 报告。