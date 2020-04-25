var o=document.getElementById("echart5");
if(o)
	{var a=echarts.init(o);a.setOption(_extends({},echartOptions.defaultOptions,{legend:{show:!0,bottom:0},series:[_extends({type:"pie"},echartOptions.pieRing,{label:echartOptions.pieLabelCenterHover,data:[{name:"Completed",value:80,itemStyle:{color:"#663399"}},{name:"Pending",value:20,itemStyle:{color:"#ced4da"}}]})]})),$(window).on("resize",function(){setTimeout(function(){a.resize()},500)})
}