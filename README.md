[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration)

# Blue Archive Favor Rank

追踪蔚蓝档案学生好感度的HomeAssistant集成，数据来源[arona.icu](https://arona.icu/)

适用于国服和国际服，但目前集成只有简体中文本地化。

Including data from both CN and global servers, but currently only Simplified Chinese localization has been carried out.

### 使用
- 在 [此处](https://arona.icu/about) 申请arona.icu什亭之匣api
- 通过 [HACS](https://hacs.xyz/) 添加 Custom repositories ，仓库 `https://github.com/k96e/BAFavRank` ，类型 `Integration` ，并下载本集成，重启HomeAssistant
- 游戏内确保需要追踪的学生放入任意助战位，并记下账号好友码
- 进入HomeAssistant配置，添加集成 `Blue Archive Favor Rank` ，输入api key及好友码，选择需要追踪的学生
- Done!