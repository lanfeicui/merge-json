# merge-json
合并多个翻译片段文件，组合成新语言包JSON文件的扩展，适用于 [AUTOMATIC1111's stable diffusion webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

## 如何安装webUI简体中文语言包
### 1. 通过网址安装
- 点击 `extension` 选项卡，点击 `Install from URL` 子选项卡
- 复制本 git 仓库网址：
```
https://github.com/lanfeicui/merge-json.git
```
- 粘贴进 URL 栏，点击 `Install`

- 安装完成，跳转到 [如何使用](#如何使用)

### 2. 或者，直接下载然后放在对应路径
- [下载本 git 仓库](https://codeload.github.com/lanfeicui/merge-json/zip/refs/heads/main)为 zip 档案

- 解压，并把文件夹放置在 webui 根目录下的 `extensions` 文件夹中，放好之后应该会如下图
- 安装完成，跳转到 [如何使用](#如何使用)

## 如何使用
**重启webUI以启用扩展**
- 在 `Extensions` 选项卡，确定已勾选本扩展☑️；如未勾选，勾选后点击**橙色按钮**启用本扩展。  

**整理翻译片段json文件**
- 建立存放翻译片段json文件的文件夹，路径无限制，举例：取名 zh_CN
- 添加json文件。
-- 可以根据需求，在其下面建立多个子文件夹。
-- 文件名随意。后缀名：”json“
-- 文件名结尾含有Overwrite.json的符合条件的json文件里面翻译词条为强制替换，主要区别是运行脚本时不会提示重复词条。

**配置参数**
- packExtension
- packFolderPath
- defaultJSONPath
- outJSONPath

```bash
#语言片段文件后缀名
packExtension = "json"

#pack语言包文件夹路径(含子文件夹)
packFolderPath = "D:\stable-diffusion-webui\extensions\merge-json\zh_CN"


#参考的语言包json文件的路径
#  可为空
#defaultJSONPath = ""
defaultJSONPath = "D:\stable-diffusion-webui\extensions\stable-diffusion-webui-localization-zh_CN\localizations\zh_CN.json"

#生成新的文件路径，可以指定或空
#  若为空：
#    举例：
#      outJSONPath = "", defaultJSONPath = "D:\stable-diffusion-webui\extensions\stable-diffusion-webui-localization-zh_CN\localizations\zh_CN.json"
#      返回 D:\stable-diffusion-webui\extensions\merge-json\localizations\zh_CN-Merge-zh_CN.json
#  若为空并且defaultJSONPath也为空：
#    举例：
#      outJSONPath = "", defaultJSONPath = "",当前py文件路径："D:\stable-diffusion-webui\extensions\merge-json\merge.py"
#      返回 D:\stable-diffusion-webui\extensions\merge-json\localizations\zh_CN-AutoBuild.json

#outJSONPath = "D:\stable-diffusion-webui\localizations\zh_CN_AutoBuild.json"
outJSONPath = ""
```

**生成合并**
手动执行 build.py ，会在指定未知生成心的语言包文件。例如：zh_CN-Merge-zh_CN.json

**选择合并后的语言包（zh_CN-Merge-zh_CN）**
- 在 `Settings` 选项卡中，找到 `Localization (requires restart)` 小项，然后在下拉选单中选中 `zh_CN-Merge-zh_CN` （如果没有就按一下🔄按钮），如图
  
- 然后按一下 页面顶部的  **橙色按钮** 保存设置，再按 页面底部的 **橙色按钮** 重启webUI

**后期扩展翻译词条如何生效**
每次手动执行 build.py 之后，合并后的语言包文件不能立即在web上生效。

- 1. 重启stable-diffusion-webui（不建议）***
-- 关掉stable-diffusion-webui的启动窗口，重新启动运行 webui-user.bat (或者对应启动脚本)。

- 2. 刷新WebUI***
-- 在 `Settings` 选项卡，点击 **页面顶部**的 **橙色按钮** **ReloadUI** 刷新网站