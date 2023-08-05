/*! For license information please see chunk.54168543e4b2d36aa064.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7820],{21157:(e,t,n)=>{"use strict";n(43437);const i=n(50856).d`
/* Most common used flex styles*/
<dom-module id="iron-flex">
  <template>
    <style>
      .layout.horizontal,
      .layout.vertical {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.inline {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      }

      .layout.horizontal {
        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      }

      .layout.vertical {
        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      }

      .layout.wrap {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      }

      .layout.no-wrap {
        -ms-flex-wrap: nowrap;
        -webkit-flex-wrap: nowrap;
        flex-wrap: nowrap;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .flex {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-auto {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      }

      .flex-none {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      }
    </style>
  </template>
</dom-module>
/* Basic flexbox reverse styles */
<dom-module id="iron-flex-reverse">
  <template>
    <style>
      .layout.horizontal-reverse,
      .layout.vertical-reverse {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      }

      .layout.horizontal-reverse {
        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      }

      .layout.vertical-reverse {
        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      }

      .layout.wrap-reverse {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      }
    </style>
  </template>
</dom-module>
/* Flexbox alignment */
<dom-module id="iron-flex-alignment">
  <template>
    <style>
      /**
       * Alignment in cross axis.
       */
      .layout.start {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      }

      .layout.center,
      .layout.center-center {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      }

      .layout.end {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      }

      .layout.baseline {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      }

      /**
       * Alignment in main axis.
       */
      .layout.start-justified {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      }

      .layout.center-justified,
      .layout.center-center {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      }

      .layout.end-justified {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      }

      .layout.around-justified {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      }

      .layout.justified {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      }

      /**
       * Self alignment.
       */
      .self-start {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      }

      .self-center {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      }

      .self-end {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      }

      .self-stretch {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      }

      .self-baseline {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      }

      /**
       * multi-line alignment in main axis.
       */
      .layout.start-aligned {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      }

      .layout.end-aligned {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      }

      .layout.center-aligned {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      }

      .layout.between-aligned {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      }

      .layout.around-aligned {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      }
    </style>
  </template>
</dom-module>
/* Non-flexbox positioning helper styles */
<dom-module id="iron-flex-factors">
  <template>
    <style>
      .flex,
      .flex-1 {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      }

      .flex-2 {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      }

      .flex-3 {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      }

      .flex-4 {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      }

      .flex-5 {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      }

      .flex-6 {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      }

      .flex-7 {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      }

      .flex-8 {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      }

      .flex-9 {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      }

      .flex-10 {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      }

      .flex-11 {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      }

      .flex-12 {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      }
    </style>
  </template>
</dom-module>
<dom-module id="iron-positioning">
  <template>
    <style>
      .block {
        display: block;
      }

      [hidden] {
        display: none !important;
      }

      .invisible {
        visibility: hidden !important;
      }

      .relative {
        position: relative;
      }

      .fit {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      }

      body.fullbleed {
        margin: 0;
        height: 100vh;
      }

      .scroll {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      }

      /* fixed position */
      .fixed-bottom,
      .fixed-left,
      .fixed-right,
      .fixed-top {
        position: fixed;
      }

      .fixed-top {
        top: 0;
        left: 0;
        right: 0;
      }

      .fixed-right {
        top: 0;
        right: 0;
        bottom: 0;
      }

      .fixed-bottom {
        right: 0;
        bottom: 0;
        left: 0;
      }

      .fixed-left {
        top: 0;
        bottom: 0;
        left: 0;
      }
    </style>
  </template>
</dom-module>
`;i.setAttribute("style","display: none;"),document.head.appendChild(i.content)},91107:(e,t,n)=>{"use strict";n.d(t,{Ud:()=>c});const i=Symbol("Comlink.proxy"),l=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.thrown"),r=e=>"object"==typeof e&&null!==e||"function"==typeof e,o=new Map([["proxy",{canHandle:e=>r(e)&&e[i],serialize(e){const{port1:t,port2:n}=new MessageChannel;return function e(t,n=self){n.addEventListener("message",(function l(a){if(!a||!a.data)return;const{id:r,type:o,path:c}=Object.assign({path:[]},a.data),u=(a.data.argumentList||[]).map(x);let m;try{const n=c.slice(0,-1).reduce((e,t)=>e[t],t),l=c.reduce((e,t)=>e[t],t);switch(o){case 0:m=l;break;case 1:n[c.slice(-1)[0]]=x(a.data.value),m=!0;break;case 2:m=l.apply(n,u);break;case 3:m=function(e){return Object.assign(e,{[i]:!0})}(new l(...u));break;case 4:{const{port1:n,port2:i}=new MessageChannel;e(t,i),m=function(e,t){return p.set(e,t),e}(n,[n])}break;case 5:m=void 0}}catch(b){m={value:b,[s]:0}}Promise.resolve(m).catch(e=>({value:e,[s]:0})).then(e=>{const[t,i]=d(e);n.postMessage(Object.assign(Object.assign({},t),{id:r}),i),5===o&&(n.removeEventListener("message",l),f(n))})})),n.start&&n.start()}(e,t),[n,[n]]},deserialize:e=>(e.start(),c(e))}],["throw",{canHandle:e=>r(e)&&s in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function f(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function c(e,t){return function e(t,n=[],i=function(){}){let s=!1;const r=new Proxy(i,{get(i,l){if(u(s),l===a)return()=>b(t,{type:5,path:n.map(e=>e.toString())}).then(()=>{f(t),s=!0});if("then"===l){if(0===n.length)return{then:()=>r};const e=b(t,{type:0,path:n.map(e=>e.toString())}).then(x);return e.then.bind(e)}return e(t,[...n,l])},set(e,i,l){u(s);const[a,r]=d(l);return b(t,{type:1,path:[...n,i].map(e=>e.toString()),value:a},r).then(x)},apply(i,a,r){u(s);const o=n[n.length-1];if(o===l)return b(t,{type:4}).then(x);if("bind"===o)return e(t,n.slice(0,-1));const[f,c]=m(r);return b(t,{type:2,path:n.map(e=>e.toString()),argumentList:f},c).then(x)},construct(e,i){u(s);const[l,a]=m(i);return b(t,{type:3,path:n.map(e=>e.toString()),argumentList:l},a).then(x)}});return r}(e,[],t)}function u(e){if(e)throw new Error("Proxy has been released and is not useable")}function m(e){const t=e.map(d);return[t.map(e=>e[0]),(n=t.map(e=>e[1]),Array.prototype.concat.apply([],n))];var n}const p=new WeakMap;function d(e){for(const[t,n]of o)if(n.canHandle(e)){const[i,l]=n.serialize(e);return[{type:3,name:t,value:i},l]}return[{type:0,value:e},p.get(e)||[]]}function x(e){switch(e.type){case 3:return o.get(e.name).deserialize(e.value);case 0:return e.value}}function b(e,t,n){return new Promise(i=>{const l=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");e.addEventListener("message",(function t(n){n.data&&n.data.id&&n.data.id===l&&(e.removeEventListener("message",t),i(n.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:l},t),n)})}},94433:(e,t,n)=>{"use strict";n.r(t);n(77330),n(21157),n(87772),n(30879),n(31206);var i=n(50856),l=n(28426);n(93546);class a extends l.H3{static get template(){return i.d`
      <style include="iron-flex"></style>
      <style>
        p {
          margin: 8px 0;
        }

        a {
          color: var(--primary-color);
        }

        p > img {
          max-width: 100%;
        }

        p.center {
          text-align: center;
        }

        p.error {
          color: #c62828;
        }

        p.submit {
          text-align: center;
          height: 41px;
        }

        ha-circular-progress {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }

        [hidden] {
          display: none;
        }
      </style>

      <div class="layout vertical">
        <template is="dom-if" if="[[isConfigurable]]">
          <ha-markdown
            breaks
            content="[[stateObj.attributes.description]]"
          ></ha-markdown>

          <p class="error" hidden$="[[!stateObj.attributes.errors]]">
            [[stateObj.attributes.errors]]
          </p>

          <template is="dom-repeat" items="[[stateObj.attributes.fields]]">
            <paper-input
              label="[[item.name]]"
              name="[[item.id]]"
              type="[[item.type]]"
              on-change="fieldChanged"
            ></paper-input>
          </template>

          <p class="submit" hidden$="[[!stateObj.attributes.submit_caption]]">
            <mwc-button
              raised=""
              disabled="[[isConfiguring]]"
              on-click="submitClicked"
            >
              <ha-circular-progress
                active="[[isConfiguring]]"
                hidden="[[!isConfiguring]]"
                alt="Configuring"
              ></ha-circular-progress>
              [[stateObj.attributes.submit_caption]]
            </mwc-button>
          </p>
        </template>
      </div>
    `}static get properties(){return{stateObj:{type:Object},action:{type:String,value:"display"},isConfigurable:{type:Boolean,computed:"computeIsConfigurable(stateObj)"},isConfiguring:{type:Boolean,value:!1},fieldInput:{type:Object,value:function(){return{}}}}}computeIsConfigurable(e){return"configure"===e.state}fieldChanged(e){const t=e.target;this.fieldInput[t.name]=t.value}submitClicked(){const e={configure_id:this.stateObj.attributes.configure_id,fields:this.fieldInput};this.isConfiguring=!0,this.hass.callService("configurator","configure",e).then(function(){this.isConfiguring=!1}.bind(this),function(){this.isConfiguring=!1}.bind(this))}}customElements.define("more-info-configurator",a)}}]);
//# sourceMappingURL=chunk.54168543e4b2d36aa064.js.map