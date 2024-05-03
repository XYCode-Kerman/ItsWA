# 编辑题目

## 基本属性

题目一共拥有六个基本属性，即**“题目名称”、“题目背景”、“题目描述”、“输入格式”、“输出格式”**。

尽管在当前版本中只有**“题目名称”**会被用到，但在后续版本中，其他属性将会被展示在本项目的OJ中。

> 除了**“题目名称”**外的属性都支持Markdown和Latex符号。

## 评测姬配置

**源文件名称**是唯一的选项，用于标识选手的源文件地址。

例如当**源文件名称**设置为*hello*时，选手的代码文件需要放置在`选手文件夹/hello/hello.cpp`，放置在其他位置则无效！

## 测试点配置

对于每个测试点而言，其拥有六个属性，分别是**“输入”、“答案”、“输入方式”、“输出方式”**、*“输入文件”、“输出文件”*（黑体字表示必选项，斜体字表示可选项）。

> :warning: 输入输出文件必须是一个相对路径，而且仅在**输入输出方式**为`FILE`时可设置。
>
> :warning: 输入输出的编码方式均为[`utf-8`](https://baike.baidu.com/item/UTF-8/481798)，使用其他编码方式输入将会导致`UnicodeDecodeError`错误（计划修复）。
>
> :loud_sound: 不必考虑CRLF和LF的区别，ItsWA已经在[judge: 测试点的CRLF和LF不兼容 (27c3f04)](https://github.com/XYCode-Kerman/ItsWA/commit/27c3f0499633620153280679fa75a8a02cbf1369)中用两行代码解决了该问题。

**输入**与**答案**不必解释。

**输入方式**有`STDIN`和`FILE`两种，当设置为`STDIN`时ItsWA将会通过[标准输入(stdin)](https://baike.baidu.com/item/%E6%A0%87%E5%87%86%E8%BE%93%E5%85%A5%E8%BE%93%E5%87%BA/4714867)为程序输入参数；设置为`FILE`时会将输入文件存储在`输入文件`中（可执行程序的CWD的相对位置）。

**输出方式**有`STDOUT`和`FILE`两种，当设置为`STDOUT`时ItsWA将会从[标准输出(stdout)](https://baike.baidu.com/item/%E6%A0%87%E5%87%86%E8%BE%93%E5%85%A5%E8%BE%93%E5%87%BA/4714867)中读取程序输出；设置为`FILE`时ItsWA将会从`输出文件`中读取程序输出（可执行程序的CWD的相对位置）。

## 从文件导入测试点

**输入文件后缀名**：即输入测试点文件的后缀名，例如当该属性设置为`in`时`a.in`和`a.out`中的`a.in`将会被视作输入测试点。默认为`in`。

**答案文件后缀名**：即测试点答案文件的后缀名，例如当该属性设置为`out`时`a.in`和`a.out`中的`a.out`将会被视作测试点答案。默认为`out`。

**测试点文件命名规则**：其中需要包含一个数字，**具有相同数字**（注意：不是*不带后缀的文件名*相同）的两个输入文件和答案文件将会被视作**一对测试点**。

**合法示例：**

1. `a1.in`和`a1.out`是一对测试点。
2. `a_1.in`和`a_1.out`是一对测试点。
3. `a___114.in`和`a___114.out`是一对测试点。
4. `a1.in`和`a_1.out`是一对测试点。

**非法示例：**

1. `a.in`和`a.out`不是一对测试点。
2. `a_1.in`和`a.out`不是一对测试点。

**形式化的，这是ITED中判断文件是否是一对测试点的代码：**

```ts
let ckpt_file_groups = computed(() => {
    const ckpt_file_names: File[] = checkpoints_files.value
    const input_files: File[] = []
    const answer_files: File[] = []

    ckpt_file_names.forEach(x => {
        if (x.name.endsWith(ckpt_input_suffix.value)) {
            input_files.push(x)
        } else if(x.name.endsWith(ckpt_answer_suffix.value)) {
            answer_files.push(x)
        }
    })

    input_files.sort(x => x.name.search(/[0-9]/))
    answer_files.sort(x => x.name.search(/[0-9]/))

    const result: File[][] = []
    input_files.forEach((x, i) => {
        //           输入文件      输出文件
        result.push([x, answer_files[i]])
    })

    return result
})
```

