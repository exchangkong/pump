# 音频合成项目

这是一个 Python 音频合成项目，可以随机组合现有的音频文件生成 3-5 秒的新音频。项目提供 API 接口，让前端可以调用进行音频合成。

## 功能特点

- 随机组合 5 个音频文件生成新的音频
- 生成的音频长度在 3-5 秒之间
- 提供 RESTful API 接口供前端调用
- 支持自定义音频长度（在 3-5 秒范围内）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 项目结构

```
.
├── app.py              # Flask应用主文件
├── audio_processor.py  # 音频处理模块
├── requirements.txt    # 项目依赖
├── audio/              # 源音频文件目录
│   ├── dog-1.wav
│   ├── dog-2.wav
│   ├── dog-3.wav
│   ├── dog-4.wav
│   └── dog-5.wav
└── output/             # 合成音频输出目录
```

## 启动服务

```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口说明

### 1. 合成音频

- **URL**: `/api/synthesize`
- **方法**: POST
- **请求参数**:

```json
{
  "duration": 4.5 // 可选，指定音频长度（3-5秒范围内）
}
```

- **响应**:

```json
{
  "success": true,
  "message": "音频合成成功",
  "file_url": "/api/audio/synthesized_12345678.wav"
}
```

### 2. 获取音频文件

- **URL**: `/api/audio/<filename>`
- **方法**: GET
- **响应**: 音频文件（WAV 格式）

### 3. 列出可用的源音频文件

- **URL**: `/api/list`
- **方法**: GET
- **响应**:

```json
{
  "success": true,
  "files": ["dog-1.wav", "dog-2.wav", "dog-3.wav", "dog-4.wav", "dog-5.wav"]
}
```

## 注意事项

- 确保系统已安装 Python 3.6+
- 需要安装 FFmpeg 以支持音频处理功能
- 默认使用 audio 目录下的音频文件作为源文件
