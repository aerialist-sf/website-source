import os
import re
import shutil
from contextlib import closing
from jinja2 import Template, FileSystemLoader, Environment

TMPL_PATH = "templates/"
STATIC_PATH = "static/"
OUTPUT = "site/"

PAGES = [{"url":"/", "name":"Home"},
        {"url":"/photos/", "name":"Photos"},
        {"url":"/video/", "Video"), ("/performances/", "Performances"), ("contact", "Contact")]
def setup():
    shutil.rmtree(os.path.join(OUTPUT, STATIC_PATH))
    shutil.copytree(STATIC_PATH, os.path.join(OUTPUT, STATIC_PATH))

def tmpl_compile(tmpl_file, out_path):
    tmpl_base,_ = tmpl.rsplit(".")
    out_path = str(OUTPUT)
    if tmpl_base != "index":
        out_path = os.path.join(out_path, tmpl_base)

    env_vars = {"url":"/%s/" % tmpl_base,
                "name":tmpl_base.title()}

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__name__)), "templates/")))
    template = env.get_template(tmpl_name)
    with closing(open(os.path.join(out_path, "index.html"), "w")) as f_out:
        print "writing to %s" % out_path
        f_out.write(template.render())

def compile_templates():
    for tmpl in [f for f in os.listdir(TMPL_PATH) if not re.match("^_.*$", f) and re.match(".*html$", f)]:
        print "working on %s" % tmpl
        tmpl_compile(tmpl)

def run_compilation():
    setup()
    compile_templates()

if __name__ == "__main__":
    run_compilation()
