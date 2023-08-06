javascript="""
        window.onload = function () {
            function TestReport(ctx, radius) {
                this.ctx = ctx || document.querySelector("canvas").getContext("2d");
                this.width = this.ctx.canvas.width;
                this.height = this.ctx.canvas.height;
                this.x0 = this.width / 2 + 75;
                this.y0 = this.height / 2;
                this.radius = radius;
                this.outLong = radius / 8;
                this.dicX = 0;
                this.dicY = 50;
                this.dicWidth = 100;
                this.dicHeight = 40;
                this.spanY = 70;
            };
            TestReport.prototype.init = function (data) {
                this.drawPie(data);
                this.showfilter();
            };
            TestReport.prototype.showfilter = function () {
                var filter = document.getElementsByClassName("c-input-1");
                var res = document.getElementsByClassName('c-result');
                var res_arr = [];
                for (j = 0; j < res.length; j++) {
                    res_arr[j] = res[j].textContent;
                    switch(res[j].textContent){
                        case "通过":
                            res[j].style.color="#3CB371";
                            break;
                        case "失败": 
                            res[j].style.color="#DC143C";
                            break;
                        case "错误": 
                            res[j].style.color="#FF8C00";
                            break;
                        case "跳过":
                            res[j].style.color="#808080";
                            break;
                    }

                }
                for (i = 0; i < filter.length; i++) {
                    if (res_arr.indexOf(filter[i].value) < 0) {
                        filter[i].setAttribute("disabled", "true");
                    }
                }
            };

            TestReport.prototype.drawPie = function (data) {
                //转化后带有弧度的数据
                var that = this;
                var angleList = this.transformAngle(data);
                var startAngle = 0;
                angleList.forEach(function (item, index) {
                    // var color = that.randomColor();
                    var color
                    switch (item.title) {
                        case "通过":
                            color = 'rgb(34,139,34)';
                            break;
                        case "失败":
                            color = 'rgb(220,20,60)';
                            break;
                        case "错误":
                            color = 'rgb(255,140,0)';
                            break;
                        case "跳过":
                            color = 'rgb(128,128,128)';
                            break;
                    }
                    that.ctx.beginPath();
                    that.ctx.arc(that.x0, that.y0, that.radius, startAngle, startAngle + item.angle);
                    that.ctx.lineTo(that.x0, that.y0);
                    that.ctx.fillStyle = color;

                    that.ctx.fill();
                    //调用drawTitle函数
                    that.drawTitle(startAngle, item.angle, color, item.title, item.ratio);
                    startAngle += item.angle;
                    that.drawDic(item.title, item.per)
                });
            };
            TestReport.prototype.drawTitle = function (startAngle, angle, color, title, ratio) {
                var out = this.outLong + this.radius;
                var du = startAngle + angle / 2;
                //伸出外面的坐标原点
                var outX = this.x0 + out * Math.cos(du);
                var outY = this.y0 + out * Math.sin(du);
                this.ctx.beginPath();
                this.ctx.moveTo(this.x0, this.y0);
                this.ctx.lineTo(outX, outY);
                this.ctx.strokeStyle = color;
                //设置标题
                this.ctx.font = '12px Microsoft Yahei';
                var textWidth = this.ctx.measureText(title).width;
                this.ctx.textBaseline = "bottom";
                if (outX > this.x0) {
                    this.ctx.textAlign = "left";
                    this.ctx.lineTo(outX + textWidth, outY);
                } else {
                    this.ctx.textAlign = "right";
                    this.ctx.lineTo(outX - textWidth, outY);
                }
                this.ctx.stroke();
                this.ctx.fillText(title + ratio, outX, outY);
                //画描述
                // this.drawDic(title);
            };
            TestReport.prototype.drawDic = function (title, per) {
                this.ctx.fillRect(this.dicX, this.dicY, this.dicWidth, this.dicHeight);
                this.ctx.font = '16px Arial Rounded MT Bold';
                this.ctx.textAlign = "left";
                this.ctx.textBaseline = "middle";
                this.ctx.fillText(title + ' (' + per + ')', this.dicX + 10, this.dicY + this.dicHeight + 10);
                this.ctx.fillText("测试结果饼状图", 0, 20)
                this.dicY += this.spanY;
            };
            TestReport.prototype.transformAngle = function (data) {
                var total = 0;
                data.forEach(function (item, index) {
                    total += item.per;
                });
                data.forEach(function (item, index) {
                    item.angle = item.per / total * 2 * Math.PI;
                    item.ratio = (item.per / total * 100).toFixed(2) + "%%"
                });

                return data;
            };
            var data = %s;
            var ctx = document.querySelector("canvas").getContext("2d");
            var pieChart = new TestReport(ctx, 125);
            pieChart.init(data);

        };
        function fifter_table(elem) {
            var outcome = elem.getAttribute("name");
            var outcome_rows = document.getElementsByClassName(outcome);
            for (var i = 0; i < outcome_rows.length; i++) {
                outcome_rows[i].hidden = !elem.checked;
            }

        }

        function show_Detail(elem) {
            var detail = elem.parentNode.parentNode.nextElementSibling;
            var flag = detail.getAttribute("class");

            if (flag != "hidden") {
                detail.hidden = true;
                detail.className = 'hidden'
            }
            else {
                detail.hidden = false;
                detail.className = 'show'
            }
        }
        function show_ScreenShot(elem) {
            var detail = elem.parentNode.parentNode.parentNode.lastElementChild;
            var flag = detail.getAttribute("class");

            if (flag != "hidden") {
                detail.hidden = true;
                detail.className = 'hidden'
            }
            else {
                detail.hidden = false;
                detail.className = 'show'
            }
        }
        function show_Report(){
            var total=document.getElementsByClassName("c-total")[0]
            var a=document.getElementsByClassName("c-a-1")[0]


            console.log(total.style.display)
            if (total.style.display !="none"){
                total.style.display="none";
                a.innerHTML="∧";
            }
            else{
                total.style.display="block";
                a.innerHTML="∨";
            }
            
        }
"""

css="""
        body{
            margin: 0px;
        }
        h3{
            font-size: 20pt;
	        color: gray;
            font-weight: 600;
            margin: 0px;
            box-sizing: border-box;
        }
        nav{
            
            box-shadow:0px 0px 5px #000;
            padding: 10px;
        }
        .c-total {
            width: 100%;
            position: relative;
            height: 350px;
            
        }

        .c-sumary-1 {
            float: left;
            /* margin-right: auto; */
            width: 550px;
            border-right: 1px solid #e7eaec;
            
        }
        .c-sumary-2{
            width: 400px;
            height: 290px;
            padding: 20px;
            
        }
        .c-canvas {
            float: left;
            /* width: 900px; */
            margin-left: 20px;
        }

        td {
            padding-top: 15px;
            padding-bottom: 15px;
            padding-right: 30px;
            padding-left: 30px;
            border:1px  solid #dee2e6;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
        }
        .c-table-1{
            box-shadow:5px 5px 20px #000;
        }
        .c-td-1 {
            text-align: left;
            border-top: 1px solid #dee2e6;
            font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
            
        }
        a{
            text-decoration: none; 
            color:teal;
            
            
        }
        .c-head-1 {
            width: 100%;
            margin: 0px;

        }

        table {
            border: 0px;
            font-size: 100%;
            width: 100%;
            border-collapse: collapse;
            
            
        }

        .c-head-2 {
            padding: 20px;
            text-align: center;
        }

        th {
            margin: 20px;
            padding: 15px;
            background-color: #E1FFFF;
            box-shadow:5px 5px 10px #ccc;
            font-family: "YouYuan";
            font-size: 5mm;
        }
        span{
            padding:0px 10px 00px 0px;
            line-height: 2;
            border: 1px solid transparent;
            color: white;
        }
        .c-span-passed{
            background-color: 	#3CB371;
            box-shadow:0px 0px 5px #000;
        }
        .c-span-failed{
            background-color: 	#DC143C;
            box-shadow:0px 0px 5px #000;
        }
        .c-span-error{
            background-color: 	#FF8C00;
            box-shadow:0px 0px 5px #000;
        }
        .c-span-skipped{
            background-color: 	#808080;
            box-shadow:0px 0px 5px #000;
        }
        p{
            font-size: small;
            font-style: oblique;
            display: inline-block;
        }
        .c-div-1{
            float: right;
            font-size: 20px;
            padding-right: 20px;
            
        }
        .c-a-1{
            color: gray;
            text-shadow:0px 0px 5px #000;
            font-weight:bold;
        }
        .c-th-2{
            width: 90px;
        }
        .c-th-3{
            width: 50%;
        }
"""


