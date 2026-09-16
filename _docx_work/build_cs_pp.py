# -*- coding: utf-8 -*-
"""PP课程标准 docx+PDF 重建（两遍法静态目录）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs_data
from build_cs import build_standard, extract_toc
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p_cs = os.path.join(BASE, "工业互联网专业《Python程序设计（项目实战）》课程标准.docx")
pdfdir = os.path.join(BASE, "教学实施资料", "课标PDF版")
os.makedirs("/tmp/cs_pass", exist_ok=True)

if __name__ == "__main__":
    build_standard(cs_data.PP, "/tmp/cs_pass/passpp.docx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    "/tmp/cs_pass", "/tmp/cs_pass/passpp.docx"], capture_output=True)
    build_standard(cs_data.PP, p_cs, toc_entries=extract_toc("/tmp/cs_pass/passpp.pdf"))
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    pdfdir, p_cs], capture_output=True)
    import datetime
    from docx import Document
    d = Document(p_cs)
    cp = d.core_properties
    cp.title = os.path.basename(p_cs)[:-5]
    cp.author = "工业互联网应用专业教学资源库"
    cp.keywords = "两江智造;P7;Litestar;Granian;多模数据库;智能体;双创中心302"
    cp.category = "高职高专教学文件"
    cp.created = cp.modified = datetime.datetime(2026, 9, 9)
    d.save(p_cs)
    print("PP课标 docx+PDF ✓")
