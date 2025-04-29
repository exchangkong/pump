import os
import random
import uuid
from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, audio_dir, output_dir):
        """初始化音频处理器
        
        Args:
            audio_dir: 源音频文件目录
            output_dir: 输出音频文件目录
        """
        self.audio_dir = audio_dir
        self.output_dir = output_dir
        self.audio_files = self._load_audio_files()
        
    def _load_audio_files(self):
        """加载音频文件列表
        
        Returns:
            dict: 按类型分类的音频文件路径字典
        """
        files = {'long': [], 'medium': [], 'min': []}
        for file in os.listdir(self.audio_dir):
            if file.endswith('.WAV'):
                if 'long' in file:
                    files['long'].append(os.path.join(self.audio_dir, file))
                elif 'medium' in file:
                    files['medium'].append(os.path.join(self.audio_dir, file))
                elif 'min' in file:
                    files['min'].append(os.path.join(self.audio_dir, file))
        return files
    
    def list_source_files(self):
        """获取所有源音频文件名称
        
        Returns:
            list: 音频文件名称列表
        """
        return [os.path.basename(file) for file in self.audio_files]
    
    def synthesize(self, target_duration=None, type=None):
        """合成新的音频文件
        
        Args:
            target_duration: 目标音频长度(秒)，如果为None则随机生成3-5秒的音频
            type: 音频类型，可选值为 'long'、'medium'、'min'，默认为 'long'
            
        Returns:
            str: 输出音频文件路径
        """
        # 验证并设置音频类型
        valid_types = ['long', 'medium', 'min']
        audio_type = type if type in valid_types else 'long'
        
        if not self.audio_files[audio_type]:
            raise Exception(f"not found {audio_type} type audio files")
        
        # 如果没有指定目标时长，则随机生成3-5秒的音频
        if target_duration is None:
            target_duration = random.uniform(3, 8)
        
        # 随机选择音频文件并合成
        combined = self._combine_audio_files(target_duration, audio_type)
        
        # 生成唯一的输出文件名
        output_filename = f"synthesized_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # 保存合成的音频
        combined.export(output_path, format="wav")
        
        return output_path
    
    def _combine_audio_files(self, target_duration, audio_type):
        """组合多个音频文件以达到目标时长
        
        Args:
            target_duration: 目标音频长度(秒)
            audio_type: 音频类型，'long'、'medium' 或 'min'
            
        Returns:
            AudioSegment: 合成的音频段
        """
        # 初始化一个空的音频段
        combined = AudioSegment.silent(duration=0)
        current_duration = 0
        
        # 获取指定类型的音频文件并随机打乱
        audio_files = self.audio_files[audio_type]
        random_files = random.sample(audio_files, len(audio_files))

        print(random_files)
        print(['target_duration', target_duration])
        
        # 循环添加音频片段直到达到目标时长
        while current_duration < target_duration:  # 转换为毫秒
            # 随机选择一个音频文件
            audio_file = random.choice(random_files)
            
            # 加载音频文件
            audio = AudioSegment.from_wav(audio_file)
            print(['while', audio_file])
            
            # 如果添加整个音频会超出目标时长，则只添加部分

            # remaining_duration = target_duration * 1000 - current_duration
            # if len(audio) > remaining_duration:
            #     audio = audio[:int(remaining_duration)]
            
            # 添加到合成音频
            combined += audio
            current_duration += 1
        
        return combined