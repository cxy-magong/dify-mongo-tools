## mongo

**Author:** mrh
**Version:** 0.0.1
**Type:** tool

### Description


## 调试

```shell
# 修改 `.env` 文件，改为 dify 的插件调试接口
cp .env.example .env
pip install -r requirements.txt
python main.py
```
## 发布

```shell
# 不同的版本和系统，下载链接不同，参见： https://github.com/langgenius/dify-plugin-daemon/releases
mkdir output;cd output
wget https://github.com/langgenius/dify-plugin-daemon/releases/download/0.0.6/dify-plugin-linux-amd64
chmod +x dify-plugin-linux-amd64
./dify-plugin-linux-amd64 plugin package ../../dify_plugin_mongo -o $PWD/dify_plugin_mongo.difypkg
```
