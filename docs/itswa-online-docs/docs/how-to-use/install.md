# 安装

ItsWA程序以源代码形式提供，ITED以编译结果形式提供（同时也开放源代码），且会被ItsWA自动下载。

## 下载程序源代码

### 稳定版

确保你的操作系统上已经安装了`python >= 3.10`，在[Releases · XYCode-Kerman/ItsWA (github.com)](https://github.com/XYCode-Kerman/ItsWA/releases)上下载一个版本，并解压到一个空文件夹。

### 开发版

确保你的操作系统上已经安装了`git`、`python >= 3.10`，然后使用`git`克隆本仓库。

```bash
git clone -b develop https://github.com/XYCode-Kerman/ItsWA.git
```

## 安装依赖

> 注意：`poetry`并不会将依赖安装到系统的`python`环境中，而是会创建一个新的虚拟环境。

本项目采用`poetry`和`pyproject.toml`管理依赖，因此请确保你安装了`poetry`，否则请使用`pip install poetry`安装。

然后，使用如下命令安装依赖：

```bash
poetry install
```

## 使用

在终端运行`poetry run python main.py`，如果正常，则应当会输出如下内容（注意：忽略了非文本内容）：

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...
Try 'main.py --help' for help.

Error
Missing command
```



