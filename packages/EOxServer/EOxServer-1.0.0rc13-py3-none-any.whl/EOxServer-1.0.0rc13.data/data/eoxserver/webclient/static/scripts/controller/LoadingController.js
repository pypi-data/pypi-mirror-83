(function(){"use strict";var a=this;a.require(["backbone","communicator","globals","app","jquery"],function(a,b,c,d){var e=a.Marionette.Controller.extend({progress_count:0,initialize:function(a){this.listenTo(b.mediator,"progress:change",this.onProgressChange)},onProgressChange:function(a){a?this.progress_count+=1:this.progress_count-=1,this.progress_count>0?$("body").addClass("wait"):$("body").removeClass("wait")}});return new e})}).call(this);