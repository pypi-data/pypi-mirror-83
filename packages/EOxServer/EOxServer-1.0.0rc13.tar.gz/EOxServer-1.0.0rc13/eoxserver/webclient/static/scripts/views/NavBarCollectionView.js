(function(){"use strict";var a=this;a.define(["backbone","communicator","views/NavBarItemView"],function(a,b,c){var d=a.Marionette.CompositeView.extend({appendHtml:function(a,b,c){a.$("ul").append(b.el)}});return{NavBarCollectionView:d}})}).call(this);