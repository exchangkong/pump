from flask import Flask, request, jsonify, send_file, send_from_directory
import os
from audio_processor import AudioProcessor
from flask_cors import CORS
import random


app = Flask(__name__, static_folder='static')
CORS(app)  # 启用CORS支持

# 初始化音频处理器
audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

audio_processor = AudioProcessor(audio_dir, output_dir)

@app.route('/api/synthesize', methods=['POST'])
def synthesize_audio():
    """合成新的音频文件
    
    Returns:
        JSON: 包含合成音频文件URL的JSON响应
    """
    try:
        # 获取请求参数，如果没有提供则使用默认值
        duration = request.json.get('duration', None)  # 可选参数，指定音频长度
        contentStr = request.json.get('text', None)  # 可选参数，指定合成的文本内容
        type = request.json.get('type', None)  # 可选参数，指定合成的文本内容
        if contentStr == None:
          return jsonify({
            "success": False,
            "message": "text is required"
          }), 500
        
        # 根据文本内容计算音频时长
        if duration is None:
            # 判断是否为纯英文（只包含英文字母、空格和标点）
            is_english = all(c.isascii() for c in contentStr)
            # 判断是否为纯中文（每个字符都是中文）
            is_chinese = all('\u4e00' <= c <= '\u9fff' for c in contentStr)
            
            if is_english:
                # 英文按照单词数计算
                words = len(contentStr.split())
                duration = min(max(words * 1, 2), 6)  # 每个单词0.5秒，最短2秒，最长6秒
            elif is_chinese:
                # 中文按照字数计算
                chars = len(contentStr)
                duration = min(max(chars * 1, 2), 6)  # 每个字0.5秒，最短2秒，最长6秒
            else:
                # 混合内容按照字符数计算
                chars = len(contentStr)
                duration = min(max(chars * 1, 2), 6)  # 每个字符0.3秒，最短2秒，最长6秒
        output_file = audio_processor.synthesize(duration, type)
        
        # 返回音频文件的URL
        file_url = f"/api/audio/{os.path.basename(output_file)}"
        
        return jsonify({
            "success": True,
            "message": "success",
            "file_url": file_url
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"audio fail: {str(e)}"
        }), 500

@app.route('/api/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """获取合成的音频文件
    
    Args:
        filename: 音频文件名
        
    Returns:
        File: 音频文件
    """
    try:
        file_path = os.path.join(output_dir, filename)
        return send_file(file_path, mimetype='audio/wav')
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"get audio fail: {str(e)}"
        }), 404

# @app.route('/api/list', methods=['GET'])
def list_audio_files():
    """列出所有可用的原始音频文件
    
    Returns:
        JSON: 包含音频文件列表的JSON响应
    """
    try:
        files = audio_processor.list_source_files()
        return jsonify({
            "success": True,
            "files": files
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"get audio list fail: {str(e)}"
        }), 500

@app.route('/')
def index():
    """提供前端页面
    
    Returns:
        HTML: 前端页面
    """
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    #port = 9000
    port = int(os.environ.get('PORT', 9000))
    print(f"服务已启动，请访问 http://localhost:%d 查看演示页面", port)
    app.run(debug=True, host='0.0.0.0', port=port)