# -*- coding: utf-8 -*-
"""PY课程标准 docx+PDF 重建（两遍法静态目录）——文件名与内部课程名《Python编程基础》一致"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cs_data
from build_cs import build_standard, extract_toc
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p_cs = os.path.join(BASE, "工业互联网专业《Python编程基础》课程标准.docx")
pdfdir = os.path.join(BASE, "教学实施资料", "课标PDF版")
os.makedirs("/tmp/cs_pass", exist_ok=True)

if __name__ == "__main__":
    build_standard(cs_data.PY, "/tmp/cs_pass/passpy.docx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    "/tmp/cs_pass", "/tmp/cs_pass/passpy.docx"], capture_output=True)
    build_standard(cs_data.PY, p_cs, toc_entries=extract_toc("/tmp/cs_pass/passpy.pdf"))
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    pdfdir, p_cs], capture_output=True)
    import datetime
    from docx import Document
    d = Document(p_cs)
    cp = d.core_properties
    cp.title = os.path.basename(p_cs)[:-5]
    cp.author = "工业互联网应用专业教学资源库"
    cp.keywords = "两江智造;Python编程基础;岗课赛证创;课程思政;双创中心302;多解法"
    cp.category = "高职高专教学文件"
    cp.created = cp.modified = datetime.datetime(2026, 9, 11)
    d.save(p_cs)
    print("PY课标 docx+PDF ✓")
