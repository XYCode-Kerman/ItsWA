## 0.0.3-alpha.1 (2024-04-16)


### ⚠ BREAKING CHANGES

* **online_judge:** 比赛管理的API结构
* **online_judge:** 修改比赛管理的API结构
* **online_judge:** 比赛管理的API结构
* **online_judge:** 将OJ相关配置从ccf_parser移动到online_judge内

### Features

* 用户鉴权 ([8e6d02b](https://github.com/XYCode-Kerman/ItsWA/commit/8e6d02b205e1a9f3ba3a836fcb169bb5ecb2c703))
* **oj:** 实现oj的用户管理 ([7e94ec6](https://github.com/XYCode-Kerman/ItsWA/commit/7e94ec6c4b1c1cb03170d4ad9dbbb284c8240f56))
* **online_judge:** 比赛管理 ([ede3426](https://github.com/XYCode-Kerman/ItsWA/commit/ede3426987313774bb2eb84e4a9cd084dd4d41a6))
* **online_judge:** 比赛管理的API结构 ([9a93548](https://github.com/XYCode-Kerman/ItsWA/commit/9a935488e31f197f618f970ec4a5547ffdce477c))
* **online_judge:** 从OJ获取题目 ([574d45e](https://github.com/XYCode-Kerman/ItsWA/commit/574d45efa75a16cedffb97085d2ef8c0a00c599d))
* **online_judge:** 将OJ相关配置从ccf_parser移动到online_judge内 ([2623008](https://github.com/XYCode-Kerman/ItsWA/commit/26230083b31f31334e47b55e53d8257c6ae33054))


### Bug Fixes

* **online_judge:** 获取解密apikey失败的问题 ([882c497](https://github.com/XYCode-Kerman/ItsWA/commit/882c497008c8f147c0993fa9c537c1f3f4d64642))


### Code Refactoring

* **online_judge:** 比赛管理的API结构 ([a55fdaa](https://github.com/XYCode-Kerman/ItsWA/commit/a55fdaaf55fdd949bb812e22113f5f224032eca7))
* **online_judge:** 修改比赛管理的API结构 ([ea283c9](https://github.com/XYCode-Kerman/ItsWA/commit/ea283c9a75840ccb738fa8279ebad1df606d40b8))


##  0.0.2-beta.1 (2024-04-12)


### Features

* **judge:** JudgingResult新增计算属性sum_score ([f8312bf](https://github.com/XYCode-Kerman/ItsWA/commit/f8312bff70357847225000100fb1319c63430784))


### Bug Fixes

* **ccf_parser:** 错误的CKPT参数将会被自动修正 ([e6979a7](https://github.com/XYCode-Kerman/ItsWA/commit/e6979a7afbd67486d6525b36b48815d6b01f4cdc))
* **judge:** 自动清理评测过程中产生的编译结果 ([9a7ed6c](https://github.com/XYCode-Kerman/ItsWA/commit/9a7ed6caba1b39d729611965bad4a2ee0a2afa93))
* **manager:** 从release下载ITED ([68d8f31](https://github.com/XYCode-Kerman/ItsWA/commit/68d8f319fd31d0b5b866a3393e25828104075876))

##  0.0.2-alpha.1 (2024-04-10)


### ⚠ BREAKING CHANGES

* **judge:** 多线程评测
* **judge:** 评测采用生成器形式

### Features

* **judge:** 多线程评测 ([25604f1](https://github.com/XYCode-Kerman/ItsWA/commit/25604f187671ff036ba2df1d7a9f4978fdcdcffb))
* **judge:** 评测采用生成器形式 ([f59293d](https://github.com/XYCode-Kerman/ItsWA/commit/f59293d4698588409cfec08628857460f613e203))
* **manager:** 自动下载最新的ITED ([db09c1d](https://github.com/XYCode-Kerman/ItsWA/commit/db09c1d021ef86da654c9f404374546dac4bdaea))


### Bug Fixes

* **judge:** 测试点的CRLF和LF不兼容 ([27c3f04](https://github.com/XYCode-Kerman/ItsWA/commit/27c3f0499633620153280679fa75a8a02cbf1369))
* **manager:** 兼容生成器形式的评测 ([fcf0def](https://github.com/XYCode-Kerman/ItsWA/commit/fcf0def3f8fcbce9e3aaf1d58ae9e2561772b544))

