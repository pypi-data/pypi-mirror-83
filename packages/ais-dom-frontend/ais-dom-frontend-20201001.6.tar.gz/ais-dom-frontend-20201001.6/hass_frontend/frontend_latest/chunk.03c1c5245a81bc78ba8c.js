(self.webpackJsonp=self.webpackJsonp||[]).push([[67],{125:function(e){e.exports=JSON.parse('{"version":"5.6.55","parts":[{"file":"8f7750e029a6ef516f402ba2a18f770d535730f8"},{"start":"airp","file":"13eee1e899d282159a04ba352d1ed4feb53e5f28"},{"start":"application-","file":"5e09d9e60767da8826acfa939fc7a192c3017fdc"},{"start":"badge-account-horizontal-","file":"091c6419ea09577a2cd23f58a2d444da902922bd"},{"start":"beer","file":"c75f23577c68209caf2ee6d8abfa1e47f9fdd346"},{"start":"border-r","file":"4a163a7cb39874ec5e31fef5a16822d472ea9d75"},{"start":"camera-","file":"75c6554ce6c38218565310f31e330d29e610be14"},{"start":"cart-arrow-r","file":"526db7af6ed90ba5e29e520e8420886a387c6ec1"},{"start":"cir","file":"10f097705a1a3a9e15a4d5304588fcbf49e9cb1b"},{"start":"cog-o","file":"14893756d8a87eee5c25262d8d2cce84e343e9f7"},{"start":"cp","file":"43533c5a4e97f2dad8a4430e8fb2e998b77180e8"},{"start":"desktop-t","file":"d7593366adef7e12c6f7beb0125ae03250a623c1"},{"start":"earth-box-p","file":"897116495125bd02c7b5c74768fca0e4ef075556"},{"start":"eve","file":"25914e849cb9677609c2e17666c7dc8787276fec"},{"start":"file-download-","file":"393c2a9700198fd5d6ee360fec426dca07b824c1"},{"start":"flask-o","file":"21c916bdafa6c4bc802eb2f067d52eb43d46d63c"},{"start":"format-letter-e","file":"71adf4da7cf052ce2f72aafb39b5038640ae7eff"},{"start":"gh","file":"b52d69de085a5028ae417fc032b8fa962b929b2c"},{"start":"hand-wash-","file":"0fbcf56d8b33b97ba907a4aebeb8399bd200c71d"},{"start":"horizontal-rotate-co","file":"aaf1ddc91d8dc645b638d1cead1c3928be0d4ae2"},{"start":"ju","file":"5792fc856cff1ad97388d397c924b547dc5773ba"},{"start":"las","file":"8a4e57c53b91f036efd825ee3924ccb927394462"},{"start":"map-marker-m","file":"faf56ee66495fe62e00e421005abe5f362a15d5e"},{"start":"microsoft-xbox-controller-m","file":"cb9dda8c3ba589951ab20cae22899eee3f75aaa2"},{"start":"noo","file":"8d79d67bba34d4662998ebd3221a6f49f72d0cbd"},{"start":"pan-t","file":"5ff2e52aedaa0c398ec4a745219c00ac5b56c564"},{"start":"pig","file":"996e32533891ce2fcc2ed79a3fc3953057539e7c"},{"start":"qq","file":"8a9a74c567094a8e0c21288a4eaa28bdd315a3ac"},{"start":"roller-skate-","file":"855d84169183b3d513e65652ebd4619fbdacbfb0"},{"start":"set-c","file":"51836c70496c6d380859ef075c18363fac468891"},{"start":"skype-","file":"a64604d28b67e989f14df4cdd5fa33c18babb0e6"},{"start":"spotlight-","file":"fa89d8e056827e5e5a45002258155fdf636dba89"},{"start":"table-ro","file":"820c478bf9e136168cc68b98852a5ee1c6f57975"},{"start":"to","file":"d7a1decb8941bb6b39a53b22cf5d660c89acc059"},{"start":"upload-network-","file":"9bb9aae327973cf8230a9817e1e48eb6767d0601"},{"start":"water-well-","file":"b107c580b29fb39e4bfad9c85db944ac4d3297b4"},{"start":"wrap-","file":"0ec45795e55edbd7f9644bd3fa1943780d99a94d"}]}')},139:function(e,t,i){"use strict";i(141);var r=i(0);i(113);const n=window;"customIconsets"in n||(n.customIconsets={});const o=n.customIconsets;const a=i(125);var s=i(64);const l=new s.a("hass-icon-db","mdi-icon-store"),c=["mdi","hass","hassio","hademo"];let d=[];var p=i(65),h=i(11);function u(e){var t,i=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const k={},w={};Object(s.c)("_version",l).then(e=>{e?e!==a.version&&Object(s.b)(l).then(()=>Object(s.d)("_version",a.version,l)):Object(s.d)("_version",a.version,l)});const x=Object(p.a)(()=>(async e=>{const t=Object.keys(e),i=await Promise.all(Object.values(e));l._withIDBStore("readwrite",r=>{i.forEach((i,n)=>{Object.entries(i).forEach(([e,t])=>{r.put(t,e)}),delete e[t[n]]})})})(w),2e3),_={};!function(e,t,i,r){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(b(o.descriptor)||b(n.descriptor)){if(m(o)||m(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(m(o)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}f(o,n)}else t.push(o)}return t}(a.d.map(u)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([Object(r.d)("ha-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.h)()],key:"icon",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_path",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(e){e.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?r.f`<iron-icon .icon=${this.icon}></iron-icon>`:r.f`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:r.f``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[e,t]=this.icon.split(":",2);let i,r=t;if(!e||!r)return;if(!c.includes(e)){if(e in o){const t=o[e];return void(t&&this._setCustomPath(t(r)))}return void(this._legacy=!0)}if(this._legacy=!1,r in k){const t=k[r];let i;t.newName?(i=`Icon ${e}:${r} was renamed to ${e}:${t.newName}, please change your config, it will be removed in version ${t.removeIn}.`,r=t.newName):i=`Icon ${e}:${r} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${t.removeIn}.`,console.warn(i),Object(h.a)(this,"write_log",{level:"warning",message:i})}if(r in _)return void(this._path=_[r]);try{i=await(e=>new Promise((t,i)=>{if(d.push([e,t,i]),d.length>1)return;const r=[];l._withIDBStore("readonly",e=>{for(const[t,i]of d)r.push([i,e.get(t)]);d=[]}).then(()=>{for(const[e,t]of r)e(t.result)}).catch(()=>{for(const[,,e]of d)e();d=[]})}))(r)}catch(p){i=void 0}if(i)return this._path=i,void(_[r]=i);const n=(e=>{let t;for(const i of a.parts){if(void 0!==i.start&&e<i.start)break;t=i}return t.file})(r);if(n in w)return void this._setPath(w[n],r);const s=fetch(`/static/mdi/${n}.json`).then(e=>e.json());w[n]=s,this._setPath(s,r),x()}},{kind:"method",key:"_setCustomPath",value:async function(e){const t=await e;this._path=t.path,this._viewBox=t.viewBox}},{kind:"method",key:"_setPath",value:async function(e,t){const i=await e;this._path=i[t],_[t]=i[t]}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      :host {
        fill: currentcolor;
      }
    `}}]}}),r.a)},160:function(e,t,i){"use strict";i.d(t,"b",(function(){return r})),i.d(t,"a",(function(){return n}));const r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>r(e.toLowerCase(),t.toLowerCase())},224:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));var r=i(156);const n=e=>Object(r.a)(e.entity_id)},242:function(e,t,i){"use strict";i.d(t,"a",(function(){return d}));i(103);var r=i(14),n=i(11),o=i(176);function a(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}const s="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0;class l extends HTMLElement{constructor(){super(),a(this,"holdTime",500),a(this,"ripple",void 0),a(this,"timer",void 0),a(this,"held",!1),a(this,"cancelled",!1),a(this,"dblClickTimeout",void 0),this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:s?"100px":"50px",height:s?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach(e=>{document.addEventListener(e,()=>{this.cancelled=!0,this.timer&&(this.stopAnimation(),clearTimeout(this.timer),this.timer=void 0)},{passive:!0})})}bind(e,t){e.actionHandler&&Object(o.a)(t,e.actionHandler.options)||(e.actionHandler?(e.removeEventListener("touchstart",e.actionHandler.start),e.removeEventListener("touchend",e.actionHandler.end),e.removeEventListener("touchcancel",e.actionHandler.end),e.removeEventListener("mousedown",e.actionHandler.start),e.removeEventListener("click",e.actionHandler.end),e.removeEventListener("keyup",e.actionHandler.handleEnter)):e.addEventListener("contextmenu",e=>{const t=e||window.event;return t.preventDefault&&t.preventDefault(),t.stopPropagation&&t.stopPropagation(),t.cancelBubble=!0,t.returnValue=!1,!1}),e.actionHandler={options:t},t.disabled||(e.actionHandler.start=e=>{let i,r;this.cancelled=!1,e.touches?(i=e.touches[0].pageX,r=e.touches[0].pageY):(i=e.pageX,r=e.pageY),t.hasHold&&(this.held=!1,this.timer=window.setTimeout(()=>{this.startAnimation(i,r),this.held=!0},this.holdTime))},e.actionHandler.end=e=>{if(["touchend","touchcancel"].includes(e.type)&&this.cancelled)return;const i=e.target;e.cancelable&&e.preventDefault(),t.hasHold&&(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0),t.hasHold&&this.held?Object(n.a)(i,"action",{action:"hold"}):t.hasDoubleClick?"click"===e.type&&e.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout(()=>{this.dblClickTimeout=void 0,Object(n.a)(i,"action",{action:"tap"})},250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,Object(n.a)(i,"action",{action:"double_tap"})):Object(n.a)(i,"action",{action:"tap"})},e.actionHandler.handleEnter=e=>{13===e.keyCode&&e.currentTarget.actionHandler.end(e)},e.addEventListener("touchstart",e.actionHandler.start,{passive:!0}),e.addEventListener("touchend",e.actionHandler.end),e.addEventListener("touchcancel",e.actionHandler.end),e.addEventListener("mousedown",e.actionHandler.start,{passive:!0}),e.addEventListener("click",e.actionHandler.end),e.addEventListener("keyup",e.actionHandler.handleEnter)))}startAnimation(e,t){Object.assign(this.style,{left:e+"px",top:t+"px",display:null}),this.ripple.disabled=!1,this.ripple.startPress(),this.ripple.unbounded=!0}stopAnimation(){this.ripple.endPress(),this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler",l);const c=(e,t)=>{const i=(()=>{const e=document.body;if(e.querySelector("action-handler"))return e.querySelector("action-handler");const t=document.createElement("action-handler");return e.appendChild(t),t})();i&&i.bind(e,t)},d=Object(r.f)((e={})=>t=>{c(t.committer.element,e)})},387:function(e,t,i){"use strict";i.d(t,"a",(function(){return r}));const r=e=>(e.cache.cfg||(e.cache.cfg=e.sendMessage({type:"config/get"})),e.cache.cfg)},443:function(e,t,i){"use strict";i.d(t,"a",(function(){return b}));var r=i(0),n=i(49),o=i(89),a=i(224);function s(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function f(e,t,i){return(f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=m(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function m(e){return(m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const b=e=>e?e.trim().split(" ").slice(0,3).map(e=>e.substr(0,1)).join(""):"?";!function(e,t,i,r){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,f.elements)}),i),f=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(a.d.map(s)),e);n.initializeClassElements(a.F,f.elements),n.runClassFinishers(a.F,f.finishers)}([Object(r.d)("ha-user-badge")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(r.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.h)({attribute:!1})],key:"user",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_personPicture",value:void 0},{kind:"field",key:"_personEntityId",value:void 0},{kind:"method",key:"updated",value:function(e){if(f(m(i.prototype),"updated",this).call(this,e),e.has("user"))return void this._getPersonPicture();const t=e.get("hass");if(this._personEntityId&&t&&this.hass.states[this._personEntityId]!==t.states[this._personEntityId]){const e=this.hass.states[this._personEntityId];e?this._personPicture=e.attributes.entity_picture:this._getPersonPicture()}else!this._personEntityId&&t&&this._getPersonPicture()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.user)return r.f``;const e=this._personPicture;if(e)return r.f`<div
        style=${Object(o.a)({backgroundImage:`url(${e})`})}
        class="picture"
      ></div>`;const t=b(this.user.name);return r.f`<div
      class="initials ${Object(n.a)({long:t.length>2})}"
    >
      ${t}
    </div>`}},{kind:"method",key:"_getPersonPicture",value:function(){if(this._personEntityId=void 0,this._personPicture=void 0,this.hass&&this.user)for(const e of Object.values(this.hass.states))if(e.attributes.user_id===this.user.id&&"person"===Object(a.a)(e)){this._personEntityId=e.entity_id,this._personPicture=e.attributes.entity_picture;break}}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      :host {
        display: contents;
      }
      .picture {
        width: 40px;
        height: 40px;
        background-size: cover;
        border-radius: 50%;
      }
      .initials {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }
      .initials.long {
        font-size: 80%;
      }
    `}}]}}),r.a)},542:function(e,t,i){"use strict";function r(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}i.d(t,"a",(function(){return o}));const n=new class{constructor(){r(this,"_storage",{}),r(this,"_listeners",{}),window.addEventListener("storage",e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach(t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key])))})}addFromStorage(e){if(!this._storage[e]){const t=window.localStorage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const i=this._listeners[e].indexOf(t);-1!==i&&this._listeners[e].splice(i,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){this._storage[e]=t;try{window.localStorage.setItem(e,JSON.stringify(t))}catch(i){}}},o=(e,t,i)=>r=>{const o=String(r.key);e=e||String(r.key);const a=r.initializer?r.initializer():void 0;n.addFromStorage(e);const s=()=>n.hasKey(e)?n.getValue(e):a;return{kind:"method",placement:"prototype",key:r.key,descriptor:{set(i){((i,o)=>{let a;t&&(a=s()),n.setValue(e,o),t&&i.requestUpdate(r.key,a)})(this,i)},get:()=>s(),enumerable:!0,configurable:!0},finisher(a){if(t){const t=a.prototype.connectedCallback,s=a.prototype.disconnectedCallback;a.prototype.connectedCallback=function(){var i;t.call(this),this["__unbsubLocalStorage"+o]=(i=this,n.subscribeChanges(e,e=>{i.requestUpdate(r.key,e)}))},a.prototype.disconnectedCallback=function(){s.call(this),this["__unbsubLocalStorage"+o]()},a.createProperty(r.key,{noAccessor:!0,...i})}}}}},869:function(e,t,i){"use strict";i.r(t);i(101),i(143);var r=i(112),n=(i(186),i(140),i(145),i(0)),o=i(49),a=i(305),s=i(157),l=i(542),c=i(11),d=i(156),p=i(160),h=i(122),u=i(179),f=i(387),m=i(242),b=i(56);i(139),i(162),i(113),i(443);function v(e){var t,i=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function k(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function E(e,t,i){return(E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=P(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function P(e){return(P=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const O=["config","developer-tools","hassio","aishelp","aisdocs"],j="scrollIntoViewIfNeeded"in document.body,T={aisaudio:1,"media-browser":2,aiszigbee:3,map:4,logbook:5,history:6,"developer-tools":9,hassio:10,config:11,aishelp:12,aisdocs:13},C=(e,t,i,r)=>{const n=e.indexOf(i.url_path),o=e.indexOf(r.url_path);return n!==o?n<o?1:-1:S(t,i,r)},S=(e,t,i)=>{const r="lovelace"===t.component_name,n="lovelace"===i.component_name;if(t.url_path===e)return-1;if(i.url_path===e)return 1;if(r&&n)return Object(p.b)(t.title,i.title);if(r&&!n)return-1;if(n)return 1;const o=t.url_path in T,a=i.url_path in T;return o&&a?T[t.url_path]-T[i.url_path]:o?-1:a?1:Object(p.b)(t.title,i.title)},$=Object(s.a)((e,t,i,r)=>{if(!e)return[[],[]];const n=[],o=[];Object.values(e).forEach(e=>{r.includes(e.url_path)||!e.title&&e.url_path!==t||(O.includes(e.url_path)?o:n).push(e)});const a=[...i].reverse();return n.sort((e,i)=>C(a,t,e,i)),o.sort((e,i)=>C(a,t,e,i)),[n,o]});let D;!function(e,t,i,r){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!g(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=x(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(k(o.descriptor)||k(n.descriptor)){if(g(o)||g(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(g(o)){if(g(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}y(o,n)}else t.push(o)}return t}(a.d.map(v)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([Object(n.d)("ha-sidebar")],(function(e,t){class s extends t{constructor(...t){super(...t),e(this)}}return{F:s,d:[{kind:"field",decorators:[Object(n.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.h)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[Object(n.h)({type:Boolean})],key:"alwaysExpand",value:()=>!1},{kind:"field",decorators:[Object(n.h)({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[Object(n.h)({type:Boolean})],key:"editMode",value:()=>!1},{kind:"field",decorators:[Object(n.g)()],key:"_externalConfig",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_notifications",value:void 0},{kind:"field",decorators:[Object(n.h)({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[Object(n.g)()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_mouseLeaveTimeout",value:void 0},{kind:"field",key:"_tooltipHideTimeout",value:void 0},{kind:"field",key:"_recentKeydownActiveUntil",value:()=>0},{kind:"field",decorators:[Object(l.a)("sidebarPanelOrder",!0,{attribute:!1})],key:"_panelOrder",value:()=>[]},{kind:"field",decorators:[Object(l.a)("sidebarHiddenPanels",!0,{attribute:!1})],key:"_hiddenPanels",value:()=>[]},{kind:"field",key:"_sortable",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass;if(!e)return n.f``;const[t,i]=$(e.panels,e.defaultPanel,this._panelOrder,this._hiddenPanels);let s=this._notifications?this._notifications.length:0;for(const r in e.states)"configurator"===Object(d.a)(r)&&s++;return n.f`
      <div
        class="menu"
        @action=${this._handleAction}
        .actionHandler=${Object(m.a)({hasHold:!this.editMode,disabled:this.editMode})}
      >
        ${this.narrow?"":n.f`
              <mwc-icon-button
                .label=${e.localize("ui.sidebar.sidebar_toggle")}
                @action=${this._toggleSidebar}
              >
                <ha-svg-icon
                  .path=${"docked"===e.dockedSidebar?r.vb:r.ub}
                ></ha-svg-icon>
              </mwc-icon-button>
            `}
        <div class="title">
          ${this.editMode?n.f`<mwc-button outlined @click=${this._closeEditMode}>
                ${e.localize("ui.sidebar.done")}
              </mwc-button>`:"Asystent domowy"}
        </div>
      </div>
      <paper-listbox
        attr-for-selected="data-panel"
        class="ha-scrollbar"
        .selected=${e.panelUrl}
        @focusin=${this._listboxFocusIn}
        @focusout=${this._listboxFocusOut}
        @scroll=${this._listboxScroll}
        @keydown=${this._listboxKeydown}
      >
        ${this.editMode?n.f`<div id="sortable">
              ${Object(a.a)([this._hiddenPanels,this._renderEmptySortable],()=>this._renderEmptySortable?"":this._renderPanels(t))}
            </div>`:this._renderPanels(t)}
        <div class="spacer" disabled></div>
        ${this.editMode&&this._hiddenPanels.length?n.f`
              ${this._hiddenPanels.map(t=>{const i=this.hass.panels[t];return i?n.f`<paper-icon-item
                  @click=${this._unhidePanel}
                  class="hidden-panel"
                  .panel=${t}
                >
                  <ha-icon
                    slot="item-icon"
                    .icon=${i.url_path===this.hass.defaultPanel?"mdi:view-dashboard":i.icon}
                  ></ha-icon>
                  <span class="item-text"
                    >${i.url_path===this.hass.defaultPanel?e.localize("panel.states"):e.localize("panel."+i.title)||i.title}</span
                  >
                  <mwc-icon-button class="show-panel">
                    <ha-svg-icon .path=${r.Rb}></ha-svg-icon>
                  </mwc-icon-button>
                </paper-icon-item>`:""})}
              <div class="spacer" disabled></div>
            `:""}
        ${this._renderPanels(i)}
        ${this._externalConfig&&this._externalConfig.hasSettingsScreen?n.f`
              <a
                aria-role="option"
                aria-label=${e.localize("ui.sidebar.external_app_configuration")}
                href="#external-app-configuration"
                tabindex="-1"
                @click=${this._handleExternalAppConfiguration}
                @mouseenter=${this._itemMouseEnter}
                @mouseleave=${this._itemMouseLeave}
              >
                <paper-icon-item>
                  <ha-svg-icon
                    slot="item-icon"
                    .path=${r.t}
                  ></ha-svg-icon>
                  <span class="item-text">
                    ${e.localize("ui.sidebar.external_app_configuration")}
                  </span>
                </paper-icon-item>
              </a>
            `:""}
      </paper-listbox>

      <div class="divider"></div>

      <div
        class="notifications-container"
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item
          class="notifications"
          aria-role="option"
          @click=${this._handleShowNotificationDrawer}
        >
          <ha-svg-icon slot="item-icon" .path=${r.n}></ha-svg-icon>
          ${!this.expanded&&s>0?n.f`
                <span class="notification-badge" slot="item-icon">
                  ${s}
                </span>
              `:""}
          <span class="item-text">
            ${e.localize("ui.notification_drawer.title")}
          </span>
          ${this.expanded&&s>0?n.f`
                <span class="notification-badge">${s}</span>
              `:""}
        </paper-icon-item>
      </div>

      <a
        class=${Object(o.a)({profile:!0,"iron-selected":"profile"===e.panelUrl})}
        href="/profile"
        data-panel="panel"
        tabindex="-1"
        aria-role="option"
        aria-label=${e.localize("panel.profile")}
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item>
          <ha-user-badge
            slot="item-icon"
            .user=${e.user}
            .hass=${e}
          ></ha-user-badge>

          <span class="item-text">
            ${e.user?e.user.name:""}
          </span>
        </paper-icon-item>
      </a>
      <div disabled class="bottom-spacer"></div>
      <div class="tooltip"></div>
    `}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("expanded")||e.has("narrow")||e.has("alwaysExpand")||e.has("_externalConfig")||e.has("_notifications")||e.has("editMode")||e.has("_renderEmptySortable")||e.has("_hiddenPanels")||e.has("_panelOrder")&&!this.editMode)return!0;if(!this.hass||!e.has("hass"))return!1;const t=e.get("hass");if(!t)return!0;const i=this.hass;return i.panels!==t.panels||i.panelUrl!==t.panelUrl||i.user!==t.user||i.localize!==t.localize||i.language!==t.language||i.states!==t.states||i.defaultPanel!==t.defaultPanel}},{kind:"method",key:"firstUpdated",value:function(e){E(P(s.prototype),"firstUpdated",this).call(this,e),this.hass&&this.hass.auth.external&&Object(f.a)(this.hass.auth.external).then(e=>{this._externalConfig=e}),Object(u.a)(this.hass.connection,e=>{this._notifications=e})}},{kind:"method",key:"updated",value:function(e){if(E(P(s.prototype),"updated",this).call(this,e),e.has("alwaysExpand")&&(this.expanded=this.alwaysExpand),e.has("editMode")&&(this.editMode?this._activateEditMode():this._deactivateEditMode()),!e.has("hass"))return;const t=e.get("hass");if(t&&t.language===this.hass.language||(this.rtl=Object(h.a)(this.hass)),j&&(!t||t.panelUrl!==this.hass.panelUrl)){const e=this.shadowRoot.querySelector(".iron-selected");e&&e.scrollIntoViewIfNeeded()}}},{kind:"get",key:"_tooltip",value:function(){return this.shadowRoot.querySelector(".tooltip")}},{kind:"method",key:"_handleAction",value:function(e){"hold"===e.detail.action&&Object(c.a)(this,"hass-edit-sidebar",{editMode:!0})}},{kind:"method",key:"_activateEditMode",value:async function(){if(!D){const[e,t]=await Promise.all([i.e(22).then(i.bind(null,313)),i.e(323).then(i.bind(null,306))]),r=document.createElement("style");r.innerHTML=t.sortableStyles.cssText,this.shadowRoot.appendChild(r),D=e.Sortable,D.mount(e.OnSpill),D.mount(e.AutoScroll())}await this.updateComplete,this._createSortable()}},{kind:"method",key:"_createSortable",value:function(){this._sortable=new D(this.shadowRoot.getElementById("sortable"),{animation:150,fallbackClass:"sortable-fallback",dataIdAttr:"data-panel",handle:"paper-icon-item",onSort:async()=>{this._panelOrder=this._sortable.toArray()}})}},{kind:"method",key:"_deactivateEditMode",value:function(){var e;null===(e=this._sortable)||void 0===e||e.destroy(),this._sortable=void 0}},{kind:"method",key:"_closeEditMode",value:function(){Object(c.a)(this,"hass-edit-sidebar",{editMode:!1})}},{kind:"method",key:"_hidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;if(this._hiddenPanels.includes(t))return;this._hiddenPanels=[...this._hiddenPanels,t],this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_unhidePanel",value:async function(e){e.preventDefault();const t=e.currentTarget.panel;this._hiddenPanels=this._hiddenPanels.filter(e=>e!==t),this._renderEmptySortable=!0,await this.updateComplete;const i=this.shadowRoot.getElementById("sortable");for(;i.lastElementChild;)i.removeChild(i.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_itemMouseEnter",value:function(e){this.expanded||(new Date).getTime()<this._recentKeydownActiveUntil||(this._mouseLeaveTimeout&&(clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=void 0),this._showTooltip(e.currentTarget))}},{kind:"method",key:"_itemMouseLeave",value:function(){this._mouseLeaveTimeout&&clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=window.setTimeout(()=>{this._hideTooltip()},500)}},{kind:"method",key:"_listboxFocusIn",value:function(e){this.expanded||"A"!==e.target.nodeName||this._showTooltip(e.target.querySelector("paper-icon-item"))}},{kind:"method",key:"_listboxFocusOut",value:function(){this._hideTooltip()}},{kind:"method",decorators:[Object(n.e)({passive:!0})],key:"_listboxScroll",value:function(){(new Date).getTime()<this._recentKeydownActiveUntil||this._hideTooltip()}},{kind:"method",key:"_listboxKeydown",value:function(){this._recentKeydownActiveUntil=(new Date).getTime()+100}},{kind:"method",key:"_showTooltip",value:function(e){this._tooltipHideTimeout&&(clearTimeout(this._tooltipHideTimeout),this._tooltipHideTimeout=void 0);const t=this._tooltip,i=this.shadowRoot.querySelector("paper-listbox");let r=e.offsetTop+11;i.contains(e)&&(r-=i.scrollTop),t.innerHTML=e.querySelector(".item-text").innerHTML,t.style.display="block",t.style.top=r+"px",t.style.left=e.offsetLeft+e.clientWidth+4+"px"}},{kind:"method",key:"_hideTooltip",value:function(){this._tooltipHideTimeout||(this._tooltipHideTimeout=window.setTimeout(()=>{this._tooltipHideTimeout=void 0,this._tooltip.style.display="none"},10))}},{kind:"method",key:"_handleShowNotificationDrawer",value:function(){Object(c.a)(this,"hass-show-notifications")}},{kind:"method",key:"_handleExternalAppConfiguration",value:function(e){e.preventDefault(),this.hass.auth.external.fireMessage({type:"config_screen/show"})}},{kind:"method",key:"_toggleSidebar",value:function(e){"tap"===e.detail.action&&Object(c.a)(this,"hass-toggle-menu")}},{kind:"method",key:"_renderPanels",value:function(e){return e.map(e=>this._renderPanel(e.url_path,e.url_path===this.hass.defaultPanel?e.title||this.hass.localize("panel.states"):this.hass.localize("panel."+e.title)||e.title,e.icon,e.url_path!==this.hass.defaultPanel||e.icon?void 0:r.uc))}},{kind:"method",key:"_renderPanel",value:function(e,t,i,o){return n.f`
      <a
        aria-role="option"
        href=${"/"+e}
        data-panel=${e}
        tabindex="-1"
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item>
          ${o?n.f`<ha-svg-icon
                slot="item-icon"
                .path=${o}
              ></ha-svg-icon>`:n.f`<ha-icon slot="item-icon" .icon=${i}></ha-icon>`}
          <span class="item-text">${t}</span>
        </paper-icon-item>
        ${this.editMode?n.f`<mwc-icon-button
              class="hide-panel"
              .panel=${e}
              @click=${this._hidePanel}
            >
              <ha-svg-icon .path=${r.C}></ha-svg-icon>
            </mwc-icon-button>`:""}
      </a>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[b.e,n.c`
        :host {
          height: 100%;
          display: block;
          overflow: hidden;
          -ms-user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          border-right: 1px solid var(--divider-color);
          background-color: var(--sidebar-background-color);
          width: 64px;
        }
        :host([expanded]) {
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl]) {
          border-right: 0;
          border-left: 1px solid var(--divider-color);
        }
        .menu {
          box-sizing: border-box;
          height: 65px;
          display: flex;
          padding: 0 8.5px;
          border-bottom: 1px solid transparent;
          white-space: nowrap;
          font-weight: 400;
          color: var(--primary-text-color);
          border-bottom: 1px solid var(--divider-color);
          background-color: var(--primary-background-color);
          font-size: 20px;
          align-items: center;
          padding-left: calc(8.5px + env(safe-area-inset-left));
        }
        :host([rtl]) .menu {
          padding-left: 8.5px;
          padding-right: calc(8.5px + env(safe-area-inset-right));
        }
        :host([expanded]) .menu {
          width: calc(256px + env(safe-area-inset-left));
        }
        :host([rtl][expanded]) .menu {
          width: calc(256px + env(safe-area-inset-right));
        }
        .menu mwc-icon-button {
          color: var(--sidebar-icon-color);
        }
        :host([expanded]) .menu mwc-icon-button {
          margin-right: 23px;
        }
        :host([expanded][rtl]) .menu mwc-icon-button {
          margin-right: 0px;
          margin-left: 23px;
        }

        .title {
          width: 100%;
          display: none;
        }
        :host([narrow]) .title {
          padding: 0 16px;
        }
        :host([expanded]) .title {
          display: initial;
        }
        .title mwc-button {
          width: 100%;
        }
        #sortable,
        .hidden-panel {
          display: none;
        }

        paper-listbox {
          padding: 4px 0;
          display: flex;
          flex-direction: column;
          box-sizing: border-box;
          height: calc(100% - 196px - env(safe-area-inset-bottom));
          overflow-x: hidden;
          background: none;
          margin-left: env(safe-area-inset-left);
        }

        :host([rtl]) paper-listbox {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }

        a {
          text-decoration: none;
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          position: relative;
          display: block;
          outline: 0;
        }

        paper-icon-item {
          box-sizing: border-box;
          margin: 4px 8px;
          padding-left: 12px;
          border-radius: 4px;
          --paper-item-min-height: 40px;
          width: 48px;
        }
        :host([expanded]) paper-icon-item {
          width: 240px;
        }
        :host([rtl]) paper-icon-item {
          padding-left: auto;
          padding-right: 12px;
        }

        ha-icon[slot="item-icon"],
        ha-svg-icon[slot="item-icon"] {
          color: var(--sidebar-icon-color);
        }

        .iron-selected paper-icon-item::before,
        a:not(.iron-selected):focus::before {
          border-radius: 4px;
          position: absolute;
          top: 0;
          right: 0;
          bottom: 0;
          left: 0;
          pointer-events: none;
          content: "";
          transition: opacity 15ms linear;
          will-change: opacity;
        }
        .iron-selected paper-icon-item::before {
          background-color: var(--sidebar-selected-icon-color);
          opacity: 0.12;
        }
        a:not(.iron-selected):focus::before {
          background-color: currentColor;
          opacity: var(--dark-divider-opacity);
          margin: 4px 8px;
        }
        .iron-selected paper-icon-item:focus::before,
        .iron-selected:focus paper-icon-item::before {
          opacity: 0.2;
        }

        .iron-selected paper-icon-item[pressed]:before {
          opacity: 0.37;
        }

        paper-icon-item span {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
        }

        a.iron-selected paper-icon-item ha-icon,
        a.iron-selected paper-icon-item ha-svg-icon {
          color: var(--sidebar-selected-icon-color);
        }

        a.iron-selected .item-text {
          color: var(--sidebar-selected-text-color);
        }

        paper-icon-item .item-text {
          display: none;
          max-width: calc(100% - 56px);
        }
        :host([expanded]) paper-icon-item .item-text {
          display: block;
        }

        .divider {
          bottom: 112px;
          padding: 10px 0;
        }
        .divider::before {
          content: " ";
          display: block;
          height: 1px;
          background-color: var(--divider-color);
        }
        .notifications-container {
          display: flex;
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .notifications-container {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .notifications {
          cursor: pointer;
        }
        .notifications .item-text {
          flex: 1;
        }
        .profile {
          margin-left: env(safe-area-inset-left);
        }
        :host([rtl]) .profile {
          margin-left: initial;
          margin-right: env(safe-area-inset-right);
        }
        .profile paper-icon-item {
          padding-left: 4px;
        }
        :host([rtl]) .profile paper-icon-item {
          padding-left: auto;
          padding-right: 4px;
        }
        .profile .item-text {
          margin-left: 8px;
        }
        :host([rtl]) .profile .item-text {
          margin-right: 8px;
        }

        .notification-badge {
          min-width: 20px;
          box-sizing: border-box;
          border-radius: 50%;
          font-weight: 400;
          background-color: var(--accent-color);
          line-height: 20px;
          text-align: center;
          padding: 0px 6px;
          color: var(--text-accent-color, var(--text-primary-color));
        }
        ha-svg-icon + .notification-badge {
          position: absolute;
          bottom: 14px;
          left: 26px;
          font-size: 0.65em;
        }

        .spacer {
          flex: 1;
          pointer-events: none;
        }

        .subheader {
          color: var(--sidebar-text-color);
          font-weight: 500;
          font-size: 14px;
          padding: 16px;
          white-space: nowrap;
        }

        .dev-tools {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          padding: 0 8px;
          width: 256px;
          box-sizing: border-box;
        }

        .dev-tools a {
          color: var(--sidebar-icon-color);
        }

        .tooltip {
          display: none;
          position: absolute;
          opacity: 0.9;
          border-radius: 2px;
          white-space: nowrap;
          color: var(--sidebar-background-color);
          background-color: var(--sidebar-text-color);
          padding: 4px;
          font-weight: 500;
        }

        :host([rtl]) .menu mwc-icon-button {
          -webkit-transform: scaleX(-1);
          transform: scaleX(-1);
        }
      `]}}]}}),n.a)}}]);
//# sourceMappingURL=chunk.03c1c5245a81bc78ba8c.js.map