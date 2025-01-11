#!/usr/bin/env python3
import os, argparse, csv, json, sys, configparser

# Named argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input csv")
parser.add_argument("-o", "--output", help="output html")
parser.add_argument("-c", "--config", help="config.ini location")
args = parser.parse_args()

# Set defaults is options not passed
input = args.input if args.input else "./input.csv"
output = args.output if args.output else "./output.html"
conf = args.config if args.config else "./config.ini"

# Print message and quit if any required file missing
miss_file = False

for f in [input, conf]:
    if not os.path.isfile(f):
        print("File %s not found. Use --%s to specify its location." % (f, f))
        miss_file = True

if miss_file:
    quit()

# Read config file
config = configparser.ConfigParser()
try:
    config.read(conf)
except:
    print("Could not parse config file. Check its contents.")
    quit()

search_fields = list(config['filters'])
search_types = dict(config['filters'])

inputs_string = "<div>\n"

for i in search_fields:
    # TODO: handle other fields
    inputs_string += '    <input type="text" id="%s" placeholder="Search by %s">\n' % (i, i)

inputs_string += "</div>"

print(inputs_string)

## Check if the configuration file exists

config.read(config)
print(config.get('other', 'use_anonymous'))  # Outputs 'True'

with open(input, newline='', encoding='utf-8') as f:
    jsonified = json.dumps([dict(r) for r in csv.DictReader(f)])

head = r"""<!DOCTYPE html>
<html lang="en">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fuzzy Find</title>
    <style type="text/css">
        body {font-family: "Roboto", sans-serif;}
        table {border-collapse: collapse; vertical-align: middle;}
        tr {border-bottom: 1px solid #ccc; height: 1.8em;}
        button.copy-button {
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button.copy-button:hover {
            background-color: #45a049;
        }
    </style>
</head>"""

body_1 = r"""
<body>
    <h1>Fuzzy Find</h1>
"""

tmp=r"""
        <!---
        <input type="text" id="indivID" placeholder="Filter by IndivID">
        <input type="text" id="fullname" placeholder="Search by Full Name">
        <label><input type="checkbox" id="maleCheckbox" value="male"> Male</label>
        <label><input type="checkbox" id="femaleCheckbox" value="female"> Female</label>
        <input type="text" id="location" placeholder="Filter by Location">
        <input type="text" id="fathername" placeholder="Search by Father Name">
        <input type="text" id="mothername" placeholder="Search by Mother Name">
        <input type="text" id="spousename" placeholder="Search by Spouse Name">
        --->"""

table = r"""
    <div id="results-container">
        <table id="results" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 2px solid black; border-top: 2px solid black;">
                    <th style="width: 5%; text-align: left;">Action</th>
                    <th style="width: 5%; text-align: left;">ID</th>
                    <th style="width: 20%; text-align: left;">Name</th>
                    <th style="width: 5%; text-align: left;">Gender</th>
                    <th style="width: 5%; text-align: left;">Age</th>
                    <th style="width: 15%; text-align: left;">Location</th>
                    <th style="width: 15%; text-align: left;">Father Name</th>
                    <th style="width: 15%; text-align: left;">Mother Name</th>
                    <th style="width: 15%; text-align: left;">Spouse(s) Name</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div> """

body_3 = r""" <!--- Load fuse.js --->
    <script>
    /**
     * Fuse.js v7.0.0 - Lightweight fuzzy-search (http://fusejs.io)
     *
     * Copyright (c) 2023 Kiro Risk (http://kiro.me)
     * All Rights Reserved. Apache Software License 2.0
     *
     * http://www.apache.org/licenses/LICENSE-2.0
     */
    var e,t;e=this,t=function(){"use strict";function e(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function t(t){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?e(Object(r),!0).forEach((function(e){c(t,e,r[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(r)):e(Object(r)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(r,e))}))}return t}function n(e){return n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},n(e)}function r(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function i(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,v(r.key),r)}}function o(e,t,n){return t&&i(e.prototype,t),n&&i(e,n),Object.defineProperty(e,"prototype",{writable:!1}),e}function c(e,t,n){return(t=v(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&u(e,t)}function s(e){return s=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},s(e)}function u(e,t){return u=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},u(e,t)}function h(e,t){if(t&&("object"==typeof t||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function l(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=s(e);if(t){var i=s(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return h(this,n)}}function f(e){return function(e){if(Array.isArray(e))return d(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||function(e,t){if(e){if("string"==typeof e)return d(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?d(e,t):void 0}}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function d(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e){return Array.isArray?Array.isArray(e):"[object Array]"===S(e)}var y=1/0;function p(e){return null==e?"":function(e){if("string"==typeof e)return e;var t=e+"";return"0"==t&&1/e==-y?"-0":t}(e)}function m(e){return"string"==typeof e}function k(e){return"number"==typeof e}function M(e){return!0===e||!1===e||function(e){return b(e)&&null!==e}(e)&&"[object Boolean]"==S(e)}function b(e){return"object"===n(e)}function x(e){return null!=e}function w(e){return!e.trim().length}function S(e){return null==e?void 0===e?"[object Undefined]":"[object Null]":Object.prototype.toString.call(e)}var L=function(e){return"Missing ".concat(e," property in key")},_=function(e){return"Property 'weight' in key '".concat(e,"' must be a positive integer")},O=Object.prototype.hasOwnProperty,j=function(){function e(t){var n=this;r(this,e),this._keys=[],this._keyMap={};var i=0;t.forEach((function(e){var t=A(e);n._keys.push(t),n._keyMap[t.id]=t,i+=t.weight})),this._keys.forEach((function(e){e.weight/=i}))}return o(e,[{key:"get",value:function(e){return this._keyMap[e]}},{key:"keys",value:function(){return this._keys}},{key:"toJSON",value:function(){return JSON.stringify(this._keys)}}]),e}();function A(e){var t=null,n=null,r=null,i=1,o=null;if(m(e)||g(e))r=e,t=I(e),n=C(e);else{if(!O.call(e,"name"))throw new Error(L("name"));var c=e.name;if(r=c,O.call(e,"weight")&&(i=e.weight)<=0)throw new Error(_(c));t=I(c),n=C(c),o=e.getFn}return{path:t,id:n,weight:i,src:r,getFn:o}}function I(e){return g(e)?e:e.split(".")}function C(e){return g(e)?e.join("."):e}var E={useExtendedSearch:!1,getFn:function(e,t){var n=[],r=!1;return function e(t,i,o){if(x(t))if(i[o]){var c=t[i[o]];if(!x(c))return;if(o===i.length-1&&(m(c)||k(c)||M(c)))n.push(p(c));else if(g(c)){r=!0;for(var a=0,s=c.length;a<s;a+=1)e(c[a],i,o+1)}else i.length&&e(c,i,o+1)}else n.push(t)}(e,m(t)?t.split("."):t,0),r?n:n[0]},ignoreLocation:!1,ignoreFieldNorm:!1,fieldNormWeight:1},$=t(t(t(t({},{isCaseSensitive:!1,includeScore:!1,keys:[],shouldSort:!0,sortFn:function(e,t){return e.score===t.score?e.idx<t.idx?-1:1:e.score<t.score?-1:1}}),{includeMatches:!1,findAllMatches:!1,minMatchCharLength:1}),{location:0,threshold:.6,distance:100}),E),F=/[^ ]+/g,R=function(){function e(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},n=t.getFn,i=void 0===n?$.getFn:n,o=t.fieldNormWeight,c=void 0===o?$.fieldNormWeight:o;r(this,e),this.norm=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1,t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:3,n=new Map,r=Math.pow(10,t);return{get:function(t){var i=t.match(F).length;if(n.has(i))return n.get(i);var o=1/Math.pow(i,.5*e),c=parseFloat(Math.round(o*r)/r);return n.set(i,c),c},clear:function(){n.clear()}}}(c,3),this.getFn=i,this.isCreated=!1,this.setIndexRecords()}return o(e,[{key:"setSources",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.docs=e}},{key:"setIndexRecords",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.records=e}},{key:"setKeys",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.keys=t,this._keysMap={},t.forEach((function(t,n){e._keysMap[t.id]=n}))}},{key:"create",value:function(){var e=this;!this.isCreated&&this.docs.length&&(this.isCreated=!0,m(this.docs[0])?this.docs.forEach((function(t,n){e._addString(t,n)})):this.docs.forEach((function(t,n){e._addObject(t,n)})),this.norm.clear())}},{key:"add",value:function(e){var t=this.size();m(e)?this._addString(e,t):this._addObject(e,t)}},{key:"removeAt",value:function(e){this.records.splice(e,1);for(var t=e,n=this.size();t<n;t+=1)this.records[t].i-=1}},{key:"getValueForItemAtKeyId",value:function(e,t){return e[this._keysMap[t]]}},{key:"size",value:function(){return this.records.length}},{key:"_addString",value:function(e,t){if(x(e)&&!w(e)){var n={v:e,i:t,n:this.norm.get(e)};this.records.push(n)}}},{key:"_addObject",value:function(e,t){var n=this,r={i:t,$:{}};this.keys.forEach((function(t,i){var o=t.getFn?t.getFn(e):n.getFn(e,t.path);if(x(o))if(g(o)){for(var c=[],a=[{nestedArrIndex:-1,value:o}];a.length;){var s=a.pop(),u=s.nestedArrIndex,h=s.value;if(x(h))if(m(h)&&!w(h)){var l={v:h,i:u,n:n.norm.get(h)};c.push(l)}else g(h)&&h.forEach((function(e,t){a.push({nestedArrIndex:t,value:e})}))}r.$[i]=c}else if(m(o)&&!w(o)){var f={v:o,n:n.norm.get(o)};r.$[i]=f}})),this.records.push(r)}},{key:"toJSON",value:function(){return{keys:this.keys,records:this.records}}}]),e}();function P(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=n.getFn,i=void 0===r?$.getFn:r,o=n.fieldNormWeight,c=void 0===o?$.fieldNormWeight:o,a=new R({getFn:i,fieldNormWeight:c});return a.setKeys(e.map(A)),a.setSources(t),a.create(),a}function N(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=t.errors,r=void 0===n?0:n,i=t.currentLocation,o=void 0===i?0:i,c=t.expectedLocation,a=void 0===c?0:c,s=t.distance,u=void 0===s?$.distance:s,h=t.ignoreLocation,l=void 0===h?$.ignoreLocation:h,f=r/e.length;if(l)return f;var d=Math.abs(a-o);return u?f+d/u:d?1:f}var W=32;function T(e,t,n){var r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:{},i=r.location,o=void 0===i?$.location:i,c=r.distance,a=void 0===c?$.distance:c,s=r.threshold,u=void 0===s?$.threshold:s,h=r.findAllMatches,l=void 0===h?$.findAllMatches:h,f=r.minMatchCharLength,d=void 0===f?$.minMatchCharLength:f,v=r.includeMatches,g=void 0===v?$.includeMatches:v,y=r.ignoreLocation,p=void 0===y?$.ignoreLocation:y;if(t.length>W)throw new Error("Pattern length exceeds max of ".concat(W,"."));for(var m,k=t.length,M=e.length,b=Math.max(0,Math.min(o,M)),x=u,w=b,S=d>1||g,L=S?Array(M):[];(m=e.indexOf(t,w))>-1;){var _=N(t,{currentLocation:m,expectedLocation:b,distance:a,ignoreLocation:p});if(x=Math.min(_,x),w=m+k,S)for(var O=0;O<k;)L[m+O]=1,O+=1}w=-1;for(var j=[],A=1,I=k+M,C=1<<k-1,E=0;E<k;E+=1){for(var F=0,R=I;F<R;)N(t,{errors:E,currentLocation:b+R,expectedLocation:b,distance:a,ignoreLocation:p})<=x?F=R:I=R,R=Math.floor((I-F)/2+F);I=R;var P=Math.max(1,b-R+1),T=l?M:Math.min(b+R,M)+k,z=Array(T+2);z[T+1]=(1<<E)-1;for(var D=T;D>=P;D-=1){var K=D-1,q=n[e.charAt(K)];if(S&&(L[K]=+!!q),z[D]=(z[D+1]<<1|1)&q,E&&(z[D]|=(j[D+1]|j[D])<<1|1|j[D+1]),z[D]&C&&(A=N(t,{errors:E,currentLocation:K,expectedLocation:b,distance:a,ignoreLocation:p}))<=x){if(x=A,(w=K)<=b)break;P=Math.max(1,2*b-w)}}if(N(t,{errors:E+1,currentLocation:b,expectedLocation:b,distance:a,ignoreLocation:p})>x)break;j=z}var B={isMatch:w>=0,score:Math.max(.001,A)};if(S){var J=function(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:$.minMatchCharLength,n=[],r=-1,i=-1,o=0,c=e.length;o<c;o+=1){var a=e[o];a&&-1===r?r=o:a||-1===r||((i=o-1)-r+1>=t&&n.push([r,i]),r=-1)}return e[o-1]&&o-r>=t&&n.push([r,o-1]),n}(L,d);J.length?g&&(B.indices=J):B.isMatch=!1}return B}function z(e){for(var t={},n=0,r=e.length;n<r;n+=1){var i=e.charAt(n);t[i]=(t[i]||0)|1<<r-n-1}return t}var D=function(){function e(t){var n=this,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},o=i.location,c=void 0===o?$.location:o,a=i.threshold,s=void 0===a?$.threshold:a,u=i.distance,h=void 0===u?$.distance:u,l=i.includeMatches,f=void 0===l?$.includeMatches:l,d=i.findAllMatches,v=void 0===d?$.findAllMatches:d,g=i.minMatchCharLength,y=void 0===g?$.minMatchCharLength:g,p=i.isCaseSensitive,m=void 0===p?$.isCaseSensitive:p,k=i.ignoreLocation,M=void 0===k?$.ignoreLocation:k;if(r(this,e),this.options={location:c,threshold:s,distance:h,includeMatches:f,findAllMatches:v,minMatchCharLength:y,isCaseSensitive:m,ignoreLocation:M},this.pattern=m?t:t.toLowerCase(),this.chunks=[],this.pattern.length){var b=function(e,t){n.chunks.push({pattern:e,alphabet:z(e),startIndex:t})},x=this.pattern.length;if(x>W){for(var w=0,S=x%W,L=x-S;w<L;)b(this.pattern.substr(w,W),w),w+=W;if(S){var _=x-W;b(this.pattern.substr(_),_)}}else b(this.pattern,0)}}return o(e,[{key:"searchIn",value:function(e){var t=this.options,n=t.isCaseSensitive,r=t.includeMatches;if(n||(e=e.toLowerCase()),this.pattern===e){var i={isMatch:!0,score:0};return r&&(i.indices=[[0,e.length-1]]),i}var o=this.options,c=o.location,a=o.distance,s=o.threshold,u=o.findAllMatches,h=o.minMatchCharLength,l=o.ignoreLocation,d=[],v=0,g=!1;this.chunks.forEach((function(t){var n=t.pattern,i=t.alphabet,o=t.startIndex,y=T(e,n,i,{location:c+o,distance:a,threshold:s,findAllMatches:u,minMatchCharLength:h,includeMatches:r,ignoreLocation:l}),p=y.isMatch,m=y.score,k=y.indices;p&&(g=!0),v+=m,p&&k&&(d=[].concat(f(d),f(k)))}));var y={isMatch:g,score:g?v/this.chunks.length:1};return g&&r&&(y.indices=d),y}}]),e}(),K=function(){function e(t){r(this,e),this.pattern=t}return o(e,[{key:"search",value:function(){}}],[{key:"isMultiMatch",value:function(e){return q(e,this.multiRegex)}},{key:"isSingleMatch",value:function(e){return q(e,this.singleRegex)}}]),e}();function q(e,t){var n=e.match(t);return n?n[1]:null}var B=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=e===this.pattern;return{isMatch:t,score:t?0:1,indices:[0,this.pattern.length-1]}}}],[{key:"type",get:function(){return"exact"}},{key:"multiRegex",get:function(){return/^="(.*)"$/}},{key:"singleRegex",get:function(){return/^=(.*)$/}}]),n}(K),J=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=-1===e.indexOf(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-exact"}},{key:"multiRegex",get:function(){return/^!"(.*)"$/}},{key:"singleRegex",get:function(){return/^!(.*)$/}}]),n}(K),U=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=e.startsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,this.pattern.length-1]}}}],[{key:"type",get:function(){return"prefix-exact"}},{key:"multiRegex",get:function(){return/^\^"(.*)"$/}},{key:"singleRegex",get:function(){return/^\^(.*)$/}}]),n}(K),V=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=!e.startsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-prefix-exact"}},{key:"multiRegex",get:function(){return/^!\^"(.*)"$/}},{key:"singleRegex",get:function(){return/^!\^(.*)$/}}]),n}(K),G=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=e.endsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[e.length-this.pattern.length,e.length-1]}}}],[{key:"type",get:function(){return"suffix-exact"}},{key:"multiRegex",get:function(){return/^"(.*)"\$$/}},{key:"singleRegex",get:function(){return/^(.*)\$$/}}]),n}(K),H=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){var t=!e.endsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-suffix-exact"}},{key:"multiRegex",get:function(){return/^!"(.*)"\$$/}},{key:"singleRegex",get:function(){return/^!(.*)\$$/}}]),n}(K),Q=function(e){a(n,e);var t=l(n);function n(e){var i,o=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},c=o.location,a=void 0===c?$.location:c,s=o.threshold,u=void 0===s?$.threshold:s,h=o.distance,l=void 0===h?$.distance:h,f=o.includeMatches,d=void 0===f?$.includeMatches:f,v=o.findAllMatches,g=void 0===v?$.findAllMatches:v,y=o.minMatchCharLength,p=void 0===y?$.minMatchCharLength:y,m=o.isCaseSensitive,k=void 0===m?$.isCaseSensitive:m,M=o.ignoreLocation,b=void 0===M?$.ignoreLocation:M;return r(this,n),(i=t.call(this,e))._bitapSearch=new D(e,{location:a,threshold:u,distance:l,includeMatches:d,findAllMatches:g,minMatchCharLength:p,isCaseSensitive:k,ignoreLocation:b}),i}return o(n,[{key:"search",value:function(e){return this._bitapSearch.searchIn(e)}}],[{key:"type",get:function(){return"fuzzy"}},{key:"multiRegex",get:function(){return/^"(.*)"$/}},{key:"singleRegex",get:function(){return/^(.*)$/}}]),n}(K),X=function(e){a(n,e);var t=l(n);function n(e){return r(this,n),t.call(this,e)}return o(n,[{key:"search",value:function(e){for(var t,n=0,r=[],i=this.pattern.length;(t=e.indexOf(this.pattern,n))>-1;)n=t+i,r.push([t,n-1]);var o=!!r.length;return{isMatch:o,score:o?0:1,indices:r}}}],[{key:"type",get:function(){return"include"}},{key:"multiRegex",get:function(){return/^'"(.*)"$/}},{key:"singleRegex",get:function(){return/^'(.*)$/}}]),n}(K),Y=[B,X,U,V,H,G,J,Q],Z=Y.length,ee=/ +(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/,te=new Set([Q.type,X.type]),ne=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},i=n.isCaseSensitive,o=void 0===i?$.isCaseSensitive:i,c=n.includeMatches,a=void 0===c?$.includeMatches:c,s=n.minMatchCharLength,u=void 0===s?$.minMatchCharLength:s,h=n.ignoreLocation,l=void 0===h?$.ignoreLocation:h,f=n.findAllMatches,d=void 0===f?$.findAllMatches:f,v=n.location,g=void 0===v?$.location:v,y=n.threshold,p=void 0===y?$.threshold:y,m=n.distance,k=void 0===m?$.distance:m;r(this,e),this.query=null,this.options={isCaseSensitive:o,includeMatches:a,minMatchCharLength:u,findAllMatches:d,ignoreLocation:l,location:g,threshold:p,distance:k},this.pattern=o?t:t.toLowerCase(),this.query=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return e.split("|").map((function(e){for(var n=e.trim().split(ee).filter((function(e){return e&&!!e.trim()})),r=[],i=0,o=n.length;i<o;i+=1){for(var c=n[i],a=!1,s=-1;!a&&++s<Z;){var u=Y[s],h=u.isMultiMatch(c);h&&(r.push(new u(h,t)),a=!0)}if(!a)for(s=-1;++s<Z;){var l=Y[s],f=l.isSingleMatch(c);if(f){r.push(new l(f,t));break}}}return r}))}(this.pattern,this.options)}return o(e,[{key:"searchIn",value:function(e){var t=this.query;if(!t)return{isMatch:!1,score:1};var n=this.options,r=n.includeMatches;e=n.isCaseSensitive?e:e.toLowerCase();for(var i=0,o=[],c=0,a=0,s=t.length;a<s;a+=1){var u=t[a];o.length=0,i=0;for(var h=0,l=u.length;h<l;h+=1){var d=u[h],v=d.search(e),g=v.isMatch,y=v.indices,p=v.score;if(!g){c=0,i=0,o.length=0;break}if(i+=1,c+=p,r){var m=d.constructor.type;te.has(m)?o=[].concat(f(o),f(y)):o.push(y)}}if(i){var k={isMatch:!0,score:c/i};return r&&(k.indices=o),k}}return{isMatch:!1,score:1}}}],[{key:"condition",value:function(e,t){return t.useExtendedSearch}}]),e}(),re=[];function ie(e,t){for(var n=0,r=re.length;n<r;n+=1){var i=re[n];if(i.condition(e,t))return new i(e,t)}return new D(e,t)}var oe="$and",ce="$or",ae="$path",se="$val",ue=function(e){return!(!e[oe]&&!e[ce])},he=function(e){return c({},oe,Object.keys(e).map((function(t){return c({},t,e[t])})))};function le(e,t){var n=(arguments.length>2&&void 0!==arguments[2]?arguments[2]:{}).auto,r=void 0===n||n;return ue(e)||(e=he(e)),function e(n){var i=Object.keys(n),o=function(e){return!!e[ae]}(n);if(!o&&i.length>1&&!ue(n))return e(he(n));if(function(e){return!g(e)&&b(e)&&!ue(e)}(n)){var c=o?n[ae]:i[0],a=o?n[se]:n[c];if(!m(a))throw new Error(function(e){return"Invalid value for key ".concat(e)}(c));var s={keyId:C(c),pattern:a};return r&&(s.searcher=ie(a,t)),s}var u={children:[],operator:i[0]};return i.forEach((function(t){var r=n[t];g(r)&&r.forEach((function(t){u.children.push(e(t))}))})),u}(e)}function fe(e,t){var n=e.matches;t.matches=[],x(n)&&n.forEach((function(e){if(x(e.indices)&&e.indices.length){var n={indices:e.indices,value:e.value};e.key&&(n.key=e.key.src),e.idx>-1&&(n.refIndex=e.idx),t.matches.push(n)}}))}function de(e,t){t.score=e.score}var ve=function(){function e(n){var i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},o=arguments.length>2?arguments[2]:void 0;r(this,e),this.options=t(t({},$),i),this.options.useExtendedSearch,this._keyStore=new j(this.options.keys),this.setCollection(n,o)}return o(e,[{key:"setCollection",value:function(e,t){if(this._docs=e,t&&!(t instanceof R))throw new Error("Incorrect 'index' type");this._myIndex=t||P(this.options.keys,this._docs,{getFn:this.options.getFn,fieldNormWeight:this.options.fieldNormWeight})}},{key:"add",value:function(e){x(e)&&(this._docs.push(e),this._myIndex.add(e))}},{key:"remove",value:function(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:function(){return!1},t=[],n=0,r=this._docs.length;n<r;n+=1){var i=this._docs[n];e(i,n)&&(this.removeAt(n),n-=1,r-=1,t.push(i))}return t}},{key:"removeAt",value:function(e){this._docs.splice(e,1),this._myIndex.removeAt(e)}},{key:"getIndex",value:function(){return this._myIndex}},{key:"search",value:function(e){var t=(arguments.length>1&&void 0!==arguments[1]?arguments[1]:{}).limit,n=void 0===t?-1:t,r=this.options,i=r.includeMatches,o=r.includeScore,c=r.shouldSort,a=r.sortFn,s=r.ignoreFieldNorm,u=m(e)?m(this._docs[0])?this._searchStringList(e):this._searchObjectList(e):this._searchLogical(e);return function(e,t){var n=t.ignoreFieldNorm,r=void 0===n?$.ignoreFieldNorm:n;e.forEach((function(e){var t=1;e.matches.forEach((function(e){var n=e.key,i=e.norm,o=e.score,c=n?n.weight:null;t*=Math.pow(0===o&&c?Number.EPSILON:o,(c||1)*(r?1:i))})),e.score=t}))}(u,{ignoreFieldNorm:s}),c&&u.sort(a),k(n)&&n>-1&&(u=u.slice(0,n)),function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=n.includeMatches,i=void 0===r?$.includeMatches:r,o=n.includeScore,c=void 0===o?$.includeScore:o,a=[];return i&&a.push(fe),c&&a.push(de),e.map((function(e){var n=e.idx,r={item:t[n],refIndex:n};return a.length&&a.forEach((function(t){t(e,r)})),r}))}(u,this._docs,{includeMatches:i,includeScore:o})}},{key:"_searchStringList",value:function(e){var t=ie(e,this.options),n=this._myIndex.records,r=[];return n.forEach((function(e){var n=e.v,i=e.i,o=e.n;if(x(n)){var c=t.searchIn(n),a=c.isMatch,s=c.score,u=c.indices;a&&r.push({item:n,idx:i,matches:[{score:s,value:n,norm:o,indices:u}]})}})),r}},{key:"_searchLogical",value:function(e){var t=this,n=le(e,this.options),r=function e(n,r,i){if(!n.children){var o=n.keyId,c=n.searcher,a=t._findMatches({key:t._keyStore.get(o),value:t._myIndex.getValueForItemAtKeyId(r,o),searcher:c});return a&&a.length?[{idx:i,item:r,matches:a}]:[]}for(var s=[],u=0,h=n.children.length;u<h;u+=1){var l=e(n.children[u],r,i);if(l.length)s.push.apply(s,f(l));else if(n.operator===oe)return[]}return s},i=this._myIndex.records,o={},c=[];return i.forEach((function(e){var t=e.$,i=e.i;if(x(t)){var a=r(n,t,i);a.length&&(o[i]||(o[i]={idx:i,item:t,matches:[]},c.push(o[i])),a.forEach((function(e){var t,n=e.matches;(t=o[i].matches).push.apply(t,f(n))})))}})),c}},{key:"_searchObjectList",value:function(e){var t=this,n=ie(e,this.options),r=this._myIndex,i=r.keys,o=r.records,c=[];return o.forEach((function(e){var r=e.$,o=e.i;if(x(r)){var a=[];i.forEach((function(e,i){a.push.apply(a,f(t._findMatches({key:e,value:r[i],searcher:n})))})),a.length&&c.push({idx:o,item:r,matches:a})}})),c}},{key:"_findMatches",value:function(e){var t=e.key,n=e.value,r=e.searcher;if(!x(n))return[];var i=[];if(g(n))n.forEach((function(e){var n=e.v,o=e.i,c=e.n;if(x(n)){var a=r.searchIn(n),s=a.isMatch,u=a.score,h=a.indices;s&&i.push({score:u,key:t,value:n,idx:o,norm:c,indices:h})}}));else{var o=n.v,c=n.n,a=r.searchIn(o),s=a.isMatch,u=a.score,h=a.indices;s&&i.push({score:u,key:t,value:o,norm:c,indices:h})}return i}}]),e}();return ve.version="7.0.0",ve.createIndex=P,ve.parseIndex=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=t.getFn,r=void 0===n?$.getFn:n,i=t.fieldNormWeight,o=void 0===i?$.fieldNormWeight:i,c=e.keys,a=e.records,s=new R({getFn:r,fieldNormWeight:o});return s.setKeys(c),s.setIndexRecords(a),s},ve.config=$,function(){re.push.apply(re,arguments)}(ne),ve},"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):(e="undefined"!=typeof globalThis?globalThis:e||self).Fuse=t();
    </script>
    <script>
      // Initialise
      let fuseName, fuseFather, fuseMother, fuseSpouse;
      const debounceDelay = 300;
      let debounceTimeout;
      const data = """

last_bit = r""";

      const processedData = data.map(item => ({
          ...item,
          full_name: `${item.firstname ?? ""} ${item.caste ?? ""}`.trim(),
      }));

      // Initialize Fuse.js for each field separately
      fuseName = new Fuse(processedData, { keys: ["full_name"], threshold: 0.4, includeScore: true });
      fuseFather = new Fuse(processedData, { keys: ["fathersname"], threshold: 0.4, includeScore: true });
      fuseMother = new Fuse(processedData, { keys: ["mothersname"], threshold: 0.4, includeScore: true });
      fuseSpouse = new Fuse(processedData, { keys: ["spousesname"], threshold: 0.4, includeScore: true });

      // Get input elements
      const indivIDInput = document.getElementById("indivID");
      const fullNameInput = document.getElementById("fullname");
      const fatherNameInput = document.getElementById("fathername");
      const motherNameInput = document.getElementById("mothername");
      const spouseNameInput = document.getElementById("spousename");
      const locationInput = document.getElementById("location");
      const resultsList = document.querySelector("#results tbody");

      // Debounce function
      const debounce = (func, delay) => {
          clearTimeout(debounceTimeout);
          debounceTimeout = setTimeout(func, delay);
      };

      // Perform the search based on the combined input values
      const performSearch = () => {
          const indivIDQuery = indivIDInput.value.trim().toLowerCase();
          const fullNameQuery = fullNameInput.value.trim();
          const fatherNameQuery = fatherNameInput.value.trim();
          const motherNameQuery = motherNameInput.value.trim();
          const spouseNameQuery = spouseNameInput.value.trim();
          const locationQuery = locationInput.value.trim().toLowerCase();

          // Get selected genders from checkboxes
          const maleChecked = document.getElementById("maleCheckbox").checked;
          const femaleChecked = document.getElementById("femaleCheckbox").checked;

          // Perform fuzzy searches separately for each field
          const nameResults = fullNameQuery ? fuseName.search(fullNameQuery).map(result => result.item) : processedData;
          const fatherResults = fatherNameQuery ? fuseFather.search(fatherNameQuery).map(result => result.item) : processedData;
          const motherResults = motherNameQuery ? fuseMother.search(motherNameQuery).map(result => result.item) : processedData;
          const spouseResults = spouseNameQuery ? fuseSpouse.search(spouseNameQuery).map(result => result.item) : processedData;

          // Combine results: Intersection of all queried results
          const combinedResults = nameResults.filter(item =>
              fatherResults.some(fatherItem => fatherItem.IndivID === item.IndivID) &&
              motherResults.some(motherItem => motherItem.IndivID === item.IndivID) &&
              spouseResults.some(spouseItem => spouseItem.IndivID === item.IndivID)
          );

          // Further filter results based on other active criteria
          const filteredResults = combinedResults.filter(item => {
              const matchesID = indivIDQuery ? item.IndivID?.toLowerCase().includes(indivIDQuery) : true;
              const matchesGender =
                  (maleChecked && item.gender?.toLowerCase() === "male") ||
                  (femaleChecked && item.gender?.toLowerCase() === "female") ||
                  (!maleChecked && !femaleChecked); // Include all if no checkbox is selected
              const matchesLocation = locationQuery ? item.location?.toLowerCase().includes(locationQuery) : true;

              // Include if all active criteria are met
              return matchesID && matchesGender && matchesLocation;
          });

          // Display results
          displayResults(filteredResults);
      };

      // Display results using table formatting
      const displayResults = (results) => {
          if (results.length === 0) {
              resultsList.innerHTML = "<tr><td colspan='9'>No results found</td></tr>";
          } else {
              resultsList.innerHTML = results
                  .map(item => {
                      const { IndivID, firstname, caste, gender, age, location, fathersname, mothersname, spousesname } = item;
                      const name = `${firstname ?? "Unknown"} ${caste ?? "Unknown"}`;
                      return `
                          <tr>
                              <td><button onclick="copyToClipboard('${IndivID}')" class="copy-button">Copy</button></td>
                              <td>${IndivID ?? "N/A"}</td>
                              <td>${name}</td>
                              <td>${gender ?? "Unspecified"}</td>
                              <td>${age ?? "N/A"}</td>
                              <td>${location ?? "N/A"}</td>
                              <td>${fathersname ?? "N/A"}</td>
                              <td>${mothersname ?? "N/A"}</td>
                              <td>${spousesname ?? "N/A"}</td>
                          </tr>
                      `;
                  })
                  .join("");
          }
      };

      // Copy to Clipboard Function
      function copyToClipboard(text) {
          if (navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(text).then(
                  () => alert(`Copied to clipboard: ${text}`),
                  err => {
                      console.error("Failed to copy using Clipboard API:", err);
                      fallbackCopy(text);
                  }
              );
          } else {
              fallbackCopy(text);
          }
      }

      // Fallback: Use a hidden input element to copy text
      function fallbackCopy(text) {
          const tempInput = document.createElement("input");
          tempInput.value = text;
          document.body.appendChild(tempInput);
          tempInput.select();
          tempInput.setSelectionRange(0, 99999); // For mobile devices
          try {
              document.execCommand("copy");
              alert(`Copied to clipboard: ${text}`);
          } catch (err) {
              console.error("Fallback: Copy command failed", err);
              alert("Failed to copy!");
          }
          document.body.removeChild(tempInput);
      }

      // Input event listeners with debouncing
      [indivIDInput, fullNameInput, fatherNameInput, motherNameInput, spouseNameInput, locationInput].forEach(input => {
          input.addEventListener("input", () => debounce(performSearch, debounceDelay));
      });
      document.getElementById("maleCheckbox").addEventListener("change", performSearch);
      document.getElementById("femaleCheckbox").addEventListener("change", performSearch);
    </script>
</body>
</html>"""

# fuzz_me_good = first_bit + jsonified + last_bit
fuzz_me_good = head + body_1 + inputs_string

# Write out the result
with open(sys.argv[2], "w", encoding="utf-8") as file:
    file.write(fuzz_me_good)
