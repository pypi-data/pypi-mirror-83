import pytest
from collections import OrderedDict
from py.xml import html,raw
from html import escape
try:
    from ansi2html import Ansi2HTMLConverter, style
    ANSI = True
except ImportError:
    # ansi2html is not installed
    ANSI = False
import bisect
from .resource.js_and_css import javascript,css
import time
from fxtest.running.config import Fxtest

import os
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    report = out.get_result()
    report.description=item.function.__doc__
    if report.when =='call' or report.when=="setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            report.screen_img=_capture_screenshot()


def _capture_screenshot():
    if Fxtest.driver is not None:
        return Fxtest.driver.get_screenshot_as_base64()
    else:
        return None
# def pytest_addhooks(pluginmanager):
#     from resource import hooks

#     pluginmanager.add_hookspecs(hooks)
def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--fxtest-html",
        action="store",
        dest="fxtesthtmlpath",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )

def pytest_configure(config):
    htmlpath=config.getoption("fxtesthtmlpath")
    print(htmlpath)
    if htmlpath:
        if not hasattr(config,"slaveinput"):
            config._html=HtmlReport(htmlpath,config)
            config.pluginmanager.register(config._html)


def pytest_unconfigure(config):
    html = getattr(config, "_html", None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)

class HtmlReport:
    def __init__(self,logfile,config):
        self.logfile = os.path.abspath(logfile)
        self.passed=0
        self.failed=0
        self.error=0
        self.skipped=0
        self.total=0
        self.duration="0.0"
        self.config=config
        self.results=[]
        self.test_logs = []

    class TestResult:
        def __init__(self, outcome, report, config):
            self.test_id = report.nodeid.encode("utf-8").decode("unicode_escape")
            self.additional_html=[]
            self.time = getattr(report, "duration", 0.0)
            self.row_table = self.row_log=self.row_image=None
            self.imgs=[]
            if outcome=="passed" :
                self.outcome="通过"
            if outcome=="failed" and "xfailed":
                self.outcome="失败"
            if outcome=="error":
                self.outcome="错误"
            if outcome=="skipped":
                self.outcome="跳过"

            self.description=report.description
            
            _detail=html.a("详情",href="javascript:;",onclick="show_Detail(this)")
            _screenshot=html.a("截图",href="javascript:;" ,onclick="show_ScreenShot(this)")
            self.append_log_html(report, self.additional_html)
            self.append_image(report,self.imgs)
            cells=[
                html.td(self.test_id),
                html.td(str(self.description)),
                html.td('%.2f' %self.time),
                html.td(self.outcome,class_="c-result")
            ]
            
            cells.append(html.td(_detail))
            cells.append(html.td(_screenshot))

            if len(cells)>0:
                self.row_table=html.tr(cells)
                self.row_log=html.tr(
                    html.td(self.additional_html,colspan="6"),class_="hidden",hidden="true",
                )
                self.row_image=html.tr(
                    html.td(self.imgs,colspan="6"),class_="hidden",hidden="true",
                )
            
            
        def __lt__(self, other):
            order = (
                "通过",
                "失败",
                "跳过",
                "错误",
            )
            return order.index(self.outcome) < order.index(other.outcome)


        def append_log_html(self,report,additional_html):
            log = html.div(class_="log")
            if report.longrepr:
                for line in report.longreprtext.splitlines():
                    separator = line.startswith("_ " * 10)
                    if separator:
                        log.append(line[:80])
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            log.append(html.span(raw(escape(line)), class_="error"))
                        else:
                            log.append(raw(escape(line)))
                    log.append(html.br())
            for section in report.sections:
                header, content = map(escape, section)
                log.append(f" {header:-^80} ")
                log.append(html.br())
                if ANSI:
                    converter = Ansi2HTMLConverter(inline=False, escaped=False)
                    content = converter.convert(content, full=False)
                log.append(raw(content))
                log.append(html.br())

            if len(log) == 0:
                log = html.div(class_="log")
                log.append("无日志生成")
            additional_html.append(log)
        
        def append_image(self,report,imgs):
            self.screen_img=None
            if hasattr(report,"screen_img") is not False:
                self.screen_img=report.screen_img
                image_base=html.div(
                    html.img(
                        src="data:image/png;base64,%s" %self.screen_img,
                        alt="screenshot"
                    )
                )
                imgs.append(image_base)
            if self.screen_img is None:
                image_base=html.div(
                    "无截图"
                )
                imgs.append(image_base)

    
    def _appendrows(self,outcome,report):
        result = self.TestResult(outcome, report, self.config)
        
        if result.row_table is not None:
            index=bisect.bisect_right(self.results, result)
            self.results.insert(index,result)
            tbody=html.tbody(
                result.row_table,
                class_=outcome
            )
            if result.row_log is not None:
                tbody.append(result.row_log)
            if result.row_image is not None:
                tbody.append(result.row_image)
            self.test_logs.insert(index,tbody)
        
    def append_passed(self,report):
        if report.when == "call":
            self.passed+=1
            self._appendrows("passed",report)

    def append_failed(self,report):
        if getattr(report, "when", None) == "call":
            self.failed+=1
            self._appendrows("failed",report)
        else:
            self.error+=1
            self._appendrows("error",report)
    
    def append_skipped(self,report):
        self.skipped+=1
        self._appendrows("skipped",report)


    def pytest_runtest_logreport(self, report):
        if report.passed:
            self.append_passed(report)
        elif report.failed:
            self.append_failed(report)
        elif report.skipped:
            self.append_skipped(report)

            
    def pytest_sessionstart(self, session):
        self.suite_start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.start_time=time.time()
    def create_head_table(self):
        rows=[]
        header={}
        header["测试开始时间:"]=self.suite_start_time
        header["测试总用时:"]='%.2f' %self.duration
        header["测试总用例数"]=self.total
        for k in header:
            raw_value_string = raw(str(header[k]))
            rows.append(html.tr(html.td(k),html.td(raw_value_string)))
        
        div1=html.div(class_="c-sumary-1")
        div2=html.div(class_="c-sumary-2")
        div2.append(html.table(rows,class_="c-table-1"))
        div1.append(div2)

        return div1

    def _generate_report(self,session):
        self.duration=time.time()-self.start_time
        self.total=self.passed+self.failed+self.error+self.skipped
        html_css=html.style(raw(css))
        head = html.head(html.meta(charset="utf-8"), html_css)
        checkboxlist=html.div(self.generate_checkbox())
        checkboxsummary=html.p("勾选对应结果筛选用例结果",class_="c-head-1")

        body_head=html.nav(
            html.h3 ("测试报告")
        )
        canvas=html.canvas(
            id="canvas",
            width="600",
            height="330",
            style="left: 400px;",
        )
        head_table=self.create_head_table()
        summary=[
            head_table,
            html.div(canvas,class_="c-canvas")
        ]

        cells=[
            html.th("测试类"),
            html.th("用例描述",class_="c-th-3"),
            html.th("运行时间",class_="c-th-2"),
            html.th("用例结果"),
            html.th("查看",colspan="2")
        ]


        body=html.body(
            html.script(raw(javascript %self.create_pie_chart()),type="text/javascript"),
            body_head,
            html.p(
                "报告概要",
                html.div(
                    html.a(
                        "∧",
                        href="javascript:show_Report();" ,
                        class_="c-a-1",
                    ),
                    class_="c-div-1"
                )
            ),
            html.div(summary,class_="c-total"),
            checkboxsummary,
            checkboxlist,
            html.table(
                [
                    html.thead(
                        html.tr(cells,class_="c-head-2")
                    ),
                    self.test_logs,
                ],class_="c-table-2",
            )
        )
        doc=html.html(head,body)
        unicode_doc = "<!DOCTYPE html>\n{}".format(doc.unicode(indent=2))
        unicode_doc = unicode_doc.encode("utf-8", errors="xmlcharrefreplace")
        return unicode_doc.decode("utf-8")


    def generate_checkbox(self):
        
        self.checkboxlist=[]
        checkbox_kwargs={
            "passed":"通过",
            "failed":"失败",
            "error":"错误",
            "skipped":"跳过"
        }
        for k in checkbox_kwargs:
            self._checkbox=html.input(
                checkbox_kwargs[k],
                type="checkbox",
                checked="true",
                onchange="fifter_table(this)",
                name=k,
                value=checkbox_kwargs[k],
                class_="c-input-1",
            )
            self.checkbox=html.span(self._checkbox,class_="c-span-%s" %k)

            self.checkboxlist.append(html.label(self.checkbox))

        return self.checkboxlist
        


        
    def create_pie_chart(self):
        data=[]
        pass_data={}
        pass_data["title"]="通过"
        pass_data["per"]=self.passed
        fail_data={}
        fail_data["title"]="失败"
        fail_data["per"]=self.failed
        error_data={}
        error_data["title"]="错误"
        error_data["per"]=self.error
        skip_data={}
        skip_data["title"]="跳过"
        skip_data["per"]=self.skipped
        data.append(pass_data)
        data.append(fail_data)
        data.append(error_data)
        data.append(skip_data)  
        return data


    def _save_report(self,report_content):
        dir_name = os.path.dirname(self.logfile)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        with open(self.logfile,"w",encoding="utf-8") as f:
            f.write(report_content)
    def pytest_collectreport(self, report):
        if report.failed:
            self.append_failed(report)

    def pytest_sessionfinish(self, session):
        report_content = self._generate_report(session)
        self._save_report(report_content)
        
            

