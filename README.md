# MAA_MHXY_MG

简介：[MaaFramework](https://github.com/MaaXYZ/MaaFramework)梦幻西游手游助手

## 功能介绍

### 已完成
    1.日常签到
    2.帮派签到
    3.师门任务
    4.秘境任务
    5.宝图任务（获得）
    5.宝图任务（挖）
    6.运镖任务
    7.整理背包
### 待完成
    1.其他任务
    2.副本任务（320，520）
    3.背包

## 使用说明
    1.下载对应版本 X86，arm
    2.解压后运行 `MaaPiCli.exe` 即可（有机会补充详细手册）
    3.MUMU模拟器12，1280*720 240dpi

## 使用方法
### ①
启动后会出现:
```
Welcome to use Maa Project Interface CLI!

Version: v0.0.1

### Select ADB ###

        1. Auto detect
        2. Manual input

Please input [1-2]:
```
分别代表：
1. 自动检测，如果在同一台机器上开启着模拟器，可以尝试选择这个。

```
### Select ADB ###

        1. Auto detect
        2. Manual input

Please input [1-2]: 1

Finding device...

## Select Device ##

        1. MuMuPlayer12
                H:/Program Files/Netease/MuMuPlayer-12.0/shell/adb.exe
                127.0.0.1:16672

Please input [1-1]: 1
```
选择 1 后会像上面这样，列出若干个模拟器实例，之后选择你需要进行操控的即可。

2. 手动输入，目前手动输入对于"含空格的路径"有问题，请参考下面的说明手动修改 `config/maa_pi_config.json`，如果没有则新建，修改完成后重启 `MaaPiCli`。

```
{
    "adb": {
        "adb_path": "C:/Program Files/Netease/MuMuPlayer-12.0/shell/adb.exe",
        "address": "127.0.0.1:16416",
        "config": {
            "extras": {
                "mumu": {
                    "enable": true,
                    "index": 1,
                    "path": "C:/Program Files/Netease/MuMuPlayer-12.0"
                }
            }
        }
    },
    "controller": {
        "name": "安卓端"
    },
    "resource": "官服",
    "task": [
        {
            "name": "福利签到(已完成)",
            "option": [
            ]
        }
    ],
    "win32": {
        "_placeholder": 0
    }
}
```
其中 `"adb_path"` 部分是你的adb的路径，一般你可以在你的MuMu等模拟器的安装路径下，找到 `adb.exe`。注意如果路径里面有`\`，需要替换成 `\\'` ，就像上面那样。

`address` 是模拟器实例的 ADB 端口信息，你可以从你的模拟器上获取，获取方式相关可以参考：[MAA的文档](https://maa.plus/docs/%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html#%E7%A1%AE%E8%AE%A4-adb-%E5%8F%8A%E8%BF%9E%E6%8E%A5%E5%9C%B0%E5%9D%80%E6%AD%A3%E7%A1%AE)。

### ②
在初次启动后，会让你输入启动的任务：
```
### Add task ###

        1. 普通任务
        2. 启动游戏
        3. 帮派签到(已完成)
        4. 整理背包(已完成)
        5. 福利签到(已完成)
        6. 师门任务
        7. 师门任务2(已完成)
        8. 秘境降妖（已完成）
        9. 宝图任务(已完成)
        10.挖宝图(已完成)
        11.运镖普通(已完成)

Please input multiple [1-9]:
```
选择你要执行的任务即可。

### ③

之后会反复出现：
```
Tasks:

<这里会列出你已经增加，等待执行的任务>

### Select action ###

        1. Switch controller
        2. Switch resource
        3. Add task
        4. Move task
        5. Delete task
        6. Run tasks
        7. Exit

Please input [1-7]: 
```
    其中分别代表：
    1. 调整控制器（也就是adb地址等）
    2. 调整资源（不用管，目前只有一个）
    3. 新增任务，像②中那样
    4. 移动任务
    5. 删除任务
    6. 开始执行任务，在这之后就会自动开始操控。
    7. 退出
## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！

感谢以下开发者对本项目作出的贡献:

<!-- <a href="https://github.com/MaaXYZ/M9A/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MaaXYZ/M9A&max=1000" />
</a> -->

# 如需二次开发（开发说明）

    请参考[MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate),对本项目进行完善

# MaaPracticeBoilerplate

MaaFramework 实践模板。

## 如何开发

0. 使用右上角 `Use this template` - `Create a new repository` 来基于本模板创建您自己的项目。

1. 完整克隆本项目及子项目（地址请修改为您基于本模板创建的新项目地址）。

    ```bash
    git clone --recursive https://github.com/MaaXYZ/MaaPracticeBoilerplate.git
    ```

    **请注意，一定要完整克隆子项目，不要漏了 `--recursive`**

2. 下载 MaaFramework 的 [Release 包](https://github.com/MaaXYZ/MaaFramework/releases)，解压到 `deps` 文件夹中。

3. 配置资源文件。

    ```bash
    python ./configure.py
    ```

4. 按需求修改 `assets` 中的资源文件，请参考 MaaFramework 相关文档。

    - 可使用 [MaaDebugger](https://github.com/MaaXYZ/MaaDebugger) 进行调试；
    - 也可以在本地安装后测试：

        1. 执行安装脚本
           
      ```bash
      python ./install.py
      ```
      
        2. 运行 `install/MaaPiCli.exe`

5. 完成开发工作后，上传您的代码并发布版本。

    ```bash
    # 配置 git 信息（仅第一次需要，后续不用再配置）
    git config user.name "您的 GitHub 昵称"
    git config user.email "您的 GitHub 邮箱"
    
    # 提交修改
    git add .
    git commit -m "XX 新功能"
    git push origin HEAD -u
    ```

6. 发版您的版本

    需要先修改仓库设置 `Settings` - `Actions` - `General` - `Read and write permissions` - `Save`
    
    ```bash
    # CI 检测到 tag 会自动进行发版
    git tag v1.0.0
    git push origin v1.0.0
    ```
