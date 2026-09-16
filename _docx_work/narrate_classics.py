# -*- coding: utf-8 -*-
"""给5个原理动画微课补中文旁白：TTS合成 → tpad延长视频末帧 → 合流替换原mp4"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_videos_v2 import VOICE, _dur, tts, TMPD          # noqa: E402
import subprocess                                         # noqa: E402

MAT = "/Users/joelgong/Desktop/现代制造 1/Python编程实战/教学实施资料"

# 旁白脚本（与动画内容逐段对应；分段≈动画节奏，段落间由TTS自然停顿）
NARR = {
    "04-教学管理工具包/微课视频/六步法80分钟时间盒.mp4": [
        "六步法怎么装进八十分钟课堂？两课时，每节四十分钟，一起看时间盒。",
        "资讯和计划移到课前线上完成，课堂从决策开始：十分钟，备选方案对比加决策矩阵。",
        "接着是第一轮实施，三十分钟，目标是骨架贯通，先跑通再优化。",
        "中间穿插五分钟检查，三层质检：自己查、同伴查、老师抽查。",
        "然后第二轮实施二十五分钟，集中优化冲优秀标准。",
        "最后十分钟评价：量表自评加教师反馈。六个环节环环相扣，这就是六步法的课堂节奏。",
    ],
    "01-AI应用基础/微课视频/滑动窗口与RUL预测.mp4": [
        "怎么用一段振动历史预测设备的剩余寿命？关键一步：滑动窗口。",
        "把连续传感器序列切成一个个固定长度的小窗口，每个窗口后面的若干步，就是它要预测的真值。",
        "窗口像传送带一样不断向后滑动，一条长序列就变成了成百上千个训练样本。",
        "模型学会从窗口内提取退化趋势，就能输出剩余使用寿命的估计。",
        "窗口越宽，看过的历史越多，趋势越稳；但样本越少。宽度，是你要权衡的第一个超参数。",
    ],
    "01-AI应用基础/微课视频/卷积滑动演示.mp4": [
        "卷积神经网络在图像里到底在做什么？看这个小小的卷积核。",
        "它从左上角出发，每次覆盖一小块像素，对应相乘再求和，得到输出图上的一个点。",
        "向右滑动一格，再算一次；一行扫完下移一行继续。",
        "整幅图扫完，输出就是一张特征图：哪里亮，说明哪里有卷积核喜欢的模式。",
        "换个卷积核，就能提取边缘、纹理等不同特征——许多核并排工作，就是CNN的第一层。",
    ],
    "01-AI应用基础/微课视频/阈值分割对比.mp4": [
        "缺陷检测的第一步，往往是最简单的阈值分割：高于阈值的算前景，低于的算背景。",
        "阈值取低一点，缺陷完整，但背景噪声也被一起放了进来，误检多。",
        "阈值取高一点，噪声没了，可缺陷也被切得残缺不全，漏检风险大。",
        "所以工程上不追完美阈值，而是结合噪声水平和缺陷最小尺寸折中选取，必要时用自适应阈值。",
        "记住这对矛盾：误检与漏检，此消彼长，取舍标准来自业务。",
    ],
    "03-Python程序设计-项目实战/微课视频/向量化加速赛跑.mp4": [
        "同样对一百万个振动采样求特征，循环写法和向量化写法赛个跑。",
        "循环版：逐个取数、逐个计算，解释器每一步都有开销。",
        "向量化版：整列交给NumPy，底层C语言一次性完成。",
        "结果：向量化常常快一到两个数量级。数据越大，差距越明显。",
        "以后写特征工程，先问自己一句：这一步能不能向量化？",
    ],
}


def main():
    for rel, lines in NARR.items():
        path = os.path.join(MAT, rel)
        segs = [tts(t, f"cl_{os.path.basename(path)[:6]}_{i}")
                for i, t in enumerate(lines)]
        track = os.path.join(TMPD, "track_cl_" + os.path.basename(path)[:8] + ".m4a")
        lst = track + ".txt"
        with open(lst, "w") as f:
            for m, _ in segs:
                f.write(f"file '{m}'\n")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", track], check=True)
        adur = _dur(track)
        vdur = _dur(path)
        pad = max(0.0, adur - vdur)
        tmp = path + ".tmp.mp4"
        if pad > 0.05:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path,
                            "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "22",
                            "-an", tmp], check=True)
        else:
            tmp = path
        out = path + ".out.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", track,
                        "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy" if pad > 0.05 else "libx264",
                        "-c:a", "aac", "-b:a", "128k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
        os.replace(out, path)
        if pad > 0.05:
            os.remove(tmp)
        print("narrated:", os.path.basename(path), round(_dur(path), 1), "s",
              flush=True)


if __name__ == "__main__":
    main()
