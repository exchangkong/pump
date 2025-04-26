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
        if contentStr == None:
          return jsonify({
            "success": False,
            "message": "text is required"
          }), 500
        
        # 合成音频
        if duration is None:
            duration = random.randint(2, 6)  # 随机生成3-5秒的音频
        output_file = audio_processor.synthesize(duration)
        
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
    print(f"服务已启动，请访问 http://localhost:9000 查看演示页面")
    #port = 9000
    port = int(os.environ.get('PORT', 9000))
    app.run(debug=True, host='0.0.0.0', port=port)