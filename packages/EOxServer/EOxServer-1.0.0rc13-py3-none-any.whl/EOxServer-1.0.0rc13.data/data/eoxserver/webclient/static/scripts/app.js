(function(){"use strict";var a=this;a.define(["backbone","communicator","globals","regions/DialogRegion","regions/UIRegion","layouts/LayerControlLayout","layouts/ToolControlLayout","jquery","backbone.marionette","controller/ContentController","controller/DownloadController","controller/SelectionManagerController","controller/LoadingController","router"],function(a,b,c,d,e,f,g){var h=a.Marionette.Application.extend({initialize:function(a){},configure:function(a){$("body").tooltip({selector:"[data-toggle=tooltip]",position:{my:"left+5 center",at:"right center"},hide:{effect:!1,duration:0},show:{effect:!1,delay:700}});var e={},h={},i={};_.each(a.regions,function(a){var b={};b[a.name]="#"+a.name,this.addRegions(b),console.log("Added region "+b[a.name])},this),_.each(a.views,function(a){var b=require(a);$.extend(e,b)},this),_.each(a.models,function(a){var b=require(a);$.extend(h,b)},this),_.each(a.templates,function(a){var b=require(a.template);i[a.id]=b},this),c.objects.add("mapmodel",new h.MapModel({visualizationLibs:a.mapConfig.visualizationLibs,center:a.mapConfig.center,zoom:a.mapConfig.zoom})),_.each(a.mapConfig.baseLayers,function(a){c.baseLayers.add(new h.LayerModel({name:a.name,visible:a.visible,view:{id:a.id,urls:a.urls,protocol:a.protocol,projection:a.projection,attribution:a.attribution,matrixSet:a.matrixSet,style:a.style,format:a.format,resolutions:a.resolutions,maxExtent:a.maxExtent,gutter:a.gutter,buffer:a.buffer,units:a.units,transitionEffect:a.transitionEffect,isphericalMercator:a.isphericalMercator,visible:a.visible,wrapDateLine:a.wrapDateLine,zoomOffset:a.zoomOffset,time:a.time,requestEncoding:a.requestEncoding,isBaseLayer:!0}})),console.log("Added baselayer "+a.id)},this);var j={colors:d3.scale.category10(),index:0,getColor:function(){return this.colors(this.index++)}};if(_.each(a.mapConfig.products,function(a){var b=a.color?a.color:j.getColor();c.products.add(new h.LayerModel({name:a.name,visible:a.visible,timeSlider:a.timeSlider,timeSliderProtocol:a.timeSliderProtocol?a.timeSliderProtocol:"EOWCS",color:b,time:a.time,opacity:1,view:{id:a.view.id,protocol:a.view.protocol,urls:a.view.urls,visualization:a.view.visualization,projection:a.view.projection,attribution:a.view.attribution,matrixSet:a.view.matrixSet,style:a.view.style,format:a.view.format,resolutions:a.view.resolutions,maxExtent:a.view.maxExtent,gutter:a.view.gutter,buffer:a.view.buffer,units:a.view.units,transitionEffect:a.view.transitionEffect,isphericalMercator:a.view.isphericalMercator,isBaseLayer:!1,wrapDateLine:a.view.wrapDateLine,zoomOffset:a.view.zoomOffset,requestEncoding:a.view.requestEncoding},download:{id:a.download.id,protocol:a.download.protocol,url:a.download.url}})),console.log("Added product "+a.view.id)},this),_.each(a.mapConfig.overlays,function(a){c.overlays.add(new h.LayerModel({name:a.name,visible:a.visible,view:{id:a.id,urls:a.urls,protocol:a.protocol,projection:a.projection,attribution:a.attribution,matrixSet:a.matrixSet,style:a.style,format:a.format,resolutions:a.resolutions,maxExtent:a.maxExtent,gutter:a.gutter,buffer:a.buffer,units:a.units,transitionEffect:a.transitionEffect,isphericalMercator:a.isphericalMercator,isBaseLayer:!1,wrapDateLine:a.wrapDateLine,zoomOffset:a.zoomOffset,time:a.time,requestEncoding:a.requestEncoding}})),console.log("Added overlay "+a.id)},this),this.timeSliderView=new e.TimeSliderView(a.timeSlider),this.bottomBar.show(this.timeSliderView),this.map.show(new e.MapView({el:$("#map")})),a.navBarConfig){var k=new h.NavBarCollection;_.each(a.navBarConfig.items,function(a){k.add(new h.NavBarItemModel({name:a.name,icon:a.icon,eventToRaise:a.eventToRaise}))},this),this.topBar.show(new e.NavBarCollectionView({template:i.NavBar({title:a.navBarConfig.title,url:a.navBarConfig.url}),className:"navbar navbar-inverse navbar-fixed-top not-selectable",itemView:e.NavBarItemView,tag:"div",collection:k}))}this.addRegions({dialogRegion:d.extend({el:"#viewContent"})}),this.DialogContentView=new e.ContentView({template:{type:"handlebars",template:i.Info},id:"about",className:"modal fade",attributes:{role:"dialog",tabindex:"-1","aria-labelledby":"about-title","aria-hidden":!0,"data-keyboard":!0,"data-backdrop":"static"}}),this.baseLayerView=new e.BaseLayerSelectionView({collection:c.baseLayers,itemView:e.LayerItemView.extend({template:{type:"handlebars",template:i.BulletLayer},className:"radio"})}),this.productsView=new e.LayerSelectionView({collection:c.products,itemView:e.LayerItemView.extend({template:{type:"handlebars",template:i.CheckBoxLayer},className:"sortable-layer"}),className:"sortable"}),this.overlaysView=new e.BaseLayerSelectionView({collection:c.overlays,itemView:e.LayerItemView.extend({template:{type:"handlebars",template:i.CheckBoxOverlayLayer},className:"checkbox"}),className:"check"}),this.layout=new f;var l=new h.ToolCollection;_.each(a.selectionTools,function(a){l.add(new h.ToolModel({id:a.id,description:a.description,icon:a.icon,enabled:!0,active:!1,type:"selection",selectionType:a.selectionType}))},this);var m=new h.ToolCollection;_.each(a.visualizationTools,function(a){m.add(new h.ToolModel({id:a.id,eventToRaise:a.eventToRaise,description:a.description,disabledDescription:a.disabledDescription,icon:a.icon,enabled:a.enabled,active:a.active,type:"tool"}))},this),this.visualizationToolsView=new e.ToolSelectionView({collection:m,itemView:e.ToolItemView.extend({template:{type:"handlebars",template:i.ToolIcon}})}),this.selectionToolsView=new e.ToolSelectionView({collection:l,itemView:e.ToolItemView.extend({template:{type:"handlebars",template:i.ToolIcon}})}),this.toolLayout=new g,$(document).ajaxStart(function(){b.mediator.trigger("progress:change",!0)}),$(document).ajaxStop(function(){b.mediator.trigger("progress:change",!1)}),$(document).ajaxError(function(a,b,c){var d="";0!=b.status&&(d="; Status Code: "+b.status),$("#error-messages").append('<div class="alert alert-warning alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><strong>Warning!</strong> Error response on HTTP '+c.type+" to "+c.url.split("?")[0]+d+"</div>")}),a.navBarConfig&&_.each(a.navBarConfig.items,function(a){a.show&&b.mediator.trigger(a.eventToRaise)},this),$("#loadscreen").remove()}});return new h})}).call(this);