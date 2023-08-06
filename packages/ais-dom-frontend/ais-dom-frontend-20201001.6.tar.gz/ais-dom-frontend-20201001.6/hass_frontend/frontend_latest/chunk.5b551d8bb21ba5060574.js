/*! For license information please see chunk.5b551d8bb21ba5060574.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[100,14,197,199],{102:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));i(5);var s=i(68),r=i(44);const n=[s.a,r.a,{hostAttributes:{role:"option",tabindex:"0"}}]},140:function(e,t,i){"use strict";i(5),i(47),i(142);var s=i(6),r=i(4),n=i(102);Object(s.a)({_template:r.a`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[n.a]})},142:function(e,t,i){"use strict";i(47),i(80),i(52),i(57);const s=document.createElement("template");s.setAttribute("style","display: none;"),s.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(s.content)},158:function(e,t,i){"use strict";i(5),i(39),i(141),i(76),i(161),i(146),i(52),i(187),i(188);var s=i(68),r=i(44),n=i(69),o=i(70),a=i(6),l=i(3),c=i(40),h=i(4);Object(a.a)({_template:h.a`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[s.a,r.a,n.a,o.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.a)(this.$.content).getDistributedNodes(),t=0,i=e.length;t<i;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},189:function(e,t,i){"use strict";i(5);var s=i(79),r=i(6),n=i(3);Object(r.a)({is:"iron-iconset-svg",properties:{name:{type:String,observer:"_nameChanged"},size:{type:Number,value:24},rtlMirroring:{type:Boolean,value:!1},useGlobalRtlAttribute:{type:Boolean,value:!1}},created:function(){this._meta=new s.a({type:"iconset",key:null,value:null})},attached:function(){this.style.display="none"},getIconNames:function(){return this._icons=this._createIconMap(),Object.keys(this._icons).map((function(e){return this.name+":"+e}),this)},applyIcon:function(e,t){this.removeIcon(e);var i=this._cloneIcon(t,this.rtlMirroring&&this._targetIsRTL(e));if(i){var s=Object(n.a)(e.root||e);return s.insertBefore(i,s.childNodes[0]),e._svgIcon=i}return null},removeIcon:function(e){e._svgIcon&&(Object(n.a)(e.root||e).removeChild(e._svgIcon),e._svgIcon=null)},_targetIsRTL:function(e){if(null==this.__targetIsRTL)if(this.useGlobalRtlAttribute){var t=document.body&&document.body.hasAttribute("dir")?document.body:document.documentElement;this.__targetIsRTL="rtl"===t.getAttribute("dir")}else e&&e.nodeType!==Node.ELEMENT_NODE&&(e=e.host),this.__targetIsRTL=e&&"rtl"===window.getComputedStyle(e).direction;return this.__targetIsRTL},_nameChanged:function(){this._meta.value=null,this._meta.key=this.name,this._meta.value=this,this.async((function(){this.fire("iron-iconset-added",this,{node:window})}))},_createIconMap:function(){var e=Object.create(null);return Object(n.a)(this).querySelectorAll("[id]").forEach((function(t){e[t.id]=t})),e},_cloneIcon:function(e,t){return this._icons=this._icons||this._createIconMap(),this._prepareSvgClone(this._icons[e],this.size,t)},_prepareSvgClone:function(e,t,i){if(e){var s=e.cloneNode(!0),r=document.createElementNS("http://www.w3.org/2000/svg","svg"),n=s.getAttribute("viewBox")||"0 0 "+t+" "+t,o="pointer-events: none; display: block; width: 100%; height: 100%;";return i&&s.hasAttribute("mirror-in-rtl")&&(o+="-webkit-transform:scale(-1,1);transform:scale(-1,1);transform-origin:center;"),r.setAttribute("viewBox",n),r.setAttribute("preserveAspectRatio","xMidYMid meet"),r.setAttribute("focusable","false"),r.style.cssText=o,r.appendChild(s).removeAttribute("id"),r}return null}})},227:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));var s=i(9),r=i(11);const n=Object(s.a)(e=>class extends e{fire(e,t,i){return i=i||{},Object(r.a)(i.node||this,e,t,i)}})},229:function(e,t,i){"use strict";i(216),i(283);const s=document.createElement("template");s.innerHTML='<dom-module id="material-menu-overlay">\n  <template>\n    <style include="material-overlay">\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(s.content);var r=i(4);const n=r.a`<dom-module id="material-combo-box-overlay" theme-for="vaadin-combo-box-overlay">
  <template>
    <style include="material-menu-overlay">
      :host {
        /* TODO using a legacy mixin (unsupported) */
        --iron-list-items-container: {
          border-width: 8px 0;
          border-style: solid;
          border-color: transparent;
        };
      }

      [part="overlay"] {
        position: relative;
        overflow: visible;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
      }

      [part="content"] {
        padding: 0;
      }

      :host([loading]) [part="loader"] {
        height: 2px;
        position: absolute;
        z-index: 1;
        top: -2px;
        left: 0;
        right: 0;
        background:
          var(--material-background-color) linear-gradient(
            90deg,
            transparent 0%,
            transparent 20%,
            var(--material-primary-color) 20%,
            var(--material-primary-color) 40%,
            transparent 40%,
            transparent 60%,
            var(--material-primary-color) 60%,
            var(--material-primary-color) 80%,
            transparent 80%,
            transparent 100%
          ) 0 0 / 400% 100% repeat-x;
        opacity: 0;
        animation:
          3s linear infinite material-combo-box-loader-progress,
          .3s .1s both material-combo-box-loader-fade-in;
      }

      [part="loader"]::before {
        content: '';
        display: block;
        height: 100%;
        opacity: 0.16;
        background: var(--material-primary-color);
      }

      @keyframes material-combo-box-loader-fade-in {
        0% {
          opacity: 0;
        }

        100% {
          opacity: 1;
        }
      }

      @keyframes material-combo-box-loader-progress {
        0% {
          background-position: 0 0;
          background-size: 300% 100%;
        }

        33% {
          background-position: -100% 0;
          background-size: 400% 100%;
        }

        67% {
          background-position: -200% 0;
          background-size: 250% 100%;
        }

        100% {
          background-position: -300% 0;
          background-size: 300% 100%;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(n.content);i(239),i(237);const o=r.a`<dom-module id="material-item" theme-for="vaadin-item">
  <template>
    <style>
      :host {
        display: flex;
        align-items: center;
        box-sizing: border-box;
        overflow: hidden;
        font-family: var(--material-font-family);
        font-size: var(--material-body-font-size);
        line-height: 24px;
        padding: 4px 0;
      }

      /* It's the list-box's responsibility to add the focus style */
      :host([focused]) {
        outline: none;
      }

      /* Selected item has an icon */

      :host::before {
        display: var(--_material-item-selected-icon-display, none);
        content: "";
        font-family: material-icons;
        font-size: 24px;
        line-height: 1;
        font-weight: 400;
        width: 24px;
        text-align: center;
        margin-right: 10px;
        color: var(--material-secondary-text-color);
        flex: none;
      }

      :host([selected])::before {
        content: var(--material-icons-check);
      }

      /* Disabled item */

      :host([disabled]) {
        color: var(--material-disabled-text-color);
        cursor: default;
        pointer-events: none;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(o.content);var a=i(32),l=i(223);const c=e=>class extends e{static get properties(){return{_hasVaadinItemMixin:{value:!0},disabled:{type:Boolean,value:!1,observer:"_disabledChanged",reflectToAttribute:!0},selected:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_selectedChanged"},_value:String}}get value(){return void 0!==this._value?this._value:this.textContent.trim()}set value(e){this._value=e}ready(){super.ready();const e=this.getAttribute("value");null!==e&&(this.value=e),this.addEventListener("focus",e=>this._setFocused(!0),!0),this.addEventListener("blur",e=>this._setFocused(!1),!0),this.addEventListener("mousedown",e=>{this._setActive(this._mousedown=!0);const t=()=>{this._setActive(this._mousedown=!1),document.removeEventListener("mouseup",t)};document.addEventListener("mouseup",t)}),this.addEventListener("keydown",e=>this._onKeydown(e)),this.addEventListener("keyup",e=>this._onKeyup(e))}disconnectedCallback(){super.disconnectedCallback(),this.hasAttribute("active")&&this._setFocused(!1)}_selectedChanged(e){this.setAttribute("aria-selected",e)}_disabledChanged(e){e?(this.selected=!1,this.setAttribute("aria-disabled","true"),this.blur()):this.removeAttribute("aria-disabled")}_setFocused(e){e?(this.setAttribute("focused",""),this._mousedown||this.setAttribute("focus-ring","")):(this.removeAttribute("focused"),this.removeAttribute("focus-ring"),this._setActive(!1))}_setActive(e){e?this.setAttribute("active",""):this.removeAttribute("active")}_onKeydown(e){/^( |SpaceBar|Enter)$/.test(e.key)&&!e.defaultPrevented&&(e.preventDefault(),this._setActive(!0))}_onKeyup(e){this.hasAttribute("active")&&(this._setActive(!1),this.click())}};class h extends(c(Object(l.a)(a.a))){static get template(){return r.a`
    <style>
      :host {
        display: inline-block;
      }

      :host([hidden]) {
        display: none !important;
      }
    </style>
    <div part="content">
      <slot></slot>
    </div>
`}static get is(){return"vaadin-item"}static get version(){return"2.1.1"}constructor(){super(),this.value}}customElements.define(h.is,h);const d=r.a`<dom-module id="material-combo-box-item" theme-for="vaadin-combo-box-item">
  <template>
    <style include="material-item">
      :host {
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
        padding: 4px 10px;
        min-height: 36px;
        font-size: var(--material-small-font-size);
        --_material-item-selected-icon-display: block;
      }

      /* ShadyCSS workaround */
      :host::before {
        display: block;
      }

      :host(:hover) {
        background-color: var(--material-secondary-background-color);
      }

      :host([focused]) {
        background-color: var(--material-divider-color);
      }

      @media (pointer: coarse) {
        :host(:hover),
        :host([focused]) {
          background-color: transparent;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(d.content);var u=i(267),p=i(12),m=i(22),f=i(25),_=i(36),v=i(123),y=i(39),g=i(71);const b=class{toString(){return""}},w=e=>class extends e{static get properties(){return{opened:{type:Boolean,notify:!0,value:!1,reflectToAttribute:!0,observer:"_openedChanged"},disabled:{type:Boolean,value:!1,reflectToAttribute:!0},readonly:{type:Boolean,value:!1,reflectToAttribute:!0},renderer:Function,items:{type:Array,observer:"_itemsChanged"},allowCustomValue:{type:Boolean,value:!1},filteredItems:{type:Array},value:{type:String,observer:"_valueChanged",notify:!0,value:""},_lastCommittedValue:String,loading:{type:Boolean,value:!1,reflectToAttribute:!0},_focusedIndex:{type:Number,value:-1},filter:{type:String,value:"",notify:!0},selectedItem:{type:Object,notify:!0},itemLabelPath:{type:String,value:"label",observer:"_itemLabelPathChanged"},itemValuePath:{type:String,value:"value"},itemIdPath:String,name:{type:String},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_toggleElement:Object,_clearElement:Object,_inputElementValue:String,_closeOnBlurIsPrevented:Boolean,_previousDocumentPointerEvents:String,_itemTemplate:Object}}static get observers(){return["_filterChanged(filter, itemValuePath, itemLabelPath)","_itemsOrPathsChanged(items.*, itemValuePath, itemLabelPath)","_filteredItemsChanged(filteredItems.*, itemValuePath, itemLabelPath)","_templateOrRendererChanged(_itemTemplate, renderer)","_loadingChanged(loading)","_selectedItemChanged(selectedItem, itemLabelPath)","_toggleElementChanged(_toggleElement)"]}constructor(){super(),this._boundOnFocusout=this._onFocusout.bind(this),this._boundOverlaySelectedItemChanged=this._overlaySelectedItemChanged.bind(this),this._boundClose=this.close.bind(this),this._boundOnOpened=this._onOpened.bind(this),this._boundOnKeyDown=this._onKeyDown.bind(this),this._boundOnClick=this._onClick.bind(this),this._boundOnOverlayTouchAction=this._onOverlayTouchAction.bind(this),this._boundOnTouchend=this._onTouchend.bind(this)}ready(){super.ready(),this.addEventListener("focusout",this._boundOnFocusout),this._lastCommittedValue=this.value,v.a.requestAvailability(),this.$.overlay.addEventListener("selection-changed",this._boundOverlaySelectedItemChanged),this.addEventListener("vaadin-combo-box-dropdown-closed",this._boundClose),this.addEventListener("vaadin-combo-box-dropdown-opened",this._boundOnOpened),this.addEventListener("keydown",this._boundOnKeyDown),this.addEventListener("click",this._boundOnClick),this.$.overlay.addEventListener("vaadin-overlay-touch-action",this._boundOnOverlayTouchAction),this.addEventListener("touchend",this._boundOnTouchend),this._observer=new g.a(this,e=>{this._setTemplateFromNodes(e.addedNodes)})}render(){this.$.overlay._selector&&this.$.overlay._selector.querySelectorAll("vaadin-combo-box-item").forEach(e=>e._render())}_setTemplateFromNodes(e){this._itemTemplate=e.filter(e=>e.localName&&"template"===e.localName)[0]||this._itemTemplate}_removeNewRendererOrTemplate(e,t,i,s){e!==t?this._itemTemplate=void 0:i!==s&&(this.renderer=void 0)}_templateOrRendererChanged(e,t){if(e&&t)throw this._removeNewRendererOrTemplate(e,this._oldTemplate,t,this._oldRenderer),new Error("You should only use either a renderer or a template for combo box items");this._oldTemplate=e,this._oldRenderer=t}open(){this.disabled||this.readonly||(this.opened=!0)}close(){this.opened=!1}_openedChanged(e,t){void 0!==t&&(this.opened?(this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring"),this.hasAttribute("focused")||this.$.overlay.touchDevice||this.focus()):(this._onClosed(),this._openedWithFocusRing&&this.hasAttribute("focused")&&this.focusElement.setAttribute("focus-ring","")))}_onOverlayTouchAction(e){this._closeOnBlurIsPrevented=!0,this.inputElement.blur(),this._closeOnBlurIsPrevented=!1}_onClick(e){this._closeOnBlurIsPrevented=!0;const t=e.composedPath();-1!==t.indexOf(this._clearElement)||"clear-button"===t[0].getAttribute("part")?(this._clear(),this.focus()):-1!==t.indexOf(this.inputElement)&&(t.indexOf(this._toggleElement)>-1&&this.opened?this.close():this.open()),this._closeOnBlurIsPrevented=!1}_onKeyDown(e){this._isEventKey(e,"down")?(this._closeOnBlurIsPrevented=!0,this._onArrowDown(),this._closeOnBlurIsPrevented=!1,e.preventDefault()):this._isEventKey(e,"up")?(this._closeOnBlurIsPrevented=!0,this._onArrowUp(),this._closeOnBlurIsPrevented=!1,e.preventDefault()):this._isEventKey(e,"enter")?this._onEnter(e):this._isEventKey(e,"esc")&&this._onEscape(e)}_isEventKey(e,t){return y.a.keyboardEventMatchesKeys(e,t)}_getItemLabel(e){return this.$.overlay.getItemLabel(e)}_getItemValue(e){let t=e&&this.itemValuePath?this.get(this.itemValuePath,e):void 0;return void 0===t&&(t=e?e.toString():""),t}_onArrowDown(){this.opened?this.$.overlay._items&&(this._focusedIndex=Math.min(this.$.overlay._items.length-1,this._focusedIndex+1),this._prefillFocusedItemLabel()):this.open()}_onArrowUp(){this.opened?(this._focusedIndex>-1?this._focusedIndex=Math.max(0,this._focusedIndex-1):this.$.overlay._items&&(this._focusedIndex=this.$.overlay._items.length-1),this._prefillFocusedItemLabel()):this.open()}_prefillFocusedItemLabel(){this._focusedIndex>-1&&(this._inputElementValue="",setTimeout(()=>{this._inputElementValue=this._getItemLabel(this.$.overlay._focusedItem),this._markAllSelectionRange()},1))}_setSelectionRange(e,t){const i=this._nativeInput||this.inputElement;if(this.hasAttribute("focused")&&i&&i.setSelectionRange)try{i.setSelectionRange(e,t)}catch(s){}}_markAllSelectionRange(){void 0!==this._inputElementValue&&this._setSelectionRange(0,this._inputElementValue.length)}_clearSelectionRange(){if(void 0!==this._inputElementValue){const e=this._inputElementValue?this._inputElementValue.length:0;this._setSelectionRange(e,e)}}_onEnter(e){this.opened&&(this.allowCustomValue||""===this._inputElementValue||this._focusedIndex>-1)&&(this.close(),e.preventDefault(),e.stopPropagation())}_onEscape(e){this.opened&&(this._stopPropagation(e),this._focusedIndex>-1?(this._focusedIndex=-1,this._revertInputValue()):this.cancel())}_toggleElementChanged(e){e&&(e.addEventListener("mousedown",e=>e.preventDefault()),e.addEventListener("click",e=>{this.$.overlay.touchDevice&&!this.hasAttribute("focused")&&document.activeElement.blur()}))}_clear(){this.selectedItem=null,this.allowCustomValue&&(this.value=""),this._detectAndDispatchChange()}cancel(){this._revertInputValueToValue(),this._lastCommittedValue=this.value,this.close()}_onOpened(){Object(f.b)(),this.$.overlay.ensureItemsRendered(),this.$.overlay._selector.toggleScrollListener(!0),this.$.overlay.updateViewportBoundaries(),this.$.overlay._selector._increasePoolIfNeeded(),setTimeout(()=>this._resizeDropdown(),1),window.requestAnimationFrame(()=>this.$.overlay.adjustScrollPosition()),this._lastCommittedValue=this.value}_onClosed(){if(this.opened&&this.close(),this.$.overlay._items&&this._focusedIndex>-1){const e=this.$.overlay._items[this._focusedIndex];this.selectedItem!==e&&(this.selectedItem=e),this._inputElementValue=this._getItemLabel(this.selectedItem)}else if(""===this._inputElementValue||void 0===this._inputElementValue)this.selectedItem=null,this.allowCustomValue&&(this.value="");else if(!this.allowCustomValue||this.filteredItems&&this.filteredItems.filter(e=>this._getItemLabel(e)===this._inputElementValue).length)this._inputElementValue=this.selectedItem?this._getItemLabel(this.selectedItem):this.value||"";else{const e=new CustomEvent("custom-value-set",{detail:this._inputElementValue,composed:!0,cancelable:!0,bubbles:!0});if(this.dispatchEvent(e),!e.defaultPrevented){const e=this._inputElementValue;this._selectItemForValue(e),this.value=e}}this._detectAndDispatchChange(),this._clearSelectionRange(),this.dataProvider||(this.filter="")}get _propertyForValue(){return"value"}_inputValueChanged(e){-1!==e.composedPath().indexOf(this.inputElement)&&(this._inputElementValue=this.inputElement[this._propertyForValue],this._filterFromInput(e))}_filterFromInput(e){this.opened||e.__fromClearButton||this.open(),this.filter===this._inputElementValue?this._filterChanged(this.filter,this.itemValuePath,this.itemLabelPath):this.filter=this._inputElementValue}_itemLabelPathChanged(e,t){"string"!=typeof e&&console.error("You should set itemLabelPath to a valid string")}_filterChanged(e,t,i){void 0!==e&&(this.items?this.filteredItems=this._filterItems(this.items,e):this._filteredItemsChanged({path:"filteredItems",value:this.filteredItems},t,i))}_loadingChanged(e){e&&(this._focusedIndex=-1)}_revertInputValue(){""!==this.filter?this._inputElementValue=this.filter:this._revertInputValueToValue(),this._clearSelectionRange()}_revertInputValueToValue(){this.allowCustomValue&&!this.selectedItem?this._inputElementValue=this.value:this._inputElementValue=this._getItemLabel(this.selectedItem)}_resizeDropdown(){this.$.overlay.$.dropdown.notifyResize()}_updateHasValue(e){e?this.setAttribute("has-value",""):this.removeAttribute("has-value")}_selectedItemChanged(e,t){if(null==e)this.filteredItems&&(this.allowCustomValue||(this.value=""),this._updateHasValue(""!==this.value),this._inputElementValue=this.value);else{const t=this._getItemValue(e);if(this.value!==t&&(this.value=t,this.value!==t))return;this._updateHasValue(!0),this._inputElementValue=this._getItemLabel(e),this.inputElement&&(this.inputElement[this._propertyForValue]=this._inputElementValue)}this.$.overlay._selectedItem=e,this.filteredItems&&this.$.overlay._items&&(this._focusedIndex=this.filteredItems.indexOf(e))}_valueChanged(e,t){if(""!==e||void 0!==t){if(this._isValidValue(e)){let t;this._getItemValue(this.selectedItem)!==e?this._selectItemForValue(e):t=this.selectedItem,!t&&this.allowCustomValue&&(this._inputElementValue=e),this._updateHasValue(""!==this.value)}else this.selectedItem=null;this._lastCommittedValue=void 0}}_detectAndDispatchChange(){this.value!==this._lastCommittedValue&&(this.dispatchEvent(new CustomEvent("change",{bubbles:!0})),this._lastCommittedValue=this.value)}_itemsChanged(e,t){this._ensureItemsOrDataProvider(()=>{this.items=t})}_itemsOrPathsChanged(e,t,i){if(void 0!==e.value&&("items"===e.path||"items.splices"===e.path)){this.filteredItems=this.items?this.items.slice(0):this.items;const e=this._indexOfValue(this.value,this.items);this._focusedIndex=e;const t=e>-1&&this.items[e];t&&(this.selectedItem=t)}}_filteredItemsChanged(e,t,i){void 0!==e.value&&("filteredItems"!==e.path&&"filteredItems.splices"!==e.path||(this._setOverlayItems(this.filteredItems),this._focusedIndex=this.opened?this.$.overlay.indexOfLabel(this.filter):this._indexOfValue(this.value,this.filteredItems),this.opened&&this._repositionOverlay()))}_filterItems(e,t){return e?e.filter(e=>(t=t?t.toString().toLowerCase():"",this._getItemLabel(e).toString().toLowerCase().indexOf(t)>-1)):e}_selectItemForValue(e){const t=this._indexOfValue(e,this.filteredItems),i=this.selectedItem;this.selectedItem=t>=0?this.filteredItems[t]:this.dataProvider&&void 0===this.selectedItem?void 0:null,null===this.selectedItem&&null===i&&this._selectedItemChanged(this.selectedItem)}_setOverlayItems(e){this.$.overlay.set("_items",e)}_repositionOverlay(){this.__repositionOverlayDebouncer=m.a.debounce(this.__repositionOverlayDebouncer,p.d.after(500),()=>{const e=this.$.overlay._selector;e._isClientFull()||e._resetScrollPosition(e._physicalTop),this._resizeDropdown(),this.$.overlay.updateViewportBoundaries(),this.$.overlay.ensureItemsRendered(),e.notifyResize(),Object(f.b)()})}_indexOfValue(e,t){if(t&&this._isValidValue(e))for(let i=0;i<t.length;i++)if(this._getItemValue(t[i])===e)return i;return-1}_isValidValue(e){return null!=e}_overlaySelectedItemChanged(e){e.stopPropagation(),e.detail.item instanceof b||(this.opened?(this._focusedIndex=this.filteredItems.indexOf(e.detail.item),this.close()):this.selectedItem!==e.detail.item&&(this.selectedItem=e.detail.item,this._detectAndDispatchChange()))}_onFocusout(e){const t=this.$.overlay.$.dropdown;t&&t.$&&e.relatedTarget===t.$.overlay?e.composedPath()[0].focus():this._closeOnBlurIsPrevented||this.close()}_onTouchend(e){this._clearElement&&e.composedPath()[0]===this._clearElement&&(e.preventDefault(),this._clear())}validate(){return!(this.invalid=!this.checkValidity())}checkValidity(){if(this.inputElement.validate)return this.inputElement.validate()}get _instanceProps(){return{item:!0,index:!0,selected:!0,focused:!0}}_ensureTemplatized(){if(!this._TemplateClass){const e=this._itemTemplate||this._getRootTemplate();e&&(this._TemplateClass=Object(_.b)(e,this,{instanceProps:this._instanceProps,forwardHostProp:function(e,t){const i=this.$.overlay._selector.querySelectorAll("vaadin-combo-box-item");Array.prototype.forEach.call(i,i=>{i._itemTemplateInstance&&(i._itemTemplateInstance.set(e,t),i._itemTemplateInstance.notifyPath(e,t,!0))})}}))}}_getRootTemplate(){return Array.prototype.filter.call(this.children,e=>"TEMPLATE"===e.tagName)[0]}_preventInputBlur(){this._toggleElement&&this._toggleElement.addEventListener("click",this._preventDefault),this._clearElement&&this._clearElement.addEventListener("click",this._preventDefault)}_restoreInputBlur(){this._toggleElement&&this._toggleElement.removeEventListener("click",this._preventDefault),this._clearElement&&this._clearElement.removeEventListener("click",this._preventDefault)}_preventDefault(e){e.preventDefault()}_stopPropagation(e){e.stopPropagation()}},x=e=>class extends e{static get properties(){return{pageSize:{type:Number,value:50,observer:"_pageSizeChanged"},size:{type:Number,observer:"_sizeChanged"},dataProvider:{type:Object,observer:"_dataProviderChanged"},_pendingRequests:{value:()=>({})},__placeHolder:{value:new b}}}static get observers(){return["_dataProviderFilterChanged(filter, dataProvider)","_dataProviderClearFilter(dataProvider, opened, value)","_warnDataProviderValue(dataProvider, value)","_ensureFirstPage(opened)"]}_dataProviderClearFilter(e,t,i){e&&this.filter&&(this.size=void 0,this._pendingRequests={},this.filter="",this.clearCache())}ready(){super.ready(),this.clearCache(),this.$.overlay.addEventListener("index-requested",e=>{const t=e.detail.index;if(void 0!==t){const e=this._getPageForIndex(t);this._shouldLoadPage(e)&&this._loadPage(e)}})}_dataProviderFilterChanged(){this.dataProvider&&this.opened&&(this.size=void 0,this._pendingRequests={},this.clearCache())}_ensureFirstPage(e){e&&this._shouldLoadPage(0)&&this._loadPage(0)}_shouldLoadPage(e){if(!this.filteredItems||this._forceNextRequest)return this._forceNextRequest=!1,!0;const t=this.filteredItems[e*this.pageSize];return void 0!==t?t instanceof b:void 0===this.size}_loadPage(e){if(!this._pendingRequests[e]&&this.dataProvider){this.loading=!0;const t={page:e,pageSize:this.pageSize,filter:this.filter},i=(s,r)=>{if(this._pendingRequests[e]===i){if(this.filteredItems)this.splice("filteredItems",t.page*t.pageSize,s.length,...s);else{const e=[];e.splice(t.page*t.pageSize,s.length,...s),this.filteredItems=e}this._isValidValue(this.value)&&this._getItemValue(this.selectedItem)!==this.value&&this._selectItemForValue(this.value),this.size=r,delete this._pendingRequests[e],0===Object.keys(this._pendingRequests).length&&(this.loading=!1),0===e&&this.__repositionOverlayDebouncer&&s.length>(this.__maxRenderedItems||0)&&(setTimeout(()=>this.__repositionOverlayDebouncer.flush()),this.__maxRenderedItems=s.length)}};this._pendingRequests[e]=i,this.dataProvider(t,i)}}_getPageForIndex(e){return Math.floor(e/this.pageSize)}clearCache(){if(!this.dataProvider)return;this._pendingRequests={};const e=[];for(let t=0;t<(this.size||0);t++)e.push(this.__placeHolder);this.filteredItems=e,this.opened?this._loadPage(0):this._forceNextRequest=!0}_sizeChanged(e=0){const t=(this.filteredItems||[]).slice(0,e);for(let i=0;i<e;i++)t[i]=void 0!==t[i]?t[i]:this.__placeHolder;this.filteredItems=t}_pageSizeChanged(e,t){if(Math.floor(e)!==e||e<1)throw this.pageSize=t,new Error("`pageSize` value must be an integer > 0");this.clearCache()}_dataProviderChanged(e,t){this._ensureItemsOrDataProvider(()=>{this.dataProvider=t})}_ensureItemsOrDataProvider(e){if(void 0!==this.items&&void 0!==this.dataProvider)throw e(),new Error("Using `items` and `dataProvider` together is not supported");this.dataProvider&&!this.filteredItems&&(this.filteredItems=[])}_warnDataProviderValue(e,t){if(e&&""!==t&&(void 0===this.selectedItem||null===this.selectedItem)){const e=this._indexOfValue(t,this.filteredItems);(e<0||!this._getItemLabel(this.filteredItems[e]))&&console.warn("Warning: unable to determine the label for the provided `value`. Nothing to display in the text field. This usually happens when setting an initial `value` before any items are returned from the `dataProvider` callback. Consider setting `selectedItem` instead of `value`")}}};i(5);var I=i(126),E=i(236),k=i(132),O=i(6),S=i(3),C=i(131),P=i(2),T=navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/),j=T&&T[1]>=8;Object(O.a)({_template:r.a`
    <style>
      :host {
        display: block;
      }

      @media only screen and (-webkit-max-device-pixel-ratio: 1) {
        :host {
          will-change: transform;
        }
      }

      #items {
        @apply --iron-list-items-container;
        position: relative;
      }

      :host(:not([grid])) #items > ::slotted(*) {
        width: 100%;
      }

      #items > ::slotted(*) {
        box-sizing: border-box;
        margin: 0;
        position: absolute;
        top: 0;
        will-change: transform;
      }
    </style>

    <array-selector id="selector" items="{{items}}" selected="{{selectedItems}}" selected-item="{{selectedItem}}"></array-selector>

    <div id="items">
      <slot></slot>
    </div>
`,is:"iron-list",properties:{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},selectedAs:{type:String,value:"selected"},grid:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_gridChanged"},selectionEnabled:{type:Boolean,value:!1},selectedItem:{type:Object,notify:!0},selectedItems:{type:Object,notify:!0},multiSelection:{type:Boolean,value:!1},scrollOffset:{type:Number,value:0}},observers:["_itemsChanged(items.*)","_selectionEnabledChanged(selectionEnabled)","_multiSelectionChanged(multiSelection)","_setOverflow(scrollTarget, scrollOffset)"],behaviors:[C.a,I.a,E.a,k.a],_ratio:.5,_scrollerPaddingTop:0,_scrollPosition:0,_physicalSize:0,_physicalAverage:0,_physicalAverageCount:0,_physicalTop:0,_virtualCount:0,_estScrollHeight:0,_scrollHeight:0,_viewportHeight:0,_viewportWidth:0,_physicalItems:null,_physicalSizes:null,_firstVisibleIndexVal:null,_lastVisibleIndexVal:null,_maxPages:2,_focusedItem:null,_focusedVirtualIndex:-1,_focusedPhysicalIndex:-1,_offscreenFocusedItem:null,_focusBackfillItem:null,_itemsPerRow:1,_itemWidth:0,_rowHeight:0,_templateCost:0,_parentModel:!0,get _physicalBottom(){return this._physicalTop+this._physicalSize},get _scrollBottom(){return this._scrollPosition+this._viewportHeight},get _virtualEnd(){return this._virtualStart+this._physicalCount-1},get _hiddenContentSize(){return(this.grid?this._physicalRows*this._rowHeight:this._physicalSize)-this._viewportHeight},get _itemsParent(){return Object(S.a)(Object(S.a)(this._userTemplate).parentNode)},get _maxScrollTop(){return this._estScrollHeight-this._viewportHeight+this._scrollOffset},get _maxVirtualStart(){var e=this._convertIndexToCompleteRow(this._virtualCount);return Math.max(0,e-this._physicalCount)},set _virtualStart(e){e=this._clamp(e,0,this._maxVirtualStart),this.grid&&(e-=e%this._itemsPerRow),this._virtualStartVal=e},get _virtualStart(){return this._virtualStartVal||0},set _physicalStart(e){(e%=this._physicalCount)<0&&(e=this._physicalCount+e),this.grid&&(e-=e%this._itemsPerRow),this._physicalStartVal=e},get _physicalStart(){return this._physicalStartVal||0},get _physicalEnd(){return(this._physicalStart+this._physicalCount-1)%this._physicalCount},set _physicalCount(e){this._physicalCountVal=e},get _physicalCount(){return this._physicalCountVal||0},get _optPhysicalSize(){return 0===this._viewportHeight?1/0:this._viewportHeight*this._maxPages},get _isVisible(){return Boolean(this.offsetWidth||this.offsetHeight)},get firstVisibleIndex(){var e=this._firstVisibleIndexVal;if(null==e){var t=this._physicalTop+this._scrollOffset;e=this._iterateItems((function(e,i){return(t+=this._getPhysicalSizeIncrement(e))>this._scrollPosition?this.grid?i-i%this._itemsPerRow:i:this.grid&&this._virtualCount-1===i?i-i%this._itemsPerRow:void 0}))||0,this._firstVisibleIndexVal=e}return e},get lastVisibleIndex(){var e=this._lastVisibleIndexVal;if(null==e){if(this.grid)e=Math.min(this._virtualCount,this.firstVisibleIndex+this._estRowsInView*this._itemsPerRow-1);else{var t=this._physicalTop+this._scrollOffset;this._iterateItems((function(i,s){t<this._scrollBottom&&(e=s),t+=this._getPhysicalSizeIncrement(i)}))}this._lastVisibleIndexVal=e}return e},get _defaultScrollTarget(){return this},get _virtualRowCount(){return Math.ceil(this._virtualCount/this._itemsPerRow)},get _estRowsInView(){return Math.ceil(this._viewportHeight/this._rowHeight)},get _physicalRows(){return Math.ceil(this._physicalCount/this._itemsPerRow)},get _scrollOffset(){return this._scrollerPaddingTop+this.scrollOffset},ready:function(){this.addEventListener("focus",this._didFocus.bind(this),!0)},attached:function(){this._debounce("_render",this._render,p.a),this.listen(this,"iron-resize","_resizeHandler"),this.listen(this,"keydown","_keydownHandler")},detached:function(){this.unlisten(this,"iron-resize","_resizeHandler"),this.unlisten(this,"keydown","_keydownHandler")},_setOverflow:function(e){this.style.webkitOverflowScrolling=e===this?"touch":"",this.style.overflowY=e===this?"auto":"",this._lastVisibleIndexVal=null,this._firstVisibleIndexVal=null,this._debounce("_render",this._render,p.a)},updateViewportBoundaries:function(){var e=window.getComputedStyle(this);this._scrollerPaddingTop=this.scrollTarget===this?0:parseInt(e["padding-top"],10),this._isRTL=Boolean("rtl"===e.direction),this._viewportWidth=this.$.items.offsetWidth,this._viewportHeight=this._scrollTargetHeight,this.grid&&this._updateGridMetrics()},_scrollHandler:function(){var e=Math.max(0,Math.min(this._maxScrollTop,this._scrollTop)),t=e-this._scrollPosition,i=t>=0;if(this._scrollPosition=e,this._firstVisibleIndexVal=null,this._lastVisibleIndexVal=null,Math.abs(t)>this._physicalSize&&this._physicalSize>0){t-=this._scrollOffset;var s=Math.round(t/this._physicalAverage)*this._itemsPerRow;this._virtualStart=this._virtualStart+s,this._physicalStart=this._physicalStart+s,this._physicalTop=Math.floor(this._virtualStart/this._itemsPerRow)*this._physicalAverage,this._update()}else if(this._physicalCount>0){var r=this._getReusables(i);i?(this._physicalTop=r.physicalTop,this._virtualStart=this._virtualStart+r.indexes.length,this._physicalStart=this._physicalStart+r.indexes.length):(this._virtualStart=this._virtualStart-r.indexes.length,this._physicalStart=this._physicalStart-r.indexes.length),this._update(r.indexes,i?null:r.indexes),this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,0),p.c)}},_getReusables:function(e){var t,i,s,r=[],n=this._hiddenContentSize*this._ratio,o=this._virtualStart,a=this._virtualEnd,l=this._physicalCount,c=this._physicalTop+this._scrollOffset,h=this._physicalBottom+this._scrollOffset,d=this._scrollTop,u=this._scrollBottom;for(e?(t=this._physicalStart,this._physicalEnd,i=d-c):(t=this._physicalEnd,this._physicalStart,i=h-u);i-=s=this._getPhysicalSizeIncrement(t),!(r.length>=l||i<=n);)if(e){if(a+r.length+1>=this._virtualCount)break;if(c+s>=d-this._scrollOffset)break;r.push(t),c+=s,t=(t+1)%l}else{if(o-r.length<=0)break;if(c+this._physicalSize-s<=u)break;r.push(t),c-=s,t=0===t?l-1:t-1}return{indexes:r,physicalTop:c-this._scrollOffset}},_update:function(e,t){if(!(e&&0===e.length||0===this._physicalCount)){if(this._manageFocus(),this._assignModels(e),this._updateMetrics(e),t)for(;t.length;){var i=t.pop();this._physicalTop-=this._getPhysicalSizeIncrement(i)}this._positionItems(),this._updateScrollerSize()}},_createPool:function(e){var t,i;this._ensureTemplatized();var s=new Array(e);for(t=0;t<e;t++)i=this.stamp(null),s[t]=i.root.querySelector("*"),this._itemsParent.appendChild(i.root);return s},_isClientFull:function(){return 0!=this._scrollBottom&&this._physicalBottom-1>=this._scrollBottom&&this._physicalTop<=this._scrollPosition},_increasePoolIfNeeded:function(e){var t=this._clamp(this._physicalCount+e,3,this._virtualCount-this._virtualStart);if(t=this._convertIndexToCompleteRow(t),this.grid){var i=t%this._itemsPerRow;i&&t-i<=this._physicalCount&&(t+=this._itemsPerRow),t-=i}var s=t-this._physicalCount,r=Math.round(.5*this._physicalCount);if(!(s<0)){if(s>0){var n=window.performance.now();[].push.apply(this._physicalItems,this._createPool(s));for(var o=0;o<s;o++)this._physicalSizes.push(0);this._physicalCount=this._physicalCount+s,this._physicalStart>this._physicalEnd&&this._isIndexRendered(this._focusedVirtualIndex)&&this._getPhysicalIndex(this._focusedVirtualIndex)<this._physicalEnd&&(this._physicalStart=this._physicalStart+s),this._update(),this._templateCost=(window.performance.now()-n)/s,r=Math.round(.5*this._physicalCount)}this._virtualEnd>=this._virtualCount-1||0===r||(this._isClientFull()?this._physicalSize<this._optPhysicalSize&&this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,this._clamp(Math.round(50/this._templateCost),1,r)),p.b):this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,r),p.c))}},_render:function(){if(this.isAttached&&this._isVisible)if(0!==this._physicalCount){var e=this._getReusables(!0);this._physicalTop=e.physicalTop,this._virtualStart=this._virtualStart+e.indexes.length,this._physicalStart=this._physicalStart+e.indexes.length,this._update(e.indexes),this._update(),this._increasePoolIfNeeded(0)}else this._virtualCount>0&&(this.updateViewportBoundaries(),this._increasePoolIfNeeded(3))},_ensureTemplatized:function(){if(!this.ctor){this._userTemplate=this.queryEffectiveChildren("template"),this._userTemplate||console.warn("iron-list requires a template to be provided in light-dom");var e={__key__:!0};e[this.as]=!0,e[this.indexAs]=!0,e[this.selectedAs]=!0,e.tabIndex=!0,this._instanceProps=e,this.templatize(this._userTemplate,this.mutableData)}},_gridChanged:function(e,t){void 0!==t&&(this.notifyResize(),Object(f.b)(),e&&this._updateGridMetrics())},_itemsChanged:function(e){if("items"===e.path)this._virtualStart=0,this._physicalTop=0,this._virtualCount=this.items?this.items.length:0,this._physicalIndexForKey={},this._firstVisibleIndexVal=null,this._lastVisibleIndexVal=null,this._physicalCount=this._physicalCount||0,this._physicalItems=this._physicalItems||[],this._physicalSizes=this._physicalSizes||[],this._physicalStart=0,this._scrollTop>this._scrollOffset&&this._resetScrollPosition(0),this._removeFocusedItem(),this._debounce("_render",this._render,p.a);else if("items.splices"===e.path){if(this._adjustVirtualIndex(e.value.indexSplices),this._virtualCount=this.items?this.items.length:0,e.value.indexSplices.some((function(e){return e.addedCount>0||e.removed.length>0}))){var t=this._getActiveElement();this.contains(t)&&t.blur()}var i=e.value.indexSplices.some((function(e){return e.index+e.addedCount>=this._virtualStart&&e.index<=this._virtualEnd}),this);this._isClientFull()&&!i||this._debounce("_render",this._render,p.a)}else"items.length"!==e.path&&this._forwardItemPath(e.path,e.value)},_forwardItemPath:function(e,t){var i,s,r,n=(e=e.slice(6)).indexOf(".");-1===n&&(n=e.length);var o=this.modelForElement(this._offscreenFocusedItem),a=parseInt(e.substring(0,n),10);(i=this._isIndexRendered(a))?(s=this._getPhysicalIndex(a),r=this.modelForElement(this._physicalItems[s])):o&&(r=o),r&&r[this.indexAs]===a&&(e=e.substring(n+1),e=this.as+(e?"."+e:""),r._setPendingPropertyOrPath(e,t,!1,!0),r._flushProperties&&r._flushProperties(!0),i&&(this._updateMetrics([s]),this._positionItems(),this._updateScrollerSize()))},_adjustVirtualIndex:function(e){e.forEach((function(e){if(e.removed.forEach(this._removeItem,this),e.index<this._virtualStart){var t=Math.max(e.addedCount-e.removed.length,e.index-this._virtualStart);this._virtualStart=this._virtualStart+t,this._focusedVirtualIndex>=0&&(this._focusedVirtualIndex=this._focusedVirtualIndex+t)}}),this)},_removeItem:function(e){this.$.selector.deselect(e),this._focusedItem&&this.modelForElement(this._focusedItem)[this.as]===e&&this._removeFocusedItem()},_iterateItems:function(e,t){var i,s,r,n;if(2===arguments.length&&t){for(n=0;n<t.length;n++)if(i=t[n],s=this._computeVidx(i),null!=(r=e.call(this,i,s)))return r}else{for(i=this._physicalStart,s=this._virtualStart;i<this._physicalCount;i++,s++)if(null!=(r=e.call(this,i,s)))return r;for(i=0;i<this._physicalStart;i++,s++)if(null!=(r=e.call(this,i,s)))return r}},_computeVidx:function(e){return e>=this._physicalStart?this._virtualStart+(e-this._physicalStart):this._virtualStart+(this._physicalCount-this._physicalStart)+e},_assignModels:function(e){this._iterateItems((function(e,t){var i=this._physicalItems[e],s=this.items&&this.items[t];if(null!=s){var r=this.modelForElement(i);r.__key__=null,this._forwardProperty(r,this.as,s),this._forwardProperty(r,this.selectedAs,this.$.selector.isSelected(s)),this._forwardProperty(r,this.indexAs,t),this._forwardProperty(r,"tabIndex",this._focusedVirtualIndex===t?0:-1),this._physicalIndexForKey[r.__key__]=e,r._flushProperties&&r._flushProperties(!0),i.removeAttribute("hidden")}else i.setAttribute("hidden","")}),e)},_updateMetrics:function(e){Object(f.b)();var t=0,i=0,s=this._physicalAverageCount,r=this._physicalAverage;this._iterateItems((function(e,s){i+=this._physicalSizes[e],this._physicalSizes[e]=this._physicalItems[e].offsetHeight,t+=this._physicalSizes[e],this._physicalAverageCount+=this._physicalSizes[e]?1:0}),e),this.grid?(this._updateGridMetrics(),this._physicalSize=Math.ceil(this._physicalCount/this._itemsPerRow)*this._rowHeight):(i=1===this._itemsPerRow?i:Math.ceil(this._physicalCount/this._itemsPerRow)*this._rowHeight,this._physicalSize=this._physicalSize+t-i,this._itemsPerRow=1),this._physicalAverageCount!==s&&(this._physicalAverage=Math.round((r*s+t)/this._physicalAverageCount))},_updateGridMetrics:function(){this._itemWidth=this._physicalCount>0?this._physicalItems[0].getBoundingClientRect().width:200,this._rowHeight=this._physicalCount>0?this._physicalItems[0].offsetHeight:200,this._itemsPerRow=this._itemWidth?Math.floor(this._viewportWidth/this._itemWidth):this._itemsPerRow},_positionItems:function(){this._adjustScrollPosition();var e=this._physicalTop;if(this.grid){var t=this._itemsPerRow*this._itemWidth,i=(this._viewportWidth-t)/2;this._iterateItems((function(t,s){var r=s%this._itemsPerRow,n=Math.floor(r*this._itemWidth+i);this._isRTL&&(n*=-1),this.translate3d(n+"px",e+"px",0,this._physicalItems[t]),this._shouldRenderNextRow(s)&&(e+=this._rowHeight)}))}else this._iterateItems((function(t,i){this.translate3d(0,e+"px",0,this._physicalItems[t]),e+=this._physicalSizes[t]}))},_getPhysicalSizeIncrement:function(e){return this.grid?this._computeVidx(e)%this._itemsPerRow!=this._itemsPerRow-1?0:this._rowHeight:this._physicalSizes[e]},_shouldRenderNextRow:function(e){return e%this._itemsPerRow==this._itemsPerRow-1},_adjustScrollPosition:function(){var e=0===this._virtualStart?this._physicalTop:Math.min(this._scrollPosition+this._physicalTop,0);if(0!==e){this._physicalTop=this._physicalTop-e;var t=this._scrollTop;!j&&t>0&&this._resetScrollPosition(t-e)}},_resetScrollPosition:function(e){this.scrollTarget&&e>=0&&(this._scrollTop=e,this._scrollPosition=this._scrollTop)},_updateScrollerSize:function(e){this.grid?this._estScrollHeight=this._virtualRowCount*this._rowHeight:this._estScrollHeight=this._physicalBottom+Math.max(this._virtualCount-this._physicalCount-this._virtualStart,0)*this._physicalAverage,((e=(e=(e=e||0===this._scrollHeight)||this._scrollPosition>=this._estScrollHeight-this._physicalSize)||this.grid&&this.$.items.style.height<this._estScrollHeight)||Math.abs(this._estScrollHeight-this._scrollHeight)>=this._viewportHeight)&&(this.$.items.style.height=this._estScrollHeight+"px",this._scrollHeight=this._estScrollHeight)},scrollToItem:function(e){return this.scrollToIndex(this.items.indexOf(e))},scrollToIndex:function(e){if(!("number"!=typeof e||e<0||e>this.items.length-1)&&(Object(f.b)(),0!==this._physicalCount)){e=this._clamp(e,0,this._virtualCount-1),(!this._isIndexRendered(e)||e>=this._maxVirtualStart)&&(this._virtualStart=this.grid?e-2*this._itemsPerRow:e-1),this._manageFocus(),this._assignModels(),this._updateMetrics(),this._physicalTop=Math.floor(this._virtualStart/this._itemsPerRow)*this._physicalAverage;for(var t=this._physicalStart,i=this._virtualStart,s=0,r=this._hiddenContentSize;i<e&&s<=r;)s+=this._getPhysicalSizeIncrement(t),t=(t+1)%this._physicalCount,i++;this._updateScrollerSize(!0),this._positionItems(),this._resetScrollPosition(this._physicalTop+this._scrollOffset+s),this._increasePoolIfNeeded(0),this._firstVisibleIndexVal=null,this._lastVisibleIndexVal=null}},_resetAverage:function(){this._physicalAverage=0,this._physicalAverageCount=0},_resizeHandler:function(){this._debounce("_render",(function(){this._firstVisibleIndexVal=null,this._lastVisibleIndexVal=null,this._isVisible?(this.updateViewportBoundaries(),this.toggleScrollListener(!0),this._resetAverage(),this._render()):this.toggleScrollListener(!1)}),p.a)},selectItem:function(e){return this.selectIndex(this.items.indexOf(e))},selectIndex:function(e){if(!(e<0||e>=this._virtualCount)){if(!this.multiSelection&&this.selectedItem&&this.clearSelection(),this._isIndexRendered(e)){var t=this.modelForElement(this._physicalItems[this._getPhysicalIndex(e)]);t&&(t[this.selectedAs]=!0),this.updateSizeForIndex(e)}this.$.selector.selectIndex(e)}},deselectItem:function(e){return this.deselectIndex(this.items.indexOf(e))},deselectIndex:function(e){if(!(e<0||e>=this._virtualCount)){if(this._isIndexRendered(e))this.modelForElement(this._physicalItems[this._getPhysicalIndex(e)])[this.selectedAs]=!1,this.updateSizeForIndex(e);this.$.selector.deselectIndex(e)}},toggleSelectionForItem:function(e){return this.toggleSelectionForIndex(this.items.indexOf(e))},toggleSelectionForIndex:function(e){(this.$.selector.isIndexSelected?this.$.selector.isIndexSelected(e):this.$.selector.isSelected(this.items[e]))?this.deselectIndex(e):this.selectIndex(e)},clearSelection:function(){this._iterateItems((function(e,t){this.modelForElement(this._physicalItems[e])[this.selectedAs]=!1})),this.$.selector.clearSelection()},_selectionEnabledChanged:function(e){(e?this.listen:this.unlisten).call(this,this,"tap","_selectionHandler")},_selectionHandler:function(e){var t=this.modelForElement(e.target);if(t){var i,s,r=Object(S.a)(e).path[0],n=this._getActiveElement(),o=this._physicalItems[this._getPhysicalIndex(t[this.indexAs])];"input"!==r.localName&&"button"!==r.localName&&"select"!==r.localName&&(i=t.tabIndex,t.tabIndex=-100,s=n?n.tabIndex:-1,t.tabIndex=i,n&&o!==n&&o.contains(n)&&-100!==s||this.toggleSelectionForItem(t[this.as]))}},_multiSelectionChanged:function(e){this.clearSelection(),this.$.selector.multi=e},updateSizeForItem:function(e){return this.updateSizeForIndex(this.items.indexOf(e))},updateSizeForIndex:function(e){return this._isIndexRendered(e)?(this._updateMetrics([this._getPhysicalIndex(e)]),this._positionItems(),null):null},_manageFocus:function(){var e=this._focusedVirtualIndex;e>=0&&e<this._virtualCount?this._isIndexRendered(e)?this._restoreFocusedItem():this._createFocusBackfillItem():this._virtualCount>0&&this._physicalCount>0&&(this._focusedPhysicalIndex=this._physicalStart,this._focusedVirtualIndex=this._virtualStart,this._focusedItem=this._physicalItems[this._physicalStart])},_convertIndexToCompleteRow:function(e){return this._itemsPerRow=this._itemsPerRow||1,this.grid?Math.ceil(e/this._itemsPerRow)*this._itemsPerRow:e},_isIndexRendered:function(e){return e>=this._virtualStart&&e<=this._virtualEnd},_isIndexVisible:function(e){return e>=this.firstVisibleIndex&&e<=this.lastVisibleIndex},_getPhysicalIndex:function(e){return(this._physicalStart+(e-this._virtualStart))%this._physicalCount},focusItem:function(e){this._focusPhysicalItem(e)},_focusPhysicalItem:function(e){if(!(e<0||e>=this._virtualCount)){this._restoreFocusedItem(),this._isIndexRendered(e)||this.scrollToIndex(e);var t,i=this._physicalItems[this._getPhysicalIndex(e)],s=this.modelForElement(i);s.tabIndex=-100,-100===i.tabIndex&&(t=i),t||(t=Object(S.a)(i).querySelector('[tabindex="-100"]')),s.tabIndex=0,this._focusedVirtualIndex=e,t&&t.focus()}},_removeFocusedItem:function(){this._offscreenFocusedItem&&this._itemsParent.removeChild(this._offscreenFocusedItem),this._offscreenFocusedItem=null,this._focusBackfillItem=null,this._focusedItem=null,this._focusedVirtualIndex=-1,this._focusedPhysicalIndex=-1},_createFocusBackfillItem:function(){var e=this._focusedPhysicalIndex;if(!(this._offscreenFocusedItem||this._focusedVirtualIndex<0)){if(!this._focusBackfillItem){var t=this.stamp(null);this._focusBackfillItem=t.root.querySelector("*"),this._itemsParent.appendChild(t.root)}this._offscreenFocusedItem=this._physicalItems[e],this.modelForElement(this._offscreenFocusedItem).tabIndex=0,this._physicalItems[e]=this._focusBackfillItem,this._focusedPhysicalIndex=e,this.translate3d(0,"-10000px",0,this._offscreenFocusedItem)}},_restoreFocusedItem:function(){if(this._offscreenFocusedItem&&!(this._focusedVirtualIndex<0)){this._assignModels();var e=this._focusedPhysicalIndex=this._getPhysicalIndex(this._focusedVirtualIndex),t=this._physicalItems[e];if(t){var i=this.modelForElement(t),s=this.modelForElement(this._offscreenFocusedItem);i[this.as]===s[this.as]?(this._focusBackfillItem=t,i.tabIndex=-1,this._physicalItems[e]=this._offscreenFocusedItem,this.translate3d(0,"-10000px",0,this._focusBackfillItem)):(this._removeFocusedItem(),this._focusBackfillItem=null),this._offscreenFocusedItem=null}}},_didFocus:function(e){var t=this.modelForElement(e.target),i=this.modelForElement(this._focusedItem),s=null!==this._offscreenFocusedItem,r=this._focusedVirtualIndex;t&&(i===t?this._isIndexVisible(r)||this.scrollToIndex(r):(this._restoreFocusedItem(),i&&(i.tabIndex=-1),t.tabIndex=0,r=t[this.indexAs],this._focusedVirtualIndex=r,this._focusedPhysicalIndex=this._getPhysicalIndex(r),this._focusedItem=this._physicalItems[this._focusedPhysicalIndex],s&&!this._offscreenFocusedItem&&this._update()))},_keydownHandler:function(e){switch(e.keyCode){case 40:this._focusedVirtualIndex<this._virtualCount-1&&e.preventDefault(),this._focusPhysicalItem(this._focusedVirtualIndex+(this.grid?this._itemsPerRow:1));break;case 39:this.grid&&this._focusPhysicalItem(this._focusedVirtualIndex+(this._isRTL?-1:1));break;case 38:this._focusedVirtualIndex>0&&e.preventDefault(),this._focusPhysicalItem(this._focusedVirtualIndex-(this.grid?this._itemsPerRow:1));break;case 37:this.grid&&this._focusPhysicalItem(this._focusedVirtualIndex+(this._isRTL?1:-1));break;case 13:this._focusPhysicalItem(this._focusedVirtualIndex),this.selectionEnabled&&this._selectionHandler(e)}},_clamp:function(e,t,i){return Math.min(i,Math.max(t,e))},_debounce:function(e,t,i){this._debouncers=this._debouncers||{},this._debouncers[e]=m.a.debounce(this._debouncers[e],i,t.bind(this)),Object(f.a)(this._debouncers[e])},_forwardProperty:function(e,t,i){e._setPendingProperty(t,i)},_forwardHostPropV2:function(e,t){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach((function(i){i&&this.modelForElement(i).forwardHostProp(e,t)}),this)},_notifyInstancePropV2:function(e,t,i){if(Object(P.e)(this.as,t)){var s=e[this.indexAs];t==this.as&&(this.items[s]=i),this.notifyPath(Object(P.i)(this.as,"items."+s,t),i)}},_getStampedChildren:function(){return this._physicalItems},_forwardInstancePath:function(e,t,i){0===t.indexOf(this.as+".")&&this.notifyPath("items."+e.__key__+"."+t.slice(this.as.length+1),i)},_forwardParentPath:function(e,t){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach((function(i){i&&this.modelForElement(i).notifyPath(e,t,!0)}),this)},_forwardParentProp:function(e,t){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach((function(i){i&&(this.modelForElement(i)[e]=t)}),this)},_getActiveElement:function(){var e=this._itemsParent.node.domHost;return Object(S.a)(e?e.root:document).activeElement}});class V extends(Object(l.a)(a.a)){static get template(){return r.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
         display: none;
      }
    </style>
    <div part="content" id="content"></div>
`}static get is(){return"vaadin-combo-box-item"}static get properties(){return{index:Number,item:Object,label:String,selected:{type:Boolean,value:!1,reflectToAttribute:!0},focused:{type:Boolean,value:!1,reflectToAttribute:!0},_itemTemplateInstance:Object,renderer:Function,_oldRenderer:Function}}static get observers(){return["_rendererOrItemChanged(renderer, index, item.*)","_updateLabel(label, _itemTemplateInstance)",'_updateTemplateInstanceVariable("index", index, _itemTemplateInstance)','_updateTemplateInstanceVariable("item", item, _itemTemplateInstance)','_updateTemplateInstanceVariable("selected", selected, _itemTemplateInstance)','_updateTemplateInstanceVariable("focused", focused, _itemTemplateInstance)']}connectedCallback(){if(super.connectedCallback(),!this._itemTemplateInstance){const e=this.getRootNode().host.getRootNode().host.__dataHost.getRootNode().host;this._comboBox=e.getRootNode().host,this._comboBox._ensureTemplatized(),this._comboBox._TemplateClass&&(this._itemTemplateInstance=new this._comboBox._TemplateClass({}),this.$.content.textContent="",this.$.content.appendChild(this._itemTemplateInstance.root))}}_render(){if(!this.renderer)return;const e={index:this.index,item:this.item};this.renderer(this.$.content,this._comboBox,e)}_rendererOrItemChanged(e,t,i){void 0!==i&&void 0!==t&&(this._oldRenderer!==e&&(this.$.content.innerHTML=""),e&&(this._oldRenderer=e,this._render()))}_updateLabel(e,t){void 0===t&&this.$.content&&!this.renderer&&(this.$.content.textContent=e)}_updateTemplateInstanceVariable(e,t,i){void 0!==e&&void 0!==t&&void 0!==i&&(i[e]=t)}}customElements.define(V.is,V);var A=i(284),$=i(285),F=i(90);class z extends $.a{static get is(){return"vaadin-combo-box-overlay"}ready(){super.ready();const e=document.createElement("div");e.setAttribute("part","loader");const t=this.shadowRoot.querySelector('[part~="content"]');t.parentNode.insertBefore(e,t)}}customElements.define(z.is,z);class L extends(Object(A.a)(Object(F.b)(I.a,a.a))){static get template(){return r.a`
    <style>
      :host {
        display: block;
      }

      :host > #overlay {
        display: none;
      }
    </style>
    <vaadin-combo-box-overlay id="overlay" hidden\$="[[hidden]]" opened="[[opened]]" template="{{template}}" style="align-items: stretch; margin: 0;" theme\$="[[theme]]">
      <slot></slot>
    </vaadin-combo-box-overlay>
`}static get is(){return"vaadin-combo-box-dropdown"}static get properties(){return{opened:{type:Boolean,observer:"_openedChanged"},template:{type:Object,notify:!0},positionTarget:{type:Object},alignedAbove:{type:Boolean,value:!1},theme:String}}constructor(){super(),this._boundSetPosition=this._setPosition.bind(this),this._boundOutsideClickListener=this._outsideClickListener.bind(this)}connectedCallback(){super.connectedCallback(),this.addEventListener("iron-resize",this._boundSetPosition)}ready(){super.ready(),this.$.overlay.addEventListener("vaadin-overlay-outside-click",e=>{e.preventDefault()})}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("iron-resize",this._boundSetPosition),this.opened=!1}notifyResize(){super.notifyResize(),this.positionTarget&&this.opened&&(this._setPosition(),requestAnimationFrame(this._setPosition.bind(this)))}_openedChanged(e,t){!!e!=!!t&&(e?(this.$.overlay.style.position=this._isPositionFixed(this.positionTarget)?"fixed":"absolute",this._setPosition(),window.addEventListener("scroll",this._boundSetPosition,!0),document.addEventListener("click",this._boundOutsideClickListener,!0),this.dispatchEvent(new CustomEvent("vaadin-combo-box-dropdown-opened",{bubbles:!0,composed:!0}))):(window.removeEventListener("scroll",this._boundSetPosition,!0),document.removeEventListener("click",this._boundOutsideClickListener,!0),this.dispatchEvent(new CustomEvent("vaadin-combo-box-dropdown-closed",{bubbles:!0,composed:!0}))))}_outsideClickListener(e){const t=e.composedPath();t.indexOf(this.positionTarget)<0&&t.indexOf(this.$.overlay)<0&&(this.opened=!1)}_isPositionFixed(e){const t=this._getOffsetParent(e);return"fixed"===window.getComputedStyle(e).position||t&&this._isPositionFixed(t)}_getOffsetParent(e){if(e.assignedSlot)return e.assignedSlot.parentElement;if(e.parentElement)return e.offsetParent;const t=e.parentNode;return t&&11===t.nodeType&&t.host?t.host:void 0}_verticalOffset(e,t){return this.alignedAbove?-e.height:t.height}_shouldAlignAbove(e){return(window.innerHeight-e.bottom-Math.min(document.body.scrollTop,0))/window.innerHeight<.3}_setPosition(e){if(this.hidden)return;if(e&&e.target){const t=e.target===document?document.body:e.target,i=this.$.overlay.parentElement;if(!t.contains(this.$.overlay)&&!t.contains(this.positionTarget)||i!==document.body)return}const t=this.positionTarget.getBoundingClientRect();this.alignedAbove=this._shouldAlignAbove(t);const i=this.$.overlay.getBoundingClientRect();this._translateX=t.left-i.left+(this._translateX||0),this._translateY=t.top-i.top+(this._translateY||0)+this._verticalOffset(i,t);const s=window.devicePixelRatio||1;this._translateX=Math.round(this._translateX*s)/s,this._translateY=Math.round(this._translateY*s)/s,this.$.overlay.style.transform=`translate3d(${this._translateX}px, ${this._translateY}px, 0)`,this.$.overlay.style.width=this.positionTarget.clientWidth+"px",this.$.overlay.style.justifyContent=this.alignedAbove?"flex-end":"flex-start",this.dispatchEvent(new CustomEvent("position-changed"))}}customElements.define(L.is,L);const D=(()=>{try{return document.createEvent("TouchEvent"),!0}catch(e){return!1}})();class R extends class extends a.a{}{static get template(){return r.a`
    <vaadin-combo-box-dropdown id="dropdown" hidden="[[_hidden(_items.*, loading)]]" position-target="[[positionTarget]]" on-template-changed="_templateChanged" on-position-changed="_setOverlayHeight" disable-upgrade="" theme="[[theme]]">
      <template>
        <style>
          #scroller {
            overflow: auto;

            /* Fixes item background from getting on top of scrollbars on Safari */
            transform: translate3d(0, 0, 0);

            /* Enable momentum scrolling on iOS (iron-list v1.2+ no longer does it for us) */
            -webkit-overflow-scrolling: touch;

            /* Fixes scrollbar disappearing when 'Show scroll bars: Always' enabled in Safari */
            box-shadow: 0 0 0 white;
          }
        </style>
        <div id="scroller" on-click="_stopPropagation">
          <iron-list id="selector" role="listbox" items="[[_getItems(opened, _items)]]" scroll-target="[[_scroller]]">
            <template>
              <vaadin-combo-box-item on-click="_onItemClick" index="[[__requestItemByIndex(item, index)]]" item="[[item]]" label="[[getItemLabel(item, _itemLabelPath)]]" selected="[[_isItemSelected(item, _selectedItem, _itemIdPath)]]" renderer="[[renderer]]" role\$="[[_getAriaRole(index)]]" aria-selected\$="[[_getAriaSelected(_focusedIndex,index)]]" focused="[[_isItemFocused(_focusedIndex,index)]]" tabindex="-1" theme\$="[[theme]]">
              </vaadin-combo-box-item>
            </template>
          </iron-list>
        </div>
      </template>
    </vaadin-combo-box-dropdown>
`}static get is(){return"vaadin-combo-box-dropdown-wrapper"}static get properties(){return{touchDevice:{type:Boolean,value:D},opened:Boolean,positionTarget:{type:Object},renderer:Function,loading:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_setOverlayHeight"},theme:String,_selectedItem:{type:Object},_items:{type:Object},_focusedIndex:{type:Number,value:-1,observer:"_focusedIndexChanged"},_focusedItem:{type:String,computed:"_getFocusedItem(_focusedIndex)"},_itemLabelPath:{type:String,value:"label"},_itemValuePath:{type:String,value:"value"},_selector:Object,_itemIdPath:String}}static get observers(){return["_selectorChanged(_selector)","_loadingChanged(loading)","_openedChanged(opened, _items, loading)"]}_fireTouchAction(e){this.dispatchEvent(new CustomEvent("vaadin-overlay-touch-action",{detail:{sourceEvent:e}}))}_getItems(e,t){return e?t:[]}_openedChanged(e,t,i){if(this.$.dropdown.hasAttribute("disable-upgrade")){if(!e)return;this._initDropdown()}this.$.dropdown.opened=!(!e||!(i||this.$.dropdown.opened||t&&t.length))}_initDropdown(){this.$.dropdown.removeAttribute("disable-upgrade"),this._templateChanged(),this._loadingChanged(this.loading),this.$.dropdown.$.overlay.addEventListener("touchend",e=>this._fireTouchAction(e)),this.$.dropdown.$.overlay.addEventListener("touchmove",e=>this._fireTouchAction(e)),this.$.dropdown.$.overlay.addEventListener("mousedown",e=>e.preventDefault()),/Trident/.test(navigator.userAgent)&&this._scroller.setAttribute("unselectable","on")}_templateChanged(e){this.$.dropdown.hasAttribute("disable-upgrade")||(this._selector=this.$.dropdown.$.overlay.content.querySelector("#selector"),this._scroller=this.$.dropdown.$.overlay.content.querySelector("#scroller"))}_loadingChanged(e){this.$.dropdown.hasAttribute("disable-upgrade")||(e?this.$.dropdown.$.overlay.setAttribute("loading",""):this.$.dropdown.$.overlay.removeAttribute("loading"))}_selectorChanged(e){this._patchWheelOverScrolling()}_setOverlayHeight(){if(!this.opened||!this.positionTarget||!this._selector)return;const e=this.positionTarget.getBoundingClientRect();this._scroller.style.maxHeight=(window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-combo-box-overlay-max-height"):getComputedStyle(this).getPropertyValue("--vaadin-combo-box-overlay-max-height"))||"65vh";const t=this._maxOverlayHeight(e);this.$.dropdown.$.overlay.style.maxHeight=t,this._selector.style.maxHeight=t,this.updateViewportBoundaries()}_maxOverlayHeight(e){return this.$.dropdown.alignedAbove?Math.max(e.top-8+Math.min(document.body.scrollTop,0),116)+"px":Math.max(document.documentElement.clientHeight-e.bottom-8,116)+"px"}_getFocusedItem(e){if(e>=0)return this._items[e]}_isItemSelected(e,t,i){return!(e instanceof b)&&(i&&void 0!==e&&void 0!==t?this.get(i,e)===this.get(i,t):e===t)}_onItemClick(e){e.detail&&e.detail.sourceEvent&&e.detail.sourceEvent.stopPropagation&&this._stopPropagation(e.detail.sourceEvent),this.dispatchEvent(new CustomEvent("selection-changed",{detail:{item:e.model.item}}))}indexOfLabel(e){if(this._items&&e)for(let t=0;t<this._items.length;t++)if(this.getItemLabel(this._items[t]).toString().toLowerCase()===e.toString().toLowerCase())return t;return-1}__requestItemByIndex(e,t){return e instanceof b&&void 0!==t&&this.dispatchEvent(new CustomEvent("index-requested",{detail:{index:t}})),t}getItemLabel(e,t){t=t||this._itemLabelPath;let i=e&&t?this.get(t,e):void 0;return null==i&&(i=e?e.toString():""),i}_isItemFocused(e,t){return e==t}_getAriaSelected(e,t){return this._isItemFocused(e,t).toString()}_getAriaRole(e){return void 0!==e&&"option"}_focusedIndexChanged(e){e>=0&&this._scrollIntoView(e)}_scrollIntoView(e){if(!(this.opened&&e>=0))return;const t=this._visibleItemsCount();if(void 0===t)return;let i=e;e>this._selector.lastVisibleIndex-1?(this._selector.scrollToIndex(e),i=e-t+1):e>this._selector.firstVisibleIndex&&(i=this._selector.firstVisibleIndex),this._selector.scrollToIndex(Math.max(0,i));const s=this._selector._getPhysicalIndex(e),r=this._selector._physicalItems[s];if(!r)return;const n=r.getBoundingClientRect(),o=this._scroller.getBoundingClientRect(),a=n.bottom-o.bottom+this._viewportTotalPaddingBottom;a>0&&(this._scroller.scrollTop+=a)}ensureItemsRendered(){this._selector._render()}adjustScrollPosition(){this.opened&&this._items&&this._scrollIntoView(this._focusedIndex)}_patchWheelOverScrolling(){const e=this._selector;e.addEventListener("wheel",t=>{const i=e._scroller||e.scrollTarget,s=0===i.scrollTop,r=i.scrollHeight-i.scrollTop-i.clientHeight<=1;(s&&t.deltaY<0||r&&t.deltaY>0)&&t.preventDefault()})}updateViewportBoundaries(){this._cachedViewportTotalPaddingBottom=void 0,this._selector.updateViewportBoundaries()}get _viewportTotalPaddingBottom(){if(void 0===this._cachedViewportTotalPaddingBottom){const e=window.getComputedStyle(this._selector.$.items);this._cachedViewportTotalPaddingBottom=[e.paddingBottom,e.borderBottomWidth].map(e=>parseInt(e,10)).reduce((e,t)=>e+t)}return this._cachedViewportTotalPaddingBottom}_visibleItemsCount(){if(this._selector)return this._selector.flushDebouncer("_debounceTemplate"),this._selector.scrollToIndex(this._selector.firstVisibleIndex),this.updateViewportBoundaries(),this._selector.lastVisibleIndex-this._selector.firstVisibleIndex+1}_selectItem(e){e="number"==typeof e?this._items[e]:e,this._selector.selectedItem!==e&&this._selector.selectItem(e)}_preventDefault(e){e.cancelable&&e.preventDefault()}_stopPropagation(e){e.stopPropagation()}_hidden(e){return!(this.loading||this._items&&this._items.length)}}customElements.define(R.is,R);var B=i(24);class H extends(Object(u.a)(Object(l.a)(x(w(a.a))))){static get template(){return r.a`
    <style>
      :host([opened]) {
        pointer-events: auto;
      }
    </style>

    <slot></slot>

    <vaadin-combo-box-dropdown-wrapper id="overlay" opened="[[opened]]" position-target="[[inputElement]]" renderer="[[renderer]]" _focused-index="[[_focusedIndex]]" _item-id-path="[[itemIdPath]]" _item-label-path="[[itemLabelPath]]" loading="[[loading]]" theme="[[theme]]">
    </vaadin-combo-box-dropdown-wrapper>
`}static get is(){return"vaadin-combo-box-light"}static get properties(){return{attrForValue:{type:String,value:"value"},inputElement:{type:Element,readOnly:!0}}}constructor(){super(),this._boundInputValueChanged=this._inputValueChanged.bind(this),this.__boundInputValueCommitted=this.__inputValueCommitted.bind(this)}ready(){super.ready(),this._toggleElement=this.querySelector(".toggle-button"),this._clearElement=this.querySelector(".clear-button"),this._clearElement&&this._clearElement.addEventListener("mousedown",e=>{e.preventDefault(),(this.inputElement._focusableElement||this.inputElement).focus()})}get focused(){return this.getRootNode().activeElement===this.inputElement}connectedCallback(){super.connectedCallback();this._setInputElement(this.querySelector("vaadin-text-field,iron-input,paper-input,.paper-input-input,.input")),this._revertInputValue(),this.inputElement.addEventListener("input",this._boundInputValueChanged),this.inputElement.addEventListener("change",this.__boundInputValueCommitted),this._preventInputBlur()}disconnectedCallback(){super.disconnectedCallback(),this.inputElement.removeEventListener("input",this._boundInputValueChanged),this.inputElement.removeEventListener("change",this.__boundInputValueCommitted),this._restoreInputBlur()}__inputValueCommitted(e){e.__fromClearButton&&this._clear()}get _propertyForValue(){return Object(B.b)(this.attrForValue)}get _inputElementValue(){return this.inputElement&&this.inputElement[this._propertyForValue]}set _inputElementValue(e){this.inputElement&&(this.inputElement[this._propertyForValue]=e)}}customElements.define(H.is,H)},234:function(e,t,i){"use strict";function s(e,t,i){return t in e?Object.defineProperty(e,t,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[t]=i,e}function r(e,t){var i=Object.keys(e);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);t&&(s=s.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),i.push.apply(i,s)}return i}function n(e){for(var t=1;t<arguments.length;t++){var i=null!=arguments[t]?arguments[t]:{};t%2?r(Object(i),!0).forEach((function(t){s(e,t,i[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(i)):r(Object(i)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(i,t))}))}return e}function o(e,t){if(null==e)return{};var i,s,r=function(e,t){if(null==e)return{};var i,s,r={},n=Object.keys(e);for(s=0;s<n.length;s++)i=n[s],t.indexOf(i)>=0||(r[i]=e[i]);return r}(e,t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);for(s=0;s<n.length;s++)i=n[s],t.indexOf(i)>=0||Object.prototype.propertyIsEnumerable.call(e,i)&&(r[i]=e[i])}return r}function a(e,t){return!0===e?[]:!1===e?[t.fail()]:e}i.d(t,"a",(function(){return c})),i.d(t,"b",(function(){return p})),i.d(t,"c",(function(){return m})),i.d(t,"d",(function(){return h})),i.d(t,"e",(function(){return f})),i.d(t,"f",(function(){return v})),i.d(t,"g",(function(){return y})),i.d(t,"h",(function(){return g})),i.d(t,"i",(function(){return b})),i.d(t,"j",(function(){return w})),i.d(t,"k",(function(){return x})),i.d(t,"l",(function(){return I}));class l{constructor(e){const{type:t,schema:i,coercer:s=(e=>e),validator:r=(()=>[]),refiner:n=(()=>[])}=e;this.type=t,this.schema=i,this.coercer=s,this.validator=r,this.refiner=n}}class c extends TypeError{constructor(e,t){const{path:i,value:s,type:r,branch:n}=e,a=o(e,["path","value","type","branch"]);super(`Expected a value of type \`${r}\`${i.length?` for \`${i.join(".")}\``:""} but received \`${JSON.stringify(s)}\`.`),this.value=s,Object.assign(this,a),this.type=r,this.path=i,this.branch=n,this.failures=function*(){yield e,yield*t},this.stack=(new Error).stack,this.__proto__=c.prototype}}function h(e,t){const i=u(e,t);if(i[0])throw i[0]}function d(e,t){const i=t.coercer(e);return h(i,t),i}function u(e,t,i=!1){i&&(e=t.coercer(e));const s=function*e(t,i,s=[],r=[]){const{type:o}=i,l={value:t,type:o,branch:r,path:s,fail:(e={})=>n({value:t,type:o,path:s,branch:[...r,t]},e),check(t,i,n,o){const a=void 0!==n?[...s,o]:s,l=void 0!==n?[...r,n]:r;return e(t,i,a,l)}},c=a(i.validator(t,l),l),[h]=c;h?(yield h,yield*c):yield*a(i.refiner(t,l),l)}(e,t),[r]=s;if(r){return[new c(r,s),void 0]}return[void 0,e]}function p(){return w("any",()=>!0)}function m(e){return new l({type:`Array<${e?e.type:"unknown"}>`,schema:e,coercer:t=>e&&Array.isArray(t)?t.map(t=>d(t,e)):t,*validator(t,i){if(Array.isArray(t)){if(e)for(const[s,r]of t.entries())yield*i.check(r,e,t,s)}else yield i.fail()}})}function f(){return w("boolean",e=>"boolean"==typeof e)}function _(){return w("never",()=>!1)}function v(){return w("number",e=>"number"==typeof e&&!isNaN(e))}function y(e){const t=e?Object.keys(e):[],i=_();return new l({type:e?`Object<{${t.join(",")}}>`:"Object",schema:e||null,coercer:e?E(e):e=>e,*validator(s,r){if("object"==typeof s&&null!=s){if(e){const n=new Set(Object.keys(s));for(const i of t){n.delete(i);const t=e[i],o=s[i];yield*r.check(o,t,s,i)}for(const e of n){const t=s[e];yield*r.check(t,i,s,e)}}}else yield r.fail()}})}function g(e){return new l({type:e.type+"?",schema:e.schema,validator:(t,i)=>void 0===t||i.check(t,e)})}function b(){return w("string",e=>"string"==typeof e)}function w(e,t){return new l({type:e,validator:t,schema:null})}function x(e){const t=Object.keys(e);return w(`Type<{${t.join(",")}}>`,(function*(i,s){if("object"==typeof i&&null!=i)for(const r of t){const t=e[r],n=i[r];yield*s.check(n,t,i,r)}else yield s.fail()}))}function I(e){return w(""+e.map(e=>e.type).join(" | "),(function*(t,i){for(const s of e){const[...e]=i.check(t,s);if(0===e.length)return}yield i.fail()}))}function E(e){const t=Object.keys(e);return i=>{if("object"!=typeof i||null==i)return i;const s={},r=new Set(Object.keys(i));for(const n of t){r.delete(n);const t=e[n],o=i[n];s[n]=d(o,t)}for(const e of r)s[e]=i[e];return s}}},236:function(e,t,i){"use strict";i.d(t,"a",(function(){return r}));i(5);var s=i(3);const r={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,t){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),t)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var i=this.domHost;this.scrollTarget=i&&i.$?i.$[e]:Object(s.a)(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(e){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=e)},set _scrollLeft(e){this.scrollTarget===this._doc?window.scrollTo(e,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=e)},scroll:function(e,t){var i;"object"==typeof e?(i=e.left,t=e.top):i=e,i=i||0,t=t||0,this.scrollTarget===this._doc?window.scrollTo(i,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=i,this.scrollTarget.scrollTop=t)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(e,t){var i=t===this._doc?window:t;e?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),i.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(i.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(e){this._shouldHaveListener=e,this._toggleScrollListener(e,this.scrollTarget)}}},240:function(e,t,i){"use strict";i(5);var s=i(6),r=i(3),n=i(4);Object(s.a)({_template:n.a`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var e=Object(r.a)(this).parentNode,t=Object(r.a)(this).getOwnerRoot();return this.for?Object(r.a)(t).querySelector("#"+this.for):e.nodeType==Node.DOCUMENT_FRAGMENT_NODE?t.host:e},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(e){"entry"===e?this.show():"exit"===e&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===Object(r.a)(this).textContent.trim()){for(var e=!0,t=Object(r.a)(this).getEffectiveChildNodes(),i=0;i<t.length;i++)if(""!==t[i].textContent.trim()){e=!1;break}if(e)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var e=this.offset;14!=this.marginTop&&14==this.offset&&(e=this.marginTop);var t,i,s=this.offsetParent.getBoundingClientRect(),r=this._target.getBoundingClientRect(),n=this.getBoundingClientRect(),o=(r.width-n.width)/2,a=(r.height-n.height)/2,l=r.left-s.left,c=r.top-s.top;switch(this.position){case"top":t=l+o,i=c-n.height-e;break;case"bottom":t=l+o,i=c+r.height+e;break;case"left":t=l-n.width-e,i=c+a;break;case"right":t=l+r.width+e,i=c+a}this.fitToVisibleBounds?(s.left+t+n.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,t)+"px",this.style.right="auto"),s.top+i+n.height>window.innerHeight?(this.style.bottom=s.height-c+e+"px",this.style.top="auto"):(this.style.top=Math.max(-s.top,i)+"px",this.style.bottom="auto")):(this.style.left=t+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(e){500!==e&&this.updateStyles({"--paper-tooltip-delay-in":e+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(e){if("entry"===e&&""!==this.animationEntry)return this.animationEntry;if("exit"===e&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[e]&&"string"==typeof this.animationConfig[e][0].name){if(this.animationConfig[e][0].timing&&this.animationConfig[e][0].timing.delay&&0!==this.animationConfig[e][0].timing.delay){var t=this.animationConfig[e][0].timing.delay;"entry"===e?this.updateStyles({"--paper-tooltip-delay-in":t+"ms"}):"exit"===e&&this.updateStyles({"--paper-tooltip-delay-out":t+"ms"})}return this.animationConfig[e][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},261:function(e,t,i){"use strict";i.d(t,"a",(function(){return s}));const s=i(0).c`
  ha-switch {
    padding: 16px 0;
  }
  .side-by-side {
    display: flex;
  }
  .side-by-side > * {
    flex: 1;
    padding-right: 4px;
  }
  .suffix {
    margin: 0 8px;
  }
`},262:function(e,t,i){"use strict";i(5),i(47);var s=i(44),r=i(70),n=i(6),o=i(3),a=i(4);Object(n.a)({_template:a.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[r.a,s.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=r.a.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=Object(o.a)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});i(149),i(148),i(150);var l=i(69),c=i(128);Object(n.a)({_template:a.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[c.a,l.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},270:function(e,t,i){"use strict";i(101),i(158),i(140),i(145);var s=i(0),r=i(11);function n(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function o(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function d(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,s=new Array(t);i<t;i++)s[i]=e[i];return s}!function(e,t,i,s){var r=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var r=t.placement;if(t.kind===s&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!a(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:i,finishers:s};var n=this.decorateConstructor(i,t);return s.push.apply(s,n.finishers),n.finishers=s,n},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var h=0;h<c.length;h++)this.addElementPlacement(c[h],t);i.push.apply(i,c)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[s])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return d(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?d(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:s,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var u=0;u<s.length;u++)r=s[u](r);var p=t((function(e){r.initializeInstanceElements(e,m.elements)}),i),m=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},s=0;s<e.length;s++){var r,n=e[s];if("method"===n.kind&&(r=t.find(i)))if(l(n.descriptor)||l(r.descriptor)){if(a(n)||a(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(a(n)){if(a(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}o(n,r)}else t.push(n)}return t}(p.d.map(n)),e);r.initializeClassElements(p.F,m.elements),r.runClassFinishers(p.F,m.finishers)}([Object(s.d)("hui-theme-select-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(s.h)()],key:"value",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"label",value:void 0},{kind:"field",decorators:[Object(s.h)({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"render",value:function(){return s.f`
      <paper-dropdown-menu
        .label=${this.label||`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`}
        dynamic-align
      >
        <paper-listbox
          slot="dropdown-content"
          .selected=${this.value}
          attr-for-selected="theme"
          @iron-select=${this._changed}
        >
          <paper-item theme="remove"
            >${this.hass.localize("ui.panel.lovelace.editor.card.generic.no_theme")}</paper-item
          >
          ${Object.keys(this.hass.themes.themes).sort().map(e=>s.f` <paper-item theme=${e}>${e}</paper-item> `)}
        </paper-listbox>
      </paper-dropdown-menu>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s.c`
      paper-dropdown-menu {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){this.hass&&""!==e.target.selected&&(this.value="remove"===e.target.selected?"":e.target.selected,Object(r.a)(this,"value-changed",{value:this.value}))}}]}}),s.a)},271:function(e,t){},321:function(e,t,i){"use strict";var s=i(4),r=i(32),n=i(219),o=(i(184),i(76),i(140),i(229),i(227));class a extends(Object(o.a)(r.a)){static get template(){return s.a`
      <style>
        paper-input > ha-icon-button {
          --mdc-icon-button-size: 24px;
          padding: 2px;
          color: var(--secondary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <vaadin-combo-box-light
        items="[[_items]]"
        item-value-path="[[itemValuePath]]"
        item-label-path="[[itemLabelPath]]"
        value="{{value}}"
        opened="{{opened}}"
        allow-custom-value="[[allowCustomValue]]"
        on-change="_fireChanged"
      >
        <paper-input
          autofocus="[[autofocus]]"
          label="[[label]]"
          class="input"
          value="[[value]]"
        >
          <ha-icon-button
            slot="suffix"
            class="clear-button"
            icon="hass:close"
            hidden$="[[!value]]"
            >Clear</ha-icon-button
          >
          <ha-icon-button
            slot="suffix"
            class="toggle-button"
            icon="[[_computeToggleIcon(opened)]]"
            hidden$="[[!items.length]]"
            >Toggle</ha-icon-button
          >
        </paper-input>
        <template>
          <style>
            paper-item {
              margin: -5px -10px;
              padding: 0;
            }
          </style>
          <paper-item>[[_computeItemLabel(item, itemLabelPath)]]</paper-item>
        </template>
      </vaadin-combo-box-light>
    `}static get properties(){return{allowCustomValue:Boolean,items:{type:Object,observer:"_itemsChanged"},_items:Object,itemLabelPath:String,itemValuePath:String,autofocus:Boolean,label:String,opened:{type:Boolean,value:!1,observer:"_openedChanged"},value:{type:String,notify:!0}}}_openedChanged(e){e||(this._items=this.items)}_itemsChanged(e){this.opened||(this._items=e)}_computeToggleIcon(e){return e?"hass:menu-up":"hass:menu-down"}_computeItemLabel(e,t){return t?e[t]:e}_fireChanged(e){e.stopPropagation(),this.fire("change")}}customElements.define("ha-combo-box",a);class l extends(Object(n.a)(r.a)){static get template(){return s.a`
      <ha-combo-box
        label="[[localize('ui.components.service-picker.service')]]"
        items="[[_services]]"
        value="{{value}}"
        allow-custom-value=""
      ></ha-combo-box>
    `}static get properties(){return{hass:{type:Object,observer:"_hassChanged"},_services:Array,value:{type:String,notify:!0}}}_hassChanged(e,t){if(!e)return void(this._services=[]);if(t&&e.services===t.services)return;const i=[];Object.keys(e.services).sort().forEach(t=>{const s=Object.keys(e.services[t]).sort();for(let e=0;e<s.length;e++)i.push(`${t}.${s[e]}`)}),this._services=i}}customElements.define("ha-service-picker",l)},332:function(e,t,i){"use strict";i.d(t,"a",(function(){return r})),i.d(t,"b",(function(){return m}));var s=i(234);const r=Object(s.g)({action:Object(s.i)(),navigation_path:Object(s.h)(Object(s.i)()),url_path:Object(s.h)(Object(s.i)()),service:Object(s.h)(Object(s.i)()),service_data:Object(s.h)(Object(s.g)())}),n=Object(s.g)({type:Object(s.i)(),name:Object(s.i)(),action_name:Object(s.h)(Object(s.i)()),tap_action:r,hold_action:Object(s.h)(r),double_tap_action:Object(s.h)(r)}),o=Object(s.g)({type:Object(s.i)(),view:Object(s.l)([Object(s.i)(),Object(s.f)()]),dashboard:Object(s.h)(Object(s.i)()),name:Object(s.h)(Object(s.i)()),icon:Object(s.h)(Object(s.i)()),hide_if_unavailable:Object(s.h)(Object(s.e)())}),a=Object(s.g)({type:Object(s.i)(),name:Object(s.i)(),service:Object(s.i)(),icon:Object(s.h)(Object(s.i)()),action_name:Object(s.h)(Object(s.i)()),service_data:Object(s.h)(Object(s.b)())}),l=Object(s.g)({type:Object(s.i)(),row:Object(s.b)(),conditions:Object(s.c)(Object(s.g)({entity:Object(s.i)(),state:Object(s.h)(Object(s.i)()),state_not:Object(s.h)(Object(s.i)())}))}),c=Object(s.g)({type:Object(s.i)(),style:Object(s.h)(Object(s.b)())}),h=Object(s.g)({type:Object(s.i)(),label:Object(s.h)(Object(s.i)())}),d=Object(s.g)({type:Object(s.i)(),url:Object(s.i)(),name:Object(s.h)(Object(s.i)()),icon:Object(s.h)(Object(s.i)())}),u=Object(s.g)({type:Object(s.i)(),entities:Object(s.c)(Object(s.l)([Object(s.g)({entity:Object(s.i)(),icon:Object(s.h)(Object(s.i)()),image:Object(s.h)(Object(s.i)()),name:Object(s.h)(Object(s.i)())}),Object(s.i)()]))}),p=Object(s.g)({type:Object(s.i)(),entity:Object(s.i)(),attribute:Object(s.i)(),prefix:Object(s.h)(Object(s.i)()),suffix:Object(s.h)(Object(s.i)()),name:Object(s.h)(Object(s.i)())}),m=Object(s.l)([Object(s.g)({entity:Object(s.i)(),name:Object(s.h)(Object(s.i)()),icon:Object(s.h)(Object(s.i)()),image:Object(s.h)(Object(s.i)()),secondary_info:Object(s.h)(Object(s.i)()),format:Object(s.h)(Object(s.i)()),state_color:Object(s.h)(Object(s.e)()),tap_action:Object(s.h)(r),hold_action:Object(s.h)(r),double_tap_action:Object(s.h)(r)}),Object(s.i)(),n,o,l,c,h,d,u,p,a])},355:function(e,t,i){"use strict";i(158),i(76),i(262),i(140),i(145);var s=i(0),r=i(11),n=i(112);i(240),i(113);function o(e){var t,i=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,s=new Array(t);i<t;i++)s[i]=e[i];return s}!function(e,t,i,s){var r=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var r=t.placement;if(t.kind===s&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!l(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:i,finishers:s};var n=this.decorateConstructor(i,t);return s.push.apply(s,n.finishers),n.finishers=s,n},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var h=0;h<c.length;h++)this.addElementPlacement(c[h],t);i.push.apply(i,c)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[s])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=d(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:s,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var n=0;n<s.length;n++)r=s[n](r);var p=t((function(e){r.initializeInstanceElements(e,m.elements)}),i),m=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},s=0;s<e.length;s++){var r,n=e[s];if("method"===n.kind&&(r=t.find(i)))if(c(n.descriptor)||c(r.descriptor)){if(l(n)||l(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(l(n)){if(l(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}a(n,r)}else t.push(n)}return t}(p.d.map(o)),e);r.initializeClassElements(p.F,m.elements),r.runClassFinishers(p.F,m.finishers)}([Object(s.d)("ha-help-tooltip")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(s.h)()],key:"label",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"position",value:()=>"top"},{kind:"method",key:"render",value:function(){return s.f`
      <ha-svg-icon .path=${n.hb}></ha-svg-icon>
      <paper-tooltip
        offset="4"
        .position=${this.position}
        .fitToVisibleBounds=${!0}
        >${this.label}</paper-tooltip
      >
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s.c`
      ha-svg-icon {
        --mdc-icon-size: var(--ha-help-tooltip-size, 14px);
        color: var(--ha-help-tooltip-color, var(--disabled-text-color));
      }
    `}}]}}),s.a);i(321);function p(e){var t,i=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,s=new Array(t);i<t;i++)s[i]=e[i];return s}!function(e,t,i,s){var r=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var r=t.placement;if(t.kind===s&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!f(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:i,finishers:s};var n=this.decorateConstructor(i,t);return s.push.apply(s,n.finishers),n.finishers=s,n},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var h=0;h<c.length;h++)this.addElementPlacement(c[h],t);i.push.apply(i,c)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[s])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=y(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:s,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var n=0;n<s.length;n++)r=s[n](r);var o=t((function(e){r.initializeInstanceElements(e,a.elements)}),i),a=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},s=0;s<e.length;s++){var r,n=e[s];if("method"===n.kind&&(r=t.find(i)))if(_(n.descriptor)||_(r.descriptor)){if(f(n)||f(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(f(n)){if(f(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}m(n,r)}else t.push(n)}return t}(o.d.map(p)),e);r.initializeClassElements(o.F,a.elements),r.runClassFinishers(o.F,a.finishers)}([Object(s.d)("hui-action-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(s.h)()],key:"config",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"label",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"actions",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"tooltipText",value:void 0},{kind:"field",decorators:[Object(s.h)()],key:"hass",value:void 0},{kind:"get",key:"_navigation_path",value:function(){return this.config.navigation_path||""}},{kind:"get",key:"_url_path",value:function(){return this.config.url_path||""}},{kind:"get",key:"_service",value:function(){return this.config.service||""}},{kind:"method",key:"render",value:function(){var e,t,i,r,n;return this.hass&&this.actions?s.f`
      <div class="dropdown">
        <paper-dropdown-menu
          .label=${this.label}
          .configValue=${"action"}
          @iron-select=${this._actionPicked}
        >
          <paper-listbox
            slot="dropdown-content"
            attr-for-selected="value"
            .selected=${null!==(e=null===(t=this.config)||void 0===t?void 0:t.action)&&void 0!==e?e:"default"}
          >
            <paper-item .value=${"default"}
              >${this.hass.localize("ui.panel.lovelace.editor.action-editor.actions.default_action")}</paper-item
            >
            ${this.actions.map(e=>s.f`
                <paper-item .value=${e}
                  >${this.hass.localize("ui.panel.lovelace.editor.action-editor.actions."+e)}</paper-item
                >
              `)}
          </paper-listbox>
        </paper-dropdown-menu>
        ${this.tooltipText?s.f`
              <ha-help-tooltip .label=${this.tooltipText}></ha-help-tooltip>
            `:""}
      </div>
      ${"navigate"===(null===(i=this.config)||void 0===i?void 0:i.action)?s.f`
            <paper-input
              label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.navigation_path")}
              .value=${this._navigation_path}
              .configValue=${"navigation_path"}
              @value-changed=${this._valueChanged}
            ></paper-input>
          `:""}
      ${"url"===(null===(r=this.config)||void 0===r?void 0:r.action)?s.f`
            <paper-input
              label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.url_path")}
              .value=${this._url_path}
              .configValue=${"url_path"}
              @value-changed=${this._valueChanged}
            ></paper-input>
          `:""}
      ${"call-service"===(null===(n=this.config)||void 0===n?void 0:n.action)?s.f`
            <ha-service-picker
              .hass=${this.hass}
              .value=${this._service}
              .configValue=${"service"}
              @value-changed=${this._valueChanged}
            ></ha-service-picker>
            <b>
              ${this.hass.localize("ui.panel.lovelace.editor.action-editor.editor_service_data")}
            </b>
          `:""}
    `:s.f``}},{kind:"method",key:"_actionPicked",value:function(e){var t;if(e.stopPropagation(),!this.hass)return;const i=e.detail.item.value;if((null===(t=this.config)||void 0===t?void 0:t.action)!==i){var s;if("default"===i)return Object(r.a)(this,"value-changed",{value:void 0}),void((null===(s=this.config)||void 0===s?void 0:s.action)&&this.shadowRoot.querySelector("paper-listbox").select(this.config.action));Object(r.a)(this,"value-changed",{value:{action:i}})}}},{kind:"method",key:"_valueChanged",value:function(e){if(e.stopPropagation(),!this.hass)return;const t=e.target,i=e.detail.value;this["_"+t.configValue]!==i&&t.configValue&&Object(r.a)(this,"value-changed",{value:{...this.config,[t.configValue]:i}})}},{kind:"get",static:!0,key:"styles",value:function(){return s.c`
      .dropdown {
        display: flex;
      }
    `}}]}}),s.a)},830:function(e,t,i){"use strict";i.r(t),i.d(t,"HuiPictureCardEditor",(function(){return _}));i(76);var s=i(0),r=i(234),n=i(11),o=(i(355),i(270),i(332)),a=i(261);function l(e){var t,i=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,s=new Array(t);i<t;i++)s[i]=e[i];return s}const f=Object(r.g)({type:Object(r.i)(),image:Object(r.h)(Object(r.i)()),tap_action:Object(r.h)(o.a),hold_action:Object(r.h)(o.a),theme:Object(r.h)(Object(r.i)())});let _=function(e,t,i,s){var r=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var r=t.placement;if(t.kind===s&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,r);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:i,finishers:s};var n=this.decorateConstructor(i,t);return s.push.apply(s,n.finishers),n.finishers=s,n},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var c=l.extras;if(c){for(var h=0;h<c.length;h++)this.addElementPlacement(c[h],t);i.push.apply(i,c)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[s])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=p(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:s,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var n=0;n<s.length;n++)r=s[n](r);var o=t((function(e){r.initializeInstanceElements(e,a.elements)}),i),a=r.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},s=0;s<e.length;s++){var r,n=e[s];if("method"===n.kind&&(r=t.find(i)))if(d(n.descriptor)||d(r.descriptor)){if(h(n)||h(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(h(n)){if(h(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}c(n,r)}else t.push(n)}return t}(o.d.map(l)),e);return r.initializeClassElements(o.F,a.elements),r.runClassFinishers(o.F,a.finishers)}([Object(s.d)("hui-picture-card-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(s.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(s.g)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){Object(r.d)(e,f),this._config=e}},{kind:"get",key:"_image",value:function(){return this._config.image||""}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"none"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"none"}}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return s.f``;const e=["navigate","url","call-service","none"];return s.f`
      <div class="card-config">
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.image")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
          .value="${this._image}"
          .configValue="${"image"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <div class="side-by-side">
          <hui-action-editor
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .hass=${this.hass}
            .config="${this._tap_action}"
            .actions="${e}"
            .configValue="${"tap_action"}"
            @value-changed="${this._valueChanged}"
          ></hui-action-editor>
          <hui-action-editor
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .hass=${this.hass}
            .config="${this._hold_action}"
            .actions="${e}"
            .configValue="${"hold_action"}"
            @value-changed="${this._valueChanged}"
          ></hui-action-editor>
          <hui-theme-select-editor
            .hass=${this.hass}
            .value="${this._theme}"
            .configValue="${"theme"}"
            @value-changed="${this._valueChanged}"
          ></hui-theme-select-editor>
        </div>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){if(!this._config||!this.hass)return;const t=e.target,i=e.detail.value;this["_"+t.configValue]!==t.value&&(t.configValue&&(!1===i||i?this._config={...this._config,[t.configValue]:i}:(this._config={...this._config},delete this._config[t.configValue])),Object(n.a)(this,"config-changed",{config:this._config}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.a}}]}}),s.a)}}]);
//# sourceMappingURL=chunk.5b551d8bb21ba5060574.js.map