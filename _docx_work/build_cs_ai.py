# -*- coding: utf-8 -*-
"""AI应用基础（16课时）课程标准 docx+PDF（两遍法静态目录）——统一文件名《AI应用基础》"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs_data
from build_cs import build_standard, extract_toc

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p_cs = os.path.join(BASE, "工业互联网专业《AI应用基础》课程标准.docx")
pdfdir = os.path.join(BASE, "教学实施资料", "课标PDF版")
os.makedirs("/tmp/cs_pass", exist_ok=True)
import subprocess

if __name__ == "__main__":
    build_standard(cs_data.AI, "/tmp/cs_pass/pass16.docx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    "/tmp/cs_pass", "/tmp/cs_pass/pass16.docx"], capture_output=True)
    build_standard(cs_data.AI, p_cs, toc_entries=extract_toc("/tmp/cs_pass/pass16.pdf"))
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    pdfdir, p_cs], capture_output=True)
    # 元数据回写
    import datetime
    from docx import Document
    d = Document(p_cs)
    cp = d.core_properties
    cp.title = os.path.basename(p_cs)[:-5]
    cp.author = "工业互联网应用专业教学资源库"
    cp.keywords = "两江智造;项目载体;岗课赛证创;课程思政;双创中心302;第4-11周;零基础"
    cp.category = "高职高专教学文件"
    cp.created = cp.modified = datetime.datetime(2026, 9, 9)
    d.save(p_cs)
    print("AI课标 docx+PDF saved:", p_cs)
