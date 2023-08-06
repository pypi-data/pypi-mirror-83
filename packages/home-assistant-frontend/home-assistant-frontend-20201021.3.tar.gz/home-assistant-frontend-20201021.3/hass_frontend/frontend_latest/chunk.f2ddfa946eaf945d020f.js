(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6186,5540,1206,4077],{70518:(e,t,i)=>{"use strict";i.d(t,{X:()=>r});const r=(e,t,i)=>(void 0!==i&&(i=!!i),e.hasAttribute(t)?!!i||(e.removeAttribute(t),!1):!1!==i&&(e.setAttribute(t,""),!0))},83849:(e,t,i)=>{"use strict";i.d(t,{c:()=>n});var r=i(47181);const n=(e,t,i=!1)=>{i?history.replaceState(null,"",t):history.pushState(null,"",t),(0,r.B)(window,"location-changed",{replace:i})}},31206:(e,t,i)=>{"use strict";var r=i(15652),n=i(40208);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=o();if(r)for(var d=0;d<r.length;d++)n=r[d](n);var h=t((function(e){n.initializeInstanceElements(e,p.elements)}),i),p=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,p.elements),n.runClassFinishers(h.F,p.finishers)}([(0,r.Mo)("ha-circular-progress")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"active",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)()],key:"alt",value:()=>"Loading"},{kind:"field",decorators:[(0,r.Cb)()],key:"size",value:()=>"medium"},{kind:"set",key:"density",value:function(e){}},{kind:"get",key:"density",value:function(){switch(this.size){case"small":return-5;case"medium":return 0;case"large":return 5;default:return 0}}},{kind:"set",key:"indeterminate",value:function(e){}},{kind:"get",key:"indeterminate",value:function(){return this.active}}]}}),n.D)},34821:(e,t,i)=>{"use strict";i.d(t,{i:()=>g});i(21458);var r=i(60814),n=i(55317),o=i(15652),a=i(87744);i(10983);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const v=customElements.get("mwc-dialog"),g=(e,t)=>o.dy`
  <span class="header_title">${t}</span>
  <mwc-icon-button
    aria-label=${e.localize("ui.dialogs.generic.close")}
    dialogAction="close"
    class="header_button"
    dir=${(0,a.Zu)(e)}
  >
    <ha-svg-icon .path=${n.r5M}></ha-svg-icon>
  </mwc-icon-button>
`;!function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,p.elements)}),i),p=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(h(o.descriptor)||h(n.descriptor)){if(d(o)||d(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(d(o)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(l)),e);n.initializeClassElements(a.F,p.elements),n.runClassFinishers(a.F,p.finishers)}([(0,o.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return o.dy`<slot name="heading">
      ${m(y(i.prototype),"renderHeading",this).call(this)}
    </slot>`}},{kind:"get",static:!0,key:"styles",value:function(){return[r.o,o.iv`
        .mdc-dialog {
          --mdc-dialog-scroll-divider-color: var(--divider-color);
          z-index: var(--dialog-z-index, 7);
        }
        .mdc-dialog__actions {
          justify-content: var(--justify-action-buttons, flex-end);
          padding-bottom: max(env(safe-area-inset-bottom), 8px);
        }
        .mdc-dialog__container {
          align-items: var(--vertial-align-dialog, center);
        }
        .mdc-dialog__title::before {
          display: block;
          height: 20px;
        }
        .mdc-dialog .mdc-dialog__content {
          position: var(--dialog-content-position, relative);
          padding: var(--dialog-content-padding, 20px 24px);
        }
        :host([hideactions]) .mdc-dialog .mdc-dialog__content {
          padding-bottom: max(
            var(--dialog-content-padding, 20px),
            env(safe-area-inset-bottom)
          );
        }
        .mdc-dialog .mdc-dialog__surface {
          position: var(--dialog-surface-position, relative);
          top: var(--dialog-surface-top);
          min-height: var(--mdc-dialog-min-height, auto);
        }
        :host([flexContent]) .mdc-dialog .mdc-dialog__content {
          display: flex;
          flex-direction: column;
        }
        .header_button {
          position: absolute;
          right: 16px;
          top: 10px;
          text-decoration: none;
          color: inherit;
        }
        .header_title {
          margin-right: 40px;
        }
        [dir="rtl"].header_button {
          right: auto;
          left: 16px;
        }
        [dir="rtl"].header_title {
          margin-left: 40px;
          margin-right: 0px;
        }
      `]}}]}}),v)},90806:(e,t,i)=>{"use strict";var r=i(23049),n=i(15652);function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=h(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function a(e){var t,i=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=o();if(r)for(var d=0;d<r.length;d++)n=r[d](n);var h=t((function(e){n.initializeInstanceElements(e,p.elements)}),i),p=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(h.d.map(a)),e);n.initializeClassElements(h.F,p.elements),n.runClassFinishers(h.F,p.finishers)}([(0,n.Mo)("ha-header-bar")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return n.dy`<header class="mdc-top-app-bar">
      <div class="mdc-top-app-bar__row">
        <section
          class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start"
          id="navigation"
        >
          <slot name="navigationIcon"></slot>
          <span class="mdc-top-app-bar__title">
            <slot name="title"></slot>
          </span>
        </section>
        <section
          class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end"
          id="actions"
          role="toolbar"
        >
          <slot name="actionItems"></slot>
        </section>
      </div>
    </header>`}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,n.$m)(r.Z),n.iv`
        .mdc-top-app-bar {
          position: static;
          color: var(--mdc-theme-on-primary, #fff);
        }
      `]}}]}}),n.oi)},92390:(e,t,i)=>{"use strict";i(31206);var r=i(50856),n=i(28426),o=i(1265),a=i(78956),s=i(44583),l=i(72986),c=i(33367),d=i(21683),h=i(49684);i(10983);let p=null;class u extends((0,c.P)([l.z],n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip ul {
          margin: 0 3px;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip li::first-line {
          line-height: 0;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartTooltip .beforeBody {
          text-align: center;
          font-weight: 300;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        ha-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <template is="dom-if" if="[[tooltip.beforeBody]]">
            <div class="beforeBody">[[tooltip.beforeBody]]</div>
          </template>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=()=>{this._debouncer=a.d.debounce(this._debouncer,d.Wc.after(10),(()=>{this._isAttached&&this.resizeChart()}))},"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver((e=>{e.forEach((()=>{this._resizeListener()}))})),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===p&&(p=Promise.all([i.e(9680),i.e(7770)]).then(i.bind(i,79109))),p.then((e=>{this.ChartClass=e.default,this.onPropsChange()}))}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(e){if(0===e.opacity)return void this.set(["tooltip","opacity"],0);e.yAlign?this.set(["tooltip","yAlign"],e.yAlign):this.set(["tooltip","yAlign"],"no-transform");const t=e.title&&e.title[0]||"";this.set(["tooltip","title"],t),e.beforeBody&&this.set(["tooltip","beforeBody"],e.beforeBody.join("\n"));const i=e.body.map((e=>e.lines));e.body&&this.set(["tooltip","lines"],i.map(((t,i)=>{const r=e.labelColors[i];return{color:r.borderColor,bgColor:r.backgroundColor,text:t.join("\n")}})));const r=this.$.chartTarget.clientWidth;let n=e.caretX;const o=this._chart.canvas.offsetTop+e.caretY;e.caretX+100>r?n=r-100:e.caretX<100&&(n=100),n+=this._chart.canvas.offsetLeft,this.tooltip={...this.tooltip,opacity:1,left:n+"px",top:o+"px"}}_legendClick(e){(e=e||window.event).stopPropagation();let t=e.target||e.srcElement;for(;"LI"!==t.nodeName;)t=t.parentElement;const i=e.model.itemsIndex,r=this._chart.getDatasetMeta(i);r.hidden=null===r.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const e=this._chart,t=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map(((i,r)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:t&&r<this.metas.length?this.metas[r].hidden:!e.isDatasetVisible(r)}))));let i=!1;if(t)for(let r=0;r<this.metas.length;r++){const t=e.getDatasetMeta(r);!!t.hidden!=!!this.metas[r].hidden&&(i=!0),t.hidden=!!this.metas[r].hidden||null}i&&e.update(),this.unit=this.data.unit}_formatTickValue(e,t,i){if(0===i.length)return e;const r=new Date(i[t].value);return(0,h.m)(r,this.hass.language)}drawChart(){const e=this.data.data,t=this.$.chartCanvas;if(e.datasets&&e.datasets.length||this._chart){if("timeline"!==this.data.type&&e.datasets.length>0){const t=e.datasets.length,i=this.constructor.getColorList(t);for(let r=0;r<t;r++)e.datasets[r].borderColor=i[r].rgbString(),e.datasets[r].backgroundColor=i[r].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=e,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=e.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!e.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let r={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};r=Chart.helpers.merge(r,this.data.options),r.scales.xAxes[0].ticks.callback=this._formatTickValue.bind(this),"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(r.elements.colorFunction=this._colorFunc),1===e.datasets.length&&(r.scales.yAxes[0].ticks?r.scales.yAxes[0].ticks.display=!1:r.scales.yAxes[0].ticks={display:!1},r.scales.yAxes[0].gridLines?r.scales.yAxes[0].gridLines.display=!1:r.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const n={type:this.data.type,data:this.data.data,options:r,plugins:i};this._chart=new this.ChartClass(t,n),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const e=this.$.chartTarget,t=this.data.data;if(0===t.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,r=this._chart.chartArea.bottom,n=this._chart.canvas.clientHeight;if(r>0&&(this._axisHeight=n-r+i),!this._axisHeight)return e.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*t.datasets.length+this._axisHeight+"px";e.style.height!==i&&(e.style.height=i),this._chart.resize()}}static getColorList(e){let t=!1;e>10&&(t=!0,e=Math.ceil(e/2));const i=360/e,r=[];for(let n=0;n<e;n++)r[n]=Color().hsl(i*n,80,38),t&&(r[n+e]=Color().hsl(i*n,80,62));return r}static getColorGenerator(e,t){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function r(e){return Color("#"+i[e%i.length])}const n={};let o=0;return t>0&&(o=t),e&&Object.keys(e).forEach((t=>{const i=e[t];isFinite(i)?n[t.toLowerCase()]=r(i):n[t.toLowerCase()]=Color(e[t])})),function(e,t){let i;const a=t[3];if(null===a)return Color().hsl(0,40,38);if(void 0===a)return Color().hsl(120,40,38);const s=a.toLowerCase();return void 0===i&&(i=n[s]),void 0===i&&(i=r(o),o++,n[s]=i),i}}}customElements.define("ha-chart-base",u);class f extends((0,o.Z)(n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        hass="[[hass]]"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}ready(){super.ready(),this.addEventListener("transitionend",(()=>{this.style.overflow="auto"}))}dataChanged(){this.drawChart()}_onRenderedChanged(e){e&&this.animateHeight()}animateHeight(){requestAnimationFrame((()=>requestAnimationFrame((()=>{this.style.height=this.$.chart.scrollHeight+"px"}))))}drawChart(){if(!this._isAttached)return;const e=this.unit,t=this.data,i=[];let r;if(0===t.length)return;function n(e){const t=parseFloat(e);return isFinite(t)?t:null}r=this.endTime||new Date(Math.max.apply(null,t.map((e=>new Date(e.states[e.states.length-1].last_changed))))),r>new Date&&(r=new Date);const o=this.names||{};t.forEach((t=>{const a=t.domain,s=o[t.entity_id]||t.name;let l;const c=[];function d(e,t){t&&(e>r||(c.forEach(((i,r)=>{i.data.push({x:e,y:t[r]})})),l=t))}function h(t,i,r){let n=!1,o=!1;r&&(n="origin"),i&&(o="before"),c.push({label:t,fill:n,steppedLine:o,pointRadius:0,data:[],unitText:e})}if("thermostat"===a||"climate"===a||"water_heater"===a){const e=t.states.some((e=>e.attributes&&e.attributes.hvac_action)),i="climate"===a&&e?e=>"heating"===e.attributes.hvac_action:e=>"heat"===e.state,r="climate"===a&&e?e=>"cooling"===e.attributes.hvac_action:e=>"cool"===e.state,o=t.states.some(i),l=t.states.some(r),c=t.states.some((e=>e.attributes&&e.attributes.target_temp_high!==e.attributes.target_temp_low));h(""+this.hass.localize("ui.card.climate.current_temperature","name",s),!0),o&&h(""+this.hass.localize("ui.card.climate.heating","name",s),!0,!0),l&&h(""+this.hass.localize("ui.card.climate.cooling","name",s),!0,!0),c?(h(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",s,"mode",this.hass.localize("ui.card.climate.high")),!0),h(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",s,"mode",this.hass.localize("ui.card.climate.low")),!0)):h(""+this.hass.localize("ui.card.climate.target_temperature_entity","name",s),!0),t.states.forEach((e=>{if(!e.attributes)return;const t=n(e.attributes.current_temperature),a=[t];if(o&&a.push(i(e)?t:null),l&&a.push(r(e)?t:null),c){const t=n(e.attributes.target_temp_high),i=n(e.attributes.target_temp_low);a.push(t,i),d(new Date(e.last_changed),a)}else{const t=n(e.attributes.temperature);a.push(t),d(new Date(e.last_changed),a)}}))}else if("humidifier"===a)h(""+this.hass.localize("ui.card.humidifier.target_humidity_entity","name",s),!0),h(""+this.hass.localize("ui.card.humidifier.on_entity","name",s),!0,!0),t.states.forEach((e=>{if(!e.attributes)return;const t=n(e.attributes.humidity),i=[t];i.push("on"===e.state?t:null),d(new Date(e.last_changed),i)}));else{h(s,"sensor"===a);let e=null,i=null,r=null;t.states.forEach((t=>{const o=n(t.state),a=new Date(t.last_changed);if(null!==o&&null!==r){const t=a.getTime(),n=r.getTime(),s=i.getTime();d(r,[(n-s)/(t-s)*(o-e)+e]),d(new Date(n+1),[null]),d(a,[o]),i=a,e=o,r=null}else null!==o&&null===r?(d(a,[o]),i=a,e=o):null===o&&null===r&&null!==e&&(r=a)}))}d(r,l),Array.prototype.push.apply(i,c)}));const a={type:"line",unit:e,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(e,t)=>{const i=e[0],r=t.datasets[i.datasetIndex].data[i.index].x;return(0,s.E)(r,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=a}}customElements.define("state-history-chart-line",f);var m=i(87744);class y extends((0,o.Z)(n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        hass="[[hass]]"
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let e=this.data;if(!this._isAttached)return;e||(e=[]);const t=new Date(e.reduce(((e,t)=>Math.min(e,new Date(t.data[0].last_changed))),new Date));let i=this.endTime||new Date(e.reduce(((e,t)=>Math.max(e,new Date(t.data[t.data.length-1].last_changed))),t));i>new Date&&(i=new Date);const r=[],n=[],o=this.names||{};e.forEach((e=>{let a,s=null,l=null,c=t;const d=o[e.entity_id]||e.name,h=[];e.data.forEach((e=>{let t=e.state;void 0!==t&&""!==t||(t=null),new Date(e.last_changed)>i||(null!==s&&t!==s?(a=new Date(e.last_changed),h.push([c,a,l,s]),s=t,l=e.state_localize,c=a):null===s&&(s=t,l=e.state_localize,c=new Date(e.last_changed)))})),null!==s&&h.push([c,i,l,s]),n.push({data:h,entity_id:e.entity_id}),r.push(d)}));const a={type:"timeline",options:{tooltips:{callbacks:{label:(e,t)=>{const i=t.datasets[e.datasetIndex].data[e.index],r=(0,s.E)(i[0],this.hass.language),n=(0,s.E)(i[1],this.hass.language);return[i[2],r,n]},beforeBody:(e,t)=>{if(!this.hass.userData||!this.hass.userData.showAdvanced||!e[0])return"";return t.datasets[e[0].datasetIndex].entity_id||""}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:e=>{e.maxWidth=.18*e.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:r,datasets:n},colors:{staticColors:{on:1,off:0,home:1,not_home:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=a}_computeRTL(e){return(0,m.HE)(e)}}customElements.define("state-history-chart-timeline",y);class v extends((0,o.Z)(n.H3)){static get template(){return r.d`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(e,t){return!t&&e&&1===e.length}_computeIsEmpty(e,t){const i=!t||!t.timeline||!t.line||0===t.timeline.length&&0===t.line.length;return!e&&i}_computeIsLoading(e){return e&&!this.historyData}_computeEndTime(e,t){return t?new Date:e}}customElements.define("state-history-charts",v)},58763:(e,t,i)=>{"use strict";i.d(t,{vq:()=>l,_J:()=>c,Nu:()=>h});var r=i(29171),n=i(22311),o=i(91741);const a=["climate","humidifier","water_heater"],s=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],l=(e,t,i,r,n=!1,o,a=!0)=>{let s="history/period";return i&&(s+="/"+i.toISOString()),s+="?filter_entity_id="+t,r&&(s+="&end_time="+r.toISOString()),n&&(s+="&skip_initial_state"),void 0!==o&&(s+="&significant_changes_only="+Number(o)),a&&(s+="&minimal_response"),e.callApi("GET",s)},c=(e,t,i,r)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${i.toISOString()}&minimal_response${r?"&filter_entity_id="+r:""}`),d=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||s.every((i=>e.attributes[i]===t.attributes[i]))),h=(e,t,i,l)=>{const c={},h=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const a=t.find((e=>e.attributes&&"unit_of_measurement"in e.attributes));let s;a?s=a.attributes.unit_of_measurement:"climate"===(0,n.N)(t[0])||"water_heater"===(0,n.N)(t[0])?s=e.config.unit_system.temperature:"humidifier"===(0,n.N)(t[0])&&(s="%"),s?s in c?c[s].push(t):c[s]=[t]:h.push(((e,t,i)=>{const n=[],a=i.length-1;for(const o of i)n.length>0&&o.state===n[n.length-1].state||(o.entity_id||(o.attributes=i[a].attributes,o.entity_id=i[a].entity_id),n.push({state_localize:(0,r.D)(e,o,t),state:o.state,last_changed:o.last_changed}));return{name:(0,o.C)(i[0]),entity_id:i[0].entity_id,data:n}})(i,l,t))}));return{line:Object.keys(c).map((e=>((e,t)=>{const i=[];for(const r of t){const e=r[r.length-1],t=(0,n.N)(e),l=[];for(const i of r){let e;if(a.includes(t)){e={state:i.state,last_changed:i.last_updated,attributes:{}};for(const t of s)t in i.attributes&&(e.attributes[t]=i.attributes[t])}else e=i;l.length>1&&d(e,l[l.length-1])&&d(e,l[l.length-2])||l.push(e)}i.push({domain:t,name:(0,o.C)(e),entity_id:e.entity_id,states:l})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:i}})(e,c[e]))),timeline:h}}},65430:(e,t,i)=>{"use strict";i(25856);var r=i(87744),n=i(46628),o=i(7778),a=i(15652);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=y(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function y(e){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let v=function(e,t,i,r){var n=s();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,p.elements)}),i),p=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(h(o.descriptor)||h(n.descriptor)){if(d(o)||d(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(d(o)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}c(o,n)}else t.push(o)}return t}(a.d.map(l)),e);return n.initializeClassElements(a.F,p.elements),n.runClassFinishers(a.F,p.finishers)}(null,(function(e,t){class i extends t{constructor(){super(),e(this),this.addEventListener("ll-rebuild",(()=>{this._cleanup(),this.config&&this._createCard(this.config)}))}}return{F:i,d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"config",value:void 0},{kind:"field",key:"_element",value:void 0},{kind:"get",key:"_error",value:function(){var e;return"HUI-ERROR-CARD"===(null===(e=this._element)||void 0===e?void 0:e.tagName)}},{kind:"method",key:"update",value:function(e){if(m(y(i.prototype),"update",this).call(this,e),e.has("config")){const i=e.get("config");if(!this.config)return void this._cleanup();if(!this.config.type)return void this._createCard((0,o.N2)("No card type found",this.config));if(!this._element)return void this._createCard(this.config);if(!this._error&&i&&this.config.type===i.type)try{this._element.setConfig(this.config)}catch(t){this._createCard((0,o.N2)(t.message,this.config))}else this._createCard(this.config)}if(e.has("hass")){const t=e.get("hass");t&&t.language===this.hass.language||(this.style.direction=(0,r.HE)(this.hass)?"rtl":"ltr"),this._element&&(this._element.hass=this.hass)}}},{kind:"method",key:"_createCard",value:function(e){this._cleanup(),this._element=(0,n.Z6)(e),this.hass&&(this._element.hass=this.hass),this.appendChild(this._element)}},{kind:"method",key:"_cleanup",value:function(){this._element&&(this.removeChild(this._element),this._element=void 0)}}]}}),a.f4);customElements.define("hui-card-preview",v)},90705:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HuiDialogEditCard:()=>E});var r=i(55317),n=i(60461),o=i.n(n),a=i(15652),s=i(47181),l=i(87744),c=(i(31206),i(34821),i(90806),i(26765)),d=i(11654),h=i(98573),p=i(54324),u=i(9893),f=i(27322);i(52231),i(65430);function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!g(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=k(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function y(e){var t,i=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let E=function(e,t,i,r){var n=m();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(b(o.descriptor)||b(n.descriptor)){if(g(o)||g(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(g(o)){if(g(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}v(o,n)}else t.push(o)}return t}(a.d.map(y)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,a.Mo)("hui-dialog-edit-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_cardConfig",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_viewConfig",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_saving",value:()=>!1},{kind:"field",decorators:[(0,a.sz)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_guiModeAvailable",value:()=>!0},{kind:"field",decorators:[(0,a.IO)("hui-element-editor")],key:"_cardEditorEl",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_GUImode",value:()=>!0},{kind:"field",decorators:[(0,a.sz)()],key:"_documentationURL",value:void 0},{kind:"field",decorators:[(0,a.sz)()],key:"_dirty",value:()=>!1},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._GUImode=!0,this._guiModeAvailable=!0;const[t,i]=e.path;this._viewConfig=e.lovelaceConfig.views[t],this._cardConfig=void 0!==i?this._viewConfig.cards[i]:e.cardConfig,this._cardConfig&&!Object.isFrozen(this._cardConfig)&&(this._cardConfig=o()(this._cardConfig)),e.cardConfig&&(this._dirty=!0)}},{kind:"method",key:"closeDialog",value:function(){return this._dirty?(this._confirmCancel(),!1):(this._params=void 0,this._cardConfig=void 0,this._error=void 0,this._documentationURL=void 0,this._dirty=!1,(0,s.B)(this,"dialog-closed",{dialog:this.localName}),!0)}},{kind:"method",key:"updated",value:function(e){if(!this._cardConfig||void 0!==this._documentationURL||!e.has("_cardConfig"))return;const t=e.get("_cardConfig");var i,r,n;(null==t?void 0:t.type)!==this._cardConfig.type&&(this._documentationURL=(i=this.hass,(r=this._cardConfig.type).startsWith(u.Qo)?null===(n=(0,u.cs)(r))||void 0===n?void 0:n.documentationURL:`${(0,f.R)(i,"/lovelace/")}${r}`))}},{kind:"method",key:"render",value:function(){if(!this._params)return a.dy``;let e;return e=this._cardConfig&&this._cardConfig.type?this.hass.localize("ui.panel.lovelace.editor.edit_card.typed_header","type",this.hass.localize(`ui.panel.lovelace.editor.card.${this._cardConfig.type}.name`)):this._cardConfig?this.hass.localize("ui.panel.lovelace.editor.edit_card.header"):this._viewConfig.title?this.hass.localize("ui.panel.lovelace.editor.edit_card.pick_card_view_title","name",`"${this._viewConfig.title}"`):this.hass.localize("ui.panel.lovelace.editor.edit_card.pick_card"),a.dy`
      <ha-dialog
        open
        scrimClickAction
        @keydown=${this._ignoreKeydown}
        @closed=${this._cancel}
        @opened=${this._opened}
        .heading=${!0}
      >
        <div slot="heading">
          <ha-header-bar>
            <div slot="title">${e}</div>
            ${void 0!==this._documentationURL?a.dy`
                  <a
                    slot="actionItems"
                    class="header_button"
                    href=${this._documentationURL}
                    title=${this.hass.localize("ui.panel.lovelace.menu.help")}
                    target="_blank"
                    rel="noreferrer"
                    dir=${(0,l.Zu)(this.hass)}
                  >
                    <mwc-icon-button>
                      <ha-svg-icon .path=${r.Xc_}></ha-svg-icon>
                    </mwc-icon-button>
                  </a>
                `:""}
          </ha-header-bar>
        </div>
        <div class="content">
          <div class="element-editor">
            <hui-element-editor
              .hass=${this.hass}
              .lovelace=${this._params.lovelaceConfig}
              .value=${this._cardConfig}
              @config-changed=${this._handleConfigChanged}
              @GUImode-changed=${this._handleGUIModeChanged}
              @editor-save=${this._save}
            ></hui-element-editor>
          </div>
          <div class="element-preview">
            <hui-card-preview
              .hass=${this.hass}
              .config=${this._cardConfig}
              class=${this._error?"blur":""}
            ></hui-card-preview>
            ${this._error?a.dy`
                  <ha-circular-progress
                    active
                    alt="Can't update card"
                  ></ha-circular-progress>
                `:""}
          </div>
        </div>
        ${void 0!==this._cardConfig?a.dy`
              <mwc-button
                slot="secondaryAction"
                @click=${this._toggleMode}
                .disabled=${!this._guiModeAvailable}
                class="gui-mode-button"
              >
                ${this.hass.localize(!this._cardEditorEl||this._GUImode?"ui.panel.lovelace.editor.edit_card.show_code_editor":"ui.panel.lovelace.editor.edit_card.show_visual_editor")}
              </mwc-button>
            `:""}
        <div slot="primaryAction" @click=${this._save}>
          <mwc-button @click=${this._cancel}>
            ${this.hass.localize("ui.common.cancel")}
          </mwc-button>
          ${void 0!==this._cardConfig?a.dy`
                <mwc-button
                  ?disabled=${!this._canSave||this._saving}
                  @click=${this._save}
                >
                  ${this._saving?a.dy`
                        <ha-circular-progress
                          active
                          title="Saving"
                          size="small"
                        ></ha-circular-progress>
                      `:this._dirty?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.close")}
                </mwc-button>
              `:""}
        </div>
      </ha-dialog>
    `}},{kind:"method",key:"_ignoreKeydown",value:function(e){e.stopPropagation()}},{kind:"method",key:"_handleConfigChanged",value:function(e){this._cardConfig=o()(e.detail.config),this._error=e.detail.error,this._guiModeAvailable=e.detail.guiModeAvailable,this._dirty=!0}},{kind:"method",key:"_handleGUIModeChanged",value:function(e){e.stopPropagation(),this._GUImode=e.detail.guiMode,this._guiModeAvailable=e.detail.guiModeAvailable}},{kind:"method",key:"_toggleMode",value:function(){var e;null===(e=this._cardEditorEl)||void 0===e||e.toggleMode()}},{kind:"method",key:"_opened",value:function(){var e;null===(e=this._cardEditorEl)||void 0===e||e.refreshYamlEditor()}},{kind:"get",key:"_canSave",value:function(){return!this._saving&&(void 0!==this._cardConfig&&(!this._cardEditorEl||!this._cardEditorEl.hasError))}},{kind:"method",key:"_confirmCancel",value:async function(){await new Promise((e=>setTimeout(e,0)));await(0,c.g7)(this,{title:this.hass.localize("ui.panel.lovelace.editor.edit_card.unsaved_changes"),text:this.hass.localize("ui.panel.lovelace.editor.edit_card.confirm_cancel"),dismissText:this.hass.localize("ui.common.no"),confirmText:this.hass.localize("ui.common.yes")})&&this._cancel()}},{kind:"method",key:"_cancel",value:function(e){e&&e.stopPropagation(),this._dirty=!1,this.closeDialog()}},{kind:"method",key:"_save",value:async function(){this._canSave&&(this._dirty?(this._saving=!0,await this._params.saveConfig(1===this._params.path.length?(0,p.Z0)(this._params.lovelaceConfig,this._params.path,this._cardConfig):(0,p.LG)(this._params.lovelaceConfig,this._params.path,this._cardConfig)),this._saving=!1,this._dirty=!1,(0,h.f)(this,this.hass),this.closeDialog()):this.closeDialog())}},{kind:"get",static:!0,key:"styles",value:function(){return[d.yu,a.iv`
        :host {
          --code-mirror-max-height: calc(100vh - 176px);
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          /* overrule the ha-style-dialog max-height on small screens */
          ha-dialog {
            --mdc-dialog-max-height: 100%;
            height: 100%;
          }
        }

        @media all and (min-width: 850px) {
          ha-dialog {
            --mdc-dialog-min-width: 845px;
            --mdc-dialog-max-height: calc(100% - 72px);
          }
        }

        ha-dialog {
          --mdc-dialog-max-width: 845px;
          --dialog-z-index: 5;
        }

        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }

        .center {
          margin-left: auto;
          margin-right: auto;
        }

        .content {
          display: flex;
          flex-direction: column;
          margin: 0 -10px;
        }
        .content hui-card-preview {
          margin: 4px auto;
          max-width: 390px;
        }
        .content .element-editor {
          margin: 0 10px;
        }

        @media (min-width: 1200px) {
          ha-dialog {
            --mdc-dialog-max-width: calc(100% - 32px);
            --mdc-dialog-min-width: 1000px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100% - 72px);
          }

          .content {
            flex-direction: row;
          }
          .content > * {
            flex-basis: 0;
            flex-grow: 1;
            flex-shrink: 1;
            min-width: 0;
          }
          .content hui-card-preview {
            padding: 8px 10px;
            margin: auto 0px;
            max-width: 500px;
          }
        }
        .hidden {
          display: none;
        }
        .element-editor {
          margin-bottom: 8px;
        }
        .blur {
          filter: blur(2px) grayscale(100%);
        }
        .element-preview {
          position: relative;
        }
        .element-preview ha-circular-progress {
          top: 50%;
          left: 50%;
          position: absolute;
          z-index: 10;
        }
        hui-card-preview {
          padding-top: 8px;
          margin-bottom: 4px;
          display: block;
          width: 100%;
          box-sizing: border-box;
        }
        .gui-mode-button {
          margin-right: auto;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .header_button {
          color: inherit;
          text-decoration: none;
        }
      `]}}]}}),a.oi)},27322:(e,t,i)=>{"use strict";i.d(t,{R:()=>r});const r=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},98573:(e,t,i)=>{"use strict";i.d(t,{f:()=>n});var r=i(81796);const n=(e,t)=>(0,r.C)(e,{message:t.localize("ui.common.successfully_saved")})}}]);
//# sourceMappingURL=chunk.f2ddfa946eaf945d020f.js.map