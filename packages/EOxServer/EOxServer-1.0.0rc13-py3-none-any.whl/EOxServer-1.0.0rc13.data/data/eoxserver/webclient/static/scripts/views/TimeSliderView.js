(function(){"use strict";var a=this;a.define(["backbone","communicator","timeslider","timeslider_plugins","globals","underscore","d3"],function(a,b,c,d,e){var f=a.Marionette.ItemView.extend({id:"timeslider",events:{selectionChanged:"onChangeTime",coverageselected:"onCoverageSelected"},initialize:function(a){this.options=a,this.active_products=[]},render:function(a){},onShow:function(a){this.listenTo(b.mediator,"date:selection:change",this.onDateSelectionChange),this.listenTo(b.mediator,"map:layer:change",this.changeLayer),this.listenTo(b.mediator,"map:position:change",this.updateExtent),this.listenTo(b.mediator,"date:selection:change",this.onDateSelectionChange),console.log(this.options);var c=new Date(this.options.brush.start),d=new Date(this.options.brush.end);this.activeWPSproducts=[],this.slider=new TimeSlider(this.el,{domain:{start:new Date(this.options.domain.start),end:new Date(this.options.domain.end)},brush:{start:c,end:d},debounce:300,ticksize:8,datasets:[]}),this.slider.zoom(new Date(this.options.domain.start),new Date(this.options.domain.end)),this.slider.hide(),_.defer(function(){b.mediator.trigger("time:change",{start:c,end:d})})},onChangeTime:function(a){b.mediator.trigger("time:change",a.originalEvent.detail)},onDateSelectionChange:function(a){this.slider.select(a.start,a.end)},changeLayer:function(a){if(!a.isBaseLayer){var c=e.products.find(function(b){return b.get("view").id==a.id});if(c)if(a.visible&&c.get("timeSlider")){switch(c.get("timeSliderProtocol")){case"WMS":this.slider.addDataset({id:"id"+strHash(c.get("view").id),color:c.get("color"),data:new TimeSlider.Plugin.WMS({url:c.get("view").urls[0],eoid:c.get("view").id,dataset:"id"+strHash(c.get("view").id)})}),this.active_products.push("id"+strHash(c.get("view").id));break;case"EOWCS":this.slider.addDataset({id:"id"+strHash(c.get("download").id),color:c.get("color"),data:new TimeSlider.Plugin.EOWCS({url:c.get("download").url,eoid:c.get("download").id,dataset:"id"+strHash(c.get("download").id)})}),this.active_products.push("id"+strHash(c.get("download").id));break;case"WPS":var d=b.reqres.request("map:get:extent");this.slider.addDataset({id:"id"+strHash(c.get("download").id),color:c.get("color"),data:new TimeSlider.Plugin.WPS({url:c.get("download").url,eoid:c.get("download").id,dataset:"id"+strHash(c.get("download").id),bbox:[d.left,d.bottom,d.right,d.top]})}),this.activeWPSproducts.push("id"+strHash(c.get("download").id)),this.active_products.push("id"+strHash(c.get("download").id)),this.slider.updateBBox([d.left,d.bottom,d.right,d.top],"id"+strHash(c.get("download").id))}this.slider.show()}else"WMS"==c.get("timeSliderProtocol")?(this.slider.removeDataset("id"+strHash(c.get("view").id)),-1!=this.active_products.indexOf("id"+strHash(c.get("view").id))&&this.active_products.splice(this.active_products.indexOf("id"+strHash(c.get("view").id)),1)):(this.slider.removeDataset("id"+strHash(c.get("download").id)),-1!=this.activeWPSproducts.indexOf("id"+strHash(c.get("download").id))&&this.activeWPSproducts.splice(this.activeWPSproducts.indexOf("id"+strHash(c.get("download").id)),1),-1!=this.active_products.indexOf("id"+strHash(c.get("download").id))&&this.active_products.splice(this.active_products.indexOf("id"+strHash(c.get("download").id)),1)),0==this.active_products.length&&this.slider.hide()}},updateExtent:function(a){for(var b=0;b<this.activeWPSproducts.length;b++)console.log(this.activeWPSproducts[b]),this.slider.updateBBox([a.left,a.bottom,a.right,a.top],this.activeWPSproducts[b])},onCoverageSelected:function(a){if(a.originalEvent.detail.bbox){var c=a.originalEvent.detail.bbox.replace(/[()]/g,"").split(",").map(parseFloat);this.slider.select(a.originalEvent.detail.start,a.originalEvent.detail.end),b.mediator.trigger("map:set:extent",c)}}});return{TimeSliderView:f}})}).call(this);