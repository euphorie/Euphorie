/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 	};
/******/
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		4: 0,
/******/ 		5: 0
/******/ 	};
/******/
/******/
/******/
/******/ 	// script path function
/******/ 	function jsonpScriptSrc(chunkId) {
/******/ 		return __webpack_require__.p + "chunks/" + ({}[chunkId]||chunkId) + "." + {"0":"5fcd3dd59a0ec56e8482","1":"cb488f66531add3f5ae4","11":"99579b72c295812f6ff7","18":"d6752f3d92efb9516784","21":"5a440affeefd4eae4731","22":"9296cacde61fab17523e","23":"9b3d8f443537ad4c8dd0","24":"b66407ff3d00fc9bcc24","25":"9abcc4bc2596375564f6","26":"a248ac55106e0762b689","27":"7a7808eab80a724ea529","28":"81ff36f81522125c88e7","29":"51004353bb58fd00ea1d","30":"fdfcf77d59b8a76b64a7","31":"bb44142e0db5d9ca01a6","32":"7102f149d77c43ebc110","33":"5639475aea31b6115783","34":"d9b0ce9b82647eb757c2","35":"80bc5a3719dfe6cbedfe","36":"c262025002ef84a1e54e","37":"1b4d2817b0d46e525eaf","38":"a10a59b288e4ffe4cbe2","39":"c4019b5bd7dbdc22c004","40":"7654a1b44926ab400b68","41":"05d480c8232c4fcfa447","42":"1f6dc9c053f3bf9d400a","43":"5a01bcb9966a4f02df4c","44":"97d581a7124c83150e6a","45":"bb7da92621650aeecaab","46":"303756b4f94b0abb90bc","47":"b6cbbad15c5a9a9100cc","48":"e680338a84fef315bb0c","49":"f58ba9cdbf0b3ae31ce0","50":"59bba2a4ba29dc02aa86","51":"850222b4033c4d4495a0","52":"1641b8656bd94a3493be","53":"22d00486e397b35bc7d6","54":"52dc9a6096279b334496","55":"8a44fd7e36df9433497d","56":"65272398dd0505a2311e","57":"ed7cf9416a89823b9516","58":"ae8f2c12c511945ab77c","59":"ece36249acc45181a039","60":"2a2fb858ea719ee34e90","61":"bf33ee337ca56170558f","62":"fe1c2944d7a9d90f254a","63":"2e35db9237673475654a","64":"b23ff04c879a262a70d1","65":"1e959e818c05585e6274","66":"65502badb754bc39309f","67":"e040715f30e3db665751","68":"d70c58da4449af1b07c7","69":"45c77b1f309294215b0f","70":"d618faedfe54151575cf","71":"b011a8d810e5331676bb","72":"403064e1a96ac633dd1e","73":"9137deb14ff847bc4bcf","74":"56aac9189ee26b0c9c65","75":"ecc3455d2527c71b4a89","76":"a362cd3def8a94f67697","77":"9ff33fd65b0d12068f33","78":"c6fd63bc0bfc0a5a5890","79":"acb8119a079bf94e4fd8","80":"6826dec79d3f6b151d10","81":"06ea24718b96ee82bfec","82":"d7d1459491bd03bcd9aa","83":"877d4059c082e466cfdb","84":"c65f1e276cfa74c497d9","85":"49651540a8102f3a7ed5","86":"e9d05ee9f360725327b0","87":"03e4b14a59a68b0167de","88":"3e3a65a2cef78fef1ae8","89":"3f20b9fc244e0e9f170f","90":"9eb4ec1731ee8814add1","91":"145fdc65f2b91bd4d8f8","92":"9de2ca8b772a3b169396","93":"16030c72aabb2032974e","94":"f1ab998aff5925123396","95":"d1483fcff3971eda19fa","96":"e918e3973e2136737714","97":"a41e487122d0ed6a9fbd","98":"74a1ab7aa6d5449dea62","99":"9193b956c3243a88ea21","100":"3a24fb5245cbe2f8a4e8","101":"6453eb87770075aa7f46","102":"590d7dcab443c8942f39","103":"dd01934f5c3b50163b9f","104":"911ee259b1957931c4d2","105":"cae12a7b82f8c05a5053","106":"877e9b11015369179db6","107":"d057834454dacccd843a","108":"2fe7cb69485da0e1e6c8","109":"c45863af05933cff0067","110":"1c191e263af83133ec1c","111":"1e8f3372cf58e131740a","112":"ef5672cc4ea5c325a462","113":"71d48ac63918a1a9cc10","114":"702d07d8f74796f28c3f","115":"eb2c89b5f030d5f90bf8","116":"fec2f32fc89bef1d046f","117":"4e489391b67fe466455d","118":"883d07cc8a78d92b7adc","119":"6563b271ac2e66a5c608","120":"aa8bc6ee0132345ebd46","121":"4203bdc8dd32b313ead7","122":"331d7a40c209b172e465","123":"c85511f58d984fa0863b","124":"25d0263fd03c5d1895d6","125":"2c1e244b41817f9292f7","126":"9a897d8057e585dd3ef5","127":"2489724fd33cddaefa2d","128":"41c3cfea4d6b355c77a5","129":"13107dc8e2215693edfb","130":"21dce418d25d785fc94e","131":"2b4151654b1a389193a9","132":"bd330932a5ab5602a344","133":"9221c7f45c1951985161","134":"02e5b3d544a8aa51e5c7","135":"407975641565819fa8c7","136":"1109c5ffedbae3767a36","137":"eeb3dde921c830d08437","138":"49560238b7a300706339","139":"7c0e477026611ed099fc","140":"3a6a2477dd3bca0e5f87","141":"5114939ed56080de7084","142":"16703aba41d3a2ebc7b5","143":"2251e2b810a65aab03a8","144":"e5f07057893dbc5467e4","145":"9e2db033ab8d84c2f27e","146":"606151d5bd1165302cda","147":"b2c146c801c065454dcb","148":"d36a98a4aa0a83905124","149":"e0a19e26ba034e7e7596","150":"64020dca73a46f22fb7c","151":"ba0fe86e6db7c1e6690f","152":"53cf1d1989c345f29e48","153":"1e87fe2c22dd588cbfa3","154":"f699aa2a1411cdb22005","155":"8369505e9c7e33e3f045"}[chunkId] + ".min.js"
/******/ 	}
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/ 	// This file contains only the entry chunk.
/******/ 	// The chunk loading function for additional chunks
/******/ 	__webpack_require__.e = function requireEnsure(chunkId) {
/******/ 		var promises = [];
/******/
/******/
/******/ 		// JSONP chunk loading for javascript
/******/
/******/ 		var installedChunkData = installedChunks[chunkId];
/******/ 		if(installedChunkData !== 0) { // 0 means "already installed".
/******/
/******/ 			// a Promise means "currently loading".
/******/ 			if(installedChunkData) {
/******/ 				promises.push(installedChunkData[2]);
/******/ 			} else {
/******/ 				// setup Promise in chunk cache
/******/ 				var promise = new Promise(function(resolve, reject) {
/******/ 					installedChunkData = installedChunks[chunkId] = [resolve, reject];
/******/ 				});
/******/ 				promises.push(installedChunkData[2] = promise);
/******/
/******/ 				// start chunk loading
/******/ 				var script = document.createElement('script');
/******/ 				var onScriptComplete;
/******/
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.src = jsonpScriptSrc(chunkId);
/******/
/******/ 				// create error before stack unwound to get useful stacktrace later
/******/ 				var error = new Error();
/******/ 				onScriptComplete = function (event) {
/******/ 					// avoid mem leaks in IE.
/******/ 					script.onerror = script.onload = null;
/******/ 					clearTimeout(timeout);
/******/ 					var chunk = installedChunks[chunkId];
/******/ 					if(chunk !== 0) {
/******/ 						if(chunk) {
/******/ 							var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 							var realSrc = event && event.target && event.target.src;
/******/ 							error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 							error.name = 'ChunkLoadError';
/******/ 							error.type = errorType;
/******/ 							error.request = realSrc;
/******/ 							chunk[1](error);
/******/ 						}
/******/ 						installedChunks[chunkId] = undefined;
/******/ 					}
/******/ 				};
/******/ 				var timeout = setTimeout(function(){
/******/ 					onScriptComplete({ type: 'timeout', target: script });
/******/ 				}, 120000);
/******/ 				script.onerror = script.onload = onScriptComplete;
/******/ 				document.head.appendChild(script);
/******/ 			}
/******/ 		}
/******/ 		return Promise.all(promises);
/******/ 	};
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// on error function for async loading
/******/ 	__webpack_require__.oe = function(err) { console.error(err); throw err; };
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 318);
/******/ })
/************************************************************************/
/******/ ({

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {module.exports = global["$"] = __webpack_require__(100);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(29)))

/***/ }),

/***/ 1:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(global) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "e", function() { return VERSION; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "p", function() { return root; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ArrayProto; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "c", function() { return ObjProto; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "d", function() { return SymbolProto; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "o", function() { return push; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "q", function() { return slice; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "t", function() { return toString; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "i", function() { return hasOwnProperty; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "r", function() { return supportsArrayBuffer; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "s", function() { return supportsDataView; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "k", function() { return nativeIsArray; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "m", function() { return nativeKeys; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "j", function() { return nativeCreate; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "l", function() { return nativeIsView; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "g", function() { return _isNaN; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "f", function() { return _isFinite; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "h", function() { return hasEnumBug; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "n", function() { return nonEnumerableProps; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return MAX_ARRAY_INDEX; });
// Current version.
var VERSION = '1.12.1';

// Establish the root object, `window` (`self`) in the browser, `global`
// on the server, or `this` in some virtual machines. We use `self`
// instead of `window` for `WebWorker` support.
var root = typeof self == 'object' && self.self === self && self ||
          typeof global == 'object' && global.global === global && global ||
          Function('return this')() ||
          {};

// Save bytes in the minified (but not gzipped) version:
var ArrayProto = Array.prototype, ObjProto = Object.prototype;
var SymbolProto = typeof Symbol !== 'undefined' ? Symbol.prototype : null;

// Create quick reference variables for speed access to core prototypes.
var push = ArrayProto.push,
    slice = ArrayProto.slice,
    toString = ObjProto.toString,
    hasOwnProperty = ObjProto.hasOwnProperty;

// Modern feature detection.
var supportsArrayBuffer = typeof ArrayBuffer !== 'undefined',
    supportsDataView = typeof DataView !== 'undefined';

// All **ECMAScript 5+** native function implementations that we hope to use
// are declared here.
var nativeIsArray = Array.isArray,
    nativeKeys = Object.keys,
    nativeCreate = Object.create,
    nativeIsView = supportsArrayBuffer && ArrayBuffer.isView;

// Create references to these builtin functions because we override them.
var _isNaN = isNaN,
    _isFinite = isFinite;

// Keys in IE < 9 that won't be iterated by `for key in ...` and thus missed.
var hasEnumBug = !{toString: null}.propertyIsEnumerable('toString');
var nonEnumerableProps = ['valueOf', 'isPrototypeOf', 'toString',
  'propertyIsEnumerable', 'hasOwnProperty', 'toLocaleString'];

// The largest integer that can be represented exactly.
var MAX_ARRAY_INDEX = Math.pow(2, 53) - 1;

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(29)))

/***/ }),

/***/ 100:
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {module.exports = global["jQuery"] = __webpack_require__(101);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(29)))

/***/ }),

/***/ 101:
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
 * jQuery JavaScript Library v3.6.0
 * https://jquery.com/
 *
 * Includes Sizzle.js
 * https://sizzlejs.com/
 *
 * Copyright OpenJS Foundation and other contributors
 * Released under the MIT license
 * https://jquery.org/license
 *
 * Date: 2021-03-02T17:08Z
 */
( function( global, factory ) {

	"use strict";

	if (  true && typeof module.exports === "object" ) {

		// For CommonJS and CommonJS-like environments where a proper `window`
		// is present, execute the factory and get jQuery.
		// For environments that do not have a `window` with a `document`
		// (such as Node.js), expose a factory as module.exports.
		// This accentuates the need for the creation of a real `window`.
		// e.g. var jQuery = require("jquery")(window);
		// See ticket #14549 for more info.
		module.exports = global.document ?
			factory( global, true ) :
			function( w ) {
				if ( !w.document ) {
					throw new Error( "jQuery requires a window with a document" );
				}
				return factory( w );
			};
	} else {
		factory( global );
	}

// Pass this if window is not defined yet
} )( typeof window !== "undefined" ? window : this, function( window, noGlobal ) {

// Edge <= 12 - 13+, Firefox <=18 - 45+, IE 10 - 11, Safari 5.1 - 9+, iOS 6 - 9.1
// throw exceptions when non-strict code (e.g., ASP.NET 4.5) accesses strict mode
// arguments.callee.caller (trac-13335). But as of jQuery 3.0 (2016), strict mode should be common
// enough that all such attempts are guarded in a try block.
"use strict";

var arr = [];

var getProto = Object.getPrototypeOf;

var slice = arr.slice;

var flat = arr.flat ? function( array ) {
	return arr.flat.call( array );
} : function( array ) {
	return arr.concat.apply( [], array );
};


var push = arr.push;

var indexOf = arr.indexOf;

var class2type = {};

var toString = class2type.toString;

var hasOwn = class2type.hasOwnProperty;

var fnToString = hasOwn.toString;

var ObjectFunctionString = fnToString.call( Object );

var support = {};

var isFunction = function isFunction( obj ) {

		// Support: Chrome <=57, Firefox <=52
		// In some browsers, typeof returns "function" for HTML <object> elements
		// (i.e., `typeof document.createElement( "object" ) === "function"`).
		// We don't want to classify *any* DOM node as a function.
		// Support: QtWeb <=3.8.5, WebKit <=534.34, wkhtmltopdf tool <=0.12.5
		// Plus for old WebKit, typeof returns "function" for HTML collections
		// (e.g., `typeof document.getElementsByTagName("div") === "function"`). (gh-4756)
		return typeof obj === "function" && typeof obj.nodeType !== "number" &&
			typeof obj.item !== "function";
	};


var isWindow = function isWindow( obj ) {
		return obj != null && obj === obj.window;
	};


var document = window.document;



	var preservedScriptAttributes = {
		type: true,
		src: true,
		nonce: true,
		noModule: true
	};

	function DOMEval( code, node, doc ) {
		doc = doc || document;

		var i, val,
			script = doc.createElement( "script" );

		script.text = code;
		if ( node ) {
			for ( i in preservedScriptAttributes ) {

				// Support: Firefox 64+, Edge 18+
				// Some browsers don't support the "nonce" property on scripts.
				// On the other hand, just using `getAttribute` is not enough as
				// the `nonce` attribute is reset to an empty string whenever it
				// becomes browsing-context connected.
				// See https://github.com/whatwg/html/issues/2369
				// See https://html.spec.whatwg.org/#nonce-attributes
				// The `node.getAttribute` check was added for the sake of
				// `jQuery.globalEval` so that it can fake a nonce-containing node
				// via an object.
				val = node[ i ] || node.getAttribute && node.getAttribute( i );
				if ( val ) {
					script.setAttribute( i, val );
				}
			}
		}
		doc.head.appendChild( script ).parentNode.removeChild( script );
	}


function toType( obj ) {
	if ( obj == null ) {
		return obj + "";
	}

	// Support: Android <=2.3 only (functionish RegExp)
	return typeof obj === "object" || typeof obj === "function" ?
		class2type[ toString.call( obj ) ] || "object" :
		typeof obj;
}
/* global Symbol */
// Defining this global in .eslintrc.json would create a danger of using the global
// unguarded in another place, it seems safer to define global only for this module



var
	version = "3.6.0",

	// Define a local copy of jQuery
	jQuery = function( selector, context ) {

		// The jQuery object is actually just the init constructor 'enhanced'
		// Need init if jQuery is called (just allow error to be thrown if not included)
		return new jQuery.fn.init( selector, context );
	};

jQuery.fn = jQuery.prototype = {

	// The current version of jQuery being used
	jquery: version,

	constructor: jQuery,

	// The default length of a jQuery object is 0
	length: 0,

	toArray: function() {
		return slice.call( this );
	},

	// Get the Nth element in the matched element set OR
	// Get the whole matched element set as a clean array
	get: function( num ) {

		// Return all the elements in a clean array
		if ( num == null ) {
			return slice.call( this );
		}

		// Return just the one element from the set
		return num < 0 ? this[ num + this.length ] : this[ num ];
	},

	// Take an array of elements and push it onto the stack
	// (returning the new matched element set)
	pushStack: function( elems ) {

		// Build a new jQuery matched element set
		var ret = jQuery.merge( this.constructor(), elems );

		// Add the old object onto the stack (as a reference)
		ret.prevObject = this;

		// Return the newly-formed element set
		return ret;
	},

	// Execute a callback for every element in the matched set.
	each: function( callback ) {
		return jQuery.each( this, callback );
	},

	map: function( callback ) {
		return this.pushStack( jQuery.map( this, function( elem, i ) {
			return callback.call( elem, i, elem );
		} ) );
	},

	slice: function() {
		return this.pushStack( slice.apply( this, arguments ) );
	},

	first: function() {
		return this.eq( 0 );
	},

	last: function() {
		return this.eq( -1 );
	},

	even: function() {
		return this.pushStack( jQuery.grep( this, function( _elem, i ) {
			return ( i + 1 ) % 2;
		} ) );
	},

	odd: function() {
		return this.pushStack( jQuery.grep( this, function( _elem, i ) {
			return i % 2;
		} ) );
	},

	eq: function( i ) {
		var len = this.length,
			j = +i + ( i < 0 ? len : 0 );
		return this.pushStack( j >= 0 && j < len ? [ this[ j ] ] : [] );
	},

	end: function() {
		return this.prevObject || this.constructor();
	},

	// For internal use only.
	// Behaves like an Array's method, not like a jQuery method.
	push: push,
	sort: arr.sort,
	splice: arr.splice
};

jQuery.extend = jQuery.fn.extend = function() {
	var options, name, src, copy, copyIsArray, clone,
		target = arguments[ 0 ] || {},
		i = 1,
		length = arguments.length,
		deep = false;

	// Handle a deep copy situation
	if ( typeof target === "boolean" ) {
		deep = target;

		// Skip the boolean and the target
		target = arguments[ i ] || {};
		i++;
	}

	// Handle case when target is a string or something (possible in deep copy)
	if ( typeof target !== "object" && !isFunction( target ) ) {
		target = {};
	}

	// Extend jQuery itself if only one argument is passed
	if ( i === length ) {
		target = this;
		i--;
	}

	for ( ; i < length; i++ ) {

		// Only deal with non-null/undefined values
		if ( ( options = arguments[ i ] ) != null ) {

			// Extend the base object
			for ( name in options ) {
				copy = options[ name ];

				// Prevent Object.prototype pollution
				// Prevent never-ending loop
				if ( name === "__proto__" || target === copy ) {
					continue;
				}

				// Recurse if we're merging plain objects or arrays
				if ( deep && copy && ( jQuery.isPlainObject( copy ) ||
					( copyIsArray = Array.isArray( copy ) ) ) ) {
					src = target[ name ];

					// Ensure proper type for the source value
					if ( copyIsArray && !Array.isArray( src ) ) {
						clone = [];
					} else if ( !copyIsArray && !jQuery.isPlainObject( src ) ) {
						clone = {};
					} else {
						clone = src;
					}
					copyIsArray = false;

					// Never move original objects, clone them
					target[ name ] = jQuery.extend( deep, clone, copy );

				// Don't bring in undefined values
				} else if ( copy !== undefined ) {
					target[ name ] = copy;
				}
			}
		}
	}

	// Return the modified object
	return target;
};

jQuery.extend( {

	// Unique for each copy of jQuery on the page
	expando: "jQuery" + ( version + Math.random() ).replace( /\D/g, "" ),

	// Assume jQuery is ready without the ready module
	isReady: true,

	error: function( msg ) {
		throw new Error( msg );
	},

	noop: function() {},

	isPlainObject: function( obj ) {
		var proto, Ctor;

		// Detect obvious negatives
		// Use toString instead of jQuery.type to catch host objects
		if ( !obj || toString.call( obj ) !== "[object Object]" ) {
			return false;
		}

		proto = getProto( obj );

		// Objects with no prototype (e.g., `Object.create( null )`) are plain
		if ( !proto ) {
			return true;
		}

		// Objects with prototype are plain iff they were constructed by a global Object function
		Ctor = hasOwn.call( proto, "constructor" ) && proto.constructor;
		return typeof Ctor === "function" && fnToString.call( Ctor ) === ObjectFunctionString;
	},

	isEmptyObject: function( obj ) {
		var name;

		for ( name in obj ) {
			return false;
		}
		return true;
	},

	// Evaluates a script in a provided context; falls back to the global one
	// if not specified.
	globalEval: function( code, options, doc ) {
		DOMEval( code, { nonce: options && options.nonce }, doc );
	},

	each: function( obj, callback ) {
		var length, i = 0;

		if ( isArrayLike( obj ) ) {
			length = obj.length;
			for ( ; i < length; i++ ) {
				if ( callback.call( obj[ i ], i, obj[ i ] ) === false ) {
					break;
				}
			}
		} else {
			for ( i in obj ) {
				if ( callback.call( obj[ i ], i, obj[ i ] ) === false ) {
					break;
				}
			}
		}

		return obj;
	},

	// results is for internal usage only
	makeArray: function( arr, results ) {
		var ret = results || [];

		if ( arr != null ) {
			if ( isArrayLike( Object( arr ) ) ) {
				jQuery.merge( ret,
					typeof arr === "string" ?
						[ arr ] : arr
				);
			} else {
				push.call( ret, arr );
			}
		}

		return ret;
	},

	inArray: function( elem, arr, i ) {
		return arr == null ? -1 : indexOf.call( arr, elem, i );
	},

	// Support: Android <=4.0 only, PhantomJS 1 only
	// push.apply(_, arraylike) throws on ancient WebKit
	merge: function( first, second ) {
		var len = +second.length,
			j = 0,
			i = first.length;

		for ( ; j < len; j++ ) {
			first[ i++ ] = second[ j ];
		}

		first.length = i;

		return first;
	},

	grep: function( elems, callback, invert ) {
		var callbackInverse,
			matches = [],
			i = 0,
			length = elems.length,
			callbackExpect = !invert;

		// Go through the array, only saving the items
		// that pass the validator function
		for ( ; i < length; i++ ) {
			callbackInverse = !callback( elems[ i ], i );
			if ( callbackInverse !== callbackExpect ) {
				matches.push( elems[ i ] );
			}
		}

		return matches;
	},

	// arg is for internal usage only
	map: function( elems, callback, arg ) {
		var length, value,
			i = 0,
			ret = [];

		// Go through the array, translating each of the items to their new values
		if ( isArrayLike( elems ) ) {
			length = elems.length;
			for ( ; i < length; i++ ) {
				value = callback( elems[ i ], i, arg );

				if ( value != null ) {
					ret.push( value );
				}
			}

		// Go through every key on the object,
		} else {
			for ( i in elems ) {
				value = callback( elems[ i ], i, arg );

				if ( value != null ) {
					ret.push( value );
				}
			}
		}

		// Flatten any nested arrays
		return flat( ret );
	},

	// A global GUID counter for objects
	guid: 1,

	// jQuery.support is not used in Core but other projects attach their
	// properties to it so it needs to exist.
	support: support
} );

if ( typeof Symbol === "function" ) {
	jQuery.fn[ Symbol.iterator ] = arr[ Symbol.iterator ];
}

// Populate the class2type map
jQuery.each( "Boolean Number String Function Array Date RegExp Object Error Symbol".split( " " ),
	function( _i, name ) {
		class2type[ "[object " + name + "]" ] = name.toLowerCase();
	} );

function isArrayLike( obj ) {

	// Support: real iOS 8.2 only (not reproducible in simulator)
	// `in` check used to prevent JIT error (gh-2145)
	// hasOwn isn't used here due to false negatives
	// regarding Nodelist length in IE
	var length = !!obj && "length" in obj && obj.length,
		type = toType( obj );

	if ( isFunction( obj ) || isWindow( obj ) ) {
		return false;
	}

	return type === "array" || length === 0 ||
		typeof length === "number" && length > 0 && ( length - 1 ) in obj;
}
var Sizzle =
/*!
 * Sizzle CSS Selector Engine v2.3.6
 * https://sizzlejs.com/
 *
 * Copyright JS Foundation and other contributors
 * Released under the MIT license
 * https://js.foundation/
 *
 * Date: 2021-02-16
 */
( function( window ) {
var i,
	support,
	Expr,
	getText,
	isXML,
	tokenize,
	compile,
	select,
	outermostContext,
	sortInput,
	hasDuplicate,

	// Local document vars
	setDocument,
	document,
	docElem,
	documentIsHTML,
	rbuggyQSA,
	rbuggyMatches,
	matches,
	contains,

	// Instance-specific data
	expando = "sizzle" + 1 * new Date(),
	preferredDoc = window.document,
	dirruns = 0,
	done = 0,
	classCache = createCache(),
	tokenCache = createCache(),
	compilerCache = createCache(),
	nonnativeSelectorCache = createCache(),
	sortOrder = function( a, b ) {
		if ( a === b ) {
			hasDuplicate = true;
		}
		return 0;
	},

	// Instance methods
	hasOwn = ( {} ).hasOwnProperty,
	arr = [],
	pop = arr.pop,
	pushNative = arr.push,
	push = arr.push,
	slice = arr.slice,

	// Use a stripped-down indexOf as it's faster than native
	// https://jsperf.com/thor-indexof-vs-for/5
	indexOf = function( list, elem ) {
		var i = 0,
			len = list.length;
		for ( ; i < len; i++ ) {
			if ( list[ i ] === elem ) {
				return i;
			}
		}
		return -1;
	},

	booleans = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|" +
		"ismap|loop|multiple|open|readonly|required|scoped",

	// Regular expressions

	// http://www.w3.org/TR/css3-selectors/#whitespace
	whitespace = "[\\x20\\t\\r\\n\\f]",

	// https://www.w3.org/TR/css-syntax-3/#ident-token-diagram
	identifier = "(?:\\\\[\\da-fA-F]{1,6}" + whitespace +
		"?|\\\\[^\\r\\n\\f]|[\\w-]|[^\0-\\x7f])+",

	// Attribute selectors: http://www.w3.org/TR/selectors/#attribute-selectors
	attributes = "\\[" + whitespace + "*(" + identifier + ")(?:" + whitespace +

		// Operator (capture 2)
		"*([*^$|!~]?=)" + whitespace +

		// "Attribute values must be CSS identifiers [capture 5]
		// or strings [capture 3 or capture 4]"
		"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + identifier + "))|)" +
		whitespace + "*\\]",

	pseudos = ":(" + identifier + ")(?:\\((" +

		// To reduce the number of selectors needing tokenize in the preFilter, prefer arguments:
		// 1. quoted (capture 3; capture 4 or capture 5)
		"('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|" +

		// 2. simple (capture 6)
		"((?:\\\\.|[^\\\\()[\\]]|" + attributes + ")*)|" +

		// 3. anything else (capture 2)
		".*" +
		")\\)|)",

	// Leading and non-escaped trailing whitespace, capturing some non-whitespace characters preceding the latter
	rwhitespace = new RegExp( whitespace + "+", "g" ),
	rtrim = new RegExp( "^" + whitespace + "+|((?:^|[^\\\\])(?:\\\\.)*)" +
		whitespace + "+$", "g" ),

	rcomma = new RegExp( "^" + whitespace + "*," + whitespace + "*" ),
	rcombinators = new RegExp( "^" + whitespace + "*([>+~]|" + whitespace + ")" + whitespace +
		"*" ),
	rdescend = new RegExp( whitespace + "|>" ),

	rpseudo = new RegExp( pseudos ),
	ridentifier = new RegExp( "^" + identifier + "$" ),

	matchExpr = {
		"ID": new RegExp( "^#(" + identifier + ")" ),
		"CLASS": new RegExp( "^\\.(" + identifier + ")" ),
		"TAG": new RegExp( "^(" + identifier + "|[*])" ),
		"ATTR": new RegExp( "^" + attributes ),
		"PSEUDO": new RegExp( "^" + pseudos ),
		"CHILD": new RegExp( "^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" +
			whitespace + "*(even|odd|(([+-]|)(\\d*)n|)" + whitespace + "*(?:([+-]|)" +
			whitespace + "*(\\d+)|))" + whitespace + "*\\)|)", "i" ),
		"bool": new RegExp( "^(?:" + booleans + ")$", "i" ),

		// For use in libraries implementing .is()
		// We use this for POS matching in `select`
		"needsContext": new RegExp( "^" + whitespace +
			"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + whitespace +
			"*((?:-\\d)?\\d*)" + whitespace + "*\\)|)(?=[^-]|$)", "i" )
	},

	rhtml = /HTML$/i,
	rinputs = /^(?:input|select|textarea|button)$/i,
	rheader = /^h\d$/i,

	rnative = /^[^{]+\{\s*\[native \w/,

	// Easily-parseable/retrievable ID or TAG or CLASS selectors
	rquickExpr = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,

	rsibling = /[+~]/,

	// CSS escapes
	// http://www.w3.org/TR/CSS21/syndata.html#escaped-characters
	runescape = new RegExp( "\\\\[\\da-fA-F]{1,6}" + whitespace + "?|\\\\([^\\r\\n\\f])", "g" ),
	funescape = function( escape, nonHex ) {
		var high = "0x" + escape.slice( 1 ) - 0x10000;

		return nonHex ?

			// Strip the backslash prefix from a non-hex escape sequence
			nonHex :

			// Replace a hexadecimal escape sequence with the encoded Unicode code point
			// Support: IE <=11+
			// For values outside the Basic Multilingual Plane (BMP), manually construct a
			// surrogate pair
			high < 0 ?
				String.fromCharCode( high + 0x10000 ) :
				String.fromCharCode( high >> 10 | 0xD800, high & 0x3FF | 0xDC00 );
	},

	// CSS string/identifier serialization
	// https://drafts.csswg.org/cssom/#common-serializing-idioms
	rcssescape = /([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,
	fcssescape = function( ch, asCodePoint ) {
		if ( asCodePoint ) {

			// U+0000 NULL becomes U+FFFD REPLACEMENT CHARACTER
			if ( ch === "\0" ) {
				return "\uFFFD";
			}

			// Control characters and (dependent upon position) numbers get escaped as code points
			return ch.slice( 0, -1 ) + "\\" +
				ch.charCodeAt( ch.length - 1 ).toString( 16 ) + " ";
		}

		// Other potentially-special ASCII characters get backslash-escaped
		return "\\" + ch;
	},

	// Used for iframes
	// See setDocument()
	// Removing the function wrapper causes a "Permission Denied"
	// error in IE
	unloadHandler = function() {
		setDocument();
	},

	inDisabledFieldset = addCombinator(
		function( elem ) {
			return elem.disabled === true && elem.nodeName.toLowerCase() === "fieldset";
		},
		{ dir: "parentNode", next: "legend" }
	);

// Optimize for push.apply( _, NodeList )
try {
	push.apply(
		( arr = slice.call( preferredDoc.childNodes ) ),
		preferredDoc.childNodes
	);

	// Support: Android<4.0
	// Detect silently failing push.apply
	// eslint-disable-next-line no-unused-expressions
	arr[ preferredDoc.childNodes.length ].nodeType;
} catch ( e ) {
	push = { apply: arr.length ?

		// Leverage slice if possible
		function( target, els ) {
			pushNative.apply( target, slice.call( els ) );
		} :

		// Support: IE<9
		// Otherwise append directly
		function( target, els ) {
			var j = target.length,
				i = 0;

			// Can't trust NodeList.length
			while ( ( target[ j++ ] = els[ i++ ] ) ) {}
			target.length = j - 1;
		}
	};
}

function Sizzle( selector, context, results, seed ) {
	var m, i, elem, nid, match, groups, newSelector,
		newContext = context && context.ownerDocument,

		// nodeType defaults to 9, since context defaults to document
		nodeType = context ? context.nodeType : 9;

	results = results || [];

	// Return early from calls with invalid selector or context
	if ( typeof selector !== "string" || !selector ||
		nodeType !== 1 && nodeType !== 9 && nodeType !== 11 ) {

		return results;
	}

	// Try to shortcut find operations (as opposed to filters) in HTML documents
	if ( !seed ) {
		setDocument( context );
		context = context || document;

		if ( documentIsHTML ) {

			// If the selector is sufficiently simple, try using a "get*By*" DOM method
			// (excepting DocumentFragment context, where the methods don't exist)
			if ( nodeType !== 11 && ( match = rquickExpr.exec( selector ) ) ) {

				// ID selector
				if ( ( m = match[ 1 ] ) ) {

					// Document context
					if ( nodeType === 9 ) {
						if ( ( elem = context.getElementById( m ) ) ) {

							// Support: IE, Opera, Webkit
							// TODO: identify versions
							// getElementById can match elements by name instead of ID
							if ( elem.id === m ) {
								results.push( elem );
								return results;
							}
						} else {
							return results;
						}

					// Element context
					} else {

						// Support: IE, Opera, Webkit
						// TODO: identify versions
						// getElementById can match elements by name instead of ID
						if ( newContext && ( elem = newContext.getElementById( m ) ) &&
							contains( context, elem ) &&
							elem.id === m ) {

							results.push( elem );
							return results;
						}
					}

				// Type selector
				} else if ( match[ 2 ] ) {
					push.apply( results, context.getElementsByTagName( selector ) );
					return results;

				// Class selector
				} else if ( ( m = match[ 3 ] ) && support.getElementsByClassName &&
					context.getElementsByClassName ) {

					push.apply( results, context.getElementsByClassName( m ) );
					return results;
				}
			}

			// Take advantage of querySelectorAll
			if ( support.qsa &&
				!nonnativeSelectorCache[ selector + " " ] &&
				( !rbuggyQSA || !rbuggyQSA.test( selector ) ) &&

				// Support: IE 8 only
				// Exclude object elements
				( nodeType !== 1 || context.nodeName.toLowerCase() !== "object" ) ) {

				newSelector = selector;
				newContext = context;

				// qSA considers elements outside a scoping root when evaluating child or
				// descendant combinators, which is not what we want.
				// In such cases, we work around the behavior by prefixing every selector in the
				// list with an ID selector referencing the scope context.
				// The technique has to be used as well when a leading combinator is used
				// as such selectors are not recognized by querySelectorAll.
				// Thanks to Andrew Dupont for this technique.
				if ( nodeType === 1 &&
					( rdescend.test( selector ) || rcombinators.test( selector ) ) ) {

					// Expand context for sibling selectors
					newContext = rsibling.test( selector ) && testContext( context.parentNode ) ||
						context;

					// We can use :scope instead of the ID hack if the browser
					// supports it & if we're not changing the context.
					if ( newContext !== context || !support.scope ) {

						// Capture the context ID, setting it first if necessary
						if ( ( nid = context.getAttribute( "id" ) ) ) {
							nid = nid.replace( rcssescape, fcssescape );
						} else {
							context.setAttribute( "id", ( nid = expando ) );
						}
					}

					// Prefix every selector in the list
					groups = tokenize( selector );
					i = groups.length;
					while ( i-- ) {
						groups[ i ] = ( nid ? "#" + nid : ":scope" ) + " " +
							toSelector( groups[ i ] );
					}
					newSelector = groups.join( "," );
				}

				try {
					push.apply( results,
						newContext.querySelectorAll( newSelector )
					);
					return results;
				} catch ( qsaError ) {
					nonnativeSelectorCache( selector, true );
				} finally {
					if ( nid === expando ) {
						context.removeAttribute( "id" );
					}
				}
			}
		}
	}

	// All others
	return select( selector.replace( rtrim, "$1" ), context, results, seed );
}

/**
 * Create key-value caches of limited size
 * @returns {function(string, object)} Returns the Object data after storing it on itself with
 *	property name the (space-suffixed) string and (if the cache is larger than Expr.cacheLength)
 *	deleting the oldest entry
 */
function createCache() {
	var keys = [];

	function cache( key, value ) {

		// Use (key + " ") to avoid collision with native prototype properties (see Issue #157)
		if ( keys.push( key + " " ) > Expr.cacheLength ) {

			// Only keep the most recent entries
			delete cache[ keys.shift() ];
		}
		return ( cache[ key + " " ] = value );
	}
	return cache;
}

/**
 * Mark a function for special use by Sizzle
 * @param {Function} fn The function to mark
 */
function markFunction( fn ) {
	fn[ expando ] = true;
	return fn;
}

/**
 * Support testing using an element
 * @param {Function} fn Passed the created element and returns a boolean result
 */
function assert( fn ) {
	var el = document.createElement( "fieldset" );

	try {
		return !!fn( el );
	} catch ( e ) {
		return false;
	} finally {

		// Remove from its parent by default
		if ( el.parentNode ) {
			el.parentNode.removeChild( el );
		}

		// release memory in IE
		el = null;
	}
}

/**
 * Adds the same handler for all of the specified attrs
 * @param {String} attrs Pipe-separated list of attributes
 * @param {Function} handler The method that will be applied
 */
function addHandle( attrs, handler ) {
	var arr = attrs.split( "|" ),
		i = arr.length;

	while ( i-- ) {
		Expr.attrHandle[ arr[ i ] ] = handler;
	}
}

/**
 * Checks document order of two siblings
 * @param {Element} a
 * @param {Element} b
 * @returns {Number} Returns less than 0 if a precedes b, greater than 0 if a follows b
 */
function siblingCheck( a, b ) {
	var cur = b && a,
		diff = cur && a.nodeType === 1 && b.nodeType === 1 &&
			a.sourceIndex - b.sourceIndex;

	// Use IE sourceIndex if available on both nodes
	if ( diff ) {
		return diff;
	}

	// Check if b follows a
	if ( cur ) {
		while ( ( cur = cur.nextSibling ) ) {
			if ( cur === b ) {
				return -1;
			}
		}
	}

	return a ? 1 : -1;
}

/**
 * Returns a function to use in pseudos for input types
 * @param {String} type
 */
function createInputPseudo( type ) {
	return function( elem ) {
		var name = elem.nodeName.toLowerCase();
		return name === "input" && elem.type === type;
	};
}

/**
 * Returns a function to use in pseudos for buttons
 * @param {String} type
 */
function createButtonPseudo( type ) {
	return function( elem ) {
		var name = elem.nodeName.toLowerCase();
		return ( name === "input" || name === "button" ) && elem.type === type;
	};
}

/**
 * Returns a function to use in pseudos for :enabled/:disabled
 * @param {Boolean} disabled true for :disabled; false for :enabled
 */
function createDisabledPseudo( disabled ) {

	// Known :disabled false positives: fieldset[disabled] > legend:nth-of-type(n+2) :can-disable
	return function( elem ) {

		// Only certain elements can match :enabled or :disabled
		// https://html.spec.whatwg.org/multipage/scripting.html#selector-enabled
		// https://html.spec.whatwg.org/multipage/scripting.html#selector-disabled
		if ( "form" in elem ) {

			// Check for inherited disabledness on relevant non-disabled elements:
			// * listed form-associated elements in a disabled fieldset
			//   https://html.spec.whatwg.org/multipage/forms.html#category-listed
			//   https://html.spec.whatwg.org/multipage/forms.html#concept-fe-disabled
			// * option elements in a disabled optgroup
			//   https://html.spec.whatwg.org/multipage/forms.html#concept-option-disabled
			// All such elements have a "form" property.
			if ( elem.parentNode && elem.disabled === false ) {

				// Option elements defer to a parent optgroup if present
				if ( "label" in elem ) {
					if ( "label" in elem.parentNode ) {
						return elem.parentNode.disabled === disabled;
					} else {
						return elem.disabled === disabled;
					}
				}

				// Support: IE 6 - 11
				// Use the isDisabled shortcut property to check for disabled fieldset ancestors
				return elem.isDisabled === disabled ||

					// Where there is no isDisabled, check manually
					/* jshint -W018 */
					elem.isDisabled !== !disabled &&
					inDisabledFieldset( elem ) === disabled;
			}

			return elem.disabled === disabled;

		// Try to winnow out elements that can't be disabled before trusting the disabled property.
		// Some victims get caught in our net (label, legend, menu, track), but it shouldn't
		// even exist on them, let alone have a boolean value.
		} else if ( "label" in elem ) {
			return elem.disabled === disabled;
		}

		// Remaining elements are neither :enabled nor :disabled
		return false;
	};
}

/**
 * Returns a function to use in pseudos for positionals
 * @param {Function} fn
 */
function createPositionalPseudo( fn ) {
	return markFunction( function( argument ) {
		argument = +argument;
		return markFunction( function( seed, matches ) {
			var j,
				matchIndexes = fn( [], seed.length, argument ),
				i = matchIndexes.length;

			// Match elements found at the specified indexes
			while ( i-- ) {
				if ( seed[ ( j = matchIndexes[ i ] ) ] ) {
					seed[ j ] = !( matches[ j ] = seed[ j ] );
				}
			}
		} );
	} );
}

/**
 * Checks a node for validity as a Sizzle context
 * @param {Element|Object=} context
 * @returns {Element|Object|Boolean} The input node if acceptable, otherwise a falsy value
 */
function testContext( context ) {
	return context && typeof context.getElementsByTagName !== "undefined" && context;
}

// Expose support vars for convenience
support = Sizzle.support = {};

/**
 * Detects XML nodes
 * @param {Element|Object} elem An element or a document
 * @returns {Boolean} True iff elem is a non-HTML XML node
 */
isXML = Sizzle.isXML = function( elem ) {
	var namespace = elem && elem.namespaceURI,
		docElem = elem && ( elem.ownerDocument || elem ).documentElement;

	// Support: IE <=8
	// Assume HTML when documentElement doesn't yet exist, such as inside loading iframes
	// https://bugs.jquery.com/ticket/4833
	return !rhtml.test( namespace || docElem && docElem.nodeName || "HTML" );
};

/**
 * Sets document-related variables once based on the current document
 * @param {Element|Object} [doc] An element or document object to use to set the document
 * @returns {Object} Returns the current document
 */
setDocument = Sizzle.setDocument = function( node ) {
	var hasCompare, subWindow,
		doc = node ? node.ownerDocument || node : preferredDoc;

	// Return early if doc is invalid or already selected
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( doc == document || doc.nodeType !== 9 || !doc.documentElement ) {
		return document;
	}

	// Update global variables
	document = doc;
	docElem = document.documentElement;
	documentIsHTML = !isXML( document );

	// Support: IE 9 - 11+, Edge 12 - 18+
	// Accessing iframe documents after unload throws "permission denied" errors (jQuery #13936)
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( preferredDoc != document &&
		( subWindow = document.defaultView ) && subWindow.top !== subWindow ) {

		// Support: IE 11, Edge
		if ( subWindow.addEventListener ) {
			subWindow.addEventListener( "unload", unloadHandler, false );

		// Support: IE 9 - 10 only
		} else if ( subWindow.attachEvent ) {
			subWindow.attachEvent( "onunload", unloadHandler );
		}
	}

	// Support: IE 8 - 11+, Edge 12 - 18+, Chrome <=16 - 25 only, Firefox <=3.6 - 31 only,
	// Safari 4 - 5 only, Opera <=11.6 - 12.x only
	// IE/Edge & older browsers don't support the :scope pseudo-class.
	// Support: Safari 6.0 only
	// Safari 6.0 supports :scope but it's an alias of :root there.
	support.scope = assert( function( el ) {
		docElem.appendChild( el ).appendChild( document.createElement( "div" ) );
		return typeof el.querySelectorAll !== "undefined" &&
			!el.querySelectorAll( ":scope fieldset div" ).length;
	} );

	/* Attributes
	---------------------------------------------------------------------- */

	// Support: IE<8
	// Verify that getAttribute really returns attributes and not properties
	// (excepting IE8 booleans)
	support.attributes = assert( function( el ) {
		el.className = "i";
		return !el.getAttribute( "className" );
	} );

	/* getElement(s)By*
	---------------------------------------------------------------------- */

	// Check if getElementsByTagName("*") returns only elements
	support.getElementsByTagName = assert( function( el ) {
		el.appendChild( document.createComment( "" ) );
		return !el.getElementsByTagName( "*" ).length;
	} );

	// Support: IE<9
	support.getElementsByClassName = rnative.test( document.getElementsByClassName );

	// Support: IE<10
	// Check if getElementById returns elements by name
	// The broken getElementById methods don't pick up programmatically-set names,
	// so use a roundabout getElementsByName test
	support.getById = assert( function( el ) {
		docElem.appendChild( el ).id = expando;
		return !document.getElementsByName || !document.getElementsByName( expando ).length;
	} );

	// ID filter and find
	if ( support.getById ) {
		Expr.filter[ "ID" ] = function( id ) {
			var attrId = id.replace( runescape, funescape );
			return function( elem ) {
				return elem.getAttribute( "id" ) === attrId;
			};
		};
		Expr.find[ "ID" ] = function( id, context ) {
			if ( typeof context.getElementById !== "undefined" && documentIsHTML ) {
				var elem = context.getElementById( id );
				return elem ? [ elem ] : [];
			}
		};
	} else {
		Expr.filter[ "ID" ] =  function( id ) {
			var attrId = id.replace( runescape, funescape );
			return function( elem ) {
				var node = typeof elem.getAttributeNode !== "undefined" &&
					elem.getAttributeNode( "id" );
				return node && node.value === attrId;
			};
		};

		// Support: IE 6 - 7 only
		// getElementById is not reliable as a find shortcut
		Expr.find[ "ID" ] = function( id, context ) {
			if ( typeof context.getElementById !== "undefined" && documentIsHTML ) {
				var node, i, elems,
					elem = context.getElementById( id );

				if ( elem ) {

					// Verify the id attribute
					node = elem.getAttributeNode( "id" );
					if ( node && node.value === id ) {
						return [ elem ];
					}

					// Fall back on getElementsByName
					elems = context.getElementsByName( id );
					i = 0;
					while ( ( elem = elems[ i++ ] ) ) {
						node = elem.getAttributeNode( "id" );
						if ( node && node.value === id ) {
							return [ elem ];
						}
					}
				}

				return [];
			}
		};
	}

	// Tag
	Expr.find[ "TAG" ] = support.getElementsByTagName ?
		function( tag, context ) {
			if ( typeof context.getElementsByTagName !== "undefined" ) {
				return context.getElementsByTagName( tag );

			// DocumentFragment nodes don't have gEBTN
			} else if ( support.qsa ) {
				return context.querySelectorAll( tag );
			}
		} :

		function( tag, context ) {
			var elem,
				tmp = [],
				i = 0,

				// By happy coincidence, a (broken) gEBTN appears on DocumentFragment nodes too
				results = context.getElementsByTagName( tag );

			// Filter out possible comments
			if ( tag === "*" ) {
				while ( ( elem = results[ i++ ] ) ) {
					if ( elem.nodeType === 1 ) {
						tmp.push( elem );
					}
				}

				return tmp;
			}
			return results;
		};

	// Class
	Expr.find[ "CLASS" ] = support.getElementsByClassName && function( className, context ) {
		if ( typeof context.getElementsByClassName !== "undefined" && documentIsHTML ) {
			return context.getElementsByClassName( className );
		}
	};

	/* QSA/matchesSelector
	---------------------------------------------------------------------- */

	// QSA and matchesSelector support

	// matchesSelector(:active) reports false when true (IE9/Opera 11.5)
	rbuggyMatches = [];

	// qSa(:focus) reports false when true (Chrome 21)
	// We allow this because of a bug in IE8/9 that throws an error
	// whenever `document.activeElement` is accessed on an iframe
	// So, we allow :focus to pass through QSA all the time to avoid the IE error
	// See https://bugs.jquery.com/ticket/13378
	rbuggyQSA = [];

	if ( ( support.qsa = rnative.test( document.querySelectorAll ) ) ) {

		// Build QSA regex
		// Regex strategy adopted from Diego Perini
		assert( function( el ) {

			var input;

			// Select is set to empty string on purpose
			// This is to test IE's treatment of not explicitly
			// setting a boolean content attribute,
			// since its presence should be enough
			// https://bugs.jquery.com/ticket/12359
			docElem.appendChild( el ).innerHTML = "<a id='" + expando + "'></a>" +
				"<select id='" + expando + "-\r\\' msallowcapture=''>" +
				"<option selected=''></option></select>";

			// Support: IE8, Opera 11-12.16
			// Nothing should be selected when empty strings follow ^= or $= or *=
			// The test attribute must be unknown in Opera but "safe" for WinRT
			// https://msdn.microsoft.com/en-us/library/ie/hh465388.aspx#attribute_section
			if ( el.querySelectorAll( "[msallowcapture^='']" ).length ) {
				rbuggyQSA.push( "[*^$]=" + whitespace + "*(?:''|\"\")" );
			}

			// Support: IE8
			// Boolean attributes and "value" are not treated correctly
			if ( !el.querySelectorAll( "[selected]" ).length ) {
				rbuggyQSA.push( "\\[" + whitespace + "*(?:value|" + booleans + ")" );
			}

			// Support: Chrome<29, Android<4.4, Safari<7.0+, iOS<7.0+, PhantomJS<1.9.8+
			if ( !el.querySelectorAll( "[id~=" + expando + "-]" ).length ) {
				rbuggyQSA.push( "~=" );
			}

			// Support: IE 11+, Edge 15 - 18+
			// IE 11/Edge don't find elements on a `[name='']` query in some cases.
			// Adding a temporary attribute to the document before the selection works
			// around the issue.
			// Interestingly, IE 10 & older don't seem to have the issue.
			input = document.createElement( "input" );
			input.setAttribute( "name", "" );
			el.appendChild( input );
			if ( !el.querySelectorAll( "[name='']" ).length ) {
				rbuggyQSA.push( "\\[" + whitespace + "*name" + whitespace + "*=" +
					whitespace + "*(?:''|\"\")" );
			}

			// Webkit/Opera - :checked should return selected option elements
			// http://www.w3.org/TR/2011/REC-css3-selectors-20110929/#checked
			// IE8 throws error here and will not see later tests
			if ( !el.querySelectorAll( ":checked" ).length ) {
				rbuggyQSA.push( ":checked" );
			}

			// Support: Safari 8+, iOS 8+
			// https://bugs.webkit.org/show_bug.cgi?id=136851
			// In-page `selector#id sibling-combinator selector` fails
			if ( !el.querySelectorAll( "a#" + expando + "+*" ).length ) {
				rbuggyQSA.push( ".#.+[+~]" );
			}

			// Support: Firefox <=3.6 - 5 only
			// Old Firefox doesn't throw on a badly-escaped identifier.
			el.querySelectorAll( "\\\f" );
			rbuggyQSA.push( "[\\r\\n\\f]" );
		} );

		assert( function( el ) {
			el.innerHTML = "<a href='' disabled='disabled'></a>" +
				"<select disabled='disabled'><option/></select>";

			// Support: Windows 8 Native Apps
			// The type and name attributes are restricted during .innerHTML assignment
			var input = document.createElement( "input" );
			input.setAttribute( "type", "hidden" );
			el.appendChild( input ).setAttribute( "name", "D" );

			// Support: IE8
			// Enforce case-sensitivity of name attribute
			if ( el.querySelectorAll( "[name=d]" ).length ) {
				rbuggyQSA.push( "name" + whitespace + "*[*^$|!~]?=" );
			}

			// FF 3.5 - :enabled/:disabled and hidden elements (hidden elements are still enabled)
			// IE8 throws error here and will not see later tests
			if ( el.querySelectorAll( ":enabled" ).length !== 2 ) {
				rbuggyQSA.push( ":enabled", ":disabled" );
			}

			// Support: IE9-11+
			// IE's :disabled selector does not pick up the children of disabled fieldsets
			docElem.appendChild( el ).disabled = true;
			if ( el.querySelectorAll( ":disabled" ).length !== 2 ) {
				rbuggyQSA.push( ":enabled", ":disabled" );
			}

			// Support: Opera 10 - 11 only
			// Opera 10-11 does not throw on post-comma invalid pseudos
			el.querySelectorAll( "*,:x" );
			rbuggyQSA.push( ",.*:" );
		} );
	}

	if ( ( support.matchesSelector = rnative.test( ( matches = docElem.matches ||
		docElem.webkitMatchesSelector ||
		docElem.mozMatchesSelector ||
		docElem.oMatchesSelector ||
		docElem.msMatchesSelector ) ) ) ) {

		assert( function( el ) {

			// Check to see if it's possible to do matchesSelector
			// on a disconnected node (IE 9)
			support.disconnectedMatch = matches.call( el, "*" );

			// This should fail with an exception
			// Gecko does not error, returns false instead
			matches.call( el, "[s!='']:x" );
			rbuggyMatches.push( "!=", pseudos );
		} );
	}

	rbuggyQSA = rbuggyQSA.length && new RegExp( rbuggyQSA.join( "|" ) );
	rbuggyMatches = rbuggyMatches.length && new RegExp( rbuggyMatches.join( "|" ) );

	/* Contains
	---------------------------------------------------------------------- */
	hasCompare = rnative.test( docElem.compareDocumentPosition );

	// Element contains another
	// Purposefully self-exclusive
	// As in, an element does not contain itself
	contains = hasCompare || rnative.test( docElem.contains ) ?
		function( a, b ) {
			var adown = a.nodeType === 9 ? a.documentElement : a,
				bup = b && b.parentNode;
			return a === bup || !!( bup && bup.nodeType === 1 && (
				adown.contains ?
					adown.contains( bup ) :
					a.compareDocumentPosition && a.compareDocumentPosition( bup ) & 16
			) );
		} :
		function( a, b ) {
			if ( b ) {
				while ( ( b = b.parentNode ) ) {
					if ( b === a ) {
						return true;
					}
				}
			}
			return false;
		};

	/* Sorting
	---------------------------------------------------------------------- */

	// Document order sorting
	sortOrder = hasCompare ?
	function( a, b ) {

		// Flag for duplicate removal
		if ( a === b ) {
			hasDuplicate = true;
			return 0;
		}

		// Sort on method existence if only one input has compareDocumentPosition
		var compare = !a.compareDocumentPosition - !b.compareDocumentPosition;
		if ( compare ) {
			return compare;
		}

		// Calculate position if both inputs belong to the same document
		// Support: IE 11+, Edge 17 - 18+
		// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
		// two documents; shallow comparisons work.
		// eslint-disable-next-line eqeqeq
		compare = ( a.ownerDocument || a ) == ( b.ownerDocument || b ) ?
			a.compareDocumentPosition( b ) :

			// Otherwise we know they are disconnected
			1;

		// Disconnected nodes
		if ( compare & 1 ||
			( !support.sortDetached && b.compareDocumentPosition( a ) === compare ) ) {

			// Choose the first element that is related to our preferred document
			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			// eslint-disable-next-line eqeqeq
			if ( a == document || a.ownerDocument == preferredDoc &&
				contains( preferredDoc, a ) ) {
				return -1;
			}

			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			// eslint-disable-next-line eqeqeq
			if ( b == document || b.ownerDocument == preferredDoc &&
				contains( preferredDoc, b ) ) {
				return 1;
			}

			// Maintain original order
			return sortInput ?
				( indexOf( sortInput, a ) - indexOf( sortInput, b ) ) :
				0;
		}

		return compare & 4 ? -1 : 1;
	} :
	function( a, b ) {

		// Exit early if the nodes are identical
		if ( a === b ) {
			hasDuplicate = true;
			return 0;
		}

		var cur,
			i = 0,
			aup = a.parentNode,
			bup = b.parentNode,
			ap = [ a ],
			bp = [ b ];

		// Parentless nodes are either documents or disconnected
		if ( !aup || !bup ) {

			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			/* eslint-disable eqeqeq */
			return a == document ? -1 :
				b == document ? 1 :
				/* eslint-enable eqeqeq */
				aup ? -1 :
				bup ? 1 :
				sortInput ?
				( indexOf( sortInput, a ) - indexOf( sortInput, b ) ) :
				0;

		// If the nodes are siblings, we can do a quick check
		} else if ( aup === bup ) {
			return siblingCheck( a, b );
		}

		// Otherwise we need full lists of their ancestors for comparison
		cur = a;
		while ( ( cur = cur.parentNode ) ) {
			ap.unshift( cur );
		}
		cur = b;
		while ( ( cur = cur.parentNode ) ) {
			bp.unshift( cur );
		}

		// Walk down the tree looking for a discrepancy
		while ( ap[ i ] === bp[ i ] ) {
			i++;
		}

		return i ?

			// Do a sibling check if the nodes have a common ancestor
			siblingCheck( ap[ i ], bp[ i ] ) :

			// Otherwise nodes in our document sort first
			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			/* eslint-disable eqeqeq */
			ap[ i ] == preferredDoc ? -1 :
			bp[ i ] == preferredDoc ? 1 :
			/* eslint-enable eqeqeq */
			0;
	};

	return document;
};

Sizzle.matches = function( expr, elements ) {
	return Sizzle( expr, null, null, elements );
};

Sizzle.matchesSelector = function( elem, expr ) {
	setDocument( elem );

	if ( support.matchesSelector && documentIsHTML &&
		!nonnativeSelectorCache[ expr + " " ] &&
		( !rbuggyMatches || !rbuggyMatches.test( expr ) ) &&
		( !rbuggyQSA     || !rbuggyQSA.test( expr ) ) ) {

		try {
			var ret = matches.call( elem, expr );

			// IE 9's matchesSelector returns false on disconnected nodes
			if ( ret || support.disconnectedMatch ||

				// As well, disconnected nodes are said to be in a document
				// fragment in IE 9
				elem.document && elem.document.nodeType !== 11 ) {
				return ret;
			}
		} catch ( e ) {
			nonnativeSelectorCache( expr, true );
		}
	}

	return Sizzle( expr, document, null, [ elem ] ).length > 0;
};

Sizzle.contains = function( context, elem ) {

	// Set document vars if needed
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( ( context.ownerDocument || context ) != document ) {
		setDocument( context );
	}
	return contains( context, elem );
};

Sizzle.attr = function( elem, name ) {

	// Set document vars if needed
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( ( elem.ownerDocument || elem ) != document ) {
		setDocument( elem );
	}

	var fn = Expr.attrHandle[ name.toLowerCase() ],

		// Don't get fooled by Object.prototype properties (jQuery #13807)
		val = fn && hasOwn.call( Expr.attrHandle, name.toLowerCase() ) ?
			fn( elem, name, !documentIsHTML ) :
			undefined;

	return val !== undefined ?
		val :
		support.attributes || !documentIsHTML ?
			elem.getAttribute( name ) :
			( val = elem.getAttributeNode( name ) ) && val.specified ?
				val.value :
				null;
};

Sizzle.escape = function( sel ) {
	return ( sel + "" ).replace( rcssescape, fcssescape );
};

Sizzle.error = function( msg ) {
	throw new Error( "Syntax error, unrecognized expression: " + msg );
};

/**
 * Document sorting and removing duplicates
 * @param {ArrayLike} results
 */
Sizzle.uniqueSort = function( results ) {
	var elem,
		duplicates = [],
		j = 0,
		i = 0;

	// Unless we *know* we can detect duplicates, assume their presence
	hasDuplicate = !support.detectDuplicates;
	sortInput = !support.sortStable && results.slice( 0 );
	results.sort( sortOrder );

	if ( hasDuplicate ) {
		while ( ( elem = results[ i++ ] ) ) {
			if ( elem === results[ i ] ) {
				j = duplicates.push( i );
			}
		}
		while ( j-- ) {
			results.splice( duplicates[ j ], 1 );
		}
	}

	// Clear input after sorting to release objects
	// See https://github.com/jquery/sizzle/pull/225
	sortInput = null;

	return results;
};

/**
 * Utility function for retrieving the text value of an array of DOM nodes
 * @param {Array|Element} elem
 */
getText = Sizzle.getText = function( elem ) {
	var node,
		ret = "",
		i = 0,
		nodeType = elem.nodeType;

	if ( !nodeType ) {

		// If no nodeType, this is expected to be an array
		while ( ( node = elem[ i++ ] ) ) {

			// Do not traverse comment nodes
			ret += getText( node );
		}
	} else if ( nodeType === 1 || nodeType === 9 || nodeType === 11 ) {

		// Use textContent for elements
		// innerText usage removed for consistency of new lines (jQuery #11153)
		if ( typeof elem.textContent === "string" ) {
			return elem.textContent;
		} else {

			// Traverse its children
			for ( elem = elem.firstChild; elem; elem = elem.nextSibling ) {
				ret += getText( elem );
			}
		}
	} else if ( nodeType === 3 || nodeType === 4 ) {
		return elem.nodeValue;
	}

	// Do not include comment or processing instruction nodes

	return ret;
};

Expr = Sizzle.selectors = {

	// Can be adjusted by the user
	cacheLength: 50,

	createPseudo: markFunction,

	match: matchExpr,

	attrHandle: {},

	find: {},

	relative: {
		">": { dir: "parentNode", first: true },
		" ": { dir: "parentNode" },
		"+": { dir: "previousSibling", first: true },
		"~": { dir: "previousSibling" }
	},

	preFilter: {
		"ATTR": function( match ) {
			match[ 1 ] = match[ 1 ].replace( runescape, funescape );

			// Move the given value to match[3] whether quoted or unquoted
			match[ 3 ] = ( match[ 3 ] || match[ 4 ] ||
				match[ 5 ] || "" ).replace( runescape, funescape );

			if ( match[ 2 ] === "~=" ) {
				match[ 3 ] = " " + match[ 3 ] + " ";
			}

			return match.slice( 0, 4 );
		},

		"CHILD": function( match ) {

			/* matches from matchExpr["CHILD"]
				1 type (only|nth|...)
				2 what (child|of-type)
				3 argument (even|odd|\d*|\d*n([+-]\d+)?|...)
				4 xn-component of xn+y argument ([+-]?\d*n|)
				5 sign of xn-component
				6 x of xn-component
				7 sign of y-component
				8 y of y-component
			*/
			match[ 1 ] = match[ 1 ].toLowerCase();

			if ( match[ 1 ].slice( 0, 3 ) === "nth" ) {

				// nth-* requires argument
				if ( !match[ 3 ] ) {
					Sizzle.error( match[ 0 ] );
				}

				// numeric x and y parameters for Expr.filter.CHILD
				// remember that false/true cast respectively to 0/1
				match[ 4 ] = +( match[ 4 ] ?
					match[ 5 ] + ( match[ 6 ] || 1 ) :
					2 * ( match[ 3 ] === "even" || match[ 3 ] === "odd" ) );
				match[ 5 ] = +( ( match[ 7 ] + match[ 8 ] ) || match[ 3 ] === "odd" );

				// other types prohibit arguments
			} else if ( match[ 3 ] ) {
				Sizzle.error( match[ 0 ] );
			}

			return match;
		},

		"PSEUDO": function( match ) {
			var excess,
				unquoted = !match[ 6 ] && match[ 2 ];

			if ( matchExpr[ "CHILD" ].test( match[ 0 ] ) ) {
				return null;
			}

			// Accept quoted arguments as-is
			if ( match[ 3 ] ) {
				match[ 2 ] = match[ 4 ] || match[ 5 ] || "";

			// Strip excess characters from unquoted arguments
			} else if ( unquoted && rpseudo.test( unquoted ) &&

				// Get excess from tokenize (recursively)
				( excess = tokenize( unquoted, true ) ) &&

				// advance to the next closing parenthesis
				( excess = unquoted.indexOf( ")", unquoted.length - excess ) - unquoted.length ) ) {

				// excess is a negative index
				match[ 0 ] = match[ 0 ].slice( 0, excess );
				match[ 2 ] = unquoted.slice( 0, excess );
			}

			// Return only captures needed by the pseudo filter method (type and argument)
			return match.slice( 0, 3 );
		}
	},

	filter: {

		"TAG": function( nodeNameSelector ) {
			var nodeName = nodeNameSelector.replace( runescape, funescape ).toLowerCase();
			return nodeNameSelector === "*" ?
				function() {
					return true;
				} :
				function( elem ) {
					return elem.nodeName && elem.nodeName.toLowerCase() === nodeName;
				};
		},

		"CLASS": function( className ) {
			var pattern = classCache[ className + " " ];

			return pattern ||
				( pattern = new RegExp( "(^|" + whitespace +
					")" + className + "(" + whitespace + "|$)" ) ) && classCache(
						className, function( elem ) {
							return pattern.test(
								typeof elem.className === "string" && elem.className ||
								typeof elem.getAttribute !== "undefined" &&
									elem.getAttribute( "class" ) ||
								""
							);
				} );
		},

		"ATTR": function( name, operator, check ) {
			return function( elem ) {
				var result = Sizzle.attr( elem, name );

				if ( result == null ) {
					return operator === "!=";
				}
				if ( !operator ) {
					return true;
				}

				result += "";

				/* eslint-disable max-len */

				return operator === "=" ? result === check :
					operator === "!=" ? result !== check :
					operator === "^=" ? check && result.indexOf( check ) === 0 :
					operator === "*=" ? check && result.indexOf( check ) > -1 :
					operator === "$=" ? check && result.slice( -check.length ) === check :
					operator === "~=" ? ( " " + result.replace( rwhitespace, " " ) + " " ).indexOf( check ) > -1 :
					operator === "|=" ? result === check || result.slice( 0, check.length + 1 ) === check + "-" :
					false;
				/* eslint-enable max-len */

			};
		},

		"CHILD": function( type, what, _argument, first, last ) {
			var simple = type.slice( 0, 3 ) !== "nth",
				forward = type.slice( -4 ) !== "last",
				ofType = what === "of-type";

			return first === 1 && last === 0 ?

				// Shortcut for :nth-*(n)
				function( elem ) {
					return !!elem.parentNode;
				} :

				function( elem, _context, xml ) {
					var cache, uniqueCache, outerCache, node, nodeIndex, start,
						dir = simple !== forward ? "nextSibling" : "previousSibling",
						parent = elem.parentNode,
						name = ofType && elem.nodeName.toLowerCase(),
						useCache = !xml && !ofType,
						diff = false;

					if ( parent ) {

						// :(first|last|only)-(child|of-type)
						if ( simple ) {
							while ( dir ) {
								node = elem;
								while ( ( node = node[ dir ] ) ) {
									if ( ofType ?
										node.nodeName.toLowerCase() === name :
										node.nodeType === 1 ) {

										return false;
									}
								}

								// Reverse direction for :only-* (if we haven't yet done so)
								start = dir = type === "only" && !start && "nextSibling";
							}
							return true;
						}

						start = [ forward ? parent.firstChild : parent.lastChild ];

						// non-xml :nth-child(...) stores cache data on `parent`
						if ( forward && useCache ) {

							// Seek `elem` from a previously-cached index

							// ...in a gzip-friendly way
							node = parent;
							outerCache = node[ expando ] || ( node[ expando ] = {} );

							// Support: IE <9 only
							// Defend against cloned attroperties (jQuery gh-1709)
							uniqueCache = outerCache[ node.uniqueID ] ||
								( outerCache[ node.uniqueID ] = {} );

							cache = uniqueCache[ type ] || [];
							nodeIndex = cache[ 0 ] === dirruns && cache[ 1 ];
							diff = nodeIndex && cache[ 2 ];
							node = nodeIndex && parent.childNodes[ nodeIndex ];

							while ( ( node = ++nodeIndex && node && node[ dir ] ||

								// Fallback to seeking `elem` from the start
								( diff = nodeIndex = 0 ) || start.pop() ) ) {

								// When found, cache indexes on `parent` and break
								if ( node.nodeType === 1 && ++diff && node === elem ) {
									uniqueCache[ type ] = [ dirruns, nodeIndex, diff ];
									break;
								}
							}

						} else {

							// Use previously-cached element index if available
							if ( useCache ) {

								// ...in a gzip-friendly way
								node = elem;
								outerCache = node[ expando ] || ( node[ expando ] = {} );

								// Support: IE <9 only
								// Defend against cloned attroperties (jQuery gh-1709)
								uniqueCache = outerCache[ node.uniqueID ] ||
									( outerCache[ node.uniqueID ] = {} );

								cache = uniqueCache[ type ] || [];
								nodeIndex = cache[ 0 ] === dirruns && cache[ 1 ];
								diff = nodeIndex;
							}

							// xml :nth-child(...)
							// or :nth-last-child(...) or :nth(-last)?-of-type(...)
							if ( diff === false ) {

								// Use the same loop as above to seek `elem` from the start
								while ( ( node = ++nodeIndex && node && node[ dir ] ||
									( diff = nodeIndex = 0 ) || start.pop() ) ) {

									if ( ( ofType ?
										node.nodeName.toLowerCase() === name :
										node.nodeType === 1 ) &&
										++diff ) {

										// Cache the index of each encountered element
										if ( useCache ) {
											outerCache = node[ expando ] ||
												( node[ expando ] = {} );

											// Support: IE <9 only
											// Defend against cloned attroperties (jQuery gh-1709)
											uniqueCache = outerCache[ node.uniqueID ] ||
												( outerCache[ node.uniqueID ] = {} );

											uniqueCache[ type ] = [ dirruns, diff ];
										}

										if ( node === elem ) {
											break;
										}
									}
								}
							}
						}

						// Incorporate the offset, then check against cycle size
						diff -= last;
						return diff === first || ( diff % first === 0 && diff / first >= 0 );
					}
				};
		},

		"PSEUDO": function( pseudo, argument ) {

			// pseudo-class names are case-insensitive
			// http://www.w3.org/TR/selectors/#pseudo-classes
			// Prioritize by case sensitivity in case custom pseudos are added with uppercase letters
			// Remember that setFilters inherits from pseudos
			var args,
				fn = Expr.pseudos[ pseudo ] || Expr.setFilters[ pseudo.toLowerCase() ] ||
					Sizzle.error( "unsupported pseudo: " + pseudo );

			// The user may use createPseudo to indicate that
			// arguments are needed to create the filter function
			// just as Sizzle does
			if ( fn[ expando ] ) {
				return fn( argument );
			}

			// But maintain support for old signatures
			if ( fn.length > 1 ) {
				args = [ pseudo, pseudo, "", argument ];
				return Expr.setFilters.hasOwnProperty( pseudo.toLowerCase() ) ?
					markFunction( function( seed, matches ) {
						var idx,
							matched = fn( seed, argument ),
							i = matched.length;
						while ( i-- ) {
							idx = indexOf( seed, matched[ i ] );
							seed[ idx ] = !( matches[ idx ] = matched[ i ] );
						}
					} ) :
					function( elem ) {
						return fn( elem, 0, args );
					};
			}

			return fn;
		}
	},

	pseudos: {

		// Potentially complex pseudos
		"not": markFunction( function( selector ) {

			// Trim the selector passed to compile
			// to avoid treating leading and trailing
			// spaces as combinators
			var input = [],
				results = [],
				matcher = compile( selector.replace( rtrim, "$1" ) );

			return matcher[ expando ] ?
				markFunction( function( seed, matches, _context, xml ) {
					var elem,
						unmatched = matcher( seed, null, xml, [] ),
						i = seed.length;

					// Match elements unmatched by `matcher`
					while ( i-- ) {
						if ( ( elem = unmatched[ i ] ) ) {
							seed[ i ] = !( matches[ i ] = elem );
						}
					}
				} ) :
				function( elem, _context, xml ) {
					input[ 0 ] = elem;
					matcher( input, null, xml, results );

					// Don't keep the element (issue #299)
					input[ 0 ] = null;
					return !results.pop();
				};
		} ),

		"has": markFunction( function( selector ) {
			return function( elem ) {
				return Sizzle( selector, elem ).length > 0;
			};
		} ),

		"contains": markFunction( function( text ) {
			text = text.replace( runescape, funescape );
			return function( elem ) {
				return ( elem.textContent || getText( elem ) ).indexOf( text ) > -1;
			};
		} ),

		// "Whether an element is represented by a :lang() selector
		// is based solely on the element's language value
		// being equal to the identifier C,
		// or beginning with the identifier C immediately followed by "-".
		// The matching of C against the element's language value is performed case-insensitively.
		// The identifier C does not have to be a valid language name."
		// http://www.w3.org/TR/selectors/#lang-pseudo
		"lang": markFunction( function( lang ) {

			// lang value must be a valid identifier
			if ( !ridentifier.test( lang || "" ) ) {
				Sizzle.error( "unsupported lang: " + lang );
			}
			lang = lang.replace( runescape, funescape ).toLowerCase();
			return function( elem ) {
				var elemLang;
				do {
					if ( ( elemLang = documentIsHTML ?
						elem.lang :
						elem.getAttribute( "xml:lang" ) || elem.getAttribute( "lang" ) ) ) {

						elemLang = elemLang.toLowerCase();
						return elemLang === lang || elemLang.indexOf( lang + "-" ) === 0;
					}
				} while ( ( elem = elem.parentNode ) && elem.nodeType === 1 );
				return false;
			};
		} ),

		// Miscellaneous
		"target": function( elem ) {
			var hash = window.location && window.location.hash;
			return hash && hash.slice( 1 ) === elem.id;
		},

		"root": function( elem ) {
			return elem === docElem;
		},

		"focus": function( elem ) {
			return elem === document.activeElement &&
				( !document.hasFocus || document.hasFocus() ) &&
				!!( elem.type || elem.href || ~elem.tabIndex );
		},

		// Boolean properties
		"enabled": createDisabledPseudo( false ),
		"disabled": createDisabledPseudo( true ),

		"checked": function( elem ) {

			// In CSS3, :checked should return both checked and selected elements
			// http://www.w3.org/TR/2011/REC-css3-selectors-20110929/#checked
			var nodeName = elem.nodeName.toLowerCase();
			return ( nodeName === "input" && !!elem.checked ) ||
				( nodeName === "option" && !!elem.selected );
		},

		"selected": function( elem ) {

			// Accessing this property makes selected-by-default
			// options in Safari work properly
			if ( elem.parentNode ) {
				// eslint-disable-next-line no-unused-expressions
				elem.parentNode.selectedIndex;
			}

			return elem.selected === true;
		},

		// Contents
		"empty": function( elem ) {

			// http://www.w3.org/TR/selectors/#empty-pseudo
			// :empty is negated by element (1) or content nodes (text: 3; cdata: 4; entity ref: 5),
			//   but not by others (comment: 8; processing instruction: 7; etc.)
			// nodeType < 6 works because attributes (2) do not appear as children
			for ( elem = elem.firstChild; elem; elem = elem.nextSibling ) {
				if ( elem.nodeType < 6 ) {
					return false;
				}
			}
			return true;
		},

		"parent": function( elem ) {
			return !Expr.pseudos[ "empty" ]( elem );
		},

		// Element/input types
		"header": function( elem ) {
			return rheader.test( elem.nodeName );
		},

		"input": function( elem ) {
			return rinputs.test( elem.nodeName );
		},

		"button": function( elem ) {
			var name = elem.nodeName.toLowerCase();
			return name === "input" && elem.type === "button" || name === "button";
		},

		"text": function( elem ) {
			var attr;
			return elem.nodeName.toLowerCase() === "input" &&
				elem.type === "text" &&

				// Support: IE<8
				// New HTML5 attribute values (e.g., "search") appear with elem.type === "text"
				( ( attr = elem.getAttribute( "type" ) ) == null ||
					attr.toLowerCase() === "text" );
		},

		// Position-in-collection
		"first": createPositionalPseudo( function() {
			return [ 0 ];
		} ),

		"last": createPositionalPseudo( function( _matchIndexes, length ) {
			return [ length - 1 ];
		} ),

		"eq": createPositionalPseudo( function( _matchIndexes, length, argument ) {
			return [ argument < 0 ? argument + length : argument ];
		} ),

		"even": createPositionalPseudo( function( matchIndexes, length ) {
			var i = 0;
			for ( ; i < length; i += 2 ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"odd": createPositionalPseudo( function( matchIndexes, length ) {
			var i = 1;
			for ( ; i < length; i += 2 ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"lt": createPositionalPseudo( function( matchIndexes, length, argument ) {
			var i = argument < 0 ?
				argument + length :
				argument > length ?
					length :
					argument;
			for ( ; --i >= 0; ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"gt": createPositionalPseudo( function( matchIndexes, length, argument ) {
			var i = argument < 0 ? argument + length : argument;
			for ( ; ++i < length; ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} )
	}
};

Expr.pseudos[ "nth" ] = Expr.pseudos[ "eq" ];

// Add button/input type pseudos
for ( i in { radio: true, checkbox: true, file: true, password: true, image: true } ) {
	Expr.pseudos[ i ] = createInputPseudo( i );
}
for ( i in { submit: true, reset: true } ) {
	Expr.pseudos[ i ] = createButtonPseudo( i );
}

// Easy API for creating new setFilters
function setFilters() {}
setFilters.prototype = Expr.filters = Expr.pseudos;
Expr.setFilters = new setFilters();

tokenize = Sizzle.tokenize = function( selector, parseOnly ) {
	var matched, match, tokens, type,
		soFar, groups, preFilters,
		cached = tokenCache[ selector + " " ];

	if ( cached ) {
		return parseOnly ? 0 : cached.slice( 0 );
	}

	soFar = selector;
	groups = [];
	preFilters = Expr.preFilter;

	while ( soFar ) {

		// Comma and first run
		if ( !matched || ( match = rcomma.exec( soFar ) ) ) {
			if ( match ) {

				// Don't consume trailing commas as valid
				soFar = soFar.slice( match[ 0 ].length ) || soFar;
			}
			groups.push( ( tokens = [] ) );
		}

		matched = false;

		// Combinators
		if ( ( match = rcombinators.exec( soFar ) ) ) {
			matched = match.shift();
			tokens.push( {
				value: matched,

				// Cast descendant combinators to space
				type: match[ 0 ].replace( rtrim, " " )
			} );
			soFar = soFar.slice( matched.length );
		}

		// Filters
		for ( type in Expr.filter ) {
			if ( ( match = matchExpr[ type ].exec( soFar ) ) && ( !preFilters[ type ] ||
				( match = preFilters[ type ]( match ) ) ) ) {
				matched = match.shift();
				tokens.push( {
					value: matched,
					type: type,
					matches: match
				} );
				soFar = soFar.slice( matched.length );
			}
		}

		if ( !matched ) {
			break;
		}
	}

	// Return the length of the invalid excess
	// if we're just parsing
	// Otherwise, throw an error or return tokens
	return parseOnly ?
		soFar.length :
		soFar ?
			Sizzle.error( selector ) :

			// Cache the tokens
			tokenCache( selector, groups ).slice( 0 );
};

function toSelector( tokens ) {
	var i = 0,
		len = tokens.length,
		selector = "";
	for ( ; i < len; i++ ) {
		selector += tokens[ i ].value;
	}
	return selector;
}

function addCombinator( matcher, combinator, base ) {
	var dir = combinator.dir,
		skip = combinator.next,
		key = skip || dir,
		checkNonElements = base && key === "parentNode",
		doneName = done++;

	return combinator.first ?

		// Check against closest ancestor/preceding element
		function( elem, context, xml ) {
			while ( ( elem = elem[ dir ] ) ) {
				if ( elem.nodeType === 1 || checkNonElements ) {
					return matcher( elem, context, xml );
				}
			}
			return false;
		} :

		// Check against all ancestor/preceding elements
		function( elem, context, xml ) {
			var oldCache, uniqueCache, outerCache,
				newCache = [ dirruns, doneName ];

			// We can't set arbitrary data on XML nodes, so they don't benefit from combinator caching
			if ( xml ) {
				while ( ( elem = elem[ dir ] ) ) {
					if ( elem.nodeType === 1 || checkNonElements ) {
						if ( matcher( elem, context, xml ) ) {
							return true;
						}
					}
				}
			} else {
				while ( ( elem = elem[ dir ] ) ) {
					if ( elem.nodeType === 1 || checkNonElements ) {
						outerCache = elem[ expando ] || ( elem[ expando ] = {} );

						// Support: IE <9 only
						// Defend against cloned attroperties (jQuery gh-1709)
						uniqueCache = outerCache[ elem.uniqueID ] ||
							( outerCache[ elem.uniqueID ] = {} );

						if ( skip && skip === elem.nodeName.toLowerCase() ) {
							elem = elem[ dir ] || elem;
						} else if ( ( oldCache = uniqueCache[ key ] ) &&
							oldCache[ 0 ] === dirruns && oldCache[ 1 ] === doneName ) {

							// Assign to newCache so results back-propagate to previous elements
							return ( newCache[ 2 ] = oldCache[ 2 ] );
						} else {

							// Reuse newcache so results back-propagate to previous elements
							uniqueCache[ key ] = newCache;

							// A match means we're done; a fail means we have to keep checking
							if ( ( newCache[ 2 ] = matcher( elem, context, xml ) ) ) {
								return true;
							}
						}
					}
				}
			}
			return false;
		};
}

function elementMatcher( matchers ) {
	return matchers.length > 1 ?
		function( elem, context, xml ) {
			var i = matchers.length;
			while ( i-- ) {
				if ( !matchers[ i ]( elem, context, xml ) ) {
					return false;
				}
			}
			return true;
		} :
		matchers[ 0 ];
}

function multipleContexts( selector, contexts, results ) {
	var i = 0,
		len = contexts.length;
	for ( ; i < len; i++ ) {
		Sizzle( selector, contexts[ i ], results );
	}
	return results;
}

function condense( unmatched, map, filter, context, xml ) {
	var elem,
		newUnmatched = [],
		i = 0,
		len = unmatched.length,
		mapped = map != null;

	for ( ; i < len; i++ ) {
		if ( ( elem = unmatched[ i ] ) ) {
			if ( !filter || filter( elem, context, xml ) ) {
				newUnmatched.push( elem );
				if ( mapped ) {
					map.push( i );
				}
			}
		}
	}

	return newUnmatched;
}

function setMatcher( preFilter, selector, matcher, postFilter, postFinder, postSelector ) {
	if ( postFilter && !postFilter[ expando ] ) {
		postFilter = setMatcher( postFilter );
	}
	if ( postFinder && !postFinder[ expando ] ) {
		postFinder = setMatcher( postFinder, postSelector );
	}
	return markFunction( function( seed, results, context, xml ) {
		var temp, i, elem,
			preMap = [],
			postMap = [],
			preexisting = results.length,

			// Get initial elements from seed or context
			elems = seed || multipleContexts(
				selector || "*",
				context.nodeType ? [ context ] : context,
				[]
			),

			// Prefilter to get matcher input, preserving a map for seed-results synchronization
			matcherIn = preFilter && ( seed || !selector ) ?
				condense( elems, preMap, preFilter, context, xml ) :
				elems,

			matcherOut = matcher ?

				// If we have a postFinder, or filtered seed, or non-seed postFilter or preexisting results,
				postFinder || ( seed ? preFilter : preexisting || postFilter ) ?

					// ...intermediate processing is necessary
					[] :

					// ...otherwise use results directly
					results :
				matcherIn;

		// Find primary matches
		if ( matcher ) {
			matcher( matcherIn, matcherOut, context, xml );
		}

		// Apply postFilter
		if ( postFilter ) {
			temp = condense( matcherOut, postMap );
			postFilter( temp, [], context, xml );

			// Un-match failing elements by moving them back to matcherIn
			i = temp.length;
			while ( i-- ) {
				if ( ( elem = temp[ i ] ) ) {
					matcherOut[ postMap[ i ] ] = !( matcherIn[ postMap[ i ] ] = elem );
				}
			}
		}

		if ( seed ) {
			if ( postFinder || preFilter ) {
				if ( postFinder ) {

					// Get the final matcherOut by condensing this intermediate into postFinder contexts
					temp = [];
					i = matcherOut.length;
					while ( i-- ) {
						if ( ( elem = matcherOut[ i ] ) ) {

							// Restore matcherIn since elem is not yet a final match
							temp.push( ( matcherIn[ i ] = elem ) );
						}
					}
					postFinder( null, ( matcherOut = [] ), temp, xml );
				}

				// Move matched elements from seed to results to keep them synchronized
				i = matcherOut.length;
				while ( i-- ) {
					if ( ( elem = matcherOut[ i ] ) &&
						( temp = postFinder ? indexOf( seed, elem ) : preMap[ i ] ) > -1 ) {

						seed[ temp ] = !( results[ temp ] = elem );
					}
				}
			}

		// Add elements to results, through postFinder if defined
		} else {
			matcherOut = condense(
				matcherOut === results ?
					matcherOut.splice( preexisting, matcherOut.length ) :
					matcherOut
			);
			if ( postFinder ) {
				postFinder( null, results, matcherOut, xml );
			} else {
				push.apply( results, matcherOut );
			}
		}
	} );
}

function matcherFromTokens( tokens ) {
	var checkContext, matcher, j,
		len = tokens.length,
		leadingRelative = Expr.relative[ tokens[ 0 ].type ],
		implicitRelative = leadingRelative || Expr.relative[ " " ],
		i = leadingRelative ? 1 : 0,

		// The foundational matcher ensures that elements are reachable from top-level context(s)
		matchContext = addCombinator( function( elem ) {
			return elem === checkContext;
		}, implicitRelative, true ),
		matchAnyContext = addCombinator( function( elem ) {
			return indexOf( checkContext, elem ) > -1;
		}, implicitRelative, true ),
		matchers = [ function( elem, context, xml ) {
			var ret = ( !leadingRelative && ( xml || context !== outermostContext ) ) || (
				( checkContext = context ).nodeType ?
					matchContext( elem, context, xml ) :
					matchAnyContext( elem, context, xml ) );

			// Avoid hanging onto element (issue #299)
			checkContext = null;
			return ret;
		} ];

	for ( ; i < len; i++ ) {
		if ( ( matcher = Expr.relative[ tokens[ i ].type ] ) ) {
			matchers = [ addCombinator( elementMatcher( matchers ), matcher ) ];
		} else {
			matcher = Expr.filter[ tokens[ i ].type ].apply( null, tokens[ i ].matches );

			// Return special upon seeing a positional matcher
			if ( matcher[ expando ] ) {

				// Find the next relative operator (if any) for proper handling
				j = ++i;
				for ( ; j < len; j++ ) {
					if ( Expr.relative[ tokens[ j ].type ] ) {
						break;
					}
				}
				return setMatcher(
					i > 1 && elementMatcher( matchers ),
					i > 1 && toSelector(

					// If the preceding token was a descendant combinator, insert an implicit any-element `*`
					tokens
						.slice( 0, i - 1 )
						.concat( { value: tokens[ i - 2 ].type === " " ? "*" : "" } )
					).replace( rtrim, "$1" ),
					matcher,
					i < j && matcherFromTokens( tokens.slice( i, j ) ),
					j < len && matcherFromTokens( ( tokens = tokens.slice( j ) ) ),
					j < len && toSelector( tokens )
				);
			}
			matchers.push( matcher );
		}
	}

	return elementMatcher( matchers );
}

function matcherFromGroupMatchers( elementMatchers, setMatchers ) {
	var bySet = setMatchers.length > 0,
		byElement = elementMatchers.length > 0,
		superMatcher = function( seed, context, xml, results, outermost ) {
			var elem, j, matcher,
				matchedCount = 0,
				i = "0",
				unmatched = seed && [],
				setMatched = [],
				contextBackup = outermostContext,

				// We must always have either seed elements or outermost context
				elems = seed || byElement && Expr.find[ "TAG" ]( "*", outermost ),

				// Use integer dirruns iff this is the outermost matcher
				dirrunsUnique = ( dirruns += contextBackup == null ? 1 : Math.random() || 0.1 ),
				len = elems.length;

			if ( outermost ) {

				// Support: IE 11+, Edge 17 - 18+
				// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
				// two documents; shallow comparisons work.
				// eslint-disable-next-line eqeqeq
				outermostContext = context == document || context || outermost;
			}

			// Add elements passing elementMatchers directly to results
			// Support: IE<9, Safari
			// Tolerate NodeList properties (IE: "length"; Safari: <number>) matching elements by id
			for ( ; i !== len && ( elem = elems[ i ] ) != null; i++ ) {
				if ( byElement && elem ) {
					j = 0;

					// Support: IE 11+, Edge 17 - 18+
					// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
					// two documents; shallow comparisons work.
					// eslint-disable-next-line eqeqeq
					if ( !context && elem.ownerDocument != document ) {
						setDocument( elem );
						xml = !documentIsHTML;
					}
					while ( ( matcher = elementMatchers[ j++ ] ) ) {
						if ( matcher( elem, context || document, xml ) ) {
							results.push( elem );
							break;
						}
					}
					if ( outermost ) {
						dirruns = dirrunsUnique;
					}
				}

				// Track unmatched elements for set filters
				if ( bySet ) {

					// They will have gone through all possible matchers
					if ( ( elem = !matcher && elem ) ) {
						matchedCount--;
					}

					// Lengthen the array for every element, matched or not
					if ( seed ) {
						unmatched.push( elem );
					}
				}
			}

			// `i` is now the count of elements visited above, and adding it to `matchedCount`
			// makes the latter nonnegative.
			matchedCount += i;

			// Apply set filters to unmatched elements
			// NOTE: This can be skipped if there are no unmatched elements (i.e., `matchedCount`
			// equals `i`), unless we didn't visit _any_ elements in the above loop because we have
			// no element matchers and no seed.
			// Incrementing an initially-string "0" `i` allows `i` to remain a string only in that
			// case, which will result in a "00" `matchedCount` that differs from `i` but is also
			// numerically zero.
			if ( bySet && i !== matchedCount ) {
				j = 0;
				while ( ( matcher = setMatchers[ j++ ] ) ) {
					matcher( unmatched, setMatched, context, xml );
				}

				if ( seed ) {

					// Reintegrate element matches to eliminate the need for sorting
					if ( matchedCount > 0 ) {
						while ( i-- ) {
							if ( !( unmatched[ i ] || setMatched[ i ] ) ) {
								setMatched[ i ] = pop.call( results );
							}
						}
					}

					// Discard index placeholder values to get only actual matches
					setMatched = condense( setMatched );
				}

				// Add matches to results
				push.apply( results, setMatched );

				// Seedless set matches succeeding multiple successful matchers stipulate sorting
				if ( outermost && !seed && setMatched.length > 0 &&
					( matchedCount + setMatchers.length ) > 1 ) {

					Sizzle.uniqueSort( results );
				}
			}

			// Override manipulation of globals by nested matchers
			if ( outermost ) {
				dirruns = dirrunsUnique;
				outermostContext = contextBackup;
			}

			return unmatched;
		};

	return bySet ?
		markFunction( superMatcher ) :
		superMatcher;
}

compile = Sizzle.compile = function( selector, match /* Internal Use Only */ ) {
	var i,
		setMatchers = [],
		elementMatchers = [],
		cached = compilerCache[ selector + " " ];

	if ( !cached ) {

		// Generate a function of recursive functions that can be used to check each element
		if ( !match ) {
			match = tokenize( selector );
		}
		i = match.length;
		while ( i-- ) {
			cached = matcherFromTokens( match[ i ] );
			if ( cached[ expando ] ) {
				setMatchers.push( cached );
			} else {
				elementMatchers.push( cached );
			}
		}

		// Cache the compiled function
		cached = compilerCache(
			selector,
			matcherFromGroupMatchers( elementMatchers, setMatchers )
		);

		// Save selector and tokenization
		cached.selector = selector;
	}
	return cached;
};

/**
 * A low-level selection function that works with Sizzle's compiled
 *  selector functions
 * @param {String|Function} selector A selector or a pre-compiled
 *  selector function built with Sizzle.compile
 * @param {Element} context
 * @param {Array} [results]
 * @param {Array} [seed] A set of elements to match against
 */
select = Sizzle.select = function( selector, context, results, seed ) {
	var i, tokens, token, type, find,
		compiled = typeof selector === "function" && selector,
		match = !seed && tokenize( ( selector = compiled.selector || selector ) );

	results = results || [];

	// Try to minimize operations if there is only one selector in the list and no seed
	// (the latter of which guarantees us context)
	if ( match.length === 1 ) {

		// Reduce context if the leading compound selector is an ID
		tokens = match[ 0 ] = match[ 0 ].slice( 0 );
		if ( tokens.length > 2 && ( token = tokens[ 0 ] ).type === "ID" &&
			context.nodeType === 9 && documentIsHTML && Expr.relative[ tokens[ 1 ].type ] ) {

			context = ( Expr.find[ "ID" ]( token.matches[ 0 ]
				.replace( runescape, funescape ), context ) || [] )[ 0 ];
			if ( !context ) {
				return results;

			// Precompiled matchers will still verify ancestry, so step up a level
			} else if ( compiled ) {
				context = context.parentNode;
			}

			selector = selector.slice( tokens.shift().value.length );
		}

		// Fetch a seed set for right-to-left matching
		i = matchExpr[ "needsContext" ].test( selector ) ? 0 : tokens.length;
		while ( i-- ) {
			token = tokens[ i ];

			// Abort if we hit a combinator
			if ( Expr.relative[ ( type = token.type ) ] ) {
				break;
			}
			if ( ( find = Expr.find[ type ] ) ) {

				// Search, expanding context for leading sibling combinators
				if ( ( seed = find(
					token.matches[ 0 ].replace( runescape, funescape ),
					rsibling.test( tokens[ 0 ].type ) && testContext( context.parentNode ) ||
						context
				) ) ) {

					// If seed is empty or no tokens remain, we can return early
					tokens.splice( i, 1 );
					selector = seed.length && toSelector( tokens );
					if ( !selector ) {
						push.apply( results, seed );
						return results;
					}

					break;
				}
			}
		}
	}

	// Compile and execute a filtering function if one is not provided
	// Provide `match` to avoid retokenization if we modified the selector above
	( compiled || compile( selector, match ) )(
		seed,
		context,
		!documentIsHTML,
		results,
		!context || rsibling.test( selector ) && testContext( context.parentNode ) || context
	);
	return results;
};

// One-time assignments

// Sort stability
support.sortStable = expando.split( "" ).sort( sortOrder ).join( "" ) === expando;

// Support: Chrome 14-35+
// Always assume duplicates if they aren't passed to the comparison function
support.detectDuplicates = !!hasDuplicate;

// Initialize against the default document
setDocument();

// Support: Webkit<537.32 - Safari 6.0.3/Chrome 25 (fixed in Chrome 27)
// Detached nodes confoundingly follow *each other*
support.sortDetached = assert( function( el ) {

	// Should return 1, but returns 4 (following)
	return el.compareDocumentPosition( document.createElement( "fieldset" ) ) & 1;
} );

// Support: IE<8
// Prevent attribute/property "interpolation"
// https://msdn.microsoft.com/en-us/library/ms536429%28VS.85%29.aspx
if ( !assert( function( el ) {
	el.innerHTML = "<a href='#'></a>";
	return el.firstChild.getAttribute( "href" ) === "#";
} ) ) {
	addHandle( "type|href|height|width", function( elem, name, isXML ) {
		if ( !isXML ) {
			return elem.getAttribute( name, name.toLowerCase() === "type" ? 1 : 2 );
		}
	} );
}

// Support: IE<9
// Use defaultValue in place of getAttribute("value")
if ( !support.attributes || !assert( function( el ) {
	el.innerHTML = "<input/>";
	el.firstChild.setAttribute( "value", "" );
	return el.firstChild.getAttribute( "value" ) === "";
} ) ) {
	addHandle( "value", function( elem, _name, isXML ) {
		if ( !isXML && elem.nodeName.toLowerCase() === "input" ) {
			return elem.defaultValue;
		}
	} );
}

// Support: IE<9
// Use getAttributeNode to fetch booleans when getAttribute lies
if ( !assert( function( el ) {
	return el.getAttribute( "disabled" ) == null;
} ) ) {
	addHandle( booleans, function( elem, name, isXML ) {
		var val;
		if ( !isXML ) {
			return elem[ name ] === true ? name.toLowerCase() :
				( val = elem.getAttributeNode( name ) ) && val.specified ?
					val.value :
					null;
		}
	} );
}

return Sizzle;

} )( window );



jQuery.find = Sizzle;
jQuery.expr = Sizzle.selectors;

// Deprecated
jQuery.expr[ ":" ] = jQuery.expr.pseudos;
jQuery.uniqueSort = jQuery.unique = Sizzle.uniqueSort;
jQuery.text = Sizzle.getText;
jQuery.isXMLDoc = Sizzle.isXML;
jQuery.contains = Sizzle.contains;
jQuery.escapeSelector = Sizzle.escape;




var dir = function( elem, dir, until ) {
	var matched = [],
		truncate = until !== undefined;

	while ( ( elem = elem[ dir ] ) && elem.nodeType !== 9 ) {
		if ( elem.nodeType === 1 ) {
			if ( truncate && jQuery( elem ).is( until ) ) {
				break;
			}
			matched.push( elem );
		}
	}
	return matched;
};


var siblings = function( n, elem ) {
	var matched = [];

	for ( ; n; n = n.nextSibling ) {
		if ( n.nodeType === 1 && n !== elem ) {
			matched.push( n );
		}
	}

	return matched;
};


var rneedsContext = jQuery.expr.match.needsContext;



function nodeName( elem, name ) {

	return elem.nodeName && elem.nodeName.toLowerCase() === name.toLowerCase();

}
var rsingleTag = ( /^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i );



// Implement the identical functionality for filter and not
function winnow( elements, qualifier, not ) {
	if ( isFunction( qualifier ) ) {
		return jQuery.grep( elements, function( elem, i ) {
			return !!qualifier.call( elem, i, elem ) !== not;
		} );
	}

	// Single element
	if ( qualifier.nodeType ) {
		return jQuery.grep( elements, function( elem ) {
			return ( elem === qualifier ) !== not;
		} );
	}

	// Arraylike of elements (jQuery, arguments, Array)
	if ( typeof qualifier !== "string" ) {
		return jQuery.grep( elements, function( elem ) {
			return ( indexOf.call( qualifier, elem ) > -1 ) !== not;
		} );
	}

	// Filtered directly for both simple and complex selectors
	return jQuery.filter( qualifier, elements, not );
}

jQuery.filter = function( expr, elems, not ) {
	var elem = elems[ 0 ];

	if ( not ) {
		expr = ":not(" + expr + ")";
	}

	if ( elems.length === 1 && elem.nodeType === 1 ) {
		return jQuery.find.matchesSelector( elem, expr ) ? [ elem ] : [];
	}

	return jQuery.find.matches( expr, jQuery.grep( elems, function( elem ) {
		return elem.nodeType === 1;
	} ) );
};

jQuery.fn.extend( {
	find: function( selector ) {
		var i, ret,
			len = this.length,
			self = this;

		if ( typeof selector !== "string" ) {
			return this.pushStack( jQuery( selector ).filter( function() {
				for ( i = 0; i < len; i++ ) {
					if ( jQuery.contains( self[ i ], this ) ) {
						return true;
					}
				}
			} ) );
		}

		ret = this.pushStack( [] );

		for ( i = 0; i < len; i++ ) {
			jQuery.find( selector, self[ i ], ret );
		}

		return len > 1 ? jQuery.uniqueSort( ret ) : ret;
	},
	filter: function( selector ) {
		return this.pushStack( winnow( this, selector || [], false ) );
	},
	not: function( selector ) {
		return this.pushStack( winnow( this, selector || [], true ) );
	},
	is: function( selector ) {
		return !!winnow(
			this,

			// If this is a positional/relative selector, check membership in the returned set
			// so $("p:first").is("p:last") won't return true for a doc with two "p".
			typeof selector === "string" && rneedsContext.test( selector ) ?
				jQuery( selector ) :
				selector || [],
			false
		).length;
	}
} );


// Initialize a jQuery object


// A central reference to the root jQuery(document)
var rootjQuery,

	// A simple way to check for HTML strings
	// Prioritize #id over <tag> to avoid XSS via location.hash (#9521)
	// Strict HTML recognition (#11290: must start with <)
	// Shortcut simple #id case for speed
	rquickExpr = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/,

	init = jQuery.fn.init = function( selector, context, root ) {
		var match, elem;

		// HANDLE: $(""), $(null), $(undefined), $(false)
		if ( !selector ) {
			return this;
		}

		// Method init() accepts an alternate rootjQuery
		// so migrate can support jQuery.sub (gh-2101)
		root = root || rootjQuery;

		// Handle HTML strings
		if ( typeof selector === "string" ) {
			if ( selector[ 0 ] === "<" &&
				selector[ selector.length - 1 ] === ">" &&
				selector.length >= 3 ) {

				// Assume that strings that start and end with <> are HTML and skip the regex check
				match = [ null, selector, null ];

			} else {
				match = rquickExpr.exec( selector );
			}

			// Match html or make sure no context is specified for #id
			if ( match && ( match[ 1 ] || !context ) ) {

				// HANDLE: $(html) -> $(array)
				if ( match[ 1 ] ) {
					context = context instanceof jQuery ? context[ 0 ] : context;

					// Option to run scripts is true for back-compat
					// Intentionally let the error be thrown if parseHTML is not present
					jQuery.merge( this, jQuery.parseHTML(
						match[ 1 ],
						context && context.nodeType ? context.ownerDocument || context : document,
						true
					) );

					// HANDLE: $(html, props)
					if ( rsingleTag.test( match[ 1 ] ) && jQuery.isPlainObject( context ) ) {
						for ( match in context ) {

							// Properties of context are called as methods if possible
							if ( isFunction( this[ match ] ) ) {
								this[ match ]( context[ match ] );

							// ...and otherwise set as attributes
							} else {
								this.attr( match, context[ match ] );
							}
						}
					}

					return this;

				// HANDLE: $(#id)
				} else {
					elem = document.getElementById( match[ 2 ] );

					if ( elem ) {

						// Inject the element directly into the jQuery object
						this[ 0 ] = elem;
						this.length = 1;
					}
					return this;
				}

			// HANDLE: $(expr, $(...))
			} else if ( !context || context.jquery ) {
				return ( context || root ).find( selector );

			// HANDLE: $(expr, context)
			// (which is just equivalent to: $(context).find(expr)
			} else {
				return this.constructor( context ).find( selector );
			}

		// HANDLE: $(DOMElement)
		} else if ( selector.nodeType ) {
			this[ 0 ] = selector;
			this.length = 1;
			return this;

		// HANDLE: $(function)
		// Shortcut for document ready
		} else if ( isFunction( selector ) ) {
			return root.ready !== undefined ?
				root.ready( selector ) :

				// Execute immediately if ready is not present
				selector( jQuery );
		}

		return jQuery.makeArray( selector, this );
	};

// Give the init function the jQuery prototype for later instantiation
init.prototype = jQuery.fn;

// Initialize central reference
rootjQuery = jQuery( document );


var rparentsprev = /^(?:parents|prev(?:Until|All))/,

	// Methods guaranteed to produce a unique set when starting from a unique set
	guaranteedUnique = {
		children: true,
		contents: true,
		next: true,
		prev: true
	};

jQuery.fn.extend( {
	has: function( target ) {
		var targets = jQuery( target, this ),
			l = targets.length;

		return this.filter( function() {
			var i = 0;
			for ( ; i < l; i++ ) {
				if ( jQuery.contains( this, targets[ i ] ) ) {
					return true;
				}
			}
		} );
	},

	closest: function( selectors, context ) {
		var cur,
			i = 0,
			l = this.length,
			matched = [],
			targets = typeof selectors !== "string" && jQuery( selectors );

		// Positional selectors never match, since there's no _selection_ context
		if ( !rneedsContext.test( selectors ) ) {
			for ( ; i < l; i++ ) {
				for ( cur = this[ i ]; cur && cur !== context; cur = cur.parentNode ) {

					// Always skip document fragments
					if ( cur.nodeType < 11 && ( targets ?
						targets.index( cur ) > -1 :

						// Don't pass non-elements to Sizzle
						cur.nodeType === 1 &&
							jQuery.find.matchesSelector( cur, selectors ) ) ) {

						matched.push( cur );
						break;
					}
				}
			}
		}

		return this.pushStack( matched.length > 1 ? jQuery.uniqueSort( matched ) : matched );
	},

	// Determine the position of an element within the set
	index: function( elem ) {

		// No argument, return index in parent
		if ( !elem ) {
			return ( this[ 0 ] && this[ 0 ].parentNode ) ? this.first().prevAll().length : -1;
		}

		// Index in selector
		if ( typeof elem === "string" ) {
			return indexOf.call( jQuery( elem ), this[ 0 ] );
		}

		// Locate the position of the desired element
		return indexOf.call( this,

			// If it receives a jQuery object, the first element is used
			elem.jquery ? elem[ 0 ] : elem
		);
	},

	add: function( selector, context ) {
		return this.pushStack(
			jQuery.uniqueSort(
				jQuery.merge( this.get(), jQuery( selector, context ) )
			)
		);
	},

	addBack: function( selector ) {
		return this.add( selector == null ?
			this.prevObject : this.prevObject.filter( selector )
		);
	}
} );

function sibling( cur, dir ) {
	while ( ( cur = cur[ dir ] ) && cur.nodeType !== 1 ) {}
	return cur;
}

jQuery.each( {
	parent: function( elem ) {
		var parent = elem.parentNode;
		return parent && parent.nodeType !== 11 ? parent : null;
	},
	parents: function( elem ) {
		return dir( elem, "parentNode" );
	},
	parentsUntil: function( elem, _i, until ) {
		return dir( elem, "parentNode", until );
	},
	next: function( elem ) {
		return sibling( elem, "nextSibling" );
	},
	prev: function( elem ) {
		return sibling( elem, "previousSibling" );
	},
	nextAll: function( elem ) {
		return dir( elem, "nextSibling" );
	},
	prevAll: function( elem ) {
		return dir( elem, "previousSibling" );
	},
	nextUntil: function( elem, _i, until ) {
		return dir( elem, "nextSibling", until );
	},
	prevUntil: function( elem, _i, until ) {
		return dir( elem, "previousSibling", until );
	},
	siblings: function( elem ) {
		return siblings( ( elem.parentNode || {} ).firstChild, elem );
	},
	children: function( elem ) {
		return siblings( elem.firstChild );
	},
	contents: function( elem ) {
		if ( elem.contentDocument != null &&

			// Support: IE 11+
			// <object> elements with no `data` attribute has an object
			// `contentDocument` with a `null` prototype.
			getProto( elem.contentDocument ) ) {

			return elem.contentDocument;
		}

		// Support: IE 9 - 11 only, iOS 7 only, Android Browser <=4.3 only
		// Treat the template element as a regular one in browsers that
		// don't support it.
		if ( nodeName( elem, "template" ) ) {
			elem = elem.content || elem;
		}

		return jQuery.merge( [], elem.childNodes );
	}
}, function( name, fn ) {
	jQuery.fn[ name ] = function( until, selector ) {
		var matched = jQuery.map( this, fn, until );

		if ( name.slice( -5 ) !== "Until" ) {
			selector = until;
		}

		if ( selector && typeof selector === "string" ) {
			matched = jQuery.filter( selector, matched );
		}

		if ( this.length > 1 ) {

			// Remove duplicates
			if ( !guaranteedUnique[ name ] ) {
				jQuery.uniqueSort( matched );
			}

			// Reverse order for parents* and prev-derivatives
			if ( rparentsprev.test( name ) ) {
				matched.reverse();
			}
		}

		return this.pushStack( matched );
	};
} );
var rnothtmlwhite = ( /[^\x20\t\r\n\f]+/g );



// Convert String-formatted options into Object-formatted ones
function createOptions( options ) {
	var object = {};
	jQuery.each( options.match( rnothtmlwhite ) || [], function( _, flag ) {
		object[ flag ] = true;
	} );
	return object;
}

/*
 * Create a callback list using the following parameters:
 *
 *	options: an optional list of space-separated options that will change how
 *			the callback list behaves or a more traditional option object
 *
 * By default a callback list will act like an event callback list and can be
 * "fired" multiple times.
 *
 * Possible options:
 *
 *	once:			will ensure the callback list can only be fired once (like a Deferred)
 *
 *	memory:			will keep track of previous values and will call any callback added
 *					after the list has been fired right away with the latest "memorized"
 *					values (like a Deferred)
 *
 *	unique:			will ensure a callback can only be added once (no duplicate in the list)
 *
 *	stopOnFalse:	interrupt callings when a callback returns false
 *
 */
jQuery.Callbacks = function( options ) {

	// Convert options from String-formatted to Object-formatted if needed
	// (we check in cache first)
	options = typeof options === "string" ?
		createOptions( options ) :
		jQuery.extend( {}, options );

	var // Flag to know if list is currently firing
		firing,

		// Last fire value for non-forgettable lists
		memory,

		// Flag to know if list was already fired
		fired,

		// Flag to prevent firing
		locked,

		// Actual callback list
		list = [],

		// Queue of execution data for repeatable lists
		queue = [],

		// Index of currently firing callback (modified by add/remove as needed)
		firingIndex = -1,

		// Fire callbacks
		fire = function() {

			// Enforce single-firing
			locked = locked || options.once;

			// Execute callbacks for all pending executions,
			// respecting firingIndex overrides and runtime changes
			fired = firing = true;
			for ( ; queue.length; firingIndex = -1 ) {
				memory = queue.shift();
				while ( ++firingIndex < list.length ) {

					// Run callback and check for early termination
					if ( list[ firingIndex ].apply( memory[ 0 ], memory[ 1 ] ) === false &&
						options.stopOnFalse ) {

						// Jump to end and forget the data so .add doesn't re-fire
						firingIndex = list.length;
						memory = false;
					}
				}
			}

			// Forget the data if we're done with it
			if ( !options.memory ) {
				memory = false;
			}

			firing = false;

			// Clean up if we're done firing for good
			if ( locked ) {

				// Keep an empty list if we have data for future add calls
				if ( memory ) {
					list = [];

				// Otherwise, this object is spent
				} else {
					list = "";
				}
			}
		},

		// Actual Callbacks object
		self = {

			// Add a callback or a collection of callbacks to the list
			add: function() {
				if ( list ) {

					// If we have memory from a past run, we should fire after adding
					if ( memory && !firing ) {
						firingIndex = list.length - 1;
						queue.push( memory );
					}

					( function add( args ) {
						jQuery.each( args, function( _, arg ) {
							if ( isFunction( arg ) ) {
								if ( !options.unique || !self.has( arg ) ) {
									list.push( arg );
								}
							} else if ( arg && arg.length && toType( arg ) !== "string" ) {

								// Inspect recursively
								add( arg );
							}
						} );
					} )( arguments );

					if ( memory && !firing ) {
						fire();
					}
				}
				return this;
			},

			// Remove a callback from the list
			remove: function() {
				jQuery.each( arguments, function( _, arg ) {
					var index;
					while ( ( index = jQuery.inArray( arg, list, index ) ) > -1 ) {
						list.splice( index, 1 );

						// Handle firing indexes
						if ( index <= firingIndex ) {
							firingIndex--;
						}
					}
				} );
				return this;
			},

			// Check if a given callback is in the list.
			// If no argument is given, return whether or not list has callbacks attached.
			has: function( fn ) {
				return fn ?
					jQuery.inArray( fn, list ) > -1 :
					list.length > 0;
			},

			// Remove all callbacks from the list
			empty: function() {
				if ( list ) {
					list = [];
				}
				return this;
			},

			// Disable .fire and .add
			// Abort any current/pending executions
			// Clear all callbacks and values
			disable: function() {
				locked = queue = [];
				list = memory = "";
				return this;
			},
			disabled: function() {
				return !list;
			},

			// Disable .fire
			// Also disable .add unless we have memory (since it would have no effect)
			// Abort any pending executions
			lock: function() {
				locked = queue = [];
				if ( !memory && !firing ) {
					list = memory = "";
				}
				return this;
			},
			locked: function() {
				return !!locked;
			},

			// Call all callbacks with the given context and arguments
			fireWith: function( context, args ) {
				if ( !locked ) {
					args = args || [];
					args = [ context, args.slice ? args.slice() : args ];
					queue.push( args );
					if ( !firing ) {
						fire();
					}
				}
				return this;
			},

			// Call all the callbacks with the given arguments
			fire: function() {
				self.fireWith( this, arguments );
				return this;
			},

			// To know if the callbacks have already been called at least once
			fired: function() {
				return !!fired;
			}
		};

	return self;
};


function Identity( v ) {
	return v;
}
function Thrower( ex ) {
	throw ex;
}

function adoptValue( value, resolve, reject, noValue ) {
	var method;

	try {

		// Check for promise aspect first to privilege synchronous behavior
		if ( value && isFunction( ( method = value.promise ) ) ) {
			method.call( value ).done( resolve ).fail( reject );

		// Other thenables
		} else if ( value && isFunction( ( method = value.then ) ) ) {
			method.call( value, resolve, reject );

		// Other non-thenables
		} else {

			// Control `resolve` arguments by letting Array#slice cast boolean `noValue` to integer:
			// * false: [ value ].slice( 0 ) => resolve( value )
			// * true: [ value ].slice( 1 ) => resolve()
			resolve.apply( undefined, [ value ].slice( noValue ) );
		}

	// For Promises/A+, convert exceptions into rejections
	// Since jQuery.when doesn't unwrap thenables, we can skip the extra checks appearing in
	// Deferred#then to conditionally suppress rejection.
	} catch ( value ) {

		// Support: Android 4.0 only
		// Strict mode functions invoked without .call/.apply get global-object context
		reject.apply( undefined, [ value ] );
	}
}

jQuery.extend( {

	Deferred: function( func ) {
		var tuples = [

				// action, add listener, callbacks,
				// ... .then handlers, argument index, [final state]
				[ "notify", "progress", jQuery.Callbacks( "memory" ),
					jQuery.Callbacks( "memory" ), 2 ],
				[ "resolve", "done", jQuery.Callbacks( "once memory" ),
					jQuery.Callbacks( "once memory" ), 0, "resolved" ],
				[ "reject", "fail", jQuery.Callbacks( "once memory" ),
					jQuery.Callbacks( "once memory" ), 1, "rejected" ]
			],
			state = "pending",
			promise = {
				state: function() {
					return state;
				},
				always: function() {
					deferred.done( arguments ).fail( arguments );
					return this;
				},
				"catch": function( fn ) {
					return promise.then( null, fn );
				},

				// Keep pipe for back-compat
				pipe: function( /* fnDone, fnFail, fnProgress */ ) {
					var fns = arguments;

					return jQuery.Deferred( function( newDefer ) {
						jQuery.each( tuples, function( _i, tuple ) {

							// Map tuples (progress, done, fail) to arguments (done, fail, progress)
							var fn = isFunction( fns[ tuple[ 4 ] ] ) && fns[ tuple[ 4 ] ];

							// deferred.progress(function() { bind to newDefer or newDefer.notify })
							// deferred.done(function() { bind to newDefer or newDefer.resolve })
							// deferred.fail(function() { bind to newDefer or newDefer.reject })
							deferred[ tuple[ 1 ] ]( function() {
								var returned = fn && fn.apply( this, arguments );
								if ( returned && isFunction( returned.promise ) ) {
									returned.promise()
										.progress( newDefer.notify )
										.done( newDefer.resolve )
										.fail( newDefer.reject );
								} else {
									newDefer[ tuple[ 0 ] + "With" ](
										this,
										fn ? [ returned ] : arguments
									);
								}
							} );
						} );
						fns = null;
					} ).promise();
				},
				then: function( onFulfilled, onRejected, onProgress ) {
					var maxDepth = 0;
					function resolve( depth, deferred, handler, special ) {
						return function() {
							var that = this,
								args = arguments,
								mightThrow = function() {
									var returned, then;

									// Support: Promises/A+ section 2.3.3.3.3
									// https://promisesaplus.com/#point-59
									// Ignore double-resolution attempts
									if ( depth < maxDepth ) {
										return;
									}

									returned = handler.apply( that, args );

									// Support: Promises/A+ section 2.3.1
									// https://promisesaplus.com/#point-48
									if ( returned === deferred.promise() ) {
										throw new TypeError( "Thenable self-resolution" );
									}

									// Support: Promises/A+ sections 2.3.3.1, 3.5
									// https://promisesaplus.com/#point-54
									// https://promisesaplus.com/#point-75
									// Retrieve `then` only once
									then = returned &&

										// Support: Promises/A+ section 2.3.4
										// https://promisesaplus.com/#point-64
										// Only check objects and functions for thenability
										( typeof returned === "object" ||
											typeof returned === "function" ) &&
										returned.then;

									// Handle a returned thenable
									if ( isFunction( then ) ) {

										// Special processors (notify) just wait for resolution
										if ( special ) {
											then.call(
												returned,
												resolve( maxDepth, deferred, Identity, special ),
												resolve( maxDepth, deferred, Thrower, special )
											);

										// Normal processors (resolve) also hook into progress
										} else {

											// ...and disregard older resolution values
											maxDepth++;

											then.call(
												returned,
												resolve( maxDepth, deferred, Identity, special ),
												resolve( maxDepth, deferred, Thrower, special ),
												resolve( maxDepth, deferred, Identity,
													deferred.notifyWith )
											);
										}

									// Handle all other returned values
									} else {

										// Only substitute handlers pass on context
										// and multiple values (non-spec behavior)
										if ( handler !== Identity ) {
											that = undefined;
											args = [ returned ];
										}

										// Process the value(s)
										// Default process is resolve
										( special || deferred.resolveWith )( that, args );
									}
								},

								// Only normal processors (resolve) catch and reject exceptions
								process = special ?
									mightThrow :
									function() {
										try {
											mightThrow();
										} catch ( e ) {

											if ( jQuery.Deferred.exceptionHook ) {
												jQuery.Deferred.exceptionHook( e,
													process.stackTrace );
											}

											// Support: Promises/A+ section 2.3.3.3.4.1
											// https://promisesaplus.com/#point-61
											// Ignore post-resolution exceptions
											if ( depth + 1 >= maxDepth ) {

												// Only substitute handlers pass on context
												// and multiple values (non-spec behavior)
												if ( handler !== Thrower ) {
													that = undefined;
													args = [ e ];
												}

												deferred.rejectWith( that, args );
											}
										}
									};

							// Support: Promises/A+ section 2.3.3.3.1
							// https://promisesaplus.com/#point-57
							// Re-resolve promises immediately to dodge false rejection from
							// subsequent errors
							if ( depth ) {
								process();
							} else {

								// Call an optional hook to record the stack, in case of exception
								// since it's otherwise lost when execution goes async
								if ( jQuery.Deferred.getStackHook ) {
									process.stackTrace = jQuery.Deferred.getStackHook();
								}
								window.setTimeout( process );
							}
						};
					}

					return jQuery.Deferred( function( newDefer ) {

						// progress_handlers.add( ... )
						tuples[ 0 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onProgress ) ?
									onProgress :
									Identity,
								newDefer.notifyWith
							)
						);

						// fulfilled_handlers.add( ... )
						tuples[ 1 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onFulfilled ) ?
									onFulfilled :
									Identity
							)
						);

						// rejected_handlers.add( ... )
						tuples[ 2 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onRejected ) ?
									onRejected :
									Thrower
							)
						);
					} ).promise();
				},

				// Get a promise for this deferred
				// If obj is provided, the promise aspect is added to the object
				promise: function( obj ) {
					return obj != null ? jQuery.extend( obj, promise ) : promise;
				}
			},
			deferred = {};

		// Add list-specific methods
		jQuery.each( tuples, function( i, tuple ) {
			var list = tuple[ 2 ],
				stateString = tuple[ 5 ];

			// promise.progress = list.add
			// promise.done = list.add
			// promise.fail = list.add
			promise[ tuple[ 1 ] ] = list.add;

			// Handle state
			if ( stateString ) {
				list.add(
					function() {

						// state = "resolved" (i.e., fulfilled)
						// state = "rejected"
						state = stateString;
					},

					// rejected_callbacks.disable
					// fulfilled_callbacks.disable
					tuples[ 3 - i ][ 2 ].disable,

					// rejected_handlers.disable
					// fulfilled_handlers.disable
					tuples[ 3 - i ][ 3 ].disable,

					// progress_callbacks.lock
					tuples[ 0 ][ 2 ].lock,

					// progress_handlers.lock
					tuples[ 0 ][ 3 ].lock
				);
			}

			// progress_handlers.fire
			// fulfilled_handlers.fire
			// rejected_handlers.fire
			list.add( tuple[ 3 ].fire );

			// deferred.notify = function() { deferred.notifyWith(...) }
			// deferred.resolve = function() { deferred.resolveWith(...) }
			// deferred.reject = function() { deferred.rejectWith(...) }
			deferred[ tuple[ 0 ] ] = function() {
				deferred[ tuple[ 0 ] + "With" ]( this === deferred ? undefined : this, arguments );
				return this;
			};

			// deferred.notifyWith = list.fireWith
			// deferred.resolveWith = list.fireWith
			// deferred.rejectWith = list.fireWith
			deferred[ tuple[ 0 ] + "With" ] = list.fireWith;
		} );

		// Make the deferred a promise
		promise.promise( deferred );

		// Call given func if any
		if ( func ) {
			func.call( deferred, deferred );
		}

		// All done!
		return deferred;
	},

	// Deferred helper
	when: function( singleValue ) {
		var

			// count of uncompleted subordinates
			remaining = arguments.length,

			// count of unprocessed arguments
			i = remaining,

			// subordinate fulfillment data
			resolveContexts = Array( i ),
			resolveValues = slice.call( arguments ),

			// the primary Deferred
			primary = jQuery.Deferred(),

			// subordinate callback factory
			updateFunc = function( i ) {
				return function( value ) {
					resolveContexts[ i ] = this;
					resolveValues[ i ] = arguments.length > 1 ? slice.call( arguments ) : value;
					if ( !( --remaining ) ) {
						primary.resolveWith( resolveContexts, resolveValues );
					}
				};
			};

		// Single- and empty arguments are adopted like Promise.resolve
		if ( remaining <= 1 ) {
			adoptValue( singleValue, primary.done( updateFunc( i ) ).resolve, primary.reject,
				!remaining );

			// Use .then() to unwrap secondary thenables (cf. gh-3000)
			if ( primary.state() === "pending" ||
				isFunction( resolveValues[ i ] && resolveValues[ i ].then ) ) {

				return primary.then();
			}
		}

		// Multiple arguments are aggregated like Promise.all array elements
		while ( i-- ) {
			adoptValue( resolveValues[ i ], updateFunc( i ), primary.reject );
		}

		return primary.promise();
	}
} );


// These usually indicate a programmer mistake during development,
// warn about them ASAP rather than swallowing them by default.
var rerrorNames = /^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;

jQuery.Deferred.exceptionHook = function( error, stack ) {

	// Support: IE 8 - 9 only
	// Console exists when dev tools are open, which can happen at any time
	if ( window.console && window.console.warn && error && rerrorNames.test( error.name ) ) {
		window.console.warn( "jQuery.Deferred exception: " + error.message, error.stack, stack );
	}
};




jQuery.readyException = function( error ) {
	window.setTimeout( function() {
		throw error;
	} );
};




// The deferred used on DOM ready
var readyList = jQuery.Deferred();

jQuery.fn.ready = function( fn ) {

	readyList
		.then( fn )

		// Wrap jQuery.readyException in a function so that the lookup
		// happens at the time of error handling instead of callback
		// registration.
		.catch( function( error ) {
			jQuery.readyException( error );
		} );

	return this;
};

jQuery.extend( {

	// Is the DOM ready to be used? Set to true once it occurs.
	isReady: false,

	// A counter to track how many items to wait for before
	// the ready event fires. See #6781
	readyWait: 1,

	// Handle when the DOM is ready
	ready: function( wait ) {

		// Abort if there are pending holds or we're already ready
		if ( wait === true ? --jQuery.readyWait : jQuery.isReady ) {
			return;
		}

		// Remember that the DOM is ready
		jQuery.isReady = true;

		// If a normal DOM Ready event fired, decrement, and wait if need be
		if ( wait !== true && --jQuery.readyWait > 0 ) {
			return;
		}

		// If there are functions bound, to execute
		readyList.resolveWith( document, [ jQuery ] );
	}
} );

jQuery.ready.then = readyList.then;

// The ready event handler and self cleanup method
function completed() {
	document.removeEventListener( "DOMContentLoaded", completed );
	window.removeEventListener( "load", completed );
	jQuery.ready();
}

// Catch cases where $(document).ready() is called
// after the browser event has already occurred.
// Support: IE <=9 - 10 only
// Older IE sometimes signals "interactive" too soon
if ( document.readyState === "complete" ||
	( document.readyState !== "loading" && !document.documentElement.doScroll ) ) {

	// Handle it asynchronously to allow scripts the opportunity to delay ready
	window.setTimeout( jQuery.ready );

} else {

	// Use the handy event callback
	document.addEventListener( "DOMContentLoaded", completed );

	// A fallback to window.onload, that will always work
	window.addEventListener( "load", completed );
}




// Multifunctional method to get and set values of a collection
// The value/s can optionally be executed if it's a function
var access = function( elems, fn, key, value, chainable, emptyGet, raw ) {
	var i = 0,
		len = elems.length,
		bulk = key == null;

	// Sets many values
	if ( toType( key ) === "object" ) {
		chainable = true;
		for ( i in key ) {
			access( elems, fn, i, key[ i ], true, emptyGet, raw );
		}

	// Sets one value
	} else if ( value !== undefined ) {
		chainable = true;

		if ( !isFunction( value ) ) {
			raw = true;
		}

		if ( bulk ) {

			// Bulk operations run against the entire set
			if ( raw ) {
				fn.call( elems, value );
				fn = null;

			// ...except when executing function values
			} else {
				bulk = fn;
				fn = function( elem, _key, value ) {
					return bulk.call( jQuery( elem ), value );
				};
			}
		}

		if ( fn ) {
			for ( ; i < len; i++ ) {
				fn(
					elems[ i ], key, raw ?
						value :
						value.call( elems[ i ], i, fn( elems[ i ], key ) )
				);
			}
		}
	}

	if ( chainable ) {
		return elems;
	}

	// Gets
	if ( bulk ) {
		return fn.call( elems );
	}

	return len ? fn( elems[ 0 ], key ) : emptyGet;
};


// Matches dashed string for camelizing
var rmsPrefix = /^-ms-/,
	rdashAlpha = /-([a-z])/g;

// Used by camelCase as callback to replace()
function fcamelCase( _all, letter ) {
	return letter.toUpperCase();
}

// Convert dashed to camelCase; used by the css and data modules
// Support: IE <=9 - 11, Edge 12 - 15
// Microsoft forgot to hump their vendor prefix (#9572)
function camelCase( string ) {
	return string.replace( rmsPrefix, "ms-" ).replace( rdashAlpha, fcamelCase );
}
var acceptData = function( owner ) {

	// Accepts only:
	//  - Node
	//    - Node.ELEMENT_NODE
	//    - Node.DOCUMENT_NODE
	//  - Object
	//    - Any
	return owner.nodeType === 1 || owner.nodeType === 9 || !( +owner.nodeType );
};




function Data() {
	this.expando = jQuery.expando + Data.uid++;
}

Data.uid = 1;

Data.prototype = {

	cache: function( owner ) {

		// Check if the owner object already has a cache
		var value = owner[ this.expando ];

		// If not, create one
		if ( !value ) {
			value = {};

			// We can accept data for non-element nodes in modern browsers,
			// but we should not, see #8335.
			// Always return an empty object.
			if ( acceptData( owner ) ) {

				// If it is a node unlikely to be stringify-ed or looped over
				// use plain assignment
				if ( owner.nodeType ) {
					owner[ this.expando ] = value;

				// Otherwise secure it in a non-enumerable property
				// configurable must be true to allow the property to be
				// deleted when data is removed
				} else {
					Object.defineProperty( owner, this.expando, {
						value: value,
						configurable: true
					} );
				}
			}
		}

		return value;
	},
	set: function( owner, data, value ) {
		var prop,
			cache = this.cache( owner );

		// Handle: [ owner, key, value ] args
		// Always use camelCase key (gh-2257)
		if ( typeof data === "string" ) {
			cache[ camelCase( data ) ] = value;

		// Handle: [ owner, { properties } ] args
		} else {

			// Copy the properties one-by-one to the cache object
			for ( prop in data ) {
				cache[ camelCase( prop ) ] = data[ prop ];
			}
		}
		return cache;
	},
	get: function( owner, key ) {
		return key === undefined ?
			this.cache( owner ) :

			// Always use camelCase key (gh-2257)
			owner[ this.expando ] && owner[ this.expando ][ camelCase( key ) ];
	},
	access: function( owner, key, value ) {

		// In cases where either:
		//
		//   1. No key was specified
		//   2. A string key was specified, but no value provided
		//
		// Take the "read" path and allow the get method to determine
		// which value to return, respectively either:
		//
		//   1. The entire cache object
		//   2. The data stored at the key
		//
		if ( key === undefined ||
				( ( key && typeof key === "string" ) && value === undefined ) ) {

			return this.get( owner, key );
		}

		// When the key is not a string, or both a key and value
		// are specified, set or extend (existing objects) with either:
		//
		//   1. An object of properties
		//   2. A key and value
		//
		this.set( owner, key, value );

		// Since the "set" path can have two possible entry points
		// return the expected data based on which path was taken[*]
		return value !== undefined ? value : key;
	},
	remove: function( owner, key ) {
		var i,
			cache = owner[ this.expando ];

		if ( cache === undefined ) {
			return;
		}

		if ( key !== undefined ) {

			// Support array or space separated string of keys
			if ( Array.isArray( key ) ) {

				// If key is an array of keys...
				// We always set camelCase keys, so remove that.
				key = key.map( camelCase );
			} else {
				key = camelCase( key );

				// If a key with the spaces exists, use it.
				// Otherwise, create an array by matching non-whitespace
				key = key in cache ?
					[ key ] :
					( key.match( rnothtmlwhite ) || [] );
			}

			i = key.length;

			while ( i-- ) {
				delete cache[ key[ i ] ];
			}
		}

		// Remove the expando if there's no more data
		if ( key === undefined || jQuery.isEmptyObject( cache ) ) {

			// Support: Chrome <=35 - 45
			// Webkit & Blink performance suffers when deleting properties
			// from DOM nodes, so set to undefined instead
			// https://bugs.chromium.org/p/chromium/issues/detail?id=378607 (bug restricted)
			if ( owner.nodeType ) {
				owner[ this.expando ] = undefined;
			} else {
				delete owner[ this.expando ];
			}
		}
	},
	hasData: function( owner ) {
		var cache = owner[ this.expando ];
		return cache !== undefined && !jQuery.isEmptyObject( cache );
	}
};
var dataPriv = new Data();

var dataUser = new Data();



//	Implementation Summary
//
//	1. Enforce API surface and semantic compatibility with 1.9.x branch
//	2. Improve the module's maintainability by reducing the storage
//		paths to a single mechanism.
//	3. Use the same single mechanism to support "private" and "user" data.
//	4. _Never_ expose "private" data to user code (TODO: Drop _data, _removeData)
//	5. Avoid exposing implementation details on user objects (eg. expando properties)
//	6. Provide a clear path for implementation upgrade to WeakMap in 2014

var rbrace = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,
	rmultiDash = /[A-Z]/g;

function getData( data ) {
	if ( data === "true" ) {
		return true;
	}

	if ( data === "false" ) {
		return false;
	}

	if ( data === "null" ) {
		return null;
	}

	// Only convert to a number if it doesn't change the string
	if ( data === +data + "" ) {
		return +data;
	}

	if ( rbrace.test( data ) ) {
		return JSON.parse( data );
	}

	return data;
}

function dataAttr( elem, key, data ) {
	var name;

	// If nothing was found internally, try to fetch any
	// data from the HTML5 data-* attribute
	if ( data === undefined && elem.nodeType === 1 ) {
		name = "data-" + key.replace( rmultiDash, "-$&" ).toLowerCase();
		data = elem.getAttribute( name );

		if ( typeof data === "string" ) {
			try {
				data = getData( data );
			} catch ( e ) {}

			// Make sure we set the data so it isn't changed later
			dataUser.set( elem, key, data );
		} else {
			data = undefined;
		}
	}
	return data;
}

jQuery.extend( {
	hasData: function( elem ) {
		return dataUser.hasData( elem ) || dataPriv.hasData( elem );
	},

	data: function( elem, name, data ) {
		return dataUser.access( elem, name, data );
	},

	removeData: function( elem, name ) {
		dataUser.remove( elem, name );
	},

	// TODO: Now that all calls to _data and _removeData have been replaced
	// with direct calls to dataPriv methods, these can be deprecated.
	_data: function( elem, name, data ) {
		return dataPriv.access( elem, name, data );
	},

	_removeData: function( elem, name ) {
		dataPriv.remove( elem, name );
	}
} );

jQuery.fn.extend( {
	data: function( key, value ) {
		var i, name, data,
			elem = this[ 0 ],
			attrs = elem && elem.attributes;

		// Gets all values
		if ( key === undefined ) {
			if ( this.length ) {
				data = dataUser.get( elem );

				if ( elem.nodeType === 1 && !dataPriv.get( elem, "hasDataAttrs" ) ) {
					i = attrs.length;
					while ( i-- ) {

						// Support: IE 11 only
						// The attrs elements can be null (#14894)
						if ( attrs[ i ] ) {
							name = attrs[ i ].name;
							if ( name.indexOf( "data-" ) === 0 ) {
								name = camelCase( name.slice( 5 ) );
								dataAttr( elem, name, data[ name ] );
							}
						}
					}
					dataPriv.set( elem, "hasDataAttrs", true );
				}
			}

			return data;
		}

		// Sets multiple values
		if ( typeof key === "object" ) {
			return this.each( function() {
				dataUser.set( this, key );
			} );
		}

		return access( this, function( value ) {
			var data;

			// The calling jQuery object (element matches) is not empty
			// (and therefore has an element appears at this[ 0 ]) and the
			// `value` parameter was not undefined. An empty jQuery object
			// will result in `undefined` for elem = this[ 0 ] which will
			// throw an exception if an attempt to read a data cache is made.
			if ( elem && value === undefined ) {

				// Attempt to get data from the cache
				// The key will always be camelCased in Data
				data = dataUser.get( elem, key );
				if ( data !== undefined ) {
					return data;
				}

				// Attempt to "discover" the data in
				// HTML5 custom data-* attrs
				data = dataAttr( elem, key );
				if ( data !== undefined ) {
					return data;
				}

				// We tried really hard, but the data doesn't exist.
				return;
			}

			// Set the data...
			this.each( function() {

				// We always store the camelCased key
				dataUser.set( this, key, value );
			} );
		}, null, value, arguments.length > 1, null, true );
	},

	removeData: function( key ) {
		return this.each( function() {
			dataUser.remove( this, key );
		} );
	}
} );


jQuery.extend( {
	queue: function( elem, type, data ) {
		var queue;

		if ( elem ) {
			type = ( type || "fx" ) + "queue";
			queue = dataPriv.get( elem, type );

			// Speed up dequeue by getting out quickly if this is just a lookup
			if ( data ) {
				if ( !queue || Array.isArray( data ) ) {
					queue = dataPriv.access( elem, type, jQuery.makeArray( data ) );
				} else {
					queue.push( data );
				}
			}
			return queue || [];
		}
	},

	dequeue: function( elem, type ) {
		type = type || "fx";

		var queue = jQuery.queue( elem, type ),
			startLength = queue.length,
			fn = queue.shift(),
			hooks = jQuery._queueHooks( elem, type ),
			next = function() {
				jQuery.dequeue( elem, type );
			};

		// If the fx queue is dequeued, always remove the progress sentinel
		if ( fn === "inprogress" ) {
			fn = queue.shift();
			startLength--;
		}

		if ( fn ) {

			// Add a progress sentinel to prevent the fx queue from being
			// automatically dequeued
			if ( type === "fx" ) {
				queue.unshift( "inprogress" );
			}

			// Clear up the last queue stop function
			delete hooks.stop;
			fn.call( elem, next, hooks );
		}

		if ( !startLength && hooks ) {
			hooks.empty.fire();
		}
	},

	// Not public - generate a queueHooks object, or return the current one
	_queueHooks: function( elem, type ) {
		var key = type + "queueHooks";
		return dataPriv.get( elem, key ) || dataPriv.access( elem, key, {
			empty: jQuery.Callbacks( "once memory" ).add( function() {
				dataPriv.remove( elem, [ type + "queue", key ] );
			} )
		} );
	}
} );

jQuery.fn.extend( {
	queue: function( type, data ) {
		var setter = 2;

		if ( typeof type !== "string" ) {
			data = type;
			type = "fx";
			setter--;
		}

		if ( arguments.length < setter ) {
			return jQuery.queue( this[ 0 ], type );
		}

		return data === undefined ?
			this :
			this.each( function() {
				var queue = jQuery.queue( this, type, data );

				// Ensure a hooks for this queue
				jQuery._queueHooks( this, type );

				if ( type === "fx" && queue[ 0 ] !== "inprogress" ) {
					jQuery.dequeue( this, type );
				}
			} );
	},
	dequeue: function( type ) {
		return this.each( function() {
			jQuery.dequeue( this, type );
		} );
	},
	clearQueue: function( type ) {
		return this.queue( type || "fx", [] );
	},

	// Get a promise resolved when queues of a certain type
	// are emptied (fx is the type by default)
	promise: function( type, obj ) {
		var tmp,
			count = 1,
			defer = jQuery.Deferred(),
			elements = this,
			i = this.length,
			resolve = function() {
				if ( !( --count ) ) {
					defer.resolveWith( elements, [ elements ] );
				}
			};

		if ( typeof type !== "string" ) {
			obj = type;
			type = undefined;
		}
		type = type || "fx";

		while ( i-- ) {
			tmp = dataPriv.get( elements[ i ], type + "queueHooks" );
			if ( tmp && tmp.empty ) {
				count++;
				tmp.empty.add( resolve );
			}
		}
		resolve();
		return defer.promise( obj );
	}
} );
var pnum = ( /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/ ).source;

var rcssNum = new RegExp( "^(?:([+-])=|)(" + pnum + ")([a-z%]*)$", "i" );


var cssExpand = [ "Top", "Right", "Bottom", "Left" ];

var documentElement = document.documentElement;



	var isAttached = function( elem ) {
			return jQuery.contains( elem.ownerDocument, elem );
		},
		composed = { composed: true };

	// Support: IE 9 - 11+, Edge 12 - 18+, iOS 10.0 - 10.2 only
	// Check attachment across shadow DOM boundaries when possible (gh-3504)
	// Support: iOS 10.0-10.2 only
	// Early iOS 10 versions support `attachShadow` but not `getRootNode`,
	// leading to errors. We need to check for `getRootNode`.
	if ( documentElement.getRootNode ) {
		isAttached = function( elem ) {
			return jQuery.contains( elem.ownerDocument, elem ) ||
				elem.getRootNode( composed ) === elem.ownerDocument;
		};
	}
var isHiddenWithinTree = function( elem, el ) {

		// isHiddenWithinTree might be called from jQuery#filter function;
		// in that case, element will be second argument
		elem = el || elem;

		// Inline style trumps all
		return elem.style.display === "none" ||
			elem.style.display === "" &&

			// Otherwise, check computed style
			// Support: Firefox <=43 - 45
			// Disconnected elements can have computed display: none, so first confirm that elem is
			// in the document.
			isAttached( elem ) &&

			jQuery.css( elem, "display" ) === "none";
	};



function adjustCSS( elem, prop, valueParts, tween ) {
	var adjusted, scale,
		maxIterations = 20,
		currentValue = tween ?
			function() {
				return tween.cur();
			} :
			function() {
				return jQuery.css( elem, prop, "" );
			},
		initial = currentValue(),
		unit = valueParts && valueParts[ 3 ] || ( jQuery.cssNumber[ prop ] ? "" : "px" ),

		// Starting value computation is required for potential unit mismatches
		initialInUnit = elem.nodeType &&
			( jQuery.cssNumber[ prop ] || unit !== "px" && +initial ) &&
			rcssNum.exec( jQuery.css( elem, prop ) );

	if ( initialInUnit && initialInUnit[ 3 ] !== unit ) {

		// Support: Firefox <=54
		// Halve the iteration target value to prevent interference from CSS upper bounds (gh-2144)
		initial = initial / 2;

		// Trust units reported by jQuery.css
		unit = unit || initialInUnit[ 3 ];

		// Iteratively approximate from a nonzero starting point
		initialInUnit = +initial || 1;

		while ( maxIterations-- ) {

			// Evaluate and update our best guess (doubling guesses that zero out).
			// Finish if the scale equals or crosses 1 (making the old*new product non-positive).
			jQuery.style( elem, prop, initialInUnit + unit );
			if ( ( 1 - scale ) * ( 1 - ( scale = currentValue() / initial || 0.5 ) ) <= 0 ) {
				maxIterations = 0;
			}
			initialInUnit = initialInUnit / scale;

		}

		initialInUnit = initialInUnit * 2;
		jQuery.style( elem, prop, initialInUnit + unit );

		// Make sure we update the tween properties later on
		valueParts = valueParts || [];
	}

	if ( valueParts ) {
		initialInUnit = +initialInUnit || +initial || 0;

		// Apply relative offset (+=/-=) if specified
		adjusted = valueParts[ 1 ] ?
			initialInUnit + ( valueParts[ 1 ] + 1 ) * valueParts[ 2 ] :
			+valueParts[ 2 ];
		if ( tween ) {
			tween.unit = unit;
			tween.start = initialInUnit;
			tween.end = adjusted;
		}
	}
	return adjusted;
}


var defaultDisplayMap = {};

function getDefaultDisplay( elem ) {
	var temp,
		doc = elem.ownerDocument,
		nodeName = elem.nodeName,
		display = defaultDisplayMap[ nodeName ];

	if ( display ) {
		return display;
	}

	temp = doc.body.appendChild( doc.createElement( nodeName ) );
	display = jQuery.css( temp, "display" );

	temp.parentNode.removeChild( temp );

	if ( display === "none" ) {
		display = "block";
	}
	defaultDisplayMap[ nodeName ] = display;

	return display;
}

function showHide( elements, show ) {
	var display, elem,
		values = [],
		index = 0,
		length = elements.length;

	// Determine new display value for elements that need to change
	for ( ; index < length; index++ ) {
		elem = elements[ index ];
		if ( !elem.style ) {
			continue;
		}

		display = elem.style.display;
		if ( show ) {

			// Since we force visibility upon cascade-hidden elements, an immediate (and slow)
			// check is required in this first loop unless we have a nonempty display value (either
			// inline or about-to-be-restored)
			if ( display === "none" ) {
				values[ index ] = dataPriv.get( elem, "display" ) || null;
				if ( !values[ index ] ) {
					elem.style.display = "";
				}
			}
			if ( elem.style.display === "" && isHiddenWithinTree( elem ) ) {
				values[ index ] = getDefaultDisplay( elem );
			}
		} else {
			if ( display !== "none" ) {
				values[ index ] = "none";

				// Remember what we're overwriting
				dataPriv.set( elem, "display", display );
			}
		}
	}

	// Set the display of the elements in a second loop to avoid constant reflow
	for ( index = 0; index < length; index++ ) {
		if ( values[ index ] != null ) {
			elements[ index ].style.display = values[ index ];
		}
	}

	return elements;
}

jQuery.fn.extend( {
	show: function() {
		return showHide( this, true );
	},
	hide: function() {
		return showHide( this );
	},
	toggle: function( state ) {
		if ( typeof state === "boolean" ) {
			return state ? this.show() : this.hide();
		}

		return this.each( function() {
			if ( isHiddenWithinTree( this ) ) {
				jQuery( this ).show();
			} else {
				jQuery( this ).hide();
			}
		} );
	}
} );
var rcheckableType = ( /^(?:checkbox|radio)$/i );

var rtagName = ( /<([a-z][^\/\0>\x20\t\r\n\f]*)/i );

var rscriptType = ( /^$|^module$|\/(?:java|ecma)script/i );



( function() {
	var fragment = document.createDocumentFragment(),
		div = fragment.appendChild( document.createElement( "div" ) ),
		input = document.createElement( "input" );

	// Support: Android 4.0 - 4.3 only
	// Check state lost if the name is set (#11217)
	// Support: Windows Web Apps (WWA)
	// `name` and `type` must use .setAttribute for WWA (#14901)
	input.setAttribute( "type", "radio" );
	input.setAttribute( "checked", "checked" );
	input.setAttribute( "name", "t" );

	div.appendChild( input );

	// Support: Android <=4.1 only
	// Older WebKit doesn't clone checked state correctly in fragments
	support.checkClone = div.cloneNode( true ).cloneNode( true ).lastChild.checked;

	// Support: IE <=11 only
	// Make sure textarea (and checkbox) defaultValue is properly cloned
	div.innerHTML = "<textarea>x</textarea>";
	support.noCloneChecked = !!div.cloneNode( true ).lastChild.defaultValue;

	// Support: IE <=9 only
	// IE <=9 replaces <option> tags with their contents when inserted outside of
	// the select element.
	div.innerHTML = "<option></option>";
	support.option = !!div.lastChild;
} )();


// We have to close these tags to support XHTML (#13200)
var wrapMap = {

	// XHTML parsers do not magically insert elements in the
	// same way that tag soup parsers do. So we cannot shorten
	// this by omitting <tbody> or other required elements.
	thead: [ 1, "<table>", "</table>" ],
	col: [ 2, "<table><colgroup>", "</colgroup></table>" ],
	tr: [ 2, "<table><tbody>", "</tbody></table>" ],
	td: [ 3, "<table><tbody><tr>", "</tr></tbody></table>" ],

	_default: [ 0, "", "" ]
};

wrapMap.tbody = wrapMap.tfoot = wrapMap.colgroup = wrapMap.caption = wrapMap.thead;
wrapMap.th = wrapMap.td;

// Support: IE <=9 only
if ( !support.option ) {
	wrapMap.optgroup = wrapMap.option = [ 1, "<select multiple='multiple'>", "</select>" ];
}


function getAll( context, tag ) {

	// Support: IE <=9 - 11 only
	// Use typeof to avoid zero-argument method invocation on host objects (#15151)
	var ret;

	if ( typeof context.getElementsByTagName !== "undefined" ) {
		ret = context.getElementsByTagName( tag || "*" );

	} else if ( typeof context.querySelectorAll !== "undefined" ) {
		ret = context.querySelectorAll( tag || "*" );

	} else {
		ret = [];
	}

	if ( tag === undefined || tag && nodeName( context, tag ) ) {
		return jQuery.merge( [ context ], ret );
	}

	return ret;
}


// Mark scripts as having already been evaluated
function setGlobalEval( elems, refElements ) {
	var i = 0,
		l = elems.length;

	for ( ; i < l; i++ ) {
		dataPriv.set(
			elems[ i ],
			"globalEval",
			!refElements || dataPriv.get( refElements[ i ], "globalEval" )
		);
	}
}


var rhtml = /<|&#?\w+;/;

function buildFragment( elems, context, scripts, selection, ignored ) {
	var elem, tmp, tag, wrap, attached, j,
		fragment = context.createDocumentFragment(),
		nodes = [],
		i = 0,
		l = elems.length;

	for ( ; i < l; i++ ) {
		elem = elems[ i ];

		if ( elem || elem === 0 ) {

			// Add nodes directly
			if ( toType( elem ) === "object" ) {

				// Support: Android <=4.0 only, PhantomJS 1 only
				// push.apply(_, arraylike) throws on ancient WebKit
				jQuery.merge( nodes, elem.nodeType ? [ elem ] : elem );

			// Convert non-html into a text node
			} else if ( !rhtml.test( elem ) ) {
				nodes.push( context.createTextNode( elem ) );

			// Convert html into DOM nodes
			} else {
				tmp = tmp || fragment.appendChild( context.createElement( "div" ) );

				// Deserialize a standard representation
				tag = ( rtagName.exec( elem ) || [ "", "" ] )[ 1 ].toLowerCase();
				wrap = wrapMap[ tag ] || wrapMap._default;
				tmp.innerHTML = wrap[ 1 ] + jQuery.htmlPrefilter( elem ) + wrap[ 2 ];

				// Descend through wrappers to the right content
				j = wrap[ 0 ];
				while ( j-- ) {
					tmp = tmp.lastChild;
				}

				// Support: Android <=4.0 only, PhantomJS 1 only
				// push.apply(_, arraylike) throws on ancient WebKit
				jQuery.merge( nodes, tmp.childNodes );

				// Remember the top-level container
				tmp = fragment.firstChild;

				// Ensure the created nodes are orphaned (#12392)
				tmp.textContent = "";
			}
		}
	}

	// Remove wrapper from fragment
	fragment.textContent = "";

	i = 0;
	while ( ( elem = nodes[ i++ ] ) ) {

		// Skip elements already in the context collection (trac-4087)
		if ( selection && jQuery.inArray( elem, selection ) > -1 ) {
			if ( ignored ) {
				ignored.push( elem );
			}
			continue;
		}

		attached = isAttached( elem );

		// Append to fragment
		tmp = getAll( fragment.appendChild( elem ), "script" );

		// Preserve script evaluation history
		if ( attached ) {
			setGlobalEval( tmp );
		}

		// Capture executables
		if ( scripts ) {
			j = 0;
			while ( ( elem = tmp[ j++ ] ) ) {
				if ( rscriptType.test( elem.type || "" ) ) {
					scripts.push( elem );
				}
			}
		}
	}

	return fragment;
}


var rtypenamespace = /^([^.]*)(?:\.(.+)|)/;

function returnTrue() {
	return true;
}

function returnFalse() {
	return false;
}

// Support: IE <=9 - 11+
// focus() and blur() are asynchronous, except when they are no-op.
// So expect focus to be synchronous when the element is already active,
// and blur to be synchronous when the element is not already active.
// (focus and blur are always synchronous in other supported browsers,
// this just defines when we can count on it).
function expectSync( elem, type ) {
	return ( elem === safeActiveElement() ) === ( type === "focus" );
}

// Support: IE <=9 only
// Accessing document.activeElement can throw unexpectedly
// https://bugs.jquery.com/ticket/13393
function safeActiveElement() {
	try {
		return document.activeElement;
	} catch ( err ) { }
}

function on( elem, types, selector, data, fn, one ) {
	var origFn, type;

	// Types can be a map of types/handlers
	if ( typeof types === "object" ) {

		// ( types-Object, selector, data )
		if ( typeof selector !== "string" ) {

			// ( types-Object, data )
			data = data || selector;
			selector = undefined;
		}
		for ( type in types ) {
			on( elem, type, selector, data, types[ type ], one );
		}
		return elem;
	}

	if ( data == null && fn == null ) {

		// ( types, fn )
		fn = selector;
		data = selector = undefined;
	} else if ( fn == null ) {
		if ( typeof selector === "string" ) {

			// ( types, selector, fn )
			fn = data;
			data = undefined;
		} else {

			// ( types, data, fn )
			fn = data;
			data = selector;
			selector = undefined;
		}
	}
	if ( fn === false ) {
		fn = returnFalse;
	} else if ( !fn ) {
		return elem;
	}

	if ( one === 1 ) {
		origFn = fn;
		fn = function( event ) {

			// Can use an empty set, since event contains the info
			jQuery().off( event );
			return origFn.apply( this, arguments );
		};

		// Use same guid so caller can remove using origFn
		fn.guid = origFn.guid || ( origFn.guid = jQuery.guid++ );
	}
	return elem.each( function() {
		jQuery.event.add( this, types, fn, data, selector );
	} );
}

/*
 * Helper functions for managing events -- not part of the public interface.
 * Props to Dean Edwards' addEvent library for many of the ideas.
 */
jQuery.event = {

	global: {},

	add: function( elem, types, handler, data, selector ) {

		var handleObjIn, eventHandle, tmp,
			events, t, handleObj,
			special, handlers, type, namespaces, origType,
			elemData = dataPriv.get( elem );

		// Only attach events to objects that accept data
		if ( !acceptData( elem ) ) {
			return;
		}

		// Caller can pass in an object of custom data in lieu of the handler
		if ( handler.handler ) {
			handleObjIn = handler;
			handler = handleObjIn.handler;
			selector = handleObjIn.selector;
		}

		// Ensure that invalid selectors throw exceptions at attach time
		// Evaluate against documentElement in case elem is a non-element node (e.g., document)
		if ( selector ) {
			jQuery.find.matchesSelector( documentElement, selector );
		}

		// Make sure that the handler has a unique ID, used to find/remove it later
		if ( !handler.guid ) {
			handler.guid = jQuery.guid++;
		}

		// Init the element's event structure and main handler, if this is the first
		if ( !( events = elemData.events ) ) {
			events = elemData.events = Object.create( null );
		}
		if ( !( eventHandle = elemData.handle ) ) {
			eventHandle = elemData.handle = function( e ) {

				// Discard the second event of a jQuery.event.trigger() and
				// when an event is called after a page has unloaded
				return typeof jQuery !== "undefined" && jQuery.event.triggered !== e.type ?
					jQuery.event.dispatch.apply( elem, arguments ) : undefined;
			};
		}

		// Handle multiple events separated by a space
		types = ( types || "" ).match( rnothtmlwhite ) || [ "" ];
		t = types.length;
		while ( t-- ) {
			tmp = rtypenamespace.exec( types[ t ] ) || [];
			type = origType = tmp[ 1 ];
			namespaces = ( tmp[ 2 ] || "" ).split( "." ).sort();

			// There *must* be a type, no attaching namespace-only handlers
			if ( !type ) {
				continue;
			}

			// If event changes its type, use the special event handlers for the changed type
			special = jQuery.event.special[ type ] || {};

			// If selector defined, determine special event api type, otherwise given type
			type = ( selector ? special.delegateType : special.bindType ) || type;

			// Update special based on newly reset type
			special = jQuery.event.special[ type ] || {};

			// handleObj is passed to all event handlers
			handleObj = jQuery.extend( {
				type: type,
				origType: origType,
				data: data,
				handler: handler,
				guid: handler.guid,
				selector: selector,
				needsContext: selector && jQuery.expr.match.needsContext.test( selector ),
				namespace: namespaces.join( "." )
			}, handleObjIn );

			// Init the event handler queue if we're the first
			if ( !( handlers = events[ type ] ) ) {
				handlers = events[ type ] = [];
				handlers.delegateCount = 0;

				// Only use addEventListener if the special events handler returns false
				if ( !special.setup ||
					special.setup.call( elem, data, namespaces, eventHandle ) === false ) {

					if ( elem.addEventListener ) {
						elem.addEventListener( type, eventHandle );
					}
				}
			}

			if ( special.add ) {
				special.add.call( elem, handleObj );

				if ( !handleObj.handler.guid ) {
					handleObj.handler.guid = handler.guid;
				}
			}

			// Add to the element's handler list, delegates in front
			if ( selector ) {
				handlers.splice( handlers.delegateCount++, 0, handleObj );
			} else {
				handlers.push( handleObj );
			}

			// Keep track of which events have ever been used, for event optimization
			jQuery.event.global[ type ] = true;
		}

	},

	// Detach an event or set of events from an element
	remove: function( elem, types, handler, selector, mappedTypes ) {

		var j, origCount, tmp,
			events, t, handleObj,
			special, handlers, type, namespaces, origType,
			elemData = dataPriv.hasData( elem ) && dataPriv.get( elem );

		if ( !elemData || !( events = elemData.events ) ) {
			return;
		}

		// Once for each type.namespace in types; type may be omitted
		types = ( types || "" ).match( rnothtmlwhite ) || [ "" ];
		t = types.length;
		while ( t-- ) {
			tmp = rtypenamespace.exec( types[ t ] ) || [];
			type = origType = tmp[ 1 ];
			namespaces = ( tmp[ 2 ] || "" ).split( "." ).sort();

			// Unbind all events (on this namespace, if provided) for the element
			if ( !type ) {
				for ( type in events ) {
					jQuery.event.remove( elem, type + types[ t ], handler, selector, true );
				}
				continue;
			}

			special = jQuery.event.special[ type ] || {};
			type = ( selector ? special.delegateType : special.bindType ) || type;
			handlers = events[ type ] || [];
			tmp = tmp[ 2 ] &&
				new RegExp( "(^|\\.)" + namespaces.join( "\\.(?:.*\\.|)" ) + "(\\.|$)" );

			// Remove matching events
			origCount = j = handlers.length;
			while ( j-- ) {
				handleObj = handlers[ j ];

				if ( ( mappedTypes || origType === handleObj.origType ) &&
					( !handler || handler.guid === handleObj.guid ) &&
					( !tmp || tmp.test( handleObj.namespace ) ) &&
					( !selector || selector === handleObj.selector ||
						selector === "**" && handleObj.selector ) ) {
					handlers.splice( j, 1 );

					if ( handleObj.selector ) {
						handlers.delegateCount--;
					}
					if ( special.remove ) {
						special.remove.call( elem, handleObj );
					}
				}
			}

			// Remove generic event handler if we removed something and no more handlers exist
			// (avoids potential for endless recursion during removal of special event handlers)
			if ( origCount && !handlers.length ) {
				if ( !special.teardown ||
					special.teardown.call( elem, namespaces, elemData.handle ) === false ) {

					jQuery.removeEvent( elem, type, elemData.handle );
				}

				delete events[ type ];
			}
		}

		// Remove data and the expando if it's no longer used
		if ( jQuery.isEmptyObject( events ) ) {
			dataPriv.remove( elem, "handle events" );
		}
	},

	dispatch: function( nativeEvent ) {

		var i, j, ret, matched, handleObj, handlerQueue,
			args = new Array( arguments.length ),

			// Make a writable jQuery.Event from the native event object
			event = jQuery.event.fix( nativeEvent ),

			handlers = (
				dataPriv.get( this, "events" ) || Object.create( null )
			)[ event.type ] || [],
			special = jQuery.event.special[ event.type ] || {};

		// Use the fix-ed jQuery.Event rather than the (read-only) native event
		args[ 0 ] = event;

		for ( i = 1; i < arguments.length; i++ ) {
			args[ i ] = arguments[ i ];
		}

		event.delegateTarget = this;

		// Call the preDispatch hook for the mapped type, and let it bail if desired
		if ( special.preDispatch && special.preDispatch.call( this, event ) === false ) {
			return;
		}

		// Determine handlers
		handlerQueue = jQuery.event.handlers.call( this, event, handlers );

		// Run delegates first; they may want to stop propagation beneath us
		i = 0;
		while ( ( matched = handlerQueue[ i++ ] ) && !event.isPropagationStopped() ) {
			event.currentTarget = matched.elem;

			j = 0;
			while ( ( handleObj = matched.handlers[ j++ ] ) &&
				!event.isImmediatePropagationStopped() ) {

				// If the event is namespaced, then each handler is only invoked if it is
				// specially universal or its namespaces are a superset of the event's.
				if ( !event.rnamespace || handleObj.namespace === false ||
					event.rnamespace.test( handleObj.namespace ) ) {

					event.handleObj = handleObj;
					event.data = handleObj.data;

					ret = ( ( jQuery.event.special[ handleObj.origType ] || {} ).handle ||
						handleObj.handler ).apply( matched.elem, args );

					if ( ret !== undefined ) {
						if ( ( event.result = ret ) === false ) {
							event.preventDefault();
							event.stopPropagation();
						}
					}
				}
			}
		}

		// Call the postDispatch hook for the mapped type
		if ( special.postDispatch ) {
			special.postDispatch.call( this, event );
		}

		return event.result;
	},

	handlers: function( event, handlers ) {
		var i, handleObj, sel, matchedHandlers, matchedSelectors,
			handlerQueue = [],
			delegateCount = handlers.delegateCount,
			cur = event.target;

		// Find delegate handlers
		if ( delegateCount &&

			// Support: IE <=9
			// Black-hole SVG <use> instance trees (trac-13180)
			cur.nodeType &&

			// Support: Firefox <=42
			// Suppress spec-violating clicks indicating a non-primary pointer button (trac-3861)
			// https://www.w3.org/TR/DOM-Level-3-Events/#event-type-click
			// Support: IE 11 only
			// ...but not arrow key "clicks" of radio inputs, which can have `button` -1 (gh-2343)
			!( event.type === "click" && event.button >= 1 ) ) {

			for ( ; cur !== this; cur = cur.parentNode || this ) {

				// Don't check non-elements (#13208)
				// Don't process clicks on disabled elements (#6911, #8165, #11382, #11764)
				if ( cur.nodeType === 1 && !( event.type === "click" && cur.disabled === true ) ) {
					matchedHandlers = [];
					matchedSelectors = {};
					for ( i = 0; i < delegateCount; i++ ) {
						handleObj = handlers[ i ];

						// Don't conflict with Object.prototype properties (#13203)
						sel = handleObj.selector + " ";

						if ( matchedSelectors[ sel ] === undefined ) {
							matchedSelectors[ sel ] = handleObj.needsContext ?
								jQuery( sel, this ).index( cur ) > -1 :
								jQuery.find( sel, this, null, [ cur ] ).length;
						}
						if ( matchedSelectors[ sel ] ) {
							matchedHandlers.push( handleObj );
						}
					}
					if ( matchedHandlers.length ) {
						handlerQueue.push( { elem: cur, handlers: matchedHandlers } );
					}
				}
			}
		}

		// Add the remaining (directly-bound) handlers
		cur = this;
		if ( delegateCount < handlers.length ) {
			handlerQueue.push( { elem: cur, handlers: handlers.slice( delegateCount ) } );
		}

		return handlerQueue;
	},

	addProp: function( name, hook ) {
		Object.defineProperty( jQuery.Event.prototype, name, {
			enumerable: true,
			configurable: true,

			get: isFunction( hook ) ?
				function() {
					if ( this.originalEvent ) {
						return hook( this.originalEvent );
					}
				} :
				function() {
					if ( this.originalEvent ) {
						return this.originalEvent[ name ];
					}
				},

			set: function( value ) {
				Object.defineProperty( this, name, {
					enumerable: true,
					configurable: true,
					writable: true,
					value: value
				} );
			}
		} );
	},

	fix: function( originalEvent ) {
		return originalEvent[ jQuery.expando ] ?
			originalEvent :
			new jQuery.Event( originalEvent );
	},

	special: {
		load: {

			// Prevent triggered image.load events from bubbling to window.load
			noBubble: true
		},
		click: {

			// Utilize native event to ensure correct state for checkable inputs
			setup: function( data ) {

				// For mutual compressibility with _default, replace `this` access with a local var.
				// `|| data` is dead code meant only to preserve the variable through minification.
				var el = this || data;

				// Claim the first handler
				if ( rcheckableType.test( el.type ) &&
					el.click && nodeName( el, "input" ) ) {

					// dataPriv.set( el, "click", ... )
					leverageNative( el, "click", returnTrue );
				}

				// Return false to allow normal processing in the caller
				return false;
			},
			trigger: function( data ) {

				// For mutual compressibility with _default, replace `this` access with a local var.
				// `|| data` is dead code meant only to preserve the variable through minification.
				var el = this || data;

				// Force setup before triggering a click
				if ( rcheckableType.test( el.type ) &&
					el.click && nodeName( el, "input" ) ) {

					leverageNative( el, "click" );
				}

				// Return non-false to allow normal event-path propagation
				return true;
			},

			// For cross-browser consistency, suppress native .click() on links
			// Also prevent it if we're currently inside a leveraged native-event stack
			_default: function( event ) {
				var target = event.target;
				return rcheckableType.test( target.type ) &&
					target.click && nodeName( target, "input" ) &&
					dataPriv.get( target, "click" ) ||
					nodeName( target, "a" );
			}
		},

		beforeunload: {
			postDispatch: function( event ) {

				// Support: Firefox 20+
				// Firefox doesn't alert if the returnValue field is not set.
				if ( event.result !== undefined && event.originalEvent ) {
					event.originalEvent.returnValue = event.result;
				}
			}
		}
	}
};

// Ensure the presence of an event listener that handles manually-triggered
// synthetic events by interrupting progress until reinvoked in response to
// *native* events that it fires directly, ensuring that state changes have
// already occurred before other listeners are invoked.
function leverageNative( el, type, expectSync ) {

	// Missing expectSync indicates a trigger call, which must force setup through jQuery.event.add
	if ( !expectSync ) {
		if ( dataPriv.get( el, type ) === undefined ) {
			jQuery.event.add( el, type, returnTrue );
		}
		return;
	}

	// Register the controller as a special universal handler for all event namespaces
	dataPriv.set( el, type, false );
	jQuery.event.add( el, type, {
		namespace: false,
		handler: function( event ) {
			var notAsync, result,
				saved = dataPriv.get( this, type );

			if ( ( event.isTrigger & 1 ) && this[ type ] ) {

				// Interrupt processing of the outer synthetic .trigger()ed event
				// Saved data should be false in such cases, but might be a leftover capture object
				// from an async native handler (gh-4350)
				if ( !saved.length ) {

					// Store arguments for use when handling the inner native event
					// There will always be at least one argument (an event object), so this array
					// will not be confused with a leftover capture object.
					saved = slice.call( arguments );
					dataPriv.set( this, type, saved );

					// Trigger the native event and capture its result
					// Support: IE <=9 - 11+
					// focus() and blur() are asynchronous
					notAsync = expectSync( this, type );
					this[ type ]();
					result = dataPriv.get( this, type );
					if ( saved !== result || notAsync ) {
						dataPriv.set( this, type, false );
					} else {
						result = {};
					}
					if ( saved !== result ) {

						// Cancel the outer synthetic event
						event.stopImmediatePropagation();
						event.preventDefault();

						// Support: Chrome 86+
						// In Chrome, if an element having a focusout handler is blurred by
						// clicking outside of it, it invokes the handler synchronously. If
						// that handler calls `.remove()` on the element, the data is cleared,
						// leaving `result` undefined. We need to guard against this.
						return result && result.value;
					}

				// If this is an inner synthetic event for an event with a bubbling surrogate
				// (focus or blur), assume that the surrogate already propagated from triggering the
				// native event and prevent that from happening again here.
				// This technically gets the ordering wrong w.r.t. to `.trigger()` (in which the
				// bubbling surrogate propagates *after* the non-bubbling base), but that seems
				// less bad than duplication.
				} else if ( ( jQuery.event.special[ type ] || {} ).delegateType ) {
					event.stopPropagation();
				}

			// If this is a native event triggered above, everything is now in order
			// Fire an inner synthetic event with the original arguments
			} else if ( saved.length ) {

				// ...and capture the result
				dataPriv.set( this, type, {
					value: jQuery.event.trigger(

						// Support: IE <=9 - 11+
						// Extend with the prototype to reset the above stopImmediatePropagation()
						jQuery.extend( saved[ 0 ], jQuery.Event.prototype ),
						saved.slice( 1 ),
						this
					)
				} );

				// Abort handling of the native event
				event.stopImmediatePropagation();
			}
		}
	} );
}

jQuery.removeEvent = function( elem, type, handle ) {

	// This "if" is needed for plain objects
	if ( elem.removeEventListener ) {
		elem.removeEventListener( type, handle );
	}
};

jQuery.Event = function( src, props ) {

	// Allow instantiation without the 'new' keyword
	if ( !( this instanceof jQuery.Event ) ) {
		return new jQuery.Event( src, props );
	}

	// Event object
	if ( src && src.type ) {
		this.originalEvent = src;
		this.type = src.type;

		// Events bubbling up the document may have been marked as prevented
		// by a handler lower down the tree; reflect the correct value.
		this.isDefaultPrevented = src.defaultPrevented ||
				src.defaultPrevented === undefined &&

				// Support: Android <=2.3 only
				src.returnValue === false ?
			returnTrue :
			returnFalse;

		// Create target properties
		// Support: Safari <=6 - 7 only
		// Target should not be a text node (#504, #13143)
		this.target = ( src.target && src.target.nodeType === 3 ) ?
			src.target.parentNode :
			src.target;

		this.currentTarget = src.currentTarget;
		this.relatedTarget = src.relatedTarget;

	// Event type
	} else {
		this.type = src;
	}

	// Put explicitly provided properties onto the event object
	if ( props ) {
		jQuery.extend( this, props );
	}

	// Create a timestamp if incoming event doesn't have one
	this.timeStamp = src && src.timeStamp || Date.now();

	// Mark it as fixed
	this[ jQuery.expando ] = true;
};

// jQuery.Event is based on DOM3 Events as specified by the ECMAScript Language Binding
// https://www.w3.org/TR/2003/WD-DOM-Level-3-Events-20030331/ecma-script-binding.html
jQuery.Event.prototype = {
	constructor: jQuery.Event,
	isDefaultPrevented: returnFalse,
	isPropagationStopped: returnFalse,
	isImmediatePropagationStopped: returnFalse,
	isSimulated: false,

	preventDefault: function() {
		var e = this.originalEvent;

		this.isDefaultPrevented = returnTrue;

		if ( e && !this.isSimulated ) {
			e.preventDefault();
		}
	},
	stopPropagation: function() {
		var e = this.originalEvent;

		this.isPropagationStopped = returnTrue;

		if ( e && !this.isSimulated ) {
			e.stopPropagation();
		}
	},
	stopImmediatePropagation: function() {
		var e = this.originalEvent;

		this.isImmediatePropagationStopped = returnTrue;

		if ( e && !this.isSimulated ) {
			e.stopImmediatePropagation();
		}

		this.stopPropagation();
	}
};

// Includes all common event props including KeyEvent and MouseEvent specific props
jQuery.each( {
	altKey: true,
	bubbles: true,
	cancelable: true,
	changedTouches: true,
	ctrlKey: true,
	detail: true,
	eventPhase: true,
	metaKey: true,
	pageX: true,
	pageY: true,
	shiftKey: true,
	view: true,
	"char": true,
	code: true,
	charCode: true,
	key: true,
	keyCode: true,
	button: true,
	buttons: true,
	clientX: true,
	clientY: true,
	offsetX: true,
	offsetY: true,
	pointerId: true,
	pointerType: true,
	screenX: true,
	screenY: true,
	targetTouches: true,
	toElement: true,
	touches: true,
	which: true
}, jQuery.event.addProp );

jQuery.each( { focus: "focusin", blur: "focusout" }, function( type, delegateType ) {
	jQuery.event.special[ type ] = {

		// Utilize native event if possible so blur/focus sequence is correct
		setup: function() {

			// Claim the first handler
			// dataPriv.set( this, "focus", ... )
			// dataPriv.set( this, "blur", ... )
			leverageNative( this, type, expectSync );

			// Return false to allow normal processing in the caller
			return false;
		},
		trigger: function() {

			// Force setup before trigger
			leverageNative( this, type );

			// Return non-false to allow normal event-path propagation
			return true;
		},

		// Suppress native focus or blur as it's already being fired
		// in leverageNative.
		_default: function() {
			return true;
		},

		delegateType: delegateType
	};
} );

// Create mouseenter/leave events using mouseover/out and event-time checks
// so that event delegation works in jQuery.
// Do the same for pointerenter/pointerleave and pointerover/pointerout
//
// Support: Safari 7 only
// Safari sends mouseenter too often; see:
// https://bugs.chromium.org/p/chromium/issues/detail?id=470258
// for the description of the bug (it existed in older Chrome versions as well).
jQuery.each( {
	mouseenter: "mouseover",
	mouseleave: "mouseout",
	pointerenter: "pointerover",
	pointerleave: "pointerout"
}, function( orig, fix ) {
	jQuery.event.special[ orig ] = {
		delegateType: fix,
		bindType: fix,

		handle: function( event ) {
			var ret,
				target = this,
				related = event.relatedTarget,
				handleObj = event.handleObj;

			// For mouseenter/leave call the handler if related is outside the target.
			// NB: No relatedTarget if the mouse left/entered the browser window
			if ( !related || ( related !== target && !jQuery.contains( target, related ) ) ) {
				event.type = handleObj.origType;
				ret = handleObj.handler.apply( this, arguments );
				event.type = fix;
			}
			return ret;
		}
	};
} );

jQuery.fn.extend( {

	on: function( types, selector, data, fn ) {
		return on( this, types, selector, data, fn );
	},
	one: function( types, selector, data, fn ) {
		return on( this, types, selector, data, fn, 1 );
	},
	off: function( types, selector, fn ) {
		var handleObj, type;
		if ( types && types.preventDefault && types.handleObj ) {

			// ( event )  dispatched jQuery.Event
			handleObj = types.handleObj;
			jQuery( types.delegateTarget ).off(
				handleObj.namespace ?
					handleObj.origType + "." + handleObj.namespace :
					handleObj.origType,
				handleObj.selector,
				handleObj.handler
			);
			return this;
		}
		if ( typeof types === "object" ) {

			// ( types-object [, selector] )
			for ( type in types ) {
				this.off( type, selector, types[ type ] );
			}
			return this;
		}
		if ( selector === false || typeof selector === "function" ) {

			// ( types [, fn] )
			fn = selector;
			selector = undefined;
		}
		if ( fn === false ) {
			fn = returnFalse;
		}
		return this.each( function() {
			jQuery.event.remove( this, types, fn, selector );
		} );
	}
} );


var

	// Support: IE <=10 - 11, Edge 12 - 13 only
	// In IE/Edge using regex groups here causes severe slowdowns.
	// See https://connect.microsoft.com/IE/feedback/details/1736512/
	rnoInnerhtml = /<script|<style|<link/i,

	// checked="checked" or checked
	rchecked = /checked\s*(?:[^=]|=\s*.checked.)/i,
	rcleanScript = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;

// Prefer a tbody over its parent table for containing new rows
function manipulationTarget( elem, content ) {
	if ( nodeName( elem, "table" ) &&
		nodeName( content.nodeType !== 11 ? content : content.firstChild, "tr" ) ) {

		return jQuery( elem ).children( "tbody" )[ 0 ] || elem;
	}

	return elem;
}

// Replace/restore the type attribute of script elements for safe DOM manipulation
function disableScript( elem ) {
	elem.type = ( elem.getAttribute( "type" ) !== null ) + "/" + elem.type;
	return elem;
}
function restoreScript( elem ) {
	if ( ( elem.type || "" ).slice( 0, 5 ) === "true/" ) {
		elem.type = elem.type.slice( 5 );
	} else {
		elem.removeAttribute( "type" );
	}

	return elem;
}

function cloneCopyEvent( src, dest ) {
	var i, l, type, pdataOld, udataOld, udataCur, events;

	if ( dest.nodeType !== 1 ) {
		return;
	}

	// 1. Copy private data: events, handlers, etc.
	if ( dataPriv.hasData( src ) ) {
		pdataOld = dataPriv.get( src );
		events = pdataOld.events;

		if ( events ) {
			dataPriv.remove( dest, "handle events" );

			for ( type in events ) {
				for ( i = 0, l = events[ type ].length; i < l; i++ ) {
					jQuery.event.add( dest, type, events[ type ][ i ] );
				}
			}
		}
	}

	// 2. Copy user data
	if ( dataUser.hasData( src ) ) {
		udataOld = dataUser.access( src );
		udataCur = jQuery.extend( {}, udataOld );

		dataUser.set( dest, udataCur );
	}
}

// Fix IE bugs, see support tests
function fixInput( src, dest ) {
	var nodeName = dest.nodeName.toLowerCase();

	// Fails to persist the checked state of a cloned checkbox or radio button.
	if ( nodeName === "input" && rcheckableType.test( src.type ) ) {
		dest.checked = src.checked;

	// Fails to return the selected option to the default selected state when cloning options
	} else if ( nodeName === "input" || nodeName === "textarea" ) {
		dest.defaultValue = src.defaultValue;
	}
}

function domManip( collection, args, callback, ignored ) {

	// Flatten any nested arrays
	args = flat( args );

	var fragment, first, scripts, hasScripts, node, doc,
		i = 0,
		l = collection.length,
		iNoClone = l - 1,
		value = args[ 0 ],
		valueIsFunction = isFunction( value );

	// We can't cloneNode fragments that contain checked, in WebKit
	if ( valueIsFunction ||
			( l > 1 && typeof value === "string" &&
				!support.checkClone && rchecked.test( value ) ) ) {
		return collection.each( function( index ) {
			var self = collection.eq( index );
			if ( valueIsFunction ) {
				args[ 0 ] = value.call( this, index, self.html() );
			}
			domManip( self, args, callback, ignored );
		} );
	}

	if ( l ) {
		fragment = buildFragment( args, collection[ 0 ].ownerDocument, false, collection, ignored );
		first = fragment.firstChild;

		if ( fragment.childNodes.length === 1 ) {
			fragment = first;
		}

		// Require either new content or an interest in ignored elements to invoke the callback
		if ( first || ignored ) {
			scripts = jQuery.map( getAll( fragment, "script" ), disableScript );
			hasScripts = scripts.length;

			// Use the original fragment for the last item
			// instead of the first because it can end up
			// being emptied incorrectly in certain situations (#8070).
			for ( ; i < l; i++ ) {
				node = fragment;

				if ( i !== iNoClone ) {
					node = jQuery.clone( node, true, true );

					// Keep references to cloned scripts for later restoration
					if ( hasScripts ) {

						// Support: Android <=4.0 only, PhantomJS 1 only
						// push.apply(_, arraylike) throws on ancient WebKit
						jQuery.merge( scripts, getAll( node, "script" ) );
					}
				}

				callback.call( collection[ i ], node, i );
			}

			if ( hasScripts ) {
				doc = scripts[ scripts.length - 1 ].ownerDocument;

				// Reenable scripts
				jQuery.map( scripts, restoreScript );

				// Evaluate executable scripts on first document insertion
				for ( i = 0; i < hasScripts; i++ ) {
					node = scripts[ i ];
					if ( rscriptType.test( node.type || "" ) &&
						!dataPriv.access( node, "globalEval" ) &&
						jQuery.contains( doc, node ) ) {

						if ( node.src && ( node.type || "" ).toLowerCase()  !== "module" ) {

							// Optional AJAX dependency, but won't run scripts if not present
							if ( jQuery._evalUrl && !node.noModule ) {
								jQuery._evalUrl( node.src, {
									nonce: node.nonce || node.getAttribute( "nonce" )
								}, doc );
							}
						} else {
							DOMEval( node.textContent.replace( rcleanScript, "" ), node, doc );
						}
					}
				}
			}
		}
	}

	return collection;
}

function remove( elem, selector, keepData ) {
	var node,
		nodes = selector ? jQuery.filter( selector, elem ) : elem,
		i = 0;

	for ( ; ( node = nodes[ i ] ) != null; i++ ) {
		if ( !keepData && node.nodeType === 1 ) {
			jQuery.cleanData( getAll( node ) );
		}

		if ( node.parentNode ) {
			if ( keepData && isAttached( node ) ) {
				setGlobalEval( getAll( node, "script" ) );
			}
			node.parentNode.removeChild( node );
		}
	}

	return elem;
}

jQuery.extend( {
	htmlPrefilter: function( html ) {
		return html;
	},

	clone: function( elem, dataAndEvents, deepDataAndEvents ) {
		var i, l, srcElements, destElements,
			clone = elem.cloneNode( true ),
			inPage = isAttached( elem );

		// Fix IE cloning issues
		if ( !support.noCloneChecked && ( elem.nodeType === 1 || elem.nodeType === 11 ) &&
				!jQuery.isXMLDoc( elem ) ) {

			// We eschew Sizzle here for performance reasons: https://jsperf.com/getall-vs-sizzle/2
			destElements = getAll( clone );
			srcElements = getAll( elem );

			for ( i = 0, l = srcElements.length; i < l; i++ ) {
				fixInput( srcElements[ i ], destElements[ i ] );
			}
		}

		// Copy the events from the original to the clone
		if ( dataAndEvents ) {
			if ( deepDataAndEvents ) {
				srcElements = srcElements || getAll( elem );
				destElements = destElements || getAll( clone );

				for ( i = 0, l = srcElements.length; i < l; i++ ) {
					cloneCopyEvent( srcElements[ i ], destElements[ i ] );
				}
			} else {
				cloneCopyEvent( elem, clone );
			}
		}

		// Preserve script evaluation history
		destElements = getAll( clone, "script" );
		if ( destElements.length > 0 ) {
			setGlobalEval( destElements, !inPage && getAll( elem, "script" ) );
		}

		// Return the cloned set
		return clone;
	},

	cleanData: function( elems ) {
		var data, elem, type,
			special = jQuery.event.special,
			i = 0;

		for ( ; ( elem = elems[ i ] ) !== undefined; i++ ) {
			if ( acceptData( elem ) ) {
				if ( ( data = elem[ dataPriv.expando ] ) ) {
					if ( data.events ) {
						for ( type in data.events ) {
							if ( special[ type ] ) {
								jQuery.event.remove( elem, type );

							// This is a shortcut to avoid jQuery.event.remove's overhead
							} else {
								jQuery.removeEvent( elem, type, data.handle );
							}
						}
					}

					// Support: Chrome <=35 - 45+
					// Assign undefined instead of using delete, see Data#remove
					elem[ dataPriv.expando ] = undefined;
				}
				if ( elem[ dataUser.expando ] ) {

					// Support: Chrome <=35 - 45+
					// Assign undefined instead of using delete, see Data#remove
					elem[ dataUser.expando ] = undefined;
				}
			}
		}
	}
} );

jQuery.fn.extend( {
	detach: function( selector ) {
		return remove( this, selector, true );
	},

	remove: function( selector ) {
		return remove( this, selector );
	},

	text: function( value ) {
		return access( this, function( value ) {
			return value === undefined ?
				jQuery.text( this ) :
				this.empty().each( function() {
					if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
						this.textContent = value;
					}
				} );
		}, null, value, arguments.length );
	},

	append: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
				var target = manipulationTarget( this, elem );
				target.appendChild( elem );
			}
		} );
	},

	prepend: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
				var target = manipulationTarget( this, elem );
				target.insertBefore( elem, target.firstChild );
			}
		} );
	},

	before: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.parentNode ) {
				this.parentNode.insertBefore( elem, this );
			}
		} );
	},

	after: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.parentNode ) {
				this.parentNode.insertBefore( elem, this.nextSibling );
			}
		} );
	},

	empty: function() {
		var elem,
			i = 0;

		for ( ; ( elem = this[ i ] ) != null; i++ ) {
			if ( elem.nodeType === 1 ) {

				// Prevent memory leaks
				jQuery.cleanData( getAll( elem, false ) );

				// Remove any remaining nodes
				elem.textContent = "";
			}
		}

		return this;
	},

	clone: function( dataAndEvents, deepDataAndEvents ) {
		dataAndEvents = dataAndEvents == null ? false : dataAndEvents;
		deepDataAndEvents = deepDataAndEvents == null ? dataAndEvents : deepDataAndEvents;

		return this.map( function() {
			return jQuery.clone( this, dataAndEvents, deepDataAndEvents );
		} );
	},

	html: function( value ) {
		return access( this, function( value ) {
			var elem = this[ 0 ] || {},
				i = 0,
				l = this.length;

			if ( value === undefined && elem.nodeType === 1 ) {
				return elem.innerHTML;
			}

			// See if we can take a shortcut and just use innerHTML
			if ( typeof value === "string" && !rnoInnerhtml.test( value ) &&
				!wrapMap[ ( rtagName.exec( value ) || [ "", "" ] )[ 1 ].toLowerCase() ] ) {

				value = jQuery.htmlPrefilter( value );

				try {
					for ( ; i < l; i++ ) {
						elem = this[ i ] || {};

						// Remove element nodes and prevent memory leaks
						if ( elem.nodeType === 1 ) {
							jQuery.cleanData( getAll( elem, false ) );
							elem.innerHTML = value;
						}
					}

					elem = 0;

				// If using innerHTML throws an exception, use the fallback method
				} catch ( e ) {}
			}

			if ( elem ) {
				this.empty().append( value );
			}
		}, null, value, arguments.length );
	},

	replaceWith: function() {
		var ignored = [];

		// Make the changes, replacing each non-ignored context element with the new content
		return domManip( this, arguments, function( elem ) {
			var parent = this.parentNode;

			if ( jQuery.inArray( this, ignored ) < 0 ) {
				jQuery.cleanData( getAll( this ) );
				if ( parent ) {
					parent.replaceChild( elem, this );
				}
			}

		// Force callback invocation
		}, ignored );
	}
} );

jQuery.each( {
	appendTo: "append",
	prependTo: "prepend",
	insertBefore: "before",
	insertAfter: "after",
	replaceAll: "replaceWith"
}, function( name, original ) {
	jQuery.fn[ name ] = function( selector ) {
		var elems,
			ret = [],
			insert = jQuery( selector ),
			last = insert.length - 1,
			i = 0;

		for ( ; i <= last; i++ ) {
			elems = i === last ? this : this.clone( true );
			jQuery( insert[ i ] )[ original ]( elems );

			// Support: Android <=4.0 only, PhantomJS 1 only
			// .get() because push.apply(_, arraylike) throws on ancient WebKit
			push.apply( ret, elems.get() );
		}

		return this.pushStack( ret );
	};
} );
var rnumnonpx = new RegExp( "^(" + pnum + ")(?!px)[a-z%]+$", "i" );

var getStyles = function( elem ) {

		// Support: IE <=11 only, Firefox <=30 (#15098, #14150)
		// IE throws on elements created in popups
		// FF meanwhile throws on frame elements through "defaultView.getComputedStyle"
		var view = elem.ownerDocument.defaultView;

		if ( !view || !view.opener ) {
			view = window;
		}

		return view.getComputedStyle( elem );
	};

var swap = function( elem, options, callback ) {
	var ret, name,
		old = {};

	// Remember the old values, and insert the new ones
	for ( name in options ) {
		old[ name ] = elem.style[ name ];
		elem.style[ name ] = options[ name ];
	}

	ret = callback.call( elem );

	// Revert the old values
	for ( name in options ) {
		elem.style[ name ] = old[ name ];
	}

	return ret;
};


var rboxStyle = new RegExp( cssExpand.join( "|" ), "i" );



( function() {

	// Executing both pixelPosition & boxSizingReliable tests require only one layout
	// so they're executed at the same time to save the second computation.
	function computeStyleTests() {

		// This is a singleton, we need to execute it only once
		if ( !div ) {
			return;
		}

		container.style.cssText = "position:absolute;left:-11111px;width:60px;" +
			"margin-top:1px;padding:0;border:0";
		div.style.cssText =
			"position:relative;display:block;box-sizing:border-box;overflow:scroll;" +
			"margin:auto;border:1px;padding:1px;" +
			"width:60%;top:1%";
		documentElement.appendChild( container ).appendChild( div );

		var divStyle = window.getComputedStyle( div );
		pixelPositionVal = divStyle.top !== "1%";

		// Support: Android 4.0 - 4.3 only, Firefox <=3 - 44
		reliableMarginLeftVal = roundPixelMeasures( divStyle.marginLeft ) === 12;

		// Support: Android 4.0 - 4.3 only, Safari <=9.1 - 10.1, iOS <=7.0 - 9.3
		// Some styles come back with percentage values, even though they shouldn't
		div.style.right = "60%";
		pixelBoxStylesVal = roundPixelMeasures( divStyle.right ) === 36;

		// Support: IE 9 - 11 only
		// Detect misreporting of content dimensions for box-sizing:border-box elements
		boxSizingReliableVal = roundPixelMeasures( divStyle.width ) === 36;

		// Support: IE 9 only
		// Detect overflow:scroll screwiness (gh-3699)
		// Support: Chrome <=64
		// Don't get tricked when zoom affects offsetWidth (gh-4029)
		div.style.position = "absolute";
		scrollboxSizeVal = roundPixelMeasures( div.offsetWidth / 3 ) === 12;

		documentElement.removeChild( container );

		// Nullify the div so it wouldn't be stored in the memory and
		// it will also be a sign that checks already performed
		div = null;
	}

	function roundPixelMeasures( measure ) {
		return Math.round( parseFloat( measure ) );
	}

	var pixelPositionVal, boxSizingReliableVal, scrollboxSizeVal, pixelBoxStylesVal,
		reliableTrDimensionsVal, reliableMarginLeftVal,
		container = document.createElement( "div" ),
		div = document.createElement( "div" );

	// Finish early in limited (non-browser) environments
	if ( !div.style ) {
		return;
	}

	// Support: IE <=9 - 11 only
	// Style of cloned element affects source element cloned (#8908)
	div.style.backgroundClip = "content-box";
	div.cloneNode( true ).style.backgroundClip = "";
	support.clearCloneStyle = div.style.backgroundClip === "content-box";

	jQuery.extend( support, {
		boxSizingReliable: function() {
			computeStyleTests();
			return boxSizingReliableVal;
		},
		pixelBoxStyles: function() {
			computeStyleTests();
			return pixelBoxStylesVal;
		},
		pixelPosition: function() {
			computeStyleTests();
			return pixelPositionVal;
		},
		reliableMarginLeft: function() {
			computeStyleTests();
			return reliableMarginLeftVal;
		},
		scrollboxSize: function() {
			computeStyleTests();
			return scrollboxSizeVal;
		},

		// Support: IE 9 - 11+, Edge 15 - 18+
		// IE/Edge misreport `getComputedStyle` of table rows with width/height
		// set in CSS while `offset*` properties report correct values.
		// Behavior in IE 9 is more subtle than in newer versions & it passes
		// some versions of this test; make sure not to make it pass there!
		//
		// Support: Firefox 70+
		// Only Firefox includes border widths
		// in computed dimensions. (gh-4529)
		reliableTrDimensions: function() {
			var table, tr, trChild, trStyle;
			if ( reliableTrDimensionsVal == null ) {
				table = document.createElement( "table" );
				tr = document.createElement( "tr" );
				trChild = document.createElement( "div" );

				table.style.cssText = "position:absolute;left:-11111px;border-collapse:separate";
				tr.style.cssText = "border:1px solid";

				// Support: Chrome 86+
				// Height set through cssText does not get applied.
				// Computed height then comes back as 0.
				tr.style.height = "1px";
				trChild.style.height = "9px";

				// Support: Android 8 Chrome 86+
				// In our bodyBackground.html iframe,
				// display for all div elements is set to "inline",
				// which causes a problem only in Android 8 Chrome 86.
				// Ensuring the div is display: block
				// gets around this issue.
				trChild.style.display = "block";

				documentElement
					.appendChild( table )
					.appendChild( tr )
					.appendChild( trChild );

				trStyle = window.getComputedStyle( tr );
				reliableTrDimensionsVal = ( parseInt( trStyle.height, 10 ) +
					parseInt( trStyle.borderTopWidth, 10 ) +
					parseInt( trStyle.borderBottomWidth, 10 ) ) === tr.offsetHeight;

				documentElement.removeChild( table );
			}
			return reliableTrDimensionsVal;
		}
	} );
} )();


function curCSS( elem, name, computed ) {
	var width, minWidth, maxWidth, ret,

		// Support: Firefox 51+
		// Retrieving style before computed somehow
		// fixes an issue with getting wrong values
		// on detached elements
		style = elem.style;

	computed = computed || getStyles( elem );

	// getPropertyValue is needed for:
	//   .css('filter') (IE 9 only, #12537)
	//   .css('--customProperty) (#3144)
	if ( computed ) {
		ret = computed.getPropertyValue( name ) || computed[ name ];

		if ( ret === "" && !isAttached( elem ) ) {
			ret = jQuery.style( elem, name );
		}

		// A tribute to the "awesome hack by Dean Edwards"
		// Android Browser returns percentage for some values,
		// but width seems to be reliably pixels.
		// This is against the CSSOM draft spec:
		// https://drafts.csswg.org/cssom/#resolved-values
		if ( !support.pixelBoxStyles() && rnumnonpx.test( ret ) && rboxStyle.test( name ) ) {

			// Remember the original values
			width = style.width;
			minWidth = style.minWidth;
			maxWidth = style.maxWidth;

			// Put in the new values to get a computed value out
			style.minWidth = style.maxWidth = style.width = ret;
			ret = computed.width;

			// Revert the changed values
			style.width = width;
			style.minWidth = minWidth;
			style.maxWidth = maxWidth;
		}
	}

	return ret !== undefined ?

		// Support: IE <=9 - 11 only
		// IE returns zIndex value as an integer.
		ret + "" :
		ret;
}


function addGetHookIf( conditionFn, hookFn ) {

	// Define the hook, we'll check on the first run if it's really needed.
	return {
		get: function() {
			if ( conditionFn() ) {

				// Hook not needed (or it's not possible to use it due
				// to missing dependency), remove it.
				delete this.get;
				return;
			}

			// Hook needed; redefine it so that the support test is not executed again.
			return ( this.get = hookFn ).apply( this, arguments );
		}
	};
}


var cssPrefixes = [ "Webkit", "Moz", "ms" ],
	emptyStyle = document.createElement( "div" ).style,
	vendorProps = {};

// Return a vendor-prefixed property or undefined
function vendorPropName( name ) {

	// Check for vendor prefixed names
	var capName = name[ 0 ].toUpperCase() + name.slice( 1 ),
		i = cssPrefixes.length;

	while ( i-- ) {
		name = cssPrefixes[ i ] + capName;
		if ( name in emptyStyle ) {
			return name;
		}
	}
}

// Return a potentially-mapped jQuery.cssProps or vendor prefixed property
function finalPropName( name ) {
	var final = jQuery.cssProps[ name ] || vendorProps[ name ];

	if ( final ) {
		return final;
	}
	if ( name in emptyStyle ) {
		return name;
	}
	return vendorProps[ name ] = vendorPropName( name ) || name;
}


var

	// Swappable if display is none or starts with table
	// except "table", "table-cell", or "table-caption"
	// See here for display values: https://developer.mozilla.org/en-US/docs/CSS/display
	rdisplayswap = /^(none|table(?!-c[ea]).+)/,
	rcustomProp = /^--/,
	cssShow = { position: "absolute", visibility: "hidden", display: "block" },
	cssNormalTransform = {
		letterSpacing: "0",
		fontWeight: "400"
	};

function setPositiveNumber( _elem, value, subtract ) {

	// Any relative (+/-) values have already been
	// normalized at this point
	var matches = rcssNum.exec( value );
	return matches ?

		// Guard against undefined "subtract", e.g., when used as in cssHooks
		Math.max( 0, matches[ 2 ] - ( subtract || 0 ) ) + ( matches[ 3 ] || "px" ) :
		value;
}

function boxModelAdjustment( elem, dimension, box, isBorderBox, styles, computedVal ) {
	var i = dimension === "width" ? 1 : 0,
		extra = 0,
		delta = 0;

	// Adjustment may not be necessary
	if ( box === ( isBorderBox ? "border" : "content" ) ) {
		return 0;
	}

	for ( ; i < 4; i += 2 ) {

		// Both box models exclude margin
		if ( box === "margin" ) {
			delta += jQuery.css( elem, box + cssExpand[ i ], true, styles );
		}

		// If we get here with a content-box, we're seeking "padding" or "border" or "margin"
		if ( !isBorderBox ) {

			// Add padding
			delta += jQuery.css( elem, "padding" + cssExpand[ i ], true, styles );

			// For "border" or "margin", add border
			if ( box !== "padding" ) {
				delta += jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );

			// But still keep track of it otherwise
			} else {
				extra += jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );
			}

		// If we get here with a border-box (content + padding + border), we're seeking "content" or
		// "padding" or "margin"
		} else {

			// For "content", subtract padding
			if ( box === "content" ) {
				delta -= jQuery.css( elem, "padding" + cssExpand[ i ], true, styles );
			}

			// For "content" or "padding", subtract border
			if ( box !== "margin" ) {
				delta -= jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );
			}
		}
	}

	// Account for positive content-box scroll gutter when requested by providing computedVal
	if ( !isBorderBox && computedVal >= 0 ) {

		// offsetWidth/offsetHeight is a rounded sum of content, padding, scroll gutter, and border
		// Assuming integer scroll gutter, subtract the rest and round down
		delta += Math.max( 0, Math.ceil(
			elem[ "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 ) ] -
			computedVal -
			delta -
			extra -
			0.5

		// If offsetWidth/offsetHeight is unknown, then we can't determine content-box scroll gutter
		// Use an explicit zero to avoid NaN (gh-3964)
		) ) || 0;
	}

	return delta;
}

function getWidthOrHeight( elem, dimension, extra ) {

	// Start with computed style
	var styles = getStyles( elem ),

		// To avoid forcing a reflow, only fetch boxSizing if we need it (gh-4322).
		// Fake content-box until we know it's needed to know the true value.
		boxSizingNeeded = !support.boxSizingReliable() || extra,
		isBorderBox = boxSizingNeeded &&
			jQuery.css( elem, "boxSizing", false, styles ) === "border-box",
		valueIsBorderBox = isBorderBox,

		val = curCSS( elem, dimension, styles ),
		offsetProp = "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 );

	// Support: Firefox <=54
	// Return a confounding non-pixel value or feign ignorance, as appropriate.
	if ( rnumnonpx.test( val ) ) {
		if ( !extra ) {
			return val;
		}
		val = "auto";
	}


	// Support: IE 9 - 11 only
	// Use offsetWidth/offsetHeight for when box sizing is unreliable.
	// In those cases, the computed value can be trusted to be border-box.
	if ( ( !support.boxSizingReliable() && isBorderBox ||

		// Support: IE 10 - 11+, Edge 15 - 18+
		// IE/Edge misreport `getComputedStyle` of table rows with width/height
		// set in CSS while `offset*` properties report correct values.
		// Interestingly, in some cases IE 9 doesn't suffer from this issue.
		!support.reliableTrDimensions() && nodeName( elem, "tr" ) ||

		// Fall back to offsetWidth/offsetHeight when value is "auto"
		// This happens for inline elements with no explicit setting (gh-3571)
		val === "auto" ||

		// Support: Android <=4.1 - 4.3 only
		// Also use offsetWidth/offsetHeight for misreported inline dimensions (gh-3602)
		!parseFloat( val ) && jQuery.css( elem, "display", false, styles ) === "inline" ) &&

		// Make sure the element is visible & connected
		elem.getClientRects().length ) {

		isBorderBox = jQuery.css( elem, "boxSizing", false, styles ) === "border-box";

		// Where available, offsetWidth/offsetHeight approximate border box dimensions.
		// Where not available (e.g., SVG), assume unreliable box-sizing and interpret the
		// retrieved value as a content box dimension.
		valueIsBorderBox = offsetProp in elem;
		if ( valueIsBorderBox ) {
			val = elem[ offsetProp ];
		}
	}

	// Normalize "" and auto
	val = parseFloat( val ) || 0;

	// Adjust for the element's box model
	return ( val +
		boxModelAdjustment(
			elem,
			dimension,
			extra || ( isBorderBox ? "border" : "content" ),
			valueIsBorderBox,
			styles,

			// Provide the current computed size to request scroll gutter calculation (gh-3589)
			val
		)
	) + "px";
}

jQuery.extend( {

	// Add in style property hooks for overriding the default
	// behavior of getting and setting a style property
	cssHooks: {
		opacity: {
			get: function( elem, computed ) {
				if ( computed ) {

					// We should always get a number back from opacity
					var ret = curCSS( elem, "opacity" );
					return ret === "" ? "1" : ret;
				}
			}
		}
	},

	// Don't automatically add "px" to these possibly-unitless properties
	cssNumber: {
		"animationIterationCount": true,
		"columnCount": true,
		"fillOpacity": true,
		"flexGrow": true,
		"flexShrink": true,
		"fontWeight": true,
		"gridArea": true,
		"gridColumn": true,
		"gridColumnEnd": true,
		"gridColumnStart": true,
		"gridRow": true,
		"gridRowEnd": true,
		"gridRowStart": true,
		"lineHeight": true,
		"opacity": true,
		"order": true,
		"orphans": true,
		"widows": true,
		"zIndex": true,
		"zoom": true
	},

	// Add in properties whose names you wish to fix before
	// setting or getting the value
	cssProps: {},

	// Get and set the style property on a DOM Node
	style: function( elem, name, value, extra ) {

		// Don't set styles on text and comment nodes
		if ( !elem || elem.nodeType === 3 || elem.nodeType === 8 || !elem.style ) {
			return;
		}

		// Make sure that we're working with the right name
		var ret, type, hooks,
			origName = camelCase( name ),
			isCustomProp = rcustomProp.test( name ),
			style = elem.style;

		// Make sure that we're working with the right name. We don't
		// want to query the value if it is a CSS custom property
		// since they are user-defined.
		if ( !isCustomProp ) {
			name = finalPropName( origName );
		}

		// Gets hook for the prefixed version, then unprefixed version
		hooks = jQuery.cssHooks[ name ] || jQuery.cssHooks[ origName ];

		// Check if we're setting a value
		if ( value !== undefined ) {
			type = typeof value;

			// Convert "+=" or "-=" to relative numbers (#7345)
			if ( type === "string" && ( ret = rcssNum.exec( value ) ) && ret[ 1 ] ) {
				value = adjustCSS( elem, name, ret );

				// Fixes bug #9237
				type = "number";
			}

			// Make sure that null and NaN values aren't set (#7116)
			if ( value == null || value !== value ) {
				return;
			}

			// If a number was passed in, add the unit (except for certain CSS properties)
			// The isCustomProp check can be removed in jQuery 4.0 when we only auto-append
			// "px" to a few hardcoded values.
			if ( type === "number" && !isCustomProp ) {
				value += ret && ret[ 3 ] || ( jQuery.cssNumber[ origName ] ? "" : "px" );
			}

			// background-* props affect original clone's values
			if ( !support.clearCloneStyle && value === "" && name.indexOf( "background" ) === 0 ) {
				style[ name ] = "inherit";
			}

			// If a hook was provided, use that value, otherwise just set the specified value
			if ( !hooks || !( "set" in hooks ) ||
				( value = hooks.set( elem, value, extra ) ) !== undefined ) {

				if ( isCustomProp ) {
					style.setProperty( name, value );
				} else {
					style[ name ] = value;
				}
			}

		} else {

			// If a hook was provided get the non-computed value from there
			if ( hooks && "get" in hooks &&
				( ret = hooks.get( elem, false, extra ) ) !== undefined ) {

				return ret;
			}

			// Otherwise just get the value from the style object
			return style[ name ];
		}
	},

	css: function( elem, name, extra, styles ) {
		var val, num, hooks,
			origName = camelCase( name ),
			isCustomProp = rcustomProp.test( name );

		// Make sure that we're working with the right name. We don't
		// want to modify the value if it is a CSS custom property
		// since they are user-defined.
		if ( !isCustomProp ) {
			name = finalPropName( origName );
		}

		// Try prefixed name followed by the unprefixed name
		hooks = jQuery.cssHooks[ name ] || jQuery.cssHooks[ origName ];

		// If a hook was provided get the computed value from there
		if ( hooks && "get" in hooks ) {
			val = hooks.get( elem, true, extra );
		}

		// Otherwise, if a way to get the computed value exists, use that
		if ( val === undefined ) {
			val = curCSS( elem, name, styles );
		}

		// Convert "normal" to computed value
		if ( val === "normal" && name in cssNormalTransform ) {
			val = cssNormalTransform[ name ];
		}

		// Make numeric if forced or a qualifier was provided and val looks numeric
		if ( extra === "" || extra ) {
			num = parseFloat( val );
			return extra === true || isFinite( num ) ? num || 0 : val;
		}

		return val;
	}
} );

jQuery.each( [ "height", "width" ], function( _i, dimension ) {
	jQuery.cssHooks[ dimension ] = {
		get: function( elem, computed, extra ) {
			if ( computed ) {

				// Certain elements can have dimension info if we invisibly show them
				// but it must have a current display style that would benefit
				return rdisplayswap.test( jQuery.css( elem, "display" ) ) &&

					// Support: Safari 8+
					// Table columns in Safari have non-zero offsetWidth & zero
					// getBoundingClientRect().width unless display is changed.
					// Support: IE <=11 only
					// Running getBoundingClientRect on a disconnected node
					// in IE throws an error.
					( !elem.getClientRects().length || !elem.getBoundingClientRect().width ) ?
					swap( elem, cssShow, function() {
						return getWidthOrHeight( elem, dimension, extra );
					} ) :
					getWidthOrHeight( elem, dimension, extra );
			}
		},

		set: function( elem, value, extra ) {
			var matches,
				styles = getStyles( elem ),

				// Only read styles.position if the test has a chance to fail
				// to avoid forcing a reflow.
				scrollboxSizeBuggy = !support.scrollboxSize() &&
					styles.position === "absolute",

				// To avoid forcing a reflow, only fetch boxSizing if we need it (gh-3991)
				boxSizingNeeded = scrollboxSizeBuggy || extra,
				isBorderBox = boxSizingNeeded &&
					jQuery.css( elem, "boxSizing", false, styles ) === "border-box",
				subtract = extra ?
					boxModelAdjustment(
						elem,
						dimension,
						extra,
						isBorderBox,
						styles
					) :
					0;

			// Account for unreliable border-box dimensions by comparing offset* to computed and
			// faking a content-box to get border and padding (gh-3699)
			if ( isBorderBox && scrollboxSizeBuggy ) {
				subtract -= Math.ceil(
					elem[ "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 ) ] -
					parseFloat( styles[ dimension ] ) -
					boxModelAdjustment( elem, dimension, "border", false, styles ) -
					0.5
				);
			}

			// Convert to pixels if value adjustment is needed
			if ( subtract && ( matches = rcssNum.exec( value ) ) &&
				( matches[ 3 ] || "px" ) !== "px" ) {

				elem.style[ dimension ] = value;
				value = jQuery.css( elem, dimension );
			}

			return setPositiveNumber( elem, value, subtract );
		}
	};
} );

jQuery.cssHooks.marginLeft = addGetHookIf( support.reliableMarginLeft,
	function( elem, computed ) {
		if ( computed ) {
			return ( parseFloat( curCSS( elem, "marginLeft" ) ) ||
				elem.getBoundingClientRect().left -
					swap( elem, { marginLeft: 0 }, function() {
						return elem.getBoundingClientRect().left;
					} )
			) + "px";
		}
	}
);

// These hooks are used by animate to expand properties
jQuery.each( {
	margin: "",
	padding: "",
	border: "Width"
}, function( prefix, suffix ) {
	jQuery.cssHooks[ prefix + suffix ] = {
		expand: function( value ) {
			var i = 0,
				expanded = {},

				// Assumes a single number if not a string
				parts = typeof value === "string" ? value.split( " " ) : [ value ];

			for ( ; i < 4; i++ ) {
				expanded[ prefix + cssExpand[ i ] + suffix ] =
					parts[ i ] || parts[ i - 2 ] || parts[ 0 ];
			}

			return expanded;
		}
	};

	if ( prefix !== "margin" ) {
		jQuery.cssHooks[ prefix + suffix ].set = setPositiveNumber;
	}
} );

jQuery.fn.extend( {
	css: function( name, value ) {
		return access( this, function( elem, name, value ) {
			var styles, len,
				map = {},
				i = 0;

			if ( Array.isArray( name ) ) {
				styles = getStyles( elem );
				len = name.length;

				for ( ; i < len; i++ ) {
					map[ name[ i ] ] = jQuery.css( elem, name[ i ], false, styles );
				}

				return map;
			}

			return value !== undefined ?
				jQuery.style( elem, name, value ) :
				jQuery.css( elem, name );
		}, name, value, arguments.length > 1 );
	}
} );


function Tween( elem, options, prop, end, easing ) {
	return new Tween.prototype.init( elem, options, prop, end, easing );
}
jQuery.Tween = Tween;

Tween.prototype = {
	constructor: Tween,
	init: function( elem, options, prop, end, easing, unit ) {
		this.elem = elem;
		this.prop = prop;
		this.easing = easing || jQuery.easing._default;
		this.options = options;
		this.start = this.now = this.cur();
		this.end = end;
		this.unit = unit || ( jQuery.cssNumber[ prop ] ? "" : "px" );
	},
	cur: function() {
		var hooks = Tween.propHooks[ this.prop ];

		return hooks && hooks.get ?
			hooks.get( this ) :
			Tween.propHooks._default.get( this );
	},
	run: function( percent ) {
		var eased,
			hooks = Tween.propHooks[ this.prop ];

		if ( this.options.duration ) {
			this.pos = eased = jQuery.easing[ this.easing ](
				percent, this.options.duration * percent, 0, 1, this.options.duration
			);
		} else {
			this.pos = eased = percent;
		}
		this.now = ( this.end - this.start ) * eased + this.start;

		if ( this.options.step ) {
			this.options.step.call( this.elem, this.now, this );
		}

		if ( hooks && hooks.set ) {
			hooks.set( this );
		} else {
			Tween.propHooks._default.set( this );
		}
		return this;
	}
};

Tween.prototype.init.prototype = Tween.prototype;

Tween.propHooks = {
	_default: {
		get: function( tween ) {
			var result;

			// Use a property on the element directly when it is not a DOM element,
			// or when there is no matching style property that exists.
			if ( tween.elem.nodeType !== 1 ||
				tween.elem[ tween.prop ] != null && tween.elem.style[ tween.prop ] == null ) {
				return tween.elem[ tween.prop ];
			}

			// Passing an empty string as a 3rd parameter to .css will automatically
			// attempt a parseFloat and fallback to a string if the parse fails.
			// Simple values such as "10px" are parsed to Float;
			// complex values such as "rotate(1rad)" are returned as-is.
			result = jQuery.css( tween.elem, tween.prop, "" );

			// Empty strings, null, undefined and "auto" are converted to 0.
			return !result || result === "auto" ? 0 : result;
		},
		set: function( tween ) {

			// Use step hook for back compat.
			// Use cssHook if its there.
			// Use .style if available and use plain properties where available.
			if ( jQuery.fx.step[ tween.prop ] ) {
				jQuery.fx.step[ tween.prop ]( tween );
			} else if ( tween.elem.nodeType === 1 && (
				jQuery.cssHooks[ tween.prop ] ||
					tween.elem.style[ finalPropName( tween.prop ) ] != null ) ) {
				jQuery.style( tween.elem, tween.prop, tween.now + tween.unit );
			} else {
				tween.elem[ tween.prop ] = tween.now;
			}
		}
	}
};

// Support: IE <=9 only
// Panic based approach to setting things on disconnected nodes
Tween.propHooks.scrollTop = Tween.propHooks.scrollLeft = {
	set: function( tween ) {
		if ( tween.elem.nodeType && tween.elem.parentNode ) {
			tween.elem[ tween.prop ] = tween.now;
		}
	}
};

jQuery.easing = {
	linear: function( p ) {
		return p;
	},
	swing: function( p ) {
		return 0.5 - Math.cos( p * Math.PI ) / 2;
	},
	_default: "swing"
};

jQuery.fx = Tween.prototype.init;

// Back compat <1.8 extension point
jQuery.fx.step = {};




var
	fxNow, inProgress,
	rfxtypes = /^(?:toggle|show|hide)$/,
	rrun = /queueHooks$/;

function schedule() {
	if ( inProgress ) {
		if ( document.hidden === false && window.requestAnimationFrame ) {
			window.requestAnimationFrame( schedule );
		} else {
			window.setTimeout( schedule, jQuery.fx.interval );
		}

		jQuery.fx.tick();
	}
}

// Animations created synchronously will run synchronously
function createFxNow() {
	window.setTimeout( function() {
		fxNow = undefined;
	} );
	return ( fxNow = Date.now() );
}

// Generate parameters to create a standard animation
function genFx( type, includeWidth ) {
	var which,
		i = 0,
		attrs = { height: type };

	// If we include width, step value is 1 to do all cssExpand values,
	// otherwise step value is 2 to skip over Left and Right
	includeWidth = includeWidth ? 1 : 0;
	for ( ; i < 4; i += 2 - includeWidth ) {
		which = cssExpand[ i ];
		attrs[ "margin" + which ] = attrs[ "padding" + which ] = type;
	}

	if ( includeWidth ) {
		attrs.opacity = attrs.width = type;
	}

	return attrs;
}

function createTween( value, prop, animation ) {
	var tween,
		collection = ( Animation.tweeners[ prop ] || [] ).concat( Animation.tweeners[ "*" ] ),
		index = 0,
		length = collection.length;
	for ( ; index < length; index++ ) {
		if ( ( tween = collection[ index ].call( animation, prop, value ) ) ) {

			// We're done with this property
			return tween;
		}
	}
}

function defaultPrefilter( elem, props, opts ) {
	var prop, value, toggle, hooks, oldfire, propTween, restoreDisplay, display,
		isBox = "width" in props || "height" in props,
		anim = this,
		orig = {},
		style = elem.style,
		hidden = elem.nodeType && isHiddenWithinTree( elem ),
		dataShow = dataPriv.get( elem, "fxshow" );

	// Queue-skipping animations hijack the fx hooks
	if ( !opts.queue ) {
		hooks = jQuery._queueHooks( elem, "fx" );
		if ( hooks.unqueued == null ) {
			hooks.unqueued = 0;
			oldfire = hooks.empty.fire;
			hooks.empty.fire = function() {
				if ( !hooks.unqueued ) {
					oldfire();
				}
			};
		}
		hooks.unqueued++;

		anim.always( function() {

			// Ensure the complete handler is called before this completes
			anim.always( function() {
				hooks.unqueued--;
				if ( !jQuery.queue( elem, "fx" ).length ) {
					hooks.empty.fire();
				}
			} );
		} );
	}

	// Detect show/hide animations
	for ( prop in props ) {
		value = props[ prop ];
		if ( rfxtypes.test( value ) ) {
			delete props[ prop ];
			toggle = toggle || value === "toggle";
			if ( value === ( hidden ? "hide" : "show" ) ) {

				// Pretend to be hidden if this is a "show" and
				// there is still data from a stopped show/hide
				if ( value === "show" && dataShow && dataShow[ prop ] !== undefined ) {
					hidden = true;

				// Ignore all other no-op show/hide data
				} else {
					continue;
				}
			}
			orig[ prop ] = dataShow && dataShow[ prop ] || jQuery.style( elem, prop );
		}
	}

	// Bail out if this is a no-op like .hide().hide()
	propTween = !jQuery.isEmptyObject( props );
	if ( !propTween && jQuery.isEmptyObject( orig ) ) {
		return;
	}

	// Restrict "overflow" and "display" styles during box animations
	if ( isBox && elem.nodeType === 1 ) {

		// Support: IE <=9 - 11, Edge 12 - 15
		// Record all 3 overflow attributes because IE does not infer the shorthand
		// from identically-valued overflowX and overflowY and Edge just mirrors
		// the overflowX value there.
		opts.overflow = [ style.overflow, style.overflowX, style.overflowY ];

		// Identify a display type, preferring old show/hide data over the CSS cascade
		restoreDisplay = dataShow && dataShow.display;
		if ( restoreDisplay == null ) {
			restoreDisplay = dataPriv.get( elem, "display" );
		}
		display = jQuery.css( elem, "display" );
		if ( display === "none" ) {
			if ( restoreDisplay ) {
				display = restoreDisplay;
			} else {

				// Get nonempty value(s) by temporarily forcing visibility
				showHide( [ elem ], true );
				restoreDisplay = elem.style.display || restoreDisplay;
				display = jQuery.css( elem, "display" );
				showHide( [ elem ] );
			}
		}

		// Animate inline elements as inline-block
		if ( display === "inline" || display === "inline-block" && restoreDisplay != null ) {
			if ( jQuery.css( elem, "float" ) === "none" ) {

				// Restore the original display value at the end of pure show/hide animations
				if ( !propTween ) {
					anim.done( function() {
						style.display = restoreDisplay;
					} );
					if ( restoreDisplay == null ) {
						display = style.display;
						restoreDisplay = display === "none" ? "" : display;
					}
				}
				style.display = "inline-block";
			}
		}
	}

	if ( opts.overflow ) {
		style.overflow = "hidden";
		anim.always( function() {
			style.overflow = opts.overflow[ 0 ];
			style.overflowX = opts.overflow[ 1 ];
			style.overflowY = opts.overflow[ 2 ];
		} );
	}

	// Implement show/hide animations
	propTween = false;
	for ( prop in orig ) {

		// General show/hide setup for this element animation
		if ( !propTween ) {
			if ( dataShow ) {
				if ( "hidden" in dataShow ) {
					hidden = dataShow.hidden;
				}
			} else {
				dataShow = dataPriv.access( elem, "fxshow", { display: restoreDisplay } );
			}

			// Store hidden/visible for toggle so `.stop().toggle()` "reverses"
			if ( toggle ) {
				dataShow.hidden = !hidden;
			}

			// Show elements before animating them
			if ( hidden ) {
				showHide( [ elem ], true );
			}

			/* eslint-disable no-loop-func */

			anim.done( function() {

				/* eslint-enable no-loop-func */

				// The final step of a "hide" animation is actually hiding the element
				if ( !hidden ) {
					showHide( [ elem ] );
				}
				dataPriv.remove( elem, "fxshow" );
				for ( prop in orig ) {
					jQuery.style( elem, prop, orig[ prop ] );
				}
			} );
		}

		// Per-property setup
		propTween = createTween( hidden ? dataShow[ prop ] : 0, prop, anim );
		if ( !( prop in dataShow ) ) {
			dataShow[ prop ] = propTween.start;
			if ( hidden ) {
				propTween.end = propTween.start;
				propTween.start = 0;
			}
		}
	}
}

function propFilter( props, specialEasing ) {
	var index, name, easing, value, hooks;

	// camelCase, specialEasing and expand cssHook pass
	for ( index in props ) {
		name = camelCase( index );
		easing = specialEasing[ name ];
		value = props[ index ];
		if ( Array.isArray( value ) ) {
			easing = value[ 1 ];
			value = props[ index ] = value[ 0 ];
		}

		if ( index !== name ) {
			props[ name ] = value;
			delete props[ index ];
		}

		hooks = jQuery.cssHooks[ name ];
		if ( hooks && "expand" in hooks ) {
			value = hooks.expand( value );
			delete props[ name ];

			// Not quite $.extend, this won't overwrite existing keys.
			// Reusing 'index' because we have the correct "name"
			for ( index in value ) {
				if ( !( index in props ) ) {
					props[ index ] = value[ index ];
					specialEasing[ index ] = easing;
				}
			}
		} else {
			specialEasing[ name ] = easing;
		}
	}
}

function Animation( elem, properties, options ) {
	var result,
		stopped,
		index = 0,
		length = Animation.prefilters.length,
		deferred = jQuery.Deferred().always( function() {

			// Don't match elem in the :animated selector
			delete tick.elem;
		} ),
		tick = function() {
			if ( stopped ) {
				return false;
			}
			var currentTime = fxNow || createFxNow(),
				remaining = Math.max( 0, animation.startTime + animation.duration - currentTime ),

				// Support: Android 2.3 only
				// Archaic crash bug won't allow us to use `1 - ( 0.5 || 0 )` (#12497)
				temp = remaining / animation.duration || 0,
				percent = 1 - temp,
				index = 0,
				length = animation.tweens.length;

			for ( ; index < length; index++ ) {
				animation.tweens[ index ].run( percent );
			}

			deferred.notifyWith( elem, [ animation, percent, remaining ] );

			// If there's more to do, yield
			if ( percent < 1 && length ) {
				return remaining;
			}

			// If this was an empty animation, synthesize a final progress notification
			if ( !length ) {
				deferred.notifyWith( elem, [ animation, 1, 0 ] );
			}

			// Resolve the animation and report its conclusion
			deferred.resolveWith( elem, [ animation ] );
			return false;
		},
		animation = deferred.promise( {
			elem: elem,
			props: jQuery.extend( {}, properties ),
			opts: jQuery.extend( true, {
				specialEasing: {},
				easing: jQuery.easing._default
			}, options ),
			originalProperties: properties,
			originalOptions: options,
			startTime: fxNow || createFxNow(),
			duration: options.duration,
			tweens: [],
			createTween: function( prop, end ) {
				var tween = jQuery.Tween( elem, animation.opts, prop, end,
					animation.opts.specialEasing[ prop ] || animation.opts.easing );
				animation.tweens.push( tween );
				return tween;
			},
			stop: function( gotoEnd ) {
				var index = 0,

					// If we are going to the end, we want to run all the tweens
					// otherwise we skip this part
					length = gotoEnd ? animation.tweens.length : 0;
				if ( stopped ) {
					return this;
				}
				stopped = true;
				for ( ; index < length; index++ ) {
					animation.tweens[ index ].run( 1 );
				}

				// Resolve when we played the last frame; otherwise, reject
				if ( gotoEnd ) {
					deferred.notifyWith( elem, [ animation, 1, 0 ] );
					deferred.resolveWith( elem, [ animation, gotoEnd ] );
				} else {
					deferred.rejectWith( elem, [ animation, gotoEnd ] );
				}
				return this;
			}
		} ),
		props = animation.props;

	propFilter( props, animation.opts.specialEasing );

	for ( ; index < length; index++ ) {
		result = Animation.prefilters[ index ].call( animation, elem, props, animation.opts );
		if ( result ) {
			if ( isFunction( result.stop ) ) {
				jQuery._queueHooks( animation.elem, animation.opts.queue ).stop =
					result.stop.bind( result );
			}
			return result;
		}
	}

	jQuery.map( props, createTween, animation );

	if ( isFunction( animation.opts.start ) ) {
		animation.opts.start.call( elem, animation );
	}

	// Attach callbacks from options
	animation
		.progress( animation.opts.progress )
		.done( animation.opts.done, animation.opts.complete )
		.fail( animation.opts.fail )
		.always( animation.opts.always );

	jQuery.fx.timer(
		jQuery.extend( tick, {
			elem: elem,
			anim: animation,
			queue: animation.opts.queue
		} )
	);

	return animation;
}

jQuery.Animation = jQuery.extend( Animation, {

	tweeners: {
		"*": [ function( prop, value ) {
			var tween = this.createTween( prop, value );
			adjustCSS( tween.elem, prop, rcssNum.exec( value ), tween );
			return tween;
		} ]
	},

	tweener: function( props, callback ) {
		if ( isFunction( props ) ) {
			callback = props;
			props = [ "*" ];
		} else {
			props = props.match( rnothtmlwhite );
		}

		var prop,
			index = 0,
			length = props.length;

		for ( ; index < length; index++ ) {
			prop = props[ index ];
			Animation.tweeners[ prop ] = Animation.tweeners[ prop ] || [];
			Animation.tweeners[ prop ].unshift( callback );
		}
	},

	prefilters: [ defaultPrefilter ],

	prefilter: function( callback, prepend ) {
		if ( prepend ) {
			Animation.prefilters.unshift( callback );
		} else {
			Animation.prefilters.push( callback );
		}
	}
} );

jQuery.speed = function( speed, easing, fn ) {
	var opt = speed && typeof speed === "object" ? jQuery.extend( {}, speed ) : {
		complete: fn || !fn && easing ||
			isFunction( speed ) && speed,
		duration: speed,
		easing: fn && easing || easing && !isFunction( easing ) && easing
	};

	// Go to the end state if fx are off
	if ( jQuery.fx.off ) {
		opt.duration = 0;

	} else {
		if ( typeof opt.duration !== "number" ) {
			if ( opt.duration in jQuery.fx.speeds ) {
				opt.duration = jQuery.fx.speeds[ opt.duration ];

			} else {
				opt.duration = jQuery.fx.speeds._default;
			}
		}
	}

	// Normalize opt.queue - true/undefined/null -> "fx"
	if ( opt.queue == null || opt.queue === true ) {
		opt.queue = "fx";
	}

	// Queueing
	opt.old = opt.complete;

	opt.complete = function() {
		if ( isFunction( opt.old ) ) {
			opt.old.call( this );
		}

		if ( opt.queue ) {
			jQuery.dequeue( this, opt.queue );
		}
	};

	return opt;
};

jQuery.fn.extend( {
	fadeTo: function( speed, to, easing, callback ) {

		// Show any hidden elements after setting opacity to 0
		return this.filter( isHiddenWithinTree ).css( "opacity", 0 ).show()

			// Animate to the value specified
			.end().animate( { opacity: to }, speed, easing, callback );
	},
	animate: function( prop, speed, easing, callback ) {
		var empty = jQuery.isEmptyObject( prop ),
			optall = jQuery.speed( speed, easing, callback ),
			doAnimation = function() {

				// Operate on a copy of prop so per-property easing won't be lost
				var anim = Animation( this, jQuery.extend( {}, prop ), optall );

				// Empty animations, or finishing resolves immediately
				if ( empty || dataPriv.get( this, "finish" ) ) {
					anim.stop( true );
				}
			};

		doAnimation.finish = doAnimation;

		return empty || optall.queue === false ?
			this.each( doAnimation ) :
			this.queue( optall.queue, doAnimation );
	},
	stop: function( type, clearQueue, gotoEnd ) {
		var stopQueue = function( hooks ) {
			var stop = hooks.stop;
			delete hooks.stop;
			stop( gotoEnd );
		};

		if ( typeof type !== "string" ) {
			gotoEnd = clearQueue;
			clearQueue = type;
			type = undefined;
		}
		if ( clearQueue ) {
			this.queue( type || "fx", [] );
		}

		return this.each( function() {
			var dequeue = true,
				index = type != null && type + "queueHooks",
				timers = jQuery.timers,
				data = dataPriv.get( this );

			if ( index ) {
				if ( data[ index ] && data[ index ].stop ) {
					stopQueue( data[ index ] );
				}
			} else {
				for ( index in data ) {
					if ( data[ index ] && data[ index ].stop && rrun.test( index ) ) {
						stopQueue( data[ index ] );
					}
				}
			}

			for ( index = timers.length; index--; ) {
				if ( timers[ index ].elem === this &&
					( type == null || timers[ index ].queue === type ) ) {

					timers[ index ].anim.stop( gotoEnd );
					dequeue = false;
					timers.splice( index, 1 );
				}
			}

			// Start the next in the queue if the last step wasn't forced.
			// Timers currently will call their complete callbacks, which
			// will dequeue but only if they were gotoEnd.
			if ( dequeue || !gotoEnd ) {
				jQuery.dequeue( this, type );
			}
		} );
	},
	finish: function( type ) {
		if ( type !== false ) {
			type = type || "fx";
		}
		return this.each( function() {
			var index,
				data = dataPriv.get( this ),
				queue = data[ type + "queue" ],
				hooks = data[ type + "queueHooks" ],
				timers = jQuery.timers,
				length = queue ? queue.length : 0;

			// Enable finishing flag on private data
			data.finish = true;

			// Empty the queue first
			jQuery.queue( this, type, [] );

			if ( hooks && hooks.stop ) {
				hooks.stop.call( this, true );
			}

			// Look for any active animations, and finish them
			for ( index = timers.length; index--; ) {
				if ( timers[ index ].elem === this && timers[ index ].queue === type ) {
					timers[ index ].anim.stop( true );
					timers.splice( index, 1 );
				}
			}

			// Look for any animations in the old queue and finish them
			for ( index = 0; index < length; index++ ) {
				if ( queue[ index ] && queue[ index ].finish ) {
					queue[ index ].finish.call( this );
				}
			}

			// Turn off finishing flag
			delete data.finish;
		} );
	}
} );

jQuery.each( [ "toggle", "show", "hide" ], function( _i, name ) {
	var cssFn = jQuery.fn[ name ];
	jQuery.fn[ name ] = function( speed, easing, callback ) {
		return speed == null || typeof speed === "boolean" ?
			cssFn.apply( this, arguments ) :
			this.animate( genFx( name, true ), speed, easing, callback );
	};
} );

// Generate shortcuts for custom animations
jQuery.each( {
	slideDown: genFx( "show" ),
	slideUp: genFx( "hide" ),
	slideToggle: genFx( "toggle" ),
	fadeIn: { opacity: "show" },
	fadeOut: { opacity: "hide" },
	fadeToggle: { opacity: "toggle" }
}, function( name, props ) {
	jQuery.fn[ name ] = function( speed, easing, callback ) {
		return this.animate( props, speed, easing, callback );
	};
} );

jQuery.timers = [];
jQuery.fx.tick = function() {
	var timer,
		i = 0,
		timers = jQuery.timers;

	fxNow = Date.now();

	for ( ; i < timers.length; i++ ) {
		timer = timers[ i ];

		// Run the timer and safely remove it when done (allowing for external removal)
		if ( !timer() && timers[ i ] === timer ) {
			timers.splice( i--, 1 );
		}
	}

	if ( !timers.length ) {
		jQuery.fx.stop();
	}
	fxNow = undefined;
};

jQuery.fx.timer = function( timer ) {
	jQuery.timers.push( timer );
	jQuery.fx.start();
};

jQuery.fx.interval = 13;
jQuery.fx.start = function() {
	if ( inProgress ) {
		return;
	}

	inProgress = true;
	schedule();
};

jQuery.fx.stop = function() {
	inProgress = null;
};

jQuery.fx.speeds = {
	slow: 600,
	fast: 200,

	// Default speed
	_default: 400
};


// Based off of the plugin by Clint Helfers, with permission.
// https://web.archive.org/web/20100324014747/http://blindsignals.com/index.php/2009/07/jquery-delay/
jQuery.fn.delay = function( time, type ) {
	time = jQuery.fx ? jQuery.fx.speeds[ time ] || time : time;
	type = type || "fx";

	return this.queue( type, function( next, hooks ) {
		var timeout = window.setTimeout( next, time );
		hooks.stop = function() {
			window.clearTimeout( timeout );
		};
	} );
};


( function() {
	var input = document.createElement( "input" ),
		select = document.createElement( "select" ),
		opt = select.appendChild( document.createElement( "option" ) );

	input.type = "checkbox";

	// Support: Android <=4.3 only
	// Default value for a checkbox should be "on"
	support.checkOn = input.value !== "";

	// Support: IE <=11 only
	// Must access selectedIndex to make default options select
	support.optSelected = opt.selected;

	// Support: IE <=11 only
	// An input loses its value after becoming a radio
	input = document.createElement( "input" );
	input.value = "t";
	input.type = "radio";
	support.radioValue = input.value === "t";
} )();


var boolHook,
	attrHandle = jQuery.expr.attrHandle;

jQuery.fn.extend( {
	attr: function( name, value ) {
		return access( this, jQuery.attr, name, value, arguments.length > 1 );
	},

	removeAttr: function( name ) {
		return this.each( function() {
			jQuery.removeAttr( this, name );
		} );
	}
} );

jQuery.extend( {
	attr: function( elem, name, value ) {
		var ret, hooks,
			nType = elem.nodeType;

		// Don't get/set attributes on text, comment and attribute nodes
		if ( nType === 3 || nType === 8 || nType === 2 ) {
			return;
		}

		// Fallback to prop when attributes are not supported
		if ( typeof elem.getAttribute === "undefined" ) {
			return jQuery.prop( elem, name, value );
		}

		// Attribute hooks are determined by the lowercase version
		// Grab necessary hook if one is defined
		if ( nType !== 1 || !jQuery.isXMLDoc( elem ) ) {
			hooks = jQuery.attrHooks[ name.toLowerCase() ] ||
				( jQuery.expr.match.bool.test( name ) ? boolHook : undefined );
		}

		if ( value !== undefined ) {
			if ( value === null ) {
				jQuery.removeAttr( elem, name );
				return;
			}

			if ( hooks && "set" in hooks &&
				( ret = hooks.set( elem, value, name ) ) !== undefined ) {
				return ret;
			}

			elem.setAttribute( name, value + "" );
			return value;
		}

		if ( hooks && "get" in hooks && ( ret = hooks.get( elem, name ) ) !== null ) {
			return ret;
		}

		ret = jQuery.find.attr( elem, name );

		// Non-existent attributes return null, we normalize to undefined
		return ret == null ? undefined : ret;
	},

	attrHooks: {
		type: {
			set: function( elem, value ) {
				if ( !support.radioValue && value === "radio" &&
					nodeName( elem, "input" ) ) {
					var val = elem.value;
					elem.setAttribute( "type", value );
					if ( val ) {
						elem.value = val;
					}
					return value;
				}
			}
		}
	},

	removeAttr: function( elem, value ) {
		var name,
			i = 0,

			// Attribute names can contain non-HTML whitespace characters
			// https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
			attrNames = value && value.match( rnothtmlwhite );

		if ( attrNames && elem.nodeType === 1 ) {
			while ( ( name = attrNames[ i++ ] ) ) {
				elem.removeAttribute( name );
			}
		}
	}
} );

// Hooks for boolean attributes
boolHook = {
	set: function( elem, value, name ) {
		if ( value === false ) {

			// Remove boolean attributes when set to false
			jQuery.removeAttr( elem, name );
		} else {
			elem.setAttribute( name, name );
		}
		return name;
	}
};

jQuery.each( jQuery.expr.match.bool.source.match( /\w+/g ), function( _i, name ) {
	var getter = attrHandle[ name ] || jQuery.find.attr;

	attrHandle[ name ] = function( elem, name, isXML ) {
		var ret, handle,
			lowercaseName = name.toLowerCase();

		if ( !isXML ) {

			// Avoid an infinite loop by temporarily removing this function from the getter
			handle = attrHandle[ lowercaseName ];
			attrHandle[ lowercaseName ] = ret;
			ret = getter( elem, name, isXML ) != null ?
				lowercaseName :
				null;
			attrHandle[ lowercaseName ] = handle;
		}
		return ret;
	};
} );




var rfocusable = /^(?:input|select|textarea|button)$/i,
	rclickable = /^(?:a|area)$/i;

jQuery.fn.extend( {
	prop: function( name, value ) {
		return access( this, jQuery.prop, name, value, arguments.length > 1 );
	},

	removeProp: function( name ) {
		return this.each( function() {
			delete this[ jQuery.propFix[ name ] || name ];
		} );
	}
} );

jQuery.extend( {
	prop: function( elem, name, value ) {
		var ret, hooks,
			nType = elem.nodeType;

		// Don't get/set properties on text, comment and attribute nodes
		if ( nType === 3 || nType === 8 || nType === 2 ) {
			return;
		}

		if ( nType !== 1 || !jQuery.isXMLDoc( elem ) ) {

			// Fix name and attach hooks
			name = jQuery.propFix[ name ] || name;
			hooks = jQuery.propHooks[ name ];
		}

		if ( value !== undefined ) {
			if ( hooks && "set" in hooks &&
				( ret = hooks.set( elem, value, name ) ) !== undefined ) {
				return ret;
			}

			return ( elem[ name ] = value );
		}

		if ( hooks && "get" in hooks && ( ret = hooks.get( elem, name ) ) !== null ) {
			return ret;
		}

		return elem[ name ];
	},

	propHooks: {
		tabIndex: {
			get: function( elem ) {

				// Support: IE <=9 - 11 only
				// elem.tabIndex doesn't always return the
				// correct value when it hasn't been explicitly set
				// https://web.archive.org/web/20141116233347/http://fluidproject.org/blog/2008/01/09/getting-setting-and-removing-tabindex-values-with-javascript/
				// Use proper attribute retrieval(#12072)
				var tabindex = jQuery.find.attr( elem, "tabindex" );

				if ( tabindex ) {
					return parseInt( tabindex, 10 );
				}

				if (
					rfocusable.test( elem.nodeName ) ||
					rclickable.test( elem.nodeName ) &&
					elem.href
				) {
					return 0;
				}

				return -1;
			}
		}
	},

	propFix: {
		"for": "htmlFor",
		"class": "className"
	}
} );

// Support: IE <=11 only
// Accessing the selectedIndex property
// forces the browser to respect setting selected
// on the option
// The getter ensures a default option is selected
// when in an optgroup
// eslint rule "no-unused-expressions" is disabled for this code
// since it considers such accessions noop
if ( !support.optSelected ) {
	jQuery.propHooks.selected = {
		get: function( elem ) {

			/* eslint no-unused-expressions: "off" */

			var parent = elem.parentNode;
			if ( parent && parent.parentNode ) {
				parent.parentNode.selectedIndex;
			}
			return null;
		},
		set: function( elem ) {

			/* eslint no-unused-expressions: "off" */

			var parent = elem.parentNode;
			if ( parent ) {
				parent.selectedIndex;

				if ( parent.parentNode ) {
					parent.parentNode.selectedIndex;
				}
			}
		}
	};
}

jQuery.each( [
	"tabIndex",
	"readOnly",
	"maxLength",
	"cellSpacing",
	"cellPadding",
	"rowSpan",
	"colSpan",
	"useMap",
	"frameBorder",
	"contentEditable"
], function() {
	jQuery.propFix[ this.toLowerCase() ] = this;
} );




	// Strip and collapse whitespace according to HTML spec
	// https://infra.spec.whatwg.org/#strip-and-collapse-ascii-whitespace
	function stripAndCollapse( value ) {
		var tokens = value.match( rnothtmlwhite ) || [];
		return tokens.join( " " );
	}


function getClass( elem ) {
	return elem.getAttribute && elem.getAttribute( "class" ) || "";
}

function classesToArray( value ) {
	if ( Array.isArray( value ) ) {
		return value;
	}
	if ( typeof value === "string" ) {
		return value.match( rnothtmlwhite ) || [];
	}
	return [];
}

jQuery.fn.extend( {
	addClass: function( value ) {
		var classes, elem, cur, curValue, clazz, j, finalValue,
			i = 0;

		if ( isFunction( value ) ) {
			return this.each( function( j ) {
				jQuery( this ).addClass( value.call( this, j, getClass( this ) ) );
			} );
		}

		classes = classesToArray( value );

		if ( classes.length ) {
			while ( ( elem = this[ i++ ] ) ) {
				curValue = getClass( elem );
				cur = elem.nodeType === 1 && ( " " + stripAndCollapse( curValue ) + " " );

				if ( cur ) {
					j = 0;
					while ( ( clazz = classes[ j++ ] ) ) {
						if ( cur.indexOf( " " + clazz + " " ) < 0 ) {
							cur += clazz + " ";
						}
					}

					// Only assign if different to avoid unneeded rendering.
					finalValue = stripAndCollapse( cur );
					if ( curValue !== finalValue ) {
						elem.setAttribute( "class", finalValue );
					}
				}
			}
		}

		return this;
	},

	removeClass: function( value ) {
		var classes, elem, cur, curValue, clazz, j, finalValue,
			i = 0;

		if ( isFunction( value ) ) {
			return this.each( function( j ) {
				jQuery( this ).removeClass( value.call( this, j, getClass( this ) ) );
			} );
		}

		if ( !arguments.length ) {
			return this.attr( "class", "" );
		}

		classes = classesToArray( value );

		if ( classes.length ) {
			while ( ( elem = this[ i++ ] ) ) {
				curValue = getClass( elem );

				// This expression is here for better compressibility (see addClass)
				cur = elem.nodeType === 1 && ( " " + stripAndCollapse( curValue ) + " " );

				if ( cur ) {
					j = 0;
					while ( ( clazz = classes[ j++ ] ) ) {

						// Remove *all* instances
						while ( cur.indexOf( " " + clazz + " " ) > -1 ) {
							cur = cur.replace( " " + clazz + " ", " " );
						}
					}

					// Only assign if different to avoid unneeded rendering.
					finalValue = stripAndCollapse( cur );
					if ( curValue !== finalValue ) {
						elem.setAttribute( "class", finalValue );
					}
				}
			}
		}

		return this;
	},

	toggleClass: function( value, stateVal ) {
		var type = typeof value,
			isValidValue = type === "string" || Array.isArray( value );

		if ( typeof stateVal === "boolean" && isValidValue ) {
			return stateVal ? this.addClass( value ) : this.removeClass( value );
		}

		if ( isFunction( value ) ) {
			return this.each( function( i ) {
				jQuery( this ).toggleClass(
					value.call( this, i, getClass( this ), stateVal ),
					stateVal
				);
			} );
		}

		return this.each( function() {
			var className, i, self, classNames;

			if ( isValidValue ) {

				// Toggle individual class names
				i = 0;
				self = jQuery( this );
				classNames = classesToArray( value );

				while ( ( className = classNames[ i++ ] ) ) {

					// Check each className given, space separated list
					if ( self.hasClass( className ) ) {
						self.removeClass( className );
					} else {
						self.addClass( className );
					}
				}

			// Toggle whole class name
			} else if ( value === undefined || type === "boolean" ) {
				className = getClass( this );
				if ( className ) {

					// Store className if set
					dataPriv.set( this, "__className__", className );
				}

				// If the element has a class name or if we're passed `false`,
				// then remove the whole classname (if there was one, the above saved it).
				// Otherwise bring back whatever was previously saved (if anything),
				// falling back to the empty string if nothing was stored.
				if ( this.setAttribute ) {
					this.setAttribute( "class",
						className || value === false ?
							"" :
							dataPriv.get( this, "__className__" ) || ""
					);
				}
			}
		} );
	},

	hasClass: function( selector ) {
		var className, elem,
			i = 0;

		className = " " + selector + " ";
		while ( ( elem = this[ i++ ] ) ) {
			if ( elem.nodeType === 1 &&
				( " " + stripAndCollapse( getClass( elem ) ) + " " ).indexOf( className ) > -1 ) {
				return true;
			}
		}

		return false;
	}
} );




var rreturn = /\r/g;

jQuery.fn.extend( {
	val: function( value ) {
		var hooks, ret, valueIsFunction,
			elem = this[ 0 ];

		if ( !arguments.length ) {
			if ( elem ) {
				hooks = jQuery.valHooks[ elem.type ] ||
					jQuery.valHooks[ elem.nodeName.toLowerCase() ];

				if ( hooks &&
					"get" in hooks &&
					( ret = hooks.get( elem, "value" ) ) !== undefined
				) {
					return ret;
				}

				ret = elem.value;

				// Handle most common string cases
				if ( typeof ret === "string" ) {
					return ret.replace( rreturn, "" );
				}

				// Handle cases where value is null/undef or number
				return ret == null ? "" : ret;
			}

			return;
		}

		valueIsFunction = isFunction( value );

		return this.each( function( i ) {
			var val;

			if ( this.nodeType !== 1 ) {
				return;
			}

			if ( valueIsFunction ) {
				val = value.call( this, i, jQuery( this ).val() );
			} else {
				val = value;
			}

			// Treat null/undefined as ""; convert numbers to string
			if ( val == null ) {
				val = "";

			} else if ( typeof val === "number" ) {
				val += "";

			} else if ( Array.isArray( val ) ) {
				val = jQuery.map( val, function( value ) {
					return value == null ? "" : value + "";
				} );
			}

			hooks = jQuery.valHooks[ this.type ] || jQuery.valHooks[ this.nodeName.toLowerCase() ];

			// If set returns undefined, fall back to normal setting
			if ( !hooks || !( "set" in hooks ) || hooks.set( this, val, "value" ) === undefined ) {
				this.value = val;
			}
		} );
	}
} );

jQuery.extend( {
	valHooks: {
		option: {
			get: function( elem ) {

				var val = jQuery.find.attr( elem, "value" );
				return val != null ?
					val :

					// Support: IE <=10 - 11 only
					// option.text throws exceptions (#14686, #14858)
					// Strip and collapse whitespace
					// https://html.spec.whatwg.org/#strip-and-collapse-whitespace
					stripAndCollapse( jQuery.text( elem ) );
			}
		},
		select: {
			get: function( elem ) {
				var value, option, i,
					options = elem.options,
					index = elem.selectedIndex,
					one = elem.type === "select-one",
					values = one ? null : [],
					max = one ? index + 1 : options.length;

				if ( index < 0 ) {
					i = max;

				} else {
					i = one ? index : 0;
				}

				// Loop through all the selected options
				for ( ; i < max; i++ ) {
					option = options[ i ];

					// Support: IE <=9 only
					// IE8-9 doesn't update selected after form reset (#2551)
					if ( ( option.selected || i === index ) &&

							// Don't return options that are disabled or in a disabled optgroup
							!option.disabled &&
							( !option.parentNode.disabled ||
								!nodeName( option.parentNode, "optgroup" ) ) ) {

						// Get the specific value for the option
						value = jQuery( option ).val();

						// We don't need an array for one selects
						if ( one ) {
							return value;
						}

						// Multi-Selects return an array
						values.push( value );
					}
				}

				return values;
			},

			set: function( elem, value ) {
				var optionSet, option,
					options = elem.options,
					values = jQuery.makeArray( value ),
					i = options.length;

				while ( i-- ) {
					option = options[ i ];

					/* eslint-disable no-cond-assign */

					if ( option.selected =
						jQuery.inArray( jQuery.valHooks.option.get( option ), values ) > -1
					) {
						optionSet = true;
					}

					/* eslint-enable no-cond-assign */
				}

				// Force browsers to behave consistently when non-matching value is set
				if ( !optionSet ) {
					elem.selectedIndex = -1;
				}
				return values;
			}
		}
	}
} );

// Radios and checkboxes getter/setter
jQuery.each( [ "radio", "checkbox" ], function() {
	jQuery.valHooks[ this ] = {
		set: function( elem, value ) {
			if ( Array.isArray( value ) ) {
				return ( elem.checked = jQuery.inArray( jQuery( elem ).val(), value ) > -1 );
			}
		}
	};
	if ( !support.checkOn ) {
		jQuery.valHooks[ this ].get = function( elem ) {
			return elem.getAttribute( "value" ) === null ? "on" : elem.value;
		};
	}
} );




// Return jQuery for attributes-only inclusion


support.focusin = "onfocusin" in window;


var rfocusMorph = /^(?:focusinfocus|focusoutblur)$/,
	stopPropagationCallback = function( e ) {
		e.stopPropagation();
	};

jQuery.extend( jQuery.event, {

	trigger: function( event, data, elem, onlyHandlers ) {

		var i, cur, tmp, bubbleType, ontype, handle, special, lastElement,
			eventPath = [ elem || document ],
			type = hasOwn.call( event, "type" ) ? event.type : event,
			namespaces = hasOwn.call( event, "namespace" ) ? event.namespace.split( "." ) : [];

		cur = lastElement = tmp = elem = elem || document;

		// Don't do events on text and comment nodes
		if ( elem.nodeType === 3 || elem.nodeType === 8 ) {
			return;
		}

		// focus/blur morphs to focusin/out; ensure we're not firing them right now
		if ( rfocusMorph.test( type + jQuery.event.triggered ) ) {
			return;
		}

		if ( type.indexOf( "." ) > -1 ) {

			// Namespaced trigger; create a regexp to match event type in handle()
			namespaces = type.split( "." );
			type = namespaces.shift();
			namespaces.sort();
		}
		ontype = type.indexOf( ":" ) < 0 && "on" + type;

		// Caller can pass in a jQuery.Event object, Object, or just an event type string
		event = event[ jQuery.expando ] ?
			event :
			new jQuery.Event( type, typeof event === "object" && event );

		// Trigger bitmask: & 1 for native handlers; & 2 for jQuery (always true)
		event.isTrigger = onlyHandlers ? 2 : 3;
		event.namespace = namespaces.join( "." );
		event.rnamespace = event.namespace ?
			new RegExp( "(^|\\.)" + namespaces.join( "\\.(?:.*\\.|)" ) + "(\\.|$)" ) :
			null;

		// Clean up the event in case it is being reused
		event.result = undefined;
		if ( !event.target ) {
			event.target = elem;
		}

		// Clone any incoming data and prepend the event, creating the handler arg list
		data = data == null ?
			[ event ] :
			jQuery.makeArray( data, [ event ] );

		// Allow special events to draw outside the lines
		special = jQuery.event.special[ type ] || {};
		if ( !onlyHandlers && special.trigger && special.trigger.apply( elem, data ) === false ) {
			return;
		}

		// Determine event propagation path in advance, per W3C events spec (#9951)
		// Bubble up to document, then to window; watch for a global ownerDocument var (#9724)
		if ( !onlyHandlers && !special.noBubble && !isWindow( elem ) ) {

			bubbleType = special.delegateType || type;
			if ( !rfocusMorph.test( bubbleType + type ) ) {
				cur = cur.parentNode;
			}
			for ( ; cur; cur = cur.parentNode ) {
				eventPath.push( cur );
				tmp = cur;
			}

			// Only add window if we got to document (e.g., not plain obj or detached DOM)
			if ( tmp === ( elem.ownerDocument || document ) ) {
				eventPath.push( tmp.defaultView || tmp.parentWindow || window );
			}
		}

		// Fire handlers on the event path
		i = 0;
		while ( ( cur = eventPath[ i++ ] ) && !event.isPropagationStopped() ) {
			lastElement = cur;
			event.type = i > 1 ?
				bubbleType :
				special.bindType || type;

			// jQuery handler
			handle = ( dataPriv.get( cur, "events" ) || Object.create( null ) )[ event.type ] &&
				dataPriv.get( cur, "handle" );
			if ( handle ) {
				handle.apply( cur, data );
			}

			// Native handler
			handle = ontype && cur[ ontype ];
			if ( handle && handle.apply && acceptData( cur ) ) {
				event.result = handle.apply( cur, data );
				if ( event.result === false ) {
					event.preventDefault();
				}
			}
		}
		event.type = type;

		// If nobody prevented the default action, do it now
		if ( !onlyHandlers && !event.isDefaultPrevented() ) {

			if ( ( !special._default ||
				special._default.apply( eventPath.pop(), data ) === false ) &&
				acceptData( elem ) ) {

				// Call a native DOM method on the target with the same name as the event.
				// Don't do default actions on window, that's where global variables be (#6170)
				if ( ontype && isFunction( elem[ type ] ) && !isWindow( elem ) ) {

					// Don't re-trigger an onFOO event when we call its FOO() method
					tmp = elem[ ontype ];

					if ( tmp ) {
						elem[ ontype ] = null;
					}

					// Prevent re-triggering of the same event, since we already bubbled it above
					jQuery.event.triggered = type;

					if ( event.isPropagationStopped() ) {
						lastElement.addEventListener( type, stopPropagationCallback );
					}

					elem[ type ]();

					if ( event.isPropagationStopped() ) {
						lastElement.removeEventListener( type, stopPropagationCallback );
					}

					jQuery.event.triggered = undefined;

					if ( tmp ) {
						elem[ ontype ] = tmp;
					}
				}
			}
		}

		return event.result;
	},

	// Piggyback on a donor event to simulate a different one
	// Used only for `focus(in | out)` events
	simulate: function( type, elem, event ) {
		var e = jQuery.extend(
			new jQuery.Event(),
			event,
			{
				type: type,
				isSimulated: true
			}
		);

		jQuery.event.trigger( e, null, elem );
	}

} );

jQuery.fn.extend( {

	trigger: function( type, data ) {
		return this.each( function() {
			jQuery.event.trigger( type, data, this );
		} );
	},
	triggerHandler: function( type, data ) {
		var elem = this[ 0 ];
		if ( elem ) {
			return jQuery.event.trigger( type, data, elem, true );
		}
	}
} );


// Support: Firefox <=44
// Firefox doesn't have focus(in | out) events
// Related ticket - https://bugzilla.mozilla.org/show_bug.cgi?id=687787
//
// Support: Chrome <=48 - 49, Safari <=9.0 - 9.1
// focus(in | out) events fire after focus & blur events,
// which is spec violation - http://www.w3.org/TR/DOM-Level-3-Events/#events-focusevent-event-order
// Related ticket - https://bugs.chromium.org/p/chromium/issues/detail?id=449857
if ( !support.focusin ) {
	jQuery.each( { focus: "focusin", blur: "focusout" }, function( orig, fix ) {

		// Attach a single capturing handler on the document while someone wants focusin/focusout
		var handler = function( event ) {
			jQuery.event.simulate( fix, event.target, jQuery.event.fix( event ) );
		};

		jQuery.event.special[ fix ] = {
			setup: function() {

				// Handle: regular nodes (via `this.ownerDocument`), window
				// (via `this.document`) & document (via `this`).
				var doc = this.ownerDocument || this.document || this,
					attaches = dataPriv.access( doc, fix );

				if ( !attaches ) {
					doc.addEventListener( orig, handler, true );
				}
				dataPriv.access( doc, fix, ( attaches || 0 ) + 1 );
			},
			teardown: function() {
				var doc = this.ownerDocument || this.document || this,
					attaches = dataPriv.access( doc, fix ) - 1;

				if ( !attaches ) {
					doc.removeEventListener( orig, handler, true );
					dataPriv.remove( doc, fix );

				} else {
					dataPriv.access( doc, fix, attaches );
				}
			}
		};
	} );
}
var location = window.location;

var nonce = { guid: Date.now() };

var rquery = ( /\?/ );



// Cross-browser xml parsing
jQuery.parseXML = function( data ) {
	var xml, parserErrorElem;
	if ( !data || typeof data !== "string" ) {
		return null;
	}

	// Support: IE 9 - 11 only
	// IE throws on parseFromString with invalid input.
	try {
		xml = ( new window.DOMParser() ).parseFromString( data, "text/xml" );
	} catch ( e ) {}

	parserErrorElem = xml && xml.getElementsByTagName( "parsererror" )[ 0 ];
	if ( !xml || parserErrorElem ) {
		jQuery.error( "Invalid XML: " + (
			parserErrorElem ?
				jQuery.map( parserErrorElem.childNodes, function( el ) {
					return el.textContent;
				} ).join( "\n" ) :
				data
		) );
	}
	return xml;
};


var
	rbracket = /\[\]$/,
	rCRLF = /\r?\n/g,
	rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
	rsubmittable = /^(?:input|select|textarea|keygen)/i;

function buildParams( prefix, obj, traditional, add ) {
	var name;

	if ( Array.isArray( obj ) ) {

		// Serialize array item.
		jQuery.each( obj, function( i, v ) {
			if ( traditional || rbracket.test( prefix ) ) {

				// Treat each array item as a scalar.
				add( prefix, v );

			} else {

				// Item is non-scalar (array or object), encode its numeric index.
				buildParams(
					prefix + "[" + ( typeof v === "object" && v != null ? i : "" ) + "]",
					v,
					traditional,
					add
				);
			}
		} );

	} else if ( !traditional && toType( obj ) === "object" ) {

		// Serialize object item.
		for ( name in obj ) {
			buildParams( prefix + "[" + name + "]", obj[ name ], traditional, add );
		}

	} else {

		// Serialize scalar item.
		add( prefix, obj );
	}
}

// Serialize an array of form elements or a set of
// key/values into a query string
jQuery.param = function( a, traditional ) {
	var prefix,
		s = [],
		add = function( key, valueOrFunction ) {

			// If value is a function, invoke it and use its return value
			var value = isFunction( valueOrFunction ) ?
				valueOrFunction() :
				valueOrFunction;

			s[ s.length ] = encodeURIComponent( key ) + "=" +
				encodeURIComponent( value == null ? "" : value );
		};

	if ( a == null ) {
		return "";
	}

	// If an array was passed in, assume that it is an array of form elements.
	if ( Array.isArray( a ) || ( a.jquery && !jQuery.isPlainObject( a ) ) ) {

		// Serialize the form elements
		jQuery.each( a, function() {
			add( this.name, this.value );
		} );

	} else {

		// If traditional, encode the "old" way (the way 1.3.2 or older
		// did it), otherwise encode params recursively.
		for ( prefix in a ) {
			buildParams( prefix, a[ prefix ], traditional, add );
		}
	}

	// Return the resulting serialization
	return s.join( "&" );
};

jQuery.fn.extend( {
	serialize: function() {
		return jQuery.param( this.serializeArray() );
	},
	serializeArray: function() {
		return this.map( function() {

			// Can add propHook for "elements" to filter or add form elements
			var elements = jQuery.prop( this, "elements" );
			return elements ? jQuery.makeArray( elements ) : this;
		} ).filter( function() {
			var type = this.type;

			// Use .is( ":disabled" ) so that fieldset[disabled] works
			return this.name && !jQuery( this ).is( ":disabled" ) &&
				rsubmittable.test( this.nodeName ) && !rsubmitterTypes.test( type ) &&
				( this.checked || !rcheckableType.test( type ) );
		} ).map( function( _i, elem ) {
			var val = jQuery( this ).val();

			if ( val == null ) {
				return null;
			}

			if ( Array.isArray( val ) ) {
				return jQuery.map( val, function( val ) {
					return { name: elem.name, value: val.replace( rCRLF, "\r\n" ) };
				} );
			}

			return { name: elem.name, value: val.replace( rCRLF, "\r\n" ) };
		} ).get();
	}
} );


var
	r20 = /%20/g,
	rhash = /#.*$/,
	rantiCache = /([?&])_=[^&]*/,
	rheaders = /^(.*?):[ \t]*([^\r\n]*)$/mg,

	// #7653, #8125, #8152: local protocol detection
	rlocalProtocol = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
	rnoContent = /^(?:GET|HEAD)$/,
	rprotocol = /^\/\//,

	/* Prefilters
	 * 1) They are useful to introduce custom dataTypes (see ajax/jsonp.js for an example)
	 * 2) These are called:
	 *    - BEFORE asking for a transport
	 *    - AFTER param serialization (s.data is a string if s.processData is true)
	 * 3) key is the dataType
	 * 4) the catchall symbol "*" can be used
	 * 5) execution will start with transport dataType and THEN continue down to "*" if needed
	 */
	prefilters = {},

	/* Transports bindings
	 * 1) key is the dataType
	 * 2) the catchall symbol "*" can be used
	 * 3) selection will start with transport dataType and THEN go to "*" if needed
	 */
	transports = {},

	// Avoid comment-prolog char sequence (#10098); must appease lint and evade compression
	allTypes = "*/".concat( "*" ),

	// Anchor tag for parsing the document origin
	originAnchor = document.createElement( "a" );

originAnchor.href = location.href;

// Base "constructor" for jQuery.ajaxPrefilter and jQuery.ajaxTransport
function addToPrefiltersOrTransports( structure ) {

	// dataTypeExpression is optional and defaults to "*"
	return function( dataTypeExpression, func ) {

		if ( typeof dataTypeExpression !== "string" ) {
			func = dataTypeExpression;
			dataTypeExpression = "*";
		}

		var dataType,
			i = 0,
			dataTypes = dataTypeExpression.toLowerCase().match( rnothtmlwhite ) || [];

		if ( isFunction( func ) ) {

			// For each dataType in the dataTypeExpression
			while ( ( dataType = dataTypes[ i++ ] ) ) {

				// Prepend if requested
				if ( dataType[ 0 ] === "+" ) {
					dataType = dataType.slice( 1 ) || "*";
					( structure[ dataType ] = structure[ dataType ] || [] ).unshift( func );

				// Otherwise append
				} else {
					( structure[ dataType ] = structure[ dataType ] || [] ).push( func );
				}
			}
		}
	};
}

// Base inspection function for prefilters and transports
function inspectPrefiltersOrTransports( structure, options, originalOptions, jqXHR ) {

	var inspected = {},
		seekingTransport = ( structure === transports );

	function inspect( dataType ) {
		var selected;
		inspected[ dataType ] = true;
		jQuery.each( structure[ dataType ] || [], function( _, prefilterOrFactory ) {
			var dataTypeOrTransport = prefilterOrFactory( options, originalOptions, jqXHR );
			if ( typeof dataTypeOrTransport === "string" &&
				!seekingTransport && !inspected[ dataTypeOrTransport ] ) {

				options.dataTypes.unshift( dataTypeOrTransport );
				inspect( dataTypeOrTransport );
				return false;
			} else if ( seekingTransport ) {
				return !( selected = dataTypeOrTransport );
			}
		} );
		return selected;
	}

	return inspect( options.dataTypes[ 0 ] ) || !inspected[ "*" ] && inspect( "*" );
}

// A special extend for ajax options
// that takes "flat" options (not to be deep extended)
// Fixes #9887
function ajaxExtend( target, src ) {
	var key, deep,
		flatOptions = jQuery.ajaxSettings.flatOptions || {};

	for ( key in src ) {
		if ( src[ key ] !== undefined ) {
			( flatOptions[ key ] ? target : ( deep || ( deep = {} ) ) )[ key ] = src[ key ];
		}
	}
	if ( deep ) {
		jQuery.extend( true, target, deep );
	}

	return target;
}

/* Handles responses to an ajax request:
 * - finds the right dataType (mediates between content-type and expected dataType)
 * - returns the corresponding response
 */
function ajaxHandleResponses( s, jqXHR, responses ) {

	var ct, type, finalDataType, firstDataType,
		contents = s.contents,
		dataTypes = s.dataTypes;

	// Remove auto dataType and get content-type in the process
	while ( dataTypes[ 0 ] === "*" ) {
		dataTypes.shift();
		if ( ct === undefined ) {
			ct = s.mimeType || jqXHR.getResponseHeader( "Content-Type" );
		}
	}

	// Check if we're dealing with a known content-type
	if ( ct ) {
		for ( type in contents ) {
			if ( contents[ type ] && contents[ type ].test( ct ) ) {
				dataTypes.unshift( type );
				break;
			}
		}
	}

	// Check to see if we have a response for the expected dataType
	if ( dataTypes[ 0 ] in responses ) {
		finalDataType = dataTypes[ 0 ];
	} else {

		// Try convertible dataTypes
		for ( type in responses ) {
			if ( !dataTypes[ 0 ] || s.converters[ type + " " + dataTypes[ 0 ] ] ) {
				finalDataType = type;
				break;
			}
			if ( !firstDataType ) {
				firstDataType = type;
			}
		}

		// Or just use first one
		finalDataType = finalDataType || firstDataType;
	}

	// If we found a dataType
	// We add the dataType to the list if needed
	// and return the corresponding response
	if ( finalDataType ) {
		if ( finalDataType !== dataTypes[ 0 ] ) {
			dataTypes.unshift( finalDataType );
		}
		return responses[ finalDataType ];
	}
}

/* Chain conversions given the request and the original response
 * Also sets the responseXXX fields on the jqXHR instance
 */
function ajaxConvert( s, response, jqXHR, isSuccess ) {
	var conv2, current, conv, tmp, prev,
		converters = {},

		// Work with a copy of dataTypes in case we need to modify it for conversion
		dataTypes = s.dataTypes.slice();

	// Create converters map with lowercased keys
	if ( dataTypes[ 1 ] ) {
		for ( conv in s.converters ) {
			converters[ conv.toLowerCase() ] = s.converters[ conv ];
		}
	}

	current = dataTypes.shift();

	// Convert to each sequential dataType
	while ( current ) {

		if ( s.responseFields[ current ] ) {
			jqXHR[ s.responseFields[ current ] ] = response;
		}

		// Apply the dataFilter if provided
		if ( !prev && isSuccess && s.dataFilter ) {
			response = s.dataFilter( response, s.dataType );
		}

		prev = current;
		current = dataTypes.shift();

		if ( current ) {

			// There's only work to do if current dataType is non-auto
			if ( current === "*" ) {

				current = prev;

			// Convert response if prev dataType is non-auto and differs from current
			} else if ( prev !== "*" && prev !== current ) {

				// Seek a direct converter
				conv = converters[ prev + " " + current ] || converters[ "* " + current ];

				// If none found, seek a pair
				if ( !conv ) {
					for ( conv2 in converters ) {

						// If conv2 outputs current
						tmp = conv2.split( " " );
						if ( tmp[ 1 ] === current ) {

							// If prev can be converted to accepted input
							conv = converters[ prev + " " + tmp[ 0 ] ] ||
								converters[ "* " + tmp[ 0 ] ];
							if ( conv ) {

								// Condense equivalence converters
								if ( conv === true ) {
									conv = converters[ conv2 ];

								// Otherwise, insert the intermediate dataType
								} else if ( converters[ conv2 ] !== true ) {
									current = tmp[ 0 ];
									dataTypes.unshift( tmp[ 1 ] );
								}
								break;
							}
						}
					}
				}

				// Apply converter (if not an equivalence)
				if ( conv !== true ) {

					// Unless errors are allowed to bubble, catch and return them
					if ( conv && s.throws ) {
						response = conv( response );
					} else {
						try {
							response = conv( response );
						} catch ( e ) {
							return {
								state: "parsererror",
								error: conv ? e : "No conversion from " + prev + " to " + current
							};
						}
					}
				}
			}
		}
	}

	return { state: "success", data: response };
}

jQuery.extend( {

	// Counter for holding the number of active queries
	active: 0,

	// Last-Modified header cache for next request
	lastModified: {},
	etag: {},

	ajaxSettings: {
		url: location.href,
		type: "GET",
		isLocal: rlocalProtocol.test( location.protocol ),
		global: true,
		processData: true,
		async: true,
		contentType: "application/x-www-form-urlencoded; charset=UTF-8",

		/*
		timeout: 0,
		data: null,
		dataType: null,
		username: null,
		password: null,
		cache: null,
		throws: false,
		traditional: false,
		headers: {},
		*/

		accepts: {
			"*": allTypes,
			text: "text/plain",
			html: "text/html",
			xml: "application/xml, text/xml",
			json: "application/json, text/javascript"
		},

		contents: {
			xml: /\bxml\b/,
			html: /\bhtml/,
			json: /\bjson\b/
		},

		responseFields: {
			xml: "responseXML",
			text: "responseText",
			json: "responseJSON"
		},

		// Data converters
		// Keys separate source (or catchall "*") and destination types with a single space
		converters: {

			// Convert anything to text
			"* text": String,

			// Text to html (true = no transformation)
			"text html": true,

			// Evaluate text as a json expression
			"text json": JSON.parse,

			// Parse text as xml
			"text xml": jQuery.parseXML
		},

		// For options that shouldn't be deep extended:
		// you can add your own custom options here if
		// and when you create one that shouldn't be
		// deep extended (see ajaxExtend)
		flatOptions: {
			url: true,
			context: true
		}
	},

	// Creates a full fledged settings object into target
	// with both ajaxSettings and settings fields.
	// If target is omitted, writes into ajaxSettings.
	ajaxSetup: function( target, settings ) {
		return settings ?

			// Building a settings object
			ajaxExtend( ajaxExtend( target, jQuery.ajaxSettings ), settings ) :

			// Extending ajaxSettings
			ajaxExtend( jQuery.ajaxSettings, target );
	},

	ajaxPrefilter: addToPrefiltersOrTransports( prefilters ),
	ajaxTransport: addToPrefiltersOrTransports( transports ),

	// Main method
	ajax: function( url, options ) {

		// If url is an object, simulate pre-1.5 signature
		if ( typeof url === "object" ) {
			options = url;
			url = undefined;
		}

		// Force options to be an object
		options = options || {};

		var transport,

			// URL without anti-cache param
			cacheURL,

			// Response headers
			responseHeadersString,
			responseHeaders,

			// timeout handle
			timeoutTimer,

			// Url cleanup var
			urlAnchor,

			// Request state (becomes false upon send and true upon completion)
			completed,

			// To know if global events are to be dispatched
			fireGlobals,

			// Loop variable
			i,

			// uncached part of the url
			uncached,

			// Create the final options object
			s = jQuery.ajaxSetup( {}, options ),

			// Callbacks context
			callbackContext = s.context || s,

			// Context for global events is callbackContext if it is a DOM node or jQuery collection
			globalEventContext = s.context &&
				( callbackContext.nodeType || callbackContext.jquery ) ?
				jQuery( callbackContext ) :
				jQuery.event,

			// Deferreds
			deferred = jQuery.Deferred(),
			completeDeferred = jQuery.Callbacks( "once memory" ),

			// Status-dependent callbacks
			statusCode = s.statusCode || {},

			// Headers (they are sent all at once)
			requestHeaders = {},
			requestHeadersNames = {},

			// Default abort message
			strAbort = "canceled",

			// Fake xhr
			jqXHR = {
				readyState: 0,

				// Builds headers hashtable if needed
				getResponseHeader: function( key ) {
					var match;
					if ( completed ) {
						if ( !responseHeaders ) {
							responseHeaders = {};
							while ( ( match = rheaders.exec( responseHeadersString ) ) ) {
								responseHeaders[ match[ 1 ].toLowerCase() + " " ] =
									( responseHeaders[ match[ 1 ].toLowerCase() + " " ] || [] )
										.concat( match[ 2 ] );
							}
						}
						match = responseHeaders[ key.toLowerCase() + " " ];
					}
					return match == null ? null : match.join( ", " );
				},

				// Raw string
				getAllResponseHeaders: function() {
					return completed ? responseHeadersString : null;
				},

				// Caches the header
				setRequestHeader: function( name, value ) {
					if ( completed == null ) {
						name = requestHeadersNames[ name.toLowerCase() ] =
							requestHeadersNames[ name.toLowerCase() ] || name;
						requestHeaders[ name ] = value;
					}
					return this;
				},

				// Overrides response content-type header
				overrideMimeType: function( type ) {
					if ( completed == null ) {
						s.mimeType = type;
					}
					return this;
				},

				// Status-dependent callbacks
				statusCode: function( map ) {
					var code;
					if ( map ) {
						if ( completed ) {

							// Execute the appropriate callbacks
							jqXHR.always( map[ jqXHR.status ] );
						} else {

							// Lazy-add the new callbacks in a way that preserves old ones
							for ( code in map ) {
								statusCode[ code ] = [ statusCode[ code ], map[ code ] ];
							}
						}
					}
					return this;
				},

				// Cancel the request
				abort: function( statusText ) {
					var finalText = statusText || strAbort;
					if ( transport ) {
						transport.abort( finalText );
					}
					done( 0, finalText );
					return this;
				}
			};

		// Attach deferreds
		deferred.promise( jqXHR );

		// Add protocol if not provided (prefilters might expect it)
		// Handle falsy url in the settings object (#10093: consistency with old signature)
		// We also use the url parameter if available
		s.url = ( ( url || s.url || location.href ) + "" )
			.replace( rprotocol, location.protocol + "//" );

		// Alias method option to type as per ticket #12004
		s.type = options.method || options.type || s.method || s.type;

		// Extract dataTypes list
		s.dataTypes = ( s.dataType || "*" ).toLowerCase().match( rnothtmlwhite ) || [ "" ];

		// A cross-domain request is in order when the origin doesn't match the current origin.
		if ( s.crossDomain == null ) {
			urlAnchor = document.createElement( "a" );

			// Support: IE <=8 - 11, Edge 12 - 15
			// IE throws exception on accessing the href property if url is malformed,
			// e.g. http://example.com:80x/
			try {
				urlAnchor.href = s.url;

				// Support: IE <=8 - 11 only
				// Anchor's host property isn't correctly set when s.url is relative
				urlAnchor.href = urlAnchor.href;
				s.crossDomain = originAnchor.protocol + "//" + originAnchor.host !==
					urlAnchor.protocol + "//" + urlAnchor.host;
			} catch ( e ) {

				// If there is an error parsing the URL, assume it is crossDomain,
				// it can be rejected by the transport if it is invalid
				s.crossDomain = true;
			}
		}

		// Convert data if not already a string
		if ( s.data && s.processData && typeof s.data !== "string" ) {
			s.data = jQuery.param( s.data, s.traditional );
		}

		// Apply prefilters
		inspectPrefiltersOrTransports( prefilters, s, options, jqXHR );

		// If request was aborted inside a prefilter, stop there
		if ( completed ) {
			return jqXHR;
		}

		// We can fire global events as of now if asked to
		// Don't fire events if jQuery.event is undefined in an AMD-usage scenario (#15118)
		fireGlobals = jQuery.event && s.global;

		// Watch for a new set of requests
		if ( fireGlobals && jQuery.active++ === 0 ) {
			jQuery.event.trigger( "ajaxStart" );
		}

		// Uppercase the type
		s.type = s.type.toUpperCase();

		// Determine if request has content
		s.hasContent = !rnoContent.test( s.type );

		// Save the URL in case we're toying with the If-Modified-Since
		// and/or If-None-Match header later on
		// Remove hash to simplify url manipulation
		cacheURL = s.url.replace( rhash, "" );

		// More options handling for requests with no content
		if ( !s.hasContent ) {

			// Remember the hash so we can put it back
			uncached = s.url.slice( cacheURL.length );

			// If data is available and should be processed, append data to url
			if ( s.data && ( s.processData || typeof s.data === "string" ) ) {
				cacheURL += ( rquery.test( cacheURL ) ? "&" : "?" ) + s.data;

				// #9682: remove data so that it's not used in an eventual retry
				delete s.data;
			}

			// Add or update anti-cache param if needed
			if ( s.cache === false ) {
				cacheURL = cacheURL.replace( rantiCache, "$1" );
				uncached = ( rquery.test( cacheURL ) ? "&" : "?" ) + "_=" + ( nonce.guid++ ) +
					uncached;
			}

			// Put hash and anti-cache on the URL that will be requested (gh-1732)
			s.url = cacheURL + uncached;

		// Change '%20' to '+' if this is encoded form body content (gh-2658)
		} else if ( s.data && s.processData &&
			( s.contentType || "" ).indexOf( "application/x-www-form-urlencoded" ) === 0 ) {
			s.data = s.data.replace( r20, "+" );
		}

		// Set the If-Modified-Since and/or If-None-Match header, if in ifModified mode.
		if ( s.ifModified ) {
			if ( jQuery.lastModified[ cacheURL ] ) {
				jqXHR.setRequestHeader( "If-Modified-Since", jQuery.lastModified[ cacheURL ] );
			}
			if ( jQuery.etag[ cacheURL ] ) {
				jqXHR.setRequestHeader( "If-None-Match", jQuery.etag[ cacheURL ] );
			}
		}

		// Set the correct header, if data is being sent
		if ( s.data && s.hasContent && s.contentType !== false || options.contentType ) {
			jqXHR.setRequestHeader( "Content-Type", s.contentType );
		}

		// Set the Accepts header for the server, depending on the dataType
		jqXHR.setRequestHeader(
			"Accept",
			s.dataTypes[ 0 ] && s.accepts[ s.dataTypes[ 0 ] ] ?
				s.accepts[ s.dataTypes[ 0 ] ] +
					( s.dataTypes[ 0 ] !== "*" ? ", " + allTypes + "; q=0.01" : "" ) :
				s.accepts[ "*" ]
		);

		// Check for headers option
		for ( i in s.headers ) {
			jqXHR.setRequestHeader( i, s.headers[ i ] );
		}

		// Allow custom headers/mimetypes and early abort
		if ( s.beforeSend &&
			( s.beforeSend.call( callbackContext, jqXHR, s ) === false || completed ) ) {

			// Abort if not done already and return
			return jqXHR.abort();
		}

		// Aborting is no longer a cancellation
		strAbort = "abort";

		// Install callbacks on deferreds
		completeDeferred.add( s.complete );
		jqXHR.done( s.success );
		jqXHR.fail( s.error );

		// Get transport
		transport = inspectPrefiltersOrTransports( transports, s, options, jqXHR );

		// If no transport, we auto-abort
		if ( !transport ) {
			done( -1, "No Transport" );
		} else {
			jqXHR.readyState = 1;

			// Send global event
			if ( fireGlobals ) {
				globalEventContext.trigger( "ajaxSend", [ jqXHR, s ] );
			}

			// If request was aborted inside ajaxSend, stop there
			if ( completed ) {
				return jqXHR;
			}

			// Timeout
			if ( s.async && s.timeout > 0 ) {
				timeoutTimer = window.setTimeout( function() {
					jqXHR.abort( "timeout" );
				}, s.timeout );
			}

			try {
				completed = false;
				transport.send( requestHeaders, done );
			} catch ( e ) {

				// Rethrow post-completion exceptions
				if ( completed ) {
					throw e;
				}

				// Propagate others as results
				done( -1, e );
			}
		}

		// Callback for when everything is done
		function done( status, nativeStatusText, responses, headers ) {
			var isSuccess, success, error, response, modified,
				statusText = nativeStatusText;

			// Ignore repeat invocations
			if ( completed ) {
				return;
			}

			completed = true;

			// Clear timeout if it exists
			if ( timeoutTimer ) {
				window.clearTimeout( timeoutTimer );
			}

			// Dereference transport for early garbage collection
			// (no matter how long the jqXHR object will be used)
			transport = undefined;

			// Cache response headers
			responseHeadersString = headers || "";

			// Set readyState
			jqXHR.readyState = status > 0 ? 4 : 0;

			// Determine if successful
			isSuccess = status >= 200 && status < 300 || status === 304;

			// Get response data
			if ( responses ) {
				response = ajaxHandleResponses( s, jqXHR, responses );
			}

			// Use a noop converter for missing script but not if jsonp
			if ( !isSuccess &&
				jQuery.inArray( "script", s.dataTypes ) > -1 &&
				jQuery.inArray( "json", s.dataTypes ) < 0 ) {
				s.converters[ "text script" ] = function() {};
			}

			// Convert no matter what (that way responseXXX fields are always set)
			response = ajaxConvert( s, response, jqXHR, isSuccess );

			// If successful, handle type chaining
			if ( isSuccess ) {

				// Set the If-Modified-Since and/or If-None-Match header, if in ifModified mode.
				if ( s.ifModified ) {
					modified = jqXHR.getResponseHeader( "Last-Modified" );
					if ( modified ) {
						jQuery.lastModified[ cacheURL ] = modified;
					}
					modified = jqXHR.getResponseHeader( "etag" );
					if ( modified ) {
						jQuery.etag[ cacheURL ] = modified;
					}
				}

				// if no content
				if ( status === 204 || s.type === "HEAD" ) {
					statusText = "nocontent";

				// if not modified
				} else if ( status === 304 ) {
					statusText = "notmodified";

				// If we have data, let's convert it
				} else {
					statusText = response.state;
					success = response.data;
					error = response.error;
					isSuccess = !error;
				}
			} else {

				// Extract error from statusText and normalize for non-aborts
				error = statusText;
				if ( status || !statusText ) {
					statusText = "error";
					if ( status < 0 ) {
						status = 0;
					}
				}
			}

			// Set data for the fake xhr object
			jqXHR.status = status;
			jqXHR.statusText = ( nativeStatusText || statusText ) + "";

			// Success/Error
			if ( isSuccess ) {
				deferred.resolveWith( callbackContext, [ success, statusText, jqXHR ] );
			} else {
				deferred.rejectWith( callbackContext, [ jqXHR, statusText, error ] );
			}

			// Status-dependent callbacks
			jqXHR.statusCode( statusCode );
			statusCode = undefined;

			if ( fireGlobals ) {
				globalEventContext.trigger( isSuccess ? "ajaxSuccess" : "ajaxError",
					[ jqXHR, s, isSuccess ? success : error ] );
			}

			// Complete
			completeDeferred.fireWith( callbackContext, [ jqXHR, statusText ] );

			if ( fireGlobals ) {
				globalEventContext.trigger( "ajaxComplete", [ jqXHR, s ] );

				// Handle the global AJAX counter
				if ( !( --jQuery.active ) ) {
					jQuery.event.trigger( "ajaxStop" );
				}
			}
		}

		return jqXHR;
	},

	getJSON: function( url, data, callback ) {
		return jQuery.get( url, data, callback, "json" );
	},

	getScript: function( url, callback ) {
		return jQuery.get( url, undefined, callback, "script" );
	}
} );

jQuery.each( [ "get", "post" ], function( _i, method ) {
	jQuery[ method ] = function( url, data, callback, type ) {

		// Shift arguments if data argument was omitted
		if ( isFunction( data ) ) {
			type = type || callback;
			callback = data;
			data = undefined;
		}

		// The url can be an options object (which then must have .url)
		return jQuery.ajax( jQuery.extend( {
			url: url,
			type: method,
			dataType: type,
			data: data,
			success: callback
		}, jQuery.isPlainObject( url ) && url ) );
	};
} );

jQuery.ajaxPrefilter( function( s ) {
	var i;
	for ( i in s.headers ) {
		if ( i.toLowerCase() === "content-type" ) {
			s.contentType = s.headers[ i ] || "";
		}
	}
} );


jQuery._evalUrl = function( url, options, doc ) {
	return jQuery.ajax( {
		url: url,

		// Make this explicit, since user can override this through ajaxSetup (#11264)
		type: "GET",
		dataType: "script",
		cache: true,
		async: false,
		global: false,

		// Only evaluate the response if it is successful (gh-4126)
		// dataFilter is not invoked for failure responses, so using it instead
		// of the default converter is kludgy but it works.
		converters: {
			"text script": function() {}
		},
		dataFilter: function( response ) {
			jQuery.globalEval( response, options, doc );
		}
	} );
};


jQuery.fn.extend( {
	wrapAll: function( html ) {
		var wrap;

		if ( this[ 0 ] ) {
			if ( isFunction( html ) ) {
				html = html.call( this[ 0 ] );
			}

			// The elements to wrap the target around
			wrap = jQuery( html, this[ 0 ].ownerDocument ).eq( 0 ).clone( true );

			if ( this[ 0 ].parentNode ) {
				wrap.insertBefore( this[ 0 ] );
			}

			wrap.map( function() {
				var elem = this;

				while ( elem.firstElementChild ) {
					elem = elem.firstElementChild;
				}

				return elem;
			} ).append( this );
		}

		return this;
	},

	wrapInner: function( html ) {
		if ( isFunction( html ) ) {
			return this.each( function( i ) {
				jQuery( this ).wrapInner( html.call( this, i ) );
			} );
		}

		return this.each( function() {
			var self = jQuery( this ),
				contents = self.contents();

			if ( contents.length ) {
				contents.wrapAll( html );

			} else {
				self.append( html );
			}
		} );
	},

	wrap: function( html ) {
		var htmlIsFunction = isFunction( html );

		return this.each( function( i ) {
			jQuery( this ).wrapAll( htmlIsFunction ? html.call( this, i ) : html );
		} );
	},

	unwrap: function( selector ) {
		this.parent( selector ).not( "body" ).each( function() {
			jQuery( this ).replaceWith( this.childNodes );
		} );
		return this;
	}
} );


jQuery.expr.pseudos.hidden = function( elem ) {
	return !jQuery.expr.pseudos.visible( elem );
};
jQuery.expr.pseudos.visible = function( elem ) {
	return !!( elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length );
};




jQuery.ajaxSettings.xhr = function() {
	try {
		return new window.XMLHttpRequest();
	} catch ( e ) {}
};

var xhrSuccessStatus = {

		// File protocol always yields status code 0, assume 200
		0: 200,

		// Support: IE <=9 only
		// #1450: sometimes IE returns 1223 when it should be 204
		1223: 204
	},
	xhrSupported = jQuery.ajaxSettings.xhr();

support.cors = !!xhrSupported && ( "withCredentials" in xhrSupported );
support.ajax = xhrSupported = !!xhrSupported;

jQuery.ajaxTransport( function( options ) {
	var callback, errorCallback;

	// Cross domain only allowed if supported through XMLHttpRequest
	if ( support.cors || xhrSupported && !options.crossDomain ) {
		return {
			send: function( headers, complete ) {
				var i,
					xhr = options.xhr();

				xhr.open(
					options.type,
					options.url,
					options.async,
					options.username,
					options.password
				);

				// Apply custom fields if provided
				if ( options.xhrFields ) {
					for ( i in options.xhrFields ) {
						xhr[ i ] = options.xhrFields[ i ];
					}
				}

				// Override mime type if needed
				if ( options.mimeType && xhr.overrideMimeType ) {
					xhr.overrideMimeType( options.mimeType );
				}

				// X-Requested-With header
				// For cross-domain requests, seeing as conditions for a preflight are
				// akin to a jigsaw puzzle, we simply never set it to be sure.
				// (it can always be set on a per-request basis or even using ajaxSetup)
				// For same-domain requests, won't change header if already provided.
				if ( !options.crossDomain && !headers[ "X-Requested-With" ] ) {
					headers[ "X-Requested-With" ] = "XMLHttpRequest";
				}

				// Set headers
				for ( i in headers ) {
					xhr.setRequestHeader( i, headers[ i ] );
				}

				// Callback
				callback = function( type ) {
					return function() {
						if ( callback ) {
							callback = errorCallback = xhr.onload =
								xhr.onerror = xhr.onabort = xhr.ontimeout =
									xhr.onreadystatechange = null;

							if ( type === "abort" ) {
								xhr.abort();
							} else if ( type === "error" ) {

								// Support: IE <=9 only
								// On a manual native abort, IE9 throws
								// errors on any property access that is not readyState
								if ( typeof xhr.status !== "number" ) {
									complete( 0, "error" );
								} else {
									complete(

										// File: protocol always yields status 0; see #8605, #14207
										xhr.status,
										xhr.statusText
									);
								}
							} else {
								complete(
									xhrSuccessStatus[ xhr.status ] || xhr.status,
									xhr.statusText,

									// Support: IE <=9 only
									// IE9 has no XHR2 but throws on binary (trac-11426)
									// For XHR2 non-text, let the caller handle it (gh-2498)
									( xhr.responseType || "text" ) !== "text"  ||
									typeof xhr.responseText !== "string" ?
										{ binary: xhr.response } :
										{ text: xhr.responseText },
									xhr.getAllResponseHeaders()
								);
							}
						}
					};
				};

				// Listen to events
				xhr.onload = callback();
				errorCallback = xhr.onerror = xhr.ontimeout = callback( "error" );

				// Support: IE 9 only
				// Use onreadystatechange to replace onabort
				// to handle uncaught aborts
				if ( xhr.onabort !== undefined ) {
					xhr.onabort = errorCallback;
				} else {
					xhr.onreadystatechange = function() {

						// Check readyState before timeout as it changes
						if ( xhr.readyState === 4 ) {

							// Allow onerror to be called first,
							// but that will not handle a native abort
							// Also, save errorCallback to a variable
							// as xhr.onerror cannot be accessed
							window.setTimeout( function() {
								if ( callback ) {
									errorCallback();
								}
							} );
						}
					};
				}

				// Create the abort callback
				callback = callback( "abort" );

				try {

					// Do send the request (this may raise an exception)
					xhr.send( options.hasContent && options.data || null );
				} catch ( e ) {

					// #14683: Only rethrow if this hasn't been notified as an error yet
					if ( callback ) {
						throw e;
					}
				}
			},

			abort: function() {
				if ( callback ) {
					callback();
				}
			}
		};
	}
} );




// Prevent auto-execution of scripts when no explicit dataType was provided (See gh-2432)
jQuery.ajaxPrefilter( function( s ) {
	if ( s.crossDomain ) {
		s.contents.script = false;
	}
} );

// Install script dataType
jQuery.ajaxSetup( {
	accepts: {
		script: "text/javascript, application/javascript, " +
			"application/ecmascript, application/x-ecmascript"
	},
	contents: {
		script: /\b(?:java|ecma)script\b/
	},
	converters: {
		"text script": function( text ) {
			jQuery.globalEval( text );
			return text;
		}
	}
} );

// Handle cache's special case and crossDomain
jQuery.ajaxPrefilter( "script", function( s ) {
	if ( s.cache === undefined ) {
		s.cache = false;
	}
	if ( s.crossDomain ) {
		s.type = "GET";
	}
} );

// Bind script tag hack transport
jQuery.ajaxTransport( "script", function( s ) {

	// This transport only deals with cross domain or forced-by-attrs requests
	if ( s.crossDomain || s.scriptAttrs ) {
		var script, callback;
		return {
			send: function( _, complete ) {
				script = jQuery( "<script>" )
					.attr( s.scriptAttrs || {} )
					.prop( { charset: s.scriptCharset, src: s.url } )
					.on( "load error", callback = function( evt ) {
						script.remove();
						callback = null;
						if ( evt ) {
							complete( evt.type === "error" ? 404 : 200, evt.type );
						}
					} );

				// Use native DOM manipulation to avoid our domManip AJAX trickery
				document.head.appendChild( script[ 0 ] );
			},
			abort: function() {
				if ( callback ) {
					callback();
				}
			}
		};
	}
} );




var oldCallbacks = [],
	rjsonp = /(=)\?(?=&|$)|\?\?/;

// Default jsonp settings
jQuery.ajaxSetup( {
	jsonp: "callback",
	jsonpCallback: function() {
		var callback = oldCallbacks.pop() || ( jQuery.expando + "_" + ( nonce.guid++ ) );
		this[ callback ] = true;
		return callback;
	}
} );

// Detect, normalize options and install callbacks for jsonp requests
jQuery.ajaxPrefilter( "json jsonp", function( s, originalSettings, jqXHR ) {

	var callbackName, overwritten, responseContainer,
		jsonProp = s.jsonp !== false && ( rjsonp.test( s.url ) ?
			"url" :
			typeof s.data === "string" &&
				( s.contentType || "" )
					.indexOf( "application/x-www-form-urlencoded" ) === 0 &&
				rjsonp.test( s.data ) && "data"
		);

	// Handle iff the expected data type is "jsonp" or we have a parameter to set
	if ( jsonProp || s.dataTypes[ 0 ] === "jsonp" ) {

		// Get callback name, remembering preexisting value associated with it
		callbackName = s.jsonpCallback = isFunction( s.jsonpCallback ) ?
			s.jsonpCallback() :
			s.jsonpCallback;

		// Insert callback into url or form data
		if ( jsonProp ) {
			s[ jsonProp ] = s[ jsonProp ].replace( rjsonp, "$1" + callbackName );
		} else if ( s.jsonp !== false ) {
			s.url += ( rquery.test( s.url ) ? "&" : "?" ) + s.jsonp + "=" + callbackName;
		}

		// Use data converter to retrieve json after script execution
		s.converters[ "script json" ] = function() {
			if ( !responseContainer ) {
				jQuery.error( callbackName + " was not called" );
			}
			return responseContainer[ 0 ];
		};

		// Force json dataType
		s.dataTypes[ 0 ] = "json";

		// Install callback
		overwritten = window[ callbackName ];
		window[ callbackName ] = function() {
			responseContainer = arguments;
		};

		// Clean-up function (fires after converters)
		jqXHR.always( function() {

			// If previous value didn't exist - remove it
			if ( overwritten === undefined ) {
				jQuery( window ).removeProp( callbackName );

			// Otherwise restore preexisting value
			} else {
				window[ callbackName ] = overwritten;
			}

			// Save back as free
			if ( s[ callbackName ] ) {

				// Make sure that re-using the options doesn't screw things around
				s.jsonpCallback = originalSettings.jsonpCallback;

				// Save the callback name for future use
				oldCallbacks.push( callbackName );
			}

			// Call if it was a function and we have a response
			if ( responseContainer && isFunction( overwritten ) ) {
				overwritten( responseContainer[ 0 ] );
			}

			responseContainer = overwritten = undefined;
		} );

		// Delegate to script
		return "script";
	}
} );




// Support: Safari 8 only
// In Safari 8 documents created via document.implementation.createHTMLDocument
// collapse sibling forms: the second one becomes a child of the first one.
// Because of that, this security measure has to be disabled in Safari 8.
// https://bugs.webkit.org/show_bug.cgi?id=137337
support.createHTMLDocument = ( function() {
	var body = document.implementation.createHTMLDocument( "" ).body;
	body.innerHTML = "<form></form><form></form>";
	return body.childNodes.length === 2;
} )();


// Argument "data" should be string of html
// context (optional): If specified, the fragment will be created in this context,
// defaults to document
// keepScripts (optional): If true, will include scripts passed in the html string
jQuery.parseHTML = function( data, context, keepScripts ) {
	if ( typeof data !== "string" ) {
		return [];
	}
	if ( typeof context === "boolean" ) {
		keepScripts = context;
		context = false;
	}

	var base, parsed, scripts;

	if ( !context ) {

		// Stop scripts or inline event handlers from being executed immediately
		// by using document.implementation
		if ( support.createHTMLDocument ) {
			context = document.implementation.createHTMLDocument( "" );

			// Set the base href for the created document
			// so any parsed elements with URLs
			// are based on the document's URL (gh-2965)
			base = context.createElement( "base" );
			base.href = document.location.href;
			context.head.appendChild( base );
		} else {
			context = document;
		}
	}

	parsed = rsingleTag.exec( data );
	scripts = !keepScripts && [];

	// Single tag
	if ( parsed ) {
		return [ context.createElement( parsed[ 1 ] ) ];
	}

	parsed = buildFragment( [ data ], context, scripts );

	if ( scripts && scripts.length ) {
		jQuery( scripts ).remove();
	}

	return jQuery.merge( [], parsed.childNodes );
};


/**
 * Load a url into a page
 */
jQuery.fn.load = function( url, params, callback ) {
	var selector, type, response,
		self = this,
		off = url.indexOf( " " );

	if ( off > -1 ) {
		selector = stripAndCollapse( url.slice( off ) );
		url = url.slice( 0, off );
	}

	// If it's a function
	if ( isFunction( params ) ) {

		// We assume that it's the callback
		callback = params;
		params = undefined;

	// Otherwise, build a param string
	} else if ( params && typeof params === "object" ) {
		type = "POST";
	}

	// If we have elements to modify, make the request
	if ( self.length > 0 ) {
		jQuery.ajax( {
			url: url,

			// If "type" variable is undefined, then "GET" method will be used.
			// Make value of this field explicit since
			// user can override it through ajaxSetup method
			type: type || "GET",
			dataType: "html",
			data: params
		} ).done( function( responseText ) {

			// Save response for use in complete callback
			response = arguments;

			self.html( selector ?

				// If a selector was specified, locate the right elements in a dummy div
				// Exclude scripts to avoid IE 'Permission Denied' errors
				jQuery( "<div>" ).append( jQuery.parseHTML( responseText ) ).find( selector ) :

				// Otherwise use the full result
				responseText );

		// If the request succeeds, this function gets "data", "status", "jqXHR"
		// but they are ignored because response was set above.
		// If it fails, this function gets "jqXHR", "status", "error"
		} ).always( callback && function( jqXHR, status ) {
			self.each( function() {
				callback.apply( this, response || [ jqXHR.responseText, status, jqXHR ] );
			} );
		} );
	}

	return this;
};




jQuery.expr.pseudos.animated = function( elem ) {
	return jQuery.grep( jQuery.timers, function( fn ) {
		return elem === fn.elem;
	} ).length;
};




jQuery.offset = {
	setOffset: function( elem, options, i ) {
		var curPosition, curLeft, curCSSTop, curTop, curOffset, curCSSLeft, calculatePosition,
			position = jQuery.css( elem, "position" ),
			curElem = jQuery( elem ),
			props = {};

		// Set position first, in-case top/left are set even on static elem
		if ( position === "static" ) {
			elem.style.position = "relative";
		}

		curOffset = curElem.offset();
		curCSSTop = jQuery.css( elem, "top" );
		curCSSLeft = jQuery.css( elem, "left" );
		calculatePosition = ( position === "absolute" || position === "fixed" ) &&
			( curCSSTop + curCSSLeft ).indexOf( "auto" ) > -1;

		// Need to be able to calculate position if either
		// top or left is auto and position is either absolute or fixed
		if ( calculatePosition ) {
			curPosition = curElem.position();
			curTop = curPosition.top;
			curLeft = curPosition.left;

		} else {
			curTop = parseFloat( curCSSTop ) || 0;
			curLeft = parseFloat( curCSSLeft ) || 0;
		}

		if ( isFunction( options ) ) {

			// Use jQuery.extend here to allow modification of coordinates argument (gh-1848)
			options = options.call( elem, i, jQuery.extend( {}, curOffset ) );
		}

		if ( options.top != null ) {
			props.top = ( options.top - curOffset.top ) + curTop;
		}
		if ( options.left != null ) {
			props.left = ( options.left - curOffset.left ) + curLeft;
		}

		if ( "using" in options ) {
			options.using.call( elem, props );

		} else {
			curElem.css( props );
		}
	}
};

jQuery.fn.extend( {

	// offset() relates an element's border box to the document origin
	offset: function( options ) {

		// Preserve chaining for setter
		if ( arguments.length ) {
			return options === undefined ?
				this :
				this.each( function( i ) {
					jQuery.offset.setOffset( this, options, i );
				} );
		}

		var rect, win,
			elem = this[ 0 ];

		if ( !elem ) {
			return;
		}

		// Return zeros for disconnected and hidden (display: none) elements (gh-2310)
		// Support: IE <=11 only
		// Running getBoundingClientRect on a
		// disconnected node in IE throws an error
		if ( !elem.getClientRects().length ) {
			return { top: 0, left: 0 };
		}

		// Get document-relative position by adding viewport scroll to viewport-relative gBCR
		rect = elem.getBoundingClientRect();
		win = elem.ownerDocument.defaultView;
		return {
			top: rect.top + win.pageYOffset,
			left: rect.left + win.pageXOffset
		};
	},

	// position() relates an element's margin box to its offset parent's padding box
	// This corresponds to the behavior of CSS absolute positioning
	position: function() {
		if ( !this[ 0 ] ) {
			return;
		}

		var offsetParent, offset, doc,
			elem = this[ 0 ],
			parentOffset = { top: 0, left: 0 };

		// position:fixed elements are offset from the viewport, which itself always has zero offset
		if ( jQuery.css( elem, "position" ) === "fixed" ) {

			// Assume position:fixed implies availability of getBoundingClientRect
			offset = elem.getBoundingClientRect();

		} else {
			offset = this.offset();

			// Account for the *real* offset parent, which can be the document or its root element
			// when a statically positioned element is identified
			doc = elem.ownerDocument;
			offsetParent = elem.offsetParent || doc.documentElement;
			while ( offsetParent &&
				( offsetParent === doc.body || offsetParent === doc.documentElement ) &&
				jQuery.css( offsetParent, "position" ) === "static" ) {

				offsetParent = offsetParent.parentNode;
			}
			if ( offsetParent && offsetParent !== elem && offsetParent.nodeType === 1 ) {

				// Incorporate borders into its offset, since they are outside its content origin
				parentOffset = jQuery( offsetParent ).offset();
				parentOffset.top += jQuery.css( offsetParent, "borderTopWidth", true );
				parentOffset.left += jQuery.css( offsetParent, "borderLeftWidth", true );
			}
		}

		// Subtract parent offsets and element margins
		return {
			top: offset.top - parentOffset.top - jQuery.css( elem, "marginTop", true ),
			left: offset.left - parentOffset.left - jQuery.css( elem, "marginLeft", true )
		};
	},

	// This method will return documentElement in the following cases:
	// 1) For the element inside the iframe without offsetParent, this method will return
	//    documentElement of the parent window
	// 2) For the hidden or detached element
	// 3) For body or html element, i.e. in case of the html node - it will return itself
	//
	// but those exceptions were never presented as a real life use-cases
	// and might be considered as more preferable results.
	//
	// This logic, however, is not guaranteed and can change at any point in the future
	offsetParent: function() {
		return this.map( function() {
			var offsetParent = this.offsetParent;

			while ( offsetParent && jQuery.css( offsetParent, "position" ) === "static" ) {
				offsetParent = offsetParent.offsetParent;
			}

			return offsetParent || documentElement;
		} );
	}
} );

// Create scrollLeft and scrollTop methods
jQuery.each( { scrollLeft: "pageXOffset", scrollTop: "pageYOffset" }, function( method, prop ) {
	var top = "pageYOffset" === prop;

	jQuery.fn[ method ] = function( val ) {
		return access( this, function( elem, method, val ) {

			// Coalesce documents and windows
			var win;
			if ( isWindow( elem ) ) {
				win = elem;
			} else if ( elem.nodeType === 9 ) {
				win = elem.defaultView;
			}

			if ( val === undefined ) {
				return win ? win[ prop ] : elem[ method ];
			}

			if ( win ) {
				win.scrollTo(
					!top ? val : win.pageXOffset,
					top ? val : win.pageYOffset
				);

			} else {
				elem[ method ] = val;
			}
		}, method, val, arguments.length );
	};
} );

// Support: Safari <=7 - 9.1, Chrome <=37 - 49
// Add the top/left cssHooks using jQuery.fn.position
// Webkit bug: https://bugs.webkit.org/show_bug.cgi?id=29084
// Blink bug: https://bugs.chromium.org/p/chromium/issues/detail?id=589347
// getComputedStyle returns percent when specified for top/left/bottom/right;
// rather than make the css module depend on the offset module, just check for it here
jQuery.each( [ "top", "left" ], function( _i, prop ) {
	jQuery.cssHooks[ prop ] = addGetHookIf( support.pixelPosition,
		function( elem, computed ) {
			if ( computed ) {
				computed = curCSS( elem, prop );

				// If curCSS returns percentage, fallback to offset
				return rnumnonpx.test( computed ) ?
					jQuery( elem ).position()[ prop ] + "px" :
					computed;
			}
		}
	);
} );


// Create innerHeight, innerWidth, height, width, outerHeight and outerWidth methods
jQuery.each( { Height: "height", Width: "width" }, function( name, type ) {
	jQuery.each( {
		padding: "inner" + name,
		content: type,
		"": "outer" + name
	}, function( defaultExtra, funcName ) {

		// Margin is only for outerHeight, outerWidth
		jQuery.fn[ funcName ] = function( margin, value ) {
			var chainable = arguments.length && ( defaultExtra || typeof margin !== "boolean" ),
				extra = defaultExtra || ( margin === true || value === true ? "margin" : "border" );

			return access( this, function( elem, type, value ) {
				var doc;

				if ( isWindow( elem ) ) {

					// $( window ).outerWidth/Height return w/h including scrollbars (gh-1729)
					return funcName.indexOf( "outer" ) === 0 ?
						elem[ "inner" + name ] :
						elem.document.documentElement[ "client" + name ];
				}

				// Get document width or height
				if ( elem.nodeType === 9 ) {
					doc = elem.documentElement;

					// Either scroll[Width/Height] or offset[Width/Height] or client[Width/Height],
					// whichever is greatest
					return Math.max(
						elem.body[ "scroll" + name ], doc[ "scroll" + name ],
						elem.body[ "offset" + name ], doc[ "offset" + name ],
						doc[ "client" + name ]
					);
				}

				return value === undefined ?

					// Get width or height on the element, requesting but not forcing parseFloat
					jQuery.css( elem, type, extra ) :

					// Set width or height on the element
					jQuery.style( elem, type, value, extra );
			}, type, chainable ? margin : undefined, chainable );
		};
	} );
} );


jQuery.each( [
	"ajaxStart",
	"ajaxStop",
	"ajaxComplete",
	"ajaxError",
	"ajaxSuccess",
	"ajaxSend"
], function( _i, type ) {
	jQuery.fn[ type ] = function( fn ) {
		return this.on( type, fn );
	};
} );




jQuery.fn.extend( {

	bind: function( types, data, fn ) {
		return this.on( types, null, data, fn );
	},
	unbind: function( types, fn ) {
		return this.off( types, null, fn );
	},

	delegate: function( selector, types, data, fn ) {
		return this.on( types, selector, data, fn );
	},
	undelegate: function( selector, types, fn ) {

		// ( namespace ) or ( selector, types [, fn] )
		return arguments.length === 1 ?
			this.off( selector, "**" ) :
			this.off( types, selector || "**", fn );
	},

	hover: function( fnOver, fnOut ) {
		return this.mouseenter( fnOver ).mouseleave( fnOut || fnOver );
	}
} );

jQuery.each(
	( "blur focus focusin focusout resize scroll click dblclick " +
	"mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave " +
	"change select submit keydown keypress keyup contextmenu" ).split( " " ),
	function( _i, name ) {

		// Handle event binding
		jQuery.fn[ name ] = function( data, fn ) {
			return arguments.length > 0 ?
				this.on( name, null, data, fn ) :
				this.trigger( name );
		};
	}
);




// Support: Android <=4.0 only
// Make sure we trim BOM and NBSP
var rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;

// Bind a function to a context, optionally partially applying any
// arguments.
// jQuery.proxy is deprecated to promote standards (specifically Function#bind)
// However, it is not slated for removal any time soon
jQuery.proxy = function( fn, context ) {
	var tmp, args, proxy;

	if ( typeof context === "string" ) {
		tmp = fn[ context ];
		context = fn;
		fn = tmp;
	}

	// Quick check to determine if target is callable, in the spec
	// this throws a TypeError, but we will just return undefined.
	if ( !isFunction( fn ) ) {
		return undefined;
	}

	// Simulated bind
	args = slice.call( arguments, 2 );
	proxy = function() {
		return fn.apply( context || this, args.concat( slice.call( arguments ) ) );
	};

	// Set the guid of unique handler to the same of original handler, so it can be removed
	proxy.guid = fn.guid = fn.guid || jQuery.guid++;

	return proxy;
};

jQuery.holdReady = function( hold ) {
	if ( hold ) {
		jQuery.readyWait++;
	} else {
		jQuery.ready( true );
	}
};
jQuery.isArray = Array.isArray;
jQuery.parseJSON = JSON.parse;
jQuery.nodeName = nodeName;
jQuery.isFunction = isFunction;
jQuery.isWindow = isWindow;
jQuery.camelCase = camelCase;
jQuery.type = toType;

jQuery.now = Date.now;

jQuery.isNumeric = function( obj ) {

	// As of jQuery 3.0, isNumeric is limited to
	// strings and numbers (primitives or objects)
	// that can be coerced to finite numbers (gh-2662)
	var type = jQuery.type( obj );
	return ( type === "number" || type === "string" ) &&

		// parseFloat NaNs numeric-cast false positives ("")
		// ...but misinterprets leading-number strings, particularly hex literals ("0x...")
		// subtraction forces infinities to NaN
		!isNaN( obj - parseFloat( obj ) );
};

jQuery.trim = function( text ) {
	return text == null ?
		"" :
		( text + "" ).replace( rtrim, "" );
};



// Register as a named AMD module, since jQuery can be concatenated with other
// files that may use define, but not via a proper concatenation script that
// understands anonymous AMD modules. A named AMD is safest and most robust
// way to register. Lowercase jquery is used because AMD module names are
// derived from file names, and jQuery is normally delivered in a lowercase
// file name. Do this after creating the global so that if an AMD module wants
// to call noConflict to hide this version of jQuery, it will work.

// Note that for maximum portability, libraries that are not jQuery should
// declare themselves as anonymous modules, and avoid setting a global if an
// AMD loader is present. jQuery is a special case. For more information, see
// https://github.com/jrburke/requirejs/wiki/Updating-existing-libraries#wiki-anon

if ( true ) {
	!(__WEBPACK_AMD_DEFINE_ARRAY__ = [], __WEBPACK_AMD_DEFINE_RESULT__ = (function() {
		return jQuery;
	}).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
}




var

	// Map over jQuery in case of overwrite
	_jQuery = window.jQuery,

	// Map over the $ in case of overwrite
	_$ = window.$;

jQuery.noConflict = function( deep ) {
	if ( window.$ === jQuery ) {
		window.$ = _$;
	}

	if ( deep && window.jQuery === jQuery ) {
		window.jQuery = _jQuery;
	}

	return jQuery;
};

// Expose jQuery and $ identifiers, even in AMD
// (#7102#comment:10, https://github.com/jquery/jquery/pull/557)
// and CommonJS for browser emulators (#13566)
if ( typeof noGlobal === "undefined" ) {
	window.jQuery = window.$ = jQuery;
}




return jQuery;
} );


/***/ }),

/***/ 102:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(4);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(2);
/**
 * Patterns autoscale - scale elements to fit available space
 *
 * Copyright 2012 Humberto Sermeno
 * Copyright 2013 Simplon B.V. - Wichert Akkerman
 */





var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"]("auto-scale");
parser.addArgument("method", "scale", ["scale", "zoom"]);
parser.addArgument("size", "width", ["width", "height", "contain", "cover"]);
parser.addArgument("min-width", 0);
parser.addArgument("max-width", 1000000);
parser.addArgument("min-height", 0);
parser.addArgument("max-height", 1000000);
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].extend({
  name: "autoscale",
  trigger: ".pat-auto-scale",
  force_method: null,
  init: function init($el, opts) {
    this.options = parser.parse(this.$el, opts);

    if (this.force_method !== null) {
      this.options.method = this.force_method;
    }

    this._setup().scale();

    return this.$el;
  },
  _setup: function _setup() {
    if (!_core_utils__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].checkCSSFeature("zoom")) {
      // See https://bugzilla.mozilla.org/show_bug.cgi?id=390936
      this.force_method = "scale";
    }

    var scaler = underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].debounce(this.scale.bind(this), 250);

    jquery__WEBPACK_IMPORTED_MODULE_0___default()(window).on("resize.autoscale", scaler);
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).on("pat-update.autoscale", scaler);
    return this;
  },
  scale: function scale() {
    var available_space, scale, scaled_height, scaled_width, container;

    if (this.$el[0].tagName === "BODY") {
      container = this.$el[0];
    } else {
      if (this.$el.closest(".auto-scale-wrapper").length != 0) {
        container = this.$el.closest(".auto-scale-wrapper").parent()[0];
      } else {
        container = this.$el.parent()[0];
      }
    }

    if (!container) {
      // Element has not been added to the DOM yet.
      return;
    }

    var style = window.getComputedStyle(container);
    available_space = {
      width: parseInt(style.width, 10),
      height: parseInt(style.height, 10)
    };
    available_space.width = Math.min(available_space.width, this.options.max.width);
    available_space.width = Math.max(available_space.width, this.options.min.width);
    available_space.height = Math.min(available_space.height, this.options.max.height);
    available_space.height = Math.max(available_space.height, this.options.min.height);

    switch (this.options.size) {
      case "width":
        scale = available_space.width / this.$el.outerWidth();
        break;

      case "height":
        scale = available_space.height / this.$el.outerHeight();
        break;

      case "contain":
        // Fit entire content on area, allowing for extra space
        scale = Math.min(available_space.width / this.$el.outerWidth(), available_space.height / this.$el.outerHeight());
        break;

      case "cover":
        // Covert entire area, possible clipping
        scale = Math.max(available_space.width / this.$el.outerWidth(), available_space.height / this.$el.outerHeight());
        break;

      default:
        return;
    }

    scaled_height = this.$el.outerHeight() * scale;
    scaled_width = this.$el.outerWidth() * scale;

    switch (this.options.method) {
      case "scale":
        this.$el.css("transform", "scale(" + scale + ")");

        if (this.$el.parent().attr("class") === undefined || this.$el.parent().attr("class") != undefined && jquery__WEBPACK_IMPORTED_MODULE_0___default.a.inArray("auto-scale-wrapper", this.$el.parent().attr("class").split(/\s+/)) === -1) {
          this.$el.wrap("<div class='auto-scale-wrapper'></div>");
        }

        this.$el.parent().height(scaled_height).width(scaled_width);
        break;

      case "zoom":
        this.$el.css("zoom", scale);
        break;
    }

    this.$el.addClass("scaled");
    return this;
  }
}));

/***/ }),

/***/ 103:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(5);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(4);
/* harmony import */ var _core_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(11);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(2);
/* harmony import */ var _core_jquery_ext__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(38);
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }






var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"]("checklist");
parser.addArgument("select", ".select-all");
parser.addArgument("deselect", ".deselect-all");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].extend({
  name: "checklist",
  trigger: ".pat-checklist",
  jquery_plugin: true,
  all_selects: [],
  all_deselects: [],
  all_checkboxes: [],
  all_radios: [],
  init: function init() {
    this.options = parser.parse(this.el, this.options, false);
    this.$el.on("patterns-injected", this._init.bind(this));

    this._init();
  },
  _init: function _init() {
    this.all_checkboxes = this.el.querySelectorAll("input[type=checkbox]");
    this.all_radios = this.el.querySelectorAll("input[type=radio]");
    this.all_selects = _core_dom__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].find_scoped(this.el, this.options.select);

    var _iterator = _createForOfIteratorHelper(this.all_selects),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var btn = _step.value;
        btn.addEventListener("click", this.select_all.bind(this));
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }

    this.all_deselects = _core_dom__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].find_scoped(this.el, this.options.deselect);

    var _iterator2 = _createForOfIteratorHelper(this.all_deselects),
        _step2;

    try {
      for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
        var _btn = _step2.value;

        _btn.addEventListener("click", this.deselect_all.bind(this));
      } // update select/deselect button status

    } catch (err) {
      _iterator2.e(err);
    } finally {
      _iterator2.f();
    }

    this.el.addEventListener("change", this._handler_change.bind(this));
    this.change_buttons();
    this.change_checked();
  },
  _handler_change: function _handler_change() {
    var _this = this;

    _core_utils__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].debounce(function () {
      return _this.change_buttons();
    }, 50)();
    _core_utils__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].debounce(function () {
      return _this.change_checked();
    }, 50)();
  },
  destroy: function destroy() {
    var _iterator3 = _createForOfIteratorHelper(this.all_selects),
        _step3;

    try {
      for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
        var it = _step3.value;
        it.removeEventListener("click", this.select_all);
      }
    } catch (err) {
      _iterator3.e(err);
    } finally {
      _iterator3.f();
    }

    var _iterator4 = _createForOfIteratorHelper(this.all_deselects),
        _step4;

    try {
      for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
        var _it = _step4.value;

        _it.removeEventListener("click", this.deselect_all);
      }
    } catch (err) {
      _iterator4.e(err);
    } finally {
      _iterator4.f();
    }

    this.el.removeEventListener("change", this._handler_change);
    this.$el.off("patterns_injected");
  },
  find_siblings: function find_siblings(el, sel) {
    // Looks for the closest elements within the `el` tree that match the
    // `sel` selector
    var res;
    var parent = el.parentNode;

    while (parent) {
      res = parent.querySelectorAll(sel);

      if (res.length || parent === this.el) {
        // return if results were found or we reached the pattern top
        return res;
      }

      parent = parent.parentNode;
    }
  },
  find_checkboxes: function find_checkboxes(ref_el, sel) {
    var chkbxs = [];

    if (this.options.select.indexOf("#") === 0) {
      chkbxs = this.el.querySelectorAll(sel);
    } else {
      chkbxs = this.find_siblings(ref_el, sel);
    }

    return chkbxs;
  },
  change_buttons: function change_buttons() {
    var chkbxs;

    var _iterator5 = _createForOfIteratorHelper(this.all_selects),
        _step5;

    try {
      for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
        var btn = _step5.value;
        chkbxs = this.find_checkboxes(btn, "input[type=checkbox]");
        btn.disabled = _toConsumableArray(chkbxs).map(function (el) {
          return el.matches(":checked");
        }).every(function (it) {
          return it === true;
        });
      }
    } catch (err) {
      _iterator5.e(err);
    } finally {
      _iterator5.f();
    }

    var _iterator6 = _createForOfIteratorHelper(this.all_deselects),
        _step6;

    try {
      for (_iterator6.s(); !(_step6 = _iterator6.n()).done;) {
        var _btn2 = _step6.value;
        chkbxs = this.find_checkboxes(_btn2, "input[type=checkbox]");
        _btn2.disabled = _toConsumableArray(chkbxs).map(function (el) {
          return el.matches(":checked");
        }).every(function (it) {
          return it === false;
        });
      }
    } catch (err) {
      _iterator6.e(err);
    } finally {
      _iterator6.f();
    }
  },
  select_all: function select_all(e) {
    e.preventDefault();
    var chkbxs = this.find_checkboxes(e.target, "input[type=checkbox]:not(:checked)");

    var _iterator7 = _createForOfIteratorHelper(chkbxs),
        _step7;

    try {
      for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
        var box = _step7.value;
        box.checked = true;
        box.dispatchEvent(new Event("change", {
          bubbles: true,
          cancelable: true
        }));
      }
    } catch (err) {
      _iterator7.e(err);
    } finally {
      _iterator7.f();
    }
  },
  deselect_all: function deselect_all(e) {
    e.preventDefault();
    var chkbxs = this.find_checkboxes(e.target, "input[type=checkbox]:checked");

    var _iterator8 = _createForOfIteratorHelper(chkbxs),
        _step8;

    try {
      for (_iterator8.s(); !(_step8 = _iterator8.n()).done;) {
        var box = _step8.value;
        box.checked = false;
        box.dispatchEvent(new Event("change", {
          bubbles: true,
          cancelable: true
        }));
      }
    } catch (err) {
      _iterator8.e(err);
    } finally {
      _iterator8.f();
    }
  },
  change_checked: function change_checked() {
    var _iterator9 = _createForOfIteratorHelper(_toConsumableArray(this.all_checkboxes).concat(_toConsumableArray(this.all_radios))),
        _step9;

    try {
      for (_iterator9.s(); !(_step9 = _iterator9.n()).done;) {
        var it = _step9.value;

        var _iterator11 = _createForOfIteratorHelper(it.labels),
            _step11;

        try {
          for (_iterator11.s(); !(_step11 = _iterator11.n()).done;) {
            var label = _step11.value;
            label.classList.remove("unchecked");
            label.classList.remove("checked");
            label.classList.add(it.checked ? "checked" : "unchecked");
          }
        } catch (err) {
          _iterator11.e(err);
        } finally {
          _iterator11.f();
        }
      }
    } catch (err) {
      _iterator9.e(err);
    } finally {
      _iterator9.f();
    }

    var _iterator10 = _createForOfIteratorHelper(_core_dom__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].querySelectorAllAndMe(this.el, "fieldset")),
        _step10;

    try {
      for (_iterator10.s(); !(_step10 = _iterator10.n()).done;) {
        var fieldset = _step10.value;

        if (fieldset.querySelectorAll("input[type=checkbox]:checked, input[type=radio]:checked").length) {
          fieldset.classList.remove("unchecked");
          fieldset.classList.add("checked");
        } else {
          fieldset.classList.remove("checked");
          fieldset.classList.add("unchecked");
        }
      }
    } catch (err) {
      _iterator10.e(err);
    } finally {
      _iterator10.f();
    }
  }
}));

/***/ }),

/***/ 104:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _inject_inject__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(23);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(4);
/* harmony import */ var _core_store__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(22);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(5);
/* harmony import */ var _core_jquery_ext__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(38);
/**
 * Patterns collapsible - Collapsible content
 *
 * Copyright 2012-2013 Florian Friesdorf
 * Copyright 2012-2013 Simplon B.V. - Wichert Akkerman
 * Copyright 2012 Markus Maier
 * Copyright 2013 Peter Lamut
 * Copyright 2012 Jonas Hoersch
 */







var log = _core_logging__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].getLogger("pat.collapsible");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"]("collapsible");
parser.addArgument("load-content");
parser.addArgument("store", "none", ["none", "session", "local"]);
parser.addArgument("transition", "slide", ["none", "css", "fade", "slide", "slide-horizontal"]);
parser.addArgument("effect-duration", "fast");
parser.addArgument("effect-easing", "swing");
parser.addArgument("closed", false);
parser.addArgument("trigger", "::first");
parser.addArgument("close-trigger");
parser.addArgument("open-trigger");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_5__[/* default */ "a"].extend({
  name: "collapsible",
  trigger: ".pat-collapsible",
  jquery_plugin: true,
  parser: parser,
  transitions: {
    "none": {
      closed: "hide",
      open: "show"
    },
    "fade": {
      closed: "fadeOut",
      open: "fadeIn"
    },
    "slide": {
      closed: "slideUp",
      open: "slideDown"
    },
    "slide-horizontal": {
      closed: "slideOut",
      open: "slideIn"
    }
  },
  init: function init($el, opts) {
    var $content, state, storage;
    this.options = _core_store__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].updateOptions($el[0], parser.parse($el, opts));

    if (this.options.trigger === "::first") {
      this.$trigger = $el.children(":first");
      $content = $el.children(":gt(0)");
    } else {
      this.$trigger = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this.options.trigger);
      $content = $el.children();
    }

    if (this.$trigger.length === 0) {
      log.error("Collapsible has no trigger.", $el[0]);
      return;
    }

    this.$panel = $el.children(".panel-content");

    if (this.$panel.length === 0) {
      if ($content.length) {
        this.$panel = $content.wrapAll("<div class='panel-content' />").parent();
      } else {
        this.$panel = jquery__WEBPACK_IMPORTED_MODULE_0___default()("<div class='panel-content' />").insertAfter(this.$trigger);
      }
    }

    state = this.options.closed || $el.hasClass("closed") ? "closed" : "open";

    if (this.options.store !== "none") {
      storage = (this.options.store === "local" ? _core_store__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].local : _core_store__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].session)(this.name);
      state = storage.get($el.attr("id")) || state;
    }

    if (state === "closed") {
      this.$trigger.removeClass("collapsible-open").addClass("collapsible-closed");
      $el.removeClass("open").addClass("closed");
      this.$panel.hide();
    } else {
      if (this.options.loadContent) this._loadContent($el, this.options.loadContent, this.$panel);
      this.$trigger.removeClass("collapsible-closed").addClass("collapsible-open");
      $el.removeClass("closed").addClass("open");
      this.$panel.show();
    }

    this.$trigger.off(".pat-collapsible").on("click.pat-collapsible", null, $el, this._onClick.bind(this)).on("keypress.pat-collapsible", null, $el, this._onKeyPress.bind(this));

    if (this.options.closeTrigger) {
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).on("click", this.options.closeTrigger, this.close.bind(this));
    }

    if (this.options.openTrigger) {
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).on("click", this.options.openTrigger, this.open.bind(this));
    }

    return $el;
  },
  open: function open() {
    if (!this.$el.hasClass("open")) this.toggle();
    return this.$el;
  },
  close: function close() {
    if (!this.$el.hasClass("closed")) this.toggle();
    return this.$el;
  },
  _onClick: function _onClick(event) {
    this.toggle(event.data);
  },
  _onKeyPress: function _onKeyPress(event) {
    var keycode = event.keyCode ? event.keyCode : event.which;
    if (keycode === 13) this.toggle();
  },
  _loadContent: function _loadContent($el, url, $target) {
    var components = url.split("#"),
        base_url = components[0],
        id = components[1] ? "#" + components[1] : "body",
        opts = [{
      url: base_url,
      source: id,
      $target: $target,
      dataType: "html"
    }];
    _inject_inject__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].execute(opts, $el);
  },
  // jQuery method to force loading of content.
  loadContent: function loadContent($el) {
    return $el.each(function (idx, el) {
      if (this.options.loadContent) this._loadContent(jquery__WEBPACK_IMPORTED_MODULE_0___default()(el), this.options.loadContent, this.$panel);
    }.bind(this));
  },
  toggle: function toggle() {
    var new_state = this.$el.hasClass("closed") ? "open" : "closed";

    if (this.options.store !== "none") {
      var storage = (this.options.store === "local" ? _core_store__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].local : _core_store__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].session)(this.name);
      storage.set(this.$el.attr("id"), new_state);
    }

    if (new_state === "open") {
      this.$el.trigger("patterns-collapsible-open");

      this._transit(this.$el, "closed", "open");
    } else {
      this.$el.trigger("patterns-collapsible-close");

      this._transit(this.$el, "open", "closed");
    }

    return this.$el; // allow chaining
  },
  _transit: function _transit($el, from_cls, to_cls) {
    if (to_cls === "open" && this.options.loadContent) {
      this._loadContent($el, this.options.loadContent, this.$panel);
    }

    var duration = this.options.transition === "css" || this.options.transition === "none" ? null : this.options.effect.duration;

    if (!duration) {
      this.$trigger.removeClass("collapsible-" + from_cls).addClass("collapsible-" + to_cls);
      $el.removeClass(from_cls).addClass(to_cls).trigger("pat-update", {
        pattern: "collapsible",
        transition: "complete"
      });
    } else {
      var t = this.transitions[this.options.transition];
      $el.addClass("in-progress").trigger("pat-update", {
        pattern: "collapsible",
        transition: "start"
      });
      this.$trigger.addClass("collapsible-in-progress");
      this.$panel[t[to_cls]](duration, this.options.effect.easing, function () {
        this.$trigger.removeClass("collapsible-" + from_cls).removeClass("collapsible-in-progress").addClass("collapsible-" + to_cls);
        $el.removeClass(from_cls).removeClass("in-progress").addClass(to_cls).trigger("pat-update", {
          pattern: "collapsible",
          transition: "complete"
        });
      }.bind(this));
    }
  }
}));

/***/ }),

/***/ 105:
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"./af.js": [
		180,
		0,
		21
	],
	"./ar-dz.js": [
		181,
		0,
		22
	],
	"./ar-kw.js": [
		182,
		0,
		23
	],
	"./ar-ly.js": [
		183,
		0,
		24
	],
	"./ar-ma.js": [
		184,
		0,
		25
	],
	"./ar-sa.js": [
		185,
		0,
		26
	],
	"./ar-tn.js": [
		186,
		0,
		27
	],
	"./ar.js": [
		187,
		0,
		28
	],
	"./az.js": [
		188,
		0,
		29
	],
	"./be.js": [
		189,
		0,
		30
	],
	"./bg.js": [
		190,
		0,
		31
	],
	"./bm.js": [
		191,
		0,
		32
	],
	"./bn-bd.js": [
		192,
		0,
		33
	],
	"./bn.js": [
		193,
		0,
		34
	],
	"./bo.js": [
		194,
		0,
		35
	],
	"./br.js": [
		195,
		0,
		36
	],
	"./bs.js": [
		196,
		0,
		37
	],
	"./ca.js": [
		197,
		0,
		38
	],
	"./cs.js": [
		198,
		0,
		39
	],
	"./cv.js": [
		199,
		0,
		40
	],
	"./cy.js": [
		200,
		0,
		41
	],
	"./da.js": [
		201,
		0,
		42
	],
	"./de-at.js": [
		202,
		0,
		43
	],
	"./de-ch.js": [
		203,
		0,
		44
	],
	"./de.js": [
		204,
		0,
		45
	],
	"./dv.js": [
		205,
		0,
		46
	],
	"./el.js": [
		206,
		0,
		47
	],
	"./en-au.js": [
		207,
		0,
		48
	],
	"./en-ca.js": [
		208,
		0,
		49
	],
	"./en-gb.js": [
		209,
		0,
		50
	],
	"./en-ie.js": [
		210,
		0,
		51
	],
	"./en-il.js": [
		211,
		0,
		52
	],
	"./en-in.js": [
		212,
		0,
		53
	],
	"./en-nz.js": [
		213,
		0,
		54
	],
	"./en-sg.js": [
		214,
		0,
		55
	],
	"./eo.js": [
		215,
		0,
		56
	],
	"./es-do.js": [
		216,
		0,
		57
	],
	"./es-mx.js": [
		217,
		0,
		58
	],
	"./es-us.js": [
		218,
		0,
		59
	],
	"./es.js": [
		219,
		0,
		60
	],
	"./et.js": [
		220,
		0,
		61
	],
	"./eu.js": [
		221,
		0,
		62
	],
	"./fa.js": [
		222,
		0,
		63
	],
	"./fi.js": [
		223,
		0,
		64
	],
	"./fil.js": [
		224,
		0,
		65
	],
	"./fo.js": [
		225,
		0,
		66
	],
	"./fr-ca.js": [
		226,
		0,
		67
	],
	"./fr-ch.js": [
		227,
		0,
		68
	],
	"./fr.js": [
		228,
		0,
		69
	],
	"./fy.js": [
		229,
		0,
		70
	],
	"./ga.js": [
		230,
		0,
		71
	],
	"./gd.js": [
		231,
		0,
		72
	],
	"./gl.js": [
		232,
		0,
		73
	],
	"./gom-deva.js": [
		233,
		0,
		74
	],
	"./gom-latn.js": [
		234,
		0,
		75
	],
	"./gu.js": [
		235,
		0,
		76
	],
	"./he.js": [
		236,
		0,
		77
	],
	"./hi.js": [
		237,
		0,
		78
	],
	"./hr.js": [
		238,
		0,
		79
	],
	"./hu.js": [
		239,
		0,
		80
	],
	"./hy-am.js": [
		240,
		0,
		81
	],
	"./id.js": [
		241,
		0,
		82
	],
	"./is.js": [
		242,
		0,
		83
	],
	"./it-ch.js": [
		243,
		0,
		84
	],
	"./it.js": [
		244,
		0,
		85
	],
	"./ja.js": [
		245,
		0,
		86
	],
	"./jv.js": [
		246,
		0,
		87
	],
	"./ka.js": [
		247,
		0,
		88
	],
	"./kk.js": [
		248,
		0,
		89
	],
	"./km.js": [
		249,
		0,
		90
	],
	"./kn.js": [
		250,
		0,
		91
	],
	"./ko.js": [
		251,
		0,
		92
	],
	"./ku.js": [
		252,
		0,
		93
	],
	"./ky.js": [
		253,
		0,
		94
	],
	"./lb.js": [
		254,
		0,
		95
	],
	"./lo.js": [
		255,
		0,
		96
	],
	"./lt.js": [
		256,
		0,
		97
	],
	"./lv.js": [
		257,
		0,
		98
	],
	"./me.js": [
		258,
		0,
		99
	],
	"./mi.js": [
		259,
		0,
		100
	],
	"./mk.js": [
		260,
		0,
		101
	],
	"./ml.js": [
		261,
		0,
		102
	],
	"./mn.js": [
		262,
		0,
		103
	],
	"./mr.js": [
		263,
		0,
		104
	],
	"./ms-my.js": [
		264,
		0,
		105
	],
	"./ms.js": [
		265,
		0,
		106
	],
	"./mt.js": [
		266,
		0,
		107
	],
	"./my.js": [
		267,
		0,
		108
	],
	"./nb.js": [
		268,
		0,
		109
	],
	"./ne.js": [
		269,
		0,
		110
	],
	"./nl-be.js": [
		270,
		0,
		111
	],
	"./nl.js": [
		271,
		0,
		112
	],
	"./nn.js": [
		272,
		0,
		113
	],
	"./oc-lnc.js": [
		273,
		0,
		114
	],
	"./pa-in.js": [
		274,
		0,
		115
	],
	"./pl.js": [
		275,
		0,
		116
	],
	"./pt-br.js": [
		276,
		0,
		117
	],
	"./pt.js": [
		277,
		0,
		118
	],
	"./ro.js": [
		278,
		0,
		119
	],
	"./ru.js": [
		279,
		0,
		120
	],
	"./sd.js": [
		280,
		0,
		121
	],
	"./se.js": [
		281,
		0,
		122
	],
	"./si.js": [
		282,
		0,
		123
	],
	"./sk.js": [
		283,
		0,
		124
	],
	"./sl.js": [
		284,
		0,
		125
	],
	"./sq.js": [
		285,
		0,
		126
	],
	"./sr-cyrl.js": [
		286,
		0,
		127
	],
	"./sr.js": [
		287,
		0,
		128
	],
	"./ss.js": [
		288,
		0,
		129
	],
	"./sv.js": [
		289,
		0,
		130
	],
	"./sw.js": [
		290,
		0,
		131
	],
	"./ta.js": [
		291,
		0,
		132
	],
	"./te.js": [
		292,
		0,
		133
	],
	"./tet.js": [
		293,
		0,
		134
	],
	"./tg.js": [
		294,
		0,
		135
	],
	"./th.js": [
		295,
		0,
		136
	],
	"./tk.js": [
		296,
		0,
		137
	],
	"./tl-ph.js": [
		297,
		0,
		138
	],
	"./tlh.js": [
		298,
		0,
		139
	],
	"./tr.js": [
		299,
		0,
		140
	],
	"./tzl.js": [
		300,
		0,
		141
	],
	"./tzm-latn.js": [
		301,
		0,
		142
	],
	"./tzm.js": [
		302,
		0,
		143
	],
	"./ug-cn.js": [
		303,
		0,
		144
	],
	"./uk.js": [
		304,
		0,
		145
	],
	"./ur.js": [
		305,
		0,
		146
	],
	"./uz-latn.js": [
		306,
		0,
		147
	],
	"./uz.js": [
		307,
		0,
		148
	],
	"./vi.js": [
		308,
		0,
		149
	],
	"./x-pseudo.js": [
		309,
		0,
		150
	],
	"./yo.js": [
		310,
		0,
		151
	],
	"./zh-cn.js": [
		311,
		0,
		152
	],
	"./zh-hk.js": [
		312,
		0,
		153
	],
	"./zh-mo.js": [
		313,
		0,
		154
	],
	"./zh-tw.js": [
		314,
		0,
		155
	]
};
function webpackAsyncContext(req) {
	if(!__webpack_require__.o(map, req)) {
		return Promise.resolve().then(function() {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}

	var ids = map[req], id = ids[0];
	return Promise.all(ids.slice(1).map(__webpack_require__.e)).then(function() {
		return __webpack_require__.t(id, 7);
	});
}
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = 105;
module.exports = webpackAsyncContext;

/***/ }),

/***/ 106:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(2);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(6);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(4);
function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }






var log = _core_logging__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].getLogger("depends");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"]("depends");
parser.addArgument("condition");
parser.addArgument("action", "show", ["show", "enable", "both"]);
parser.addArgument("transition", "none", ["none", "css", "fade", "slide"]);
parser.addArgument("effect-duration", "fast");
parser.addArgument("effect-easing", "swing");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].extend({
  name: "depends",
  trigger: ".pat-depends",
  jquery_plugin: true,
  init: function init($el, opts) {
    var _this = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var DependsHandler, dependent, options, handler, state, data, _iterator, _step, input, $form, dependents;

      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              _context.next = 2;
              return __webpack_require__.e(/* import() */ 18).then(__webpack_require__.bind(null, 316));

            case 2:
              DependsHandler = _context.sent.default;
              // prettier-ignore
              dependent = _this.$el[0];
              options = parser.parse(_this.$el, opts);
              _this.$modal = _this.$el.parents(".pat-modal");
              _context.prev = 6;
              handler = new DependsHandler(_this.$el, options.condition);
              _context.next = 14;
              break;

            case 10:
              _context.prev = 10;
              _context.t0 = _context["catch"](6);
              log.error("Invalid condition: " + _context.t0.message, dependent);
              return _context.abrupt("return");

            case 14:
              state = handler.evaluate();
              _context.t1 = options.action;
              _context.next = _context.t1 === "show" ? 18 : _context.t1 === "enable" ? 21 : _context.t1 === "both" ? 23 : 25;
              break;

            case 18:
              _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].hideOrShow($el, state, options, _this.name);

              _this.updateModal();

              return _context.abrupt("break", 25);

            case 21:
              if (state) _this.enable();else _this.disable();
              return _context.abrupt("break", 25);

            case 23:
              if (state) {
                _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].hideOrShow($el, state, options, _this.name);

                _this.updateModal();

                _this.enable();
              } else {
                _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].hideOrShow($el, state, options, _this.name);

                _this.updateModal();

                _this.disable();
              }

              return _context.abrupt("break", 25);

            case 25:
              data = {
                handler: handler,
                options: options,
                dependent: dependent
              };
              _iterator = _createForOfIteratorHelper(handler.getAllInputs());

              try {
                for (_iterator.s(); !(_step = _iterator.n()).done;) {
                  input = _step.value;

                  if (input.form) {
                    $form = jquery__WEBPACK_IMPORTED_MODULE_0___default()(input.form);
                    dependents = $form.data("patDepends.dependents");

                    if (!dependents) {
                      dependents = [data];
                      $form.on("reset.pat-depends", function () {
                        return _this.onReset;
                      });
                    } else if (dependents.indexOf(data) === -1) dependents.push(data);

                    $form.data("patDepends.dependents", dependents);
                  }

                  jquery__WEBPACK_IMPORTED_MODULE_0___default()(input).on("change.pat-depends", null, data, _this.onChange.bind(_this));
                  jquery__WEBPACK_IMPORTED_MODULE_0___default()(input).on("keyup.pat-depends", null, data, _this.onChange.bind(_this));
                }
              } catch (err) {
                _iterator.e(err);
              } finally {
                _iterator.f();
              }

            case 28:
            case "end":
              return _context.stop();
          }
        }
      }, _callee, null, [[6, 10]]);
    }))();
  },
  onReset: function onReset(event) {
    var _this2 = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
      var dependents, _iterator2, _step2, dependent;

      return regeneratorRuntime.wrap(function _callee2$(_context2) {
        while (1) {
          switch (_context2.prev = _context2.next) {
            case 0:
              dependents = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.target).data("patDepends.dependents");
              _context2.next = 3;
              return _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].timeout(50);

            case 3:
              _iterator2 = _createForOfIteratorHelper(dependents);

              try {
                for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
                  dependent = _step2.value;
                  event.data = dependent;

                  _this2.onChange(event);
                }
              } catch (err) {
                _iterator2.e(err);
              } finally {
                _iterator2.f();
              }

            case 5:
            case "end":
              return _context2.stop();
          }
        }
      }, _callee2);
    }))();
  },
  updateModal: function updateModal() {
    // If we're in a modal, make sure that it gets resized.
    if (this.$modal.length) {
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).trigger("pat-update", {
        pattern: "depends"
      });
    }
  },
  enable: function enable() {
    if (this.$el.is(":input")) {
      this.$el[0].disabled = null;
    } else if (this.$el.is("a")) {
      this.$el.off("click.patternDepends");
    }

    if (this.$el.hasClass("pat-autosuggest")) {
      this.$el.findInclusive("input.pat-autosuggest").trigger("pat-update", {
        pattern: "depends",
        enabled: true
      });
    }

    this.$el.removeClass("disabled");
  },
  disable: function disable() {
    if (this.$el.is(":input")) {
      this.$el[0].disabled = "disabled";
    } else if (this.$el.is("a")) {
      this.$el.on("click.patternDepends", function (e) {
        return e.preventDefault();
      });
    }

    if (this.$el.hasClass("pat-autosuggest")) {
      this.$el.findInclusive("input.pat-autosuggest").trigger("pat-update", {
        pattern: "depends",
        enabled: false
      });
    }

    this.$el.addClass("disabled");
  },
  onChange: function onChange(event) {
    var handler = event.data.handler;
    var options = event.data.options;
    var dependent = event.data.dependent;
    var $depdendent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dependent);
    var state = handler.evaluate();

    switch (options.action) {
      case "show":
        _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].hideOrShow($depdendent, state, options, this.name);
        this.updateModal();
        break;

      case "enable":
        if (state) {
          this.enable();
        } else {
          this.disable();
        }

        break;

      case "both":
        _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].hideOrShow($depdendent, state, options, this.name);
        this.updateModal();

        if (state) {
          this.enable();
        } else {
          this.disable();
        }

        break;
    }
  }
}));

/***/ }),

/***/ 107:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(19);
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _core_registry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(9);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(4);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(2);
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

/**
 * equaliser - Equalise height of elements in a row
 *
 * Copyright 2013 Simplon B.V. - Wichert Akkerman
 */
 // needed for ``await`` support





var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"]("equaliser");
parser.addArgument("transition", "none", ["none", "grow"]);
parser.addArgument("effect-duration", "fast");
parser.addArgument("effect-easing", "swing");
var equaliser = {
  name: "equaliser",
  trigger: ".pat-equaliser, .pat-equalizer",
  init: function init($el, opts) {
    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var ImagesLoaded;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              _context.next = 2;
              return __webpack_require__.e(/* import() */ 1).then(__webpack_require__.t.bind(null, 97, 7));

            case 2:
              ImagesLoaded = _context.sent.default;
              return _context.abrupt("return", $el.each(function () {
                var $container = jquery__WEBPACK_IMPORTED_MODULE_1___default()(this),
                    options = parser.parse($container, opts);
                $container.data("pat-equaliser", options);
                /* Assumotion, we don't need this anymore if we use Mutation observers
                // $container.on("pat-update.pat-equaliser", null, this, utils.debounce(equaliser._onEvent, 100));
                // $container.on("patterns-injected.pat-equaliser", null, this, utils.debounce(equaliser._onEvent, 100));
                // $container.parents('.pat-stacks').on("pat-update", null, this, utils.debounce(equaliser._onEvent, 100));
                */

                jquery__WEBPACK_IMPORTED_MODULE_1___default()(window).on("resize.pat-equaliser", null, this, _core_utils__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].debounce(equaliser._onEvent, 100));
                ImagesLoaded(this, jquery__WEBPACK_IMPORTED_MODULE_1___default.a.proxy(function () {
                  equaliser._update(this);
                }, this));
                var callback = _core_utils__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].debounce(equaliser._update.bind(this), 100);
                var observer = new MutationObserver(callback);
                var config = {
                  childList: true,
                  subtree: true,
                  characterData: true,
                  attributes: true
                };
                observer.observe(document.body, config);
              }));

            case 4:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }))();
  },
  _update: function _update(container) {
    var $container = jquery__WEBPACK_IMPORTED_MODULE_1___default()(container),
        options = $container.data("pat-equaliser"),
        $children = $container.children(),
        max_height = 0;

    for (var i = 0; i < $children.length; i++) {
      var $child = $children.eq(i),
          css = $child.css("height"),
          height;
      $child.css("height", "").removeClass("equalised");
      height = $child.height();
      if (height > max_height) max_height = height;
      if (css) $child.css("height", css);
    }

    var new_css = {
      height: max_height + "px"
    };

    switch (options && options.transition) {
      case "none":
        $children.css(new_css).addClass("equalised");
        break;

      case "grow":
        $children.animate(new_css, options.effect.duration, options.effect.easing, function () {
          jquery__WEBPACK_IMPORTED_MODULE_1___default()(this).addClass("equalised");
        });
        break;
    }

    $container.trigger("pat-update", {
      pattern: "equaliser"
    });
  },
  _onEvent: function _onEvent(event) {
    if (typeof event.data !== "undefined") {
      equaliser._update(event.data);
    }
  }
};
_core_registry__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].register(equaliser);
/* unused harmony default export */ var _unused_webpack_default_export = (equaliser);

/***/ }),

/***/ 108:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_registry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(9);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(2);
/* harmony import */ var _core_dom__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(11);
function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }





var legend = {
  name: "legend",
  trigger: "legend",
  _convertToIframes: function _convertToIframes($root) {
    $root.findInclusive("object[type='text/html']").each(function () {
      var $object = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
          $iframe = jquery__WEBPACK_IMPORTED_MODULE_0___default()("<iframe allowtransparency='true'/>");
      $iframe.attr("id", $object.attr("id")).attr("class", $object.attr("class")).attr("src", $object.attr("data")).attr("frameborder", "0").attr("style", "background-color:transparent");
      $object.replaceWith($iframe);
    });
  },
  transform: function transform($root) {
    var root = _core_utils__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].jqToNode($root);
    var all = _core_dom__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].querySelectorAllAndMe(root, "legend:not(.cant-touch-this)");

    var _iterator = _createForOfIteratorHelper(all),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var el = _step.value;
        jquery__WEBPACK_IMPORTED_MODULE_0___default()(el).replaceWith("<p class='legend'>" + jquery__WEBPACK_IMPORTED_MODULE_0___default()(el).html() + "</p>");
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }
  }
};
_core_registry__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].register(legend);
/* unused harmony default export */ var _unused_webpack_default_export = (legend);

/***/ }),

/***/ 109:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(19);
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(4);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(5);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(2);
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

/**
 * Patternslib pattern for Masonry
 * Copyright 2015 Syslab.com GmBH
 */
 // needed for ``await`` support





 // Lazy loading modules.

var Masonry;
var log = _core_logging__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].getLogger("pat.masonry");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"]("masonry"); // parser.addArgument("stagger", "");

parser.addArgument("column-width");
parser.addArgument("container-style", '{ "position": "relative" }');
parser.addArgument("gutter");
parser.addArgument("is-fit-width", false);
parser.addArgument("is-horizontal-order", false); // preserve horizontal order.

parser.addArgument("is-origin-left", true);
parser.addArgument("is-origin-top", true);
parser.addArgument("is-percent-position", false); // set item positions in percent values. items will not transition on resize.

parser.addArgument("is-resize", true); // adjust sizes and position on resize.

parser.addArgument("item-selector", ".item");
parser.addArgument("stamp", "");
parser.addArgument("transition-duration", "0.4s"); // is-* are masonry v3 options, here we add v4 style names.
// we keep the is-* as there is special support with options parsing.

parser.addAlias("fit-width", "is-fit-width");
parser.addAlias("origin-left", "is-origin-left");
parser.addAlias("origin-top", "is-origin-top");
parser.addAlias("horizontal-order", "is-horizontal-order");
parser.addAlias("percent-position", "is-percent-position");
parser.addAlias("resize", "is-resize");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].extend({
  name: "masonry",
  trigger: ".pat-masonry",
  init: function init($el, opts) {
    var _this = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var ImagesLoaded, imgLoad, callback, observer, config;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              _context.next = 2;
              return __webpack_require__.e(/* import() */ 11).then(__webpack_require__.t.bind(null, 315, 7));

            case 2:
              Masonry = _context.sent.default;
              _context.next = 5;
              return __webpack_require__.e(/* import() */ 1).then(__webpack_require__.t.bind(null, 97, 7));

            case 5:
              ImagesLoaded = _context.sent.default;
              _this.options = parser.parse(_this.$el, opts); // Initialize

              _this.initMasonry();

              _context.next = 10;
              return ImagesLoaded(_this.$el);

            case 10:
              imgLoad = _context.sent;
              imgLoad.on("progress", function () {
                if (!this.msnry) {
                  this.initMasonry();
                }

                this.quicklayout();
              }.bind(_this));
              imgLoad.on("always", function () {
                if (!this.msnry) {
                  this.initMasonry();
                }

                this.layout();
              }.bind(_this)); // Update if something gets injected inside the pat-masonry

              _this.$el.on("patterns-injected.pat-masonry", _core_utils__WEBPACK_IMPORTED_MODULE_5__[/* default */ "a"].debounce(_this.update.bind(_this), 100)).on("pat-update", _core_utils__WEBPACK_IMPORTED_MODULE_5__[/* default */ "a"].debounce(_this.quicklayout.bind(_this), 200));

              callback = _core_utils__WEBPACK_IMPORTED_MODULE_5__[/* default */ "a"].debounce(_this.quicklayout.bind(_this), 400);
              observer = new MutationObserver(callback);
              /* Explicitly not including style. We assume style is set dynamically only by scripts and we do all our controlled changes through classes.
                 That way we avoid masonry to react on its own style calculation */

              config = {
                childList: true,
                subtree: true,
                characterData: false,
                attributeOldValue: true,
                attributes: true,
                attributeFilter: ["class"]
              };
              observer.observe(document.body, config);

            case 18:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }))();
  },
  initMasonry: function initMasonry() {
    var _this2 = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
      var containerStyle;
      return regeneratorRuntime.wrap(function _callee2$(_context2) {
        while (1) {
          switch (_context2.prev = _context2.next) {
            case 0:
              try {
                containerStyle = JSON.parse(_this2.options.containerStyle);
              } catch (e) {
                containerStyle = {
                  position: "relative"
                };
                log.warn("Invalid value passed in as containerStyle. Needs to " + "be valid JSON so that it can be converted to an object for Masonry.");
              }

              _this2.msnry = new Masonry(_this2.$el[0], {
                columnWidth: _this2.getTypeCastedValue(_this2.options.columnWidth),
                containerStyle: containerStyle,
                fitWidth: _this2.options.is["fit-width"],
                gutter: _this2.getTypeCastedValue(_this2.options.gutter),
                horizontalOrder: _this2.options.is["horizontal-order"],
                initLayout: false,
                itemSelector: _this2.options.itemSelector,
                originLeft: _this2.options.is["origin-left"],
                originTop: _this2.options.is["origin-top"],
                percentPosition: _this2.options.is["percent-position"],
                resize: _this2.options.is["resize"],
                stamp: _this2.options.stamp,
                transitionDuration: _this2.options.transitionDuration
              });

            case 2:
            case "end":
              return _context2.stop();
          }
        }
      }, _callee2);
    }))();
  },
  update: function update() {
    this.msnry.remove();
    this.initMasonry();
    this.layout();
  },
  quicklayout: function quicklayout() {
    if (!this.msnry) {
      // Not initialized yet
      return;
    } // call masonry layout on the children before calling it on this element


    this.$el.find(".pat-masonry").each(function (idx, child) {
      jquery__WEBPACK_IMPORTED_MODULE_1___default()(child).patMasonry("quicklayout");
    });
    this.msnry.layout();
  },
  layout: function layout() {
    this.$el.removeClass("masonry-ready");
    this.msnry.on("layoutComplete", function () {
      this.$el.addClass("masonry-ready");
    }.bind(this));
    this.msnry.layout();
    this.quicklayout();
  },
  getTypeCastedValue: function getTypeCastedValue(original) {
    var val = Number(original);
    return isNaN(val) ? original || 0 : val;
  }
}));

/***/ }),

/***/ 11:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

/* Utilities for DOM traversal or navigation */
var DATA_STYLE_DISPLAY = "__patternslib__style__display";

var toNodeArray = function toNodeArray(nodes) {
  // Return an array of DOM nodes
  if (nodes.jquery || nodes instanceof NodeList) {
    // jQuery or document.querySelectorAll
    nodes = _toConsumableArray(nodes);
  } else if (nodes instanceof Array === false) {
    nodes = [nodes];
  }

  return nodes;
};

var querySelectorAllAndMe = function querySelectorAllAndMe(el, selector) {
  // Like querySelectorAll but including the element where it starts from.
  // Returns an Array, not a NodeList
  var all = _toConsumableArray(el.querySelectorAll(selector));

  if (el.matches(selector)) {
    all.unshift(el); // start element should be first.
  }

  return all;
};

var wrap = function wrap(el, wrapper) {
  // Wrap a element with a wrapper element.
  // See: https://stackoverflow.com/a/13169465/1337474
  el.parentNode.insertBefore(wrapper, el);
  wrapper.appendChild(el);
};

var hide = function hide(el) {
  // Hides the element with ``display: none``
  if (el.style.display === "none") {
    // Nothing to do.
    return;
  }

  if (el.style.display) {
    el[DATA_STYLE_DISPLAY] = el.style.display;
  }

  el.style.display = "none";
};

var show = function show(el) {
  // Shows element by removing ``display: none`` and restoring the display
  // value to whatever it was before.
  var val = el[DATA_STYLE_DISPLAY] || null;
  el.style.display = val;
  delete el[DATA_STYLE_DISPLAY];
};

var find_parents = function find_parents(el, selector) {
  var _el$parentNode, _el$parentNode$closes;

  // Return all direct parents of ``el`` matching ``selector``.
  // This matches against all parents but not the element itself.
  // The order of elements is from the search starting point up to higher
  // DOM levels.
  var ret = [];
  var parent = el === null || el === void 0 ? void 0 : (_el$parentNode = el.parentNode) === null || _el$parentNode === void 0 ? void 0 : (_el$parentNode$closes = _el$parentNode.closest) === null || _el$parentNode$closes === void 0 ? void 0 : _el$parentNode$closes.call(_el$parentNode, selector);

  while (parent) {
    var _parent$parentNode, _parent$parentNode$cl;

    ret.push(parent);
    parent = (_parent$parentNode = parent.parentNode) === null || _parent$parentNode === void 0 ? void 0 : (_parent$parentNode$cl = _parent$parentNode.closest) === null || _parent$parentNode$cl === void 0 ? void 0 : _parent$parentNode$cl.call(_parent$parentNode, selector);
  }

  return ret;
};

var find_scoped = function find_scoped(el, selector) {
  // If the selector starts with an object id do a global search,
  // otherwise do a local search.
  return (selector.indexOf("#") === 0 ? document : el).querySelectorAll(selector);
};

var get_parents = function get_parents(el) {
  // Return all HTMLElement parents of el, starting from the direct parent of el.
  // The document itself is excluded because it's not a real DOM node.
  var parents = [];
  var parent = el === null || el === void 0 ? void 0 : el.parentNode;

  while (parent) {
    var _parent;

    parents.push(parent);
    parent = (_parent = parent) === null || _parent === void 0 ? void 0 : _parent.parentNode;
    parent = parent instanceof HTMLElement ? parent : null;
  }

  return parents;
};

var is_visible = function is_visible(el) {
  // Check, if element is visible in DOM.
  // https://stackoverflow.com/a/19808107/1337474
  return el.offsetWidth > 0 && el.offsetHeight > 0;
};

var create_from_string = function create_from_string(string) {
  // Create a DOM element from a string.
  var div = document.createElement("div");
  div.innerHTML = string.trim();
  return div.firstChild;
};

var dom = {
  toNodeArray: toNodeArray,
  querySelectorAllAndMe: querySelectorAllAndMe,
  wrap: wrap,
  hide: hide,
  show: show,
  find_parents: find_parents,
  find_scoped: find_scoped,
  get_parents: get_parents,
  is_visible: is_visible,
  create_from_string: create_from_string
};
/* harmony default export */ __webpack_exports__["a"] = (dom);

/***/ }),

/***/ 110:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(4);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(6);




var log = _core_logging__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].getLogger("navigation");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"]("navigation");
parser.addArgument("item-wrapper", "li");
parser.addArgument("in-path-class", "navigation-in-path");
parser.addArgument("current-class", "current");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].extend({
  name: "navigation",
  trigger: "nav, .navigation, .pat-navigation",
  init: function init($el, opts) {
    this.options = parser.parse($el, opts);
    var current = this.options.currentClass; // check whether to load

    if ($el.hasClass("navigation-load-current")) {
      $el.find("a." + current, "." + current + " a").click(); // check for current elements injected here

      $el.on("patterns-injected-scanned", function (ev) {
        var $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target);
        if ($target.is("a." + current)) $target.click();
        if ($target.is("." + current)) $target.find("a").click();

        this._updatenavpath($el);
      }.bind(this));
    } // An anchor within this navigation triggered injection


    $el.on("patterns-inject-triggered", "a", function (ev) {
      var $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target); // remove all set current classes

      $el.find("." + current).removeClass(current); // set current class on target

      $target.addClass(current); // If target's parent is an LI, also set current class there

      $target.parents(this.options.itemWrapper).first().addClass(current);

      this._updatenavpath($el);
    }.bind(this));
    var observer = new MutationObserver(this._initialSet.bind(this));
    observer.observe($el[0], {
      childList: true,
      subtree: true,
      attributes: false,
      characterData: false
    });

    this._initialSet();
  },
  _initialSet: function _initialSet() {
    var $el = this.$el;
    var current = this.options.currentClass; // Set current class if it is not set

    if ($el[0].querySelectorAll("." + current).length === 0) {
      var ael = $el[0].querySelectorAll("a");

      for (var cnt = 0; cnt < ael.length; cnt++) {
        var $a = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ael[cnt]),
            $li = $a.parents(this.options.itemWrapper).first(),
            url = $a.attr("href"),
            path;

        if (typeof url === "undefined") {
          return;
        }

        path = this._pathfromurl(url);
        log.debug("checking url:", url, "extracted path:", path);

        if (this._match(window.location.pathname, path)) {
          log.debug("found match", $li);
          $a.addClass(current);
          $li.addClass(current);
        }
      }
    } // Set current class on item-wrapper, if not set.


    if (this.options.itemWrapper && $el[0].querySelectorAll("." + current).length > 0 && $el[0].querySelectorAll(this.options.itemWrapper + "." + current).length === 0) {
      jquery__WEBPACK_IMPORTED_MODULE_0___default()("." + current, $el).parents(this.options.itemWrapper).first().addClass(current);
    }

    this._updatenavpath($el);
  },
  _updatenavpath: function _updatenavpath($el) {
    var in_path = this.options.inPathClass;

    if (!in_path) {
      return;
    }

    $el.find("." + in_path).removeClass(in_path);
    $el.find(this.options.itemWrapper + ":not(." + this.options.currentClass + "):has(." + this.options.currentClass + ")").addClass(in_path);
  },
  _match: function _match(curpath, path) {
    if (!path) {
      log.debug("path empty");
      return false;
    } // current path needs to end in the anchor's path


    if (path !== curpath.slice(-path.length)) {
      log.debug(curpath, "does not end in", path);
      return false;
    } // XXX: we might need more exclusion tests


    return true;
  },
  _pathfromurl: function _pathfromurl(url) {
    var path = url.split("#")[0].split("://");

    if (path.length > 2) {
      log.error("weird url", url);
      return "";
    }

    if (path.length === 1) return path[0];
    return path[1].split("/").slice(1).join("/");
  }
}));

/***/ }),

/***/ 111:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(4);



var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"]("sortable");
parser.addArgument("selector", "li");
parser.addArgument("drag-class", "dragged"); // Class to apply to item that is being dragged.

parser.addArgument("drop"); // Callback function for when item is dropped (null)
// BBB for the mockup sortable pattern.

parser.addAlias("dragClass", "drag-class");
/* unused harmony default export */ var _unused_webpack_default_export = (_core_base__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].extend({
  name: "sortable",
  trigger: ".pat-sortable",
  init: function init() {
    this.$form = this.$el.closest("form");
    this.options = parser.parse(this.$el, false);
    this.recordPositions().addHandles().initScrolling();
    this.$el.on("pat-update", this.onPatternUpdate.bind(this));
  },
  onPatternUpdate: function onPatternUpdate(ev, data) {
    /* Handler which gets called when pat-update is triggered within
     * the .pat-sortable element.
     */
    if (data.pattern == "clone") {
      this.recordPositions();
      data.$el.on("dragstart", this.onDragStart.bind(this));
      data.$el.on("dragend", this.onDragEnd.bind(this));
    }

    return true;
  },
  recordPositions: function recordPositions() {
    // use only direct descendants to support nested lists
    this.$sortables = this.$el.children().filter(this.options.selector);
    this.$sortables.each(function (idx) {
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).data("patterns.sortable", {
        position: idx
      });
    });
    return this;
  },
  addHandles: function addHandles() {
    /* Add handles and make them draggable for HTML5 and IE8/9
     * it has to be an "a" tag (or img) to make it draggable in IE8/9
     */
    var $sortables_without_handles = this.$sortables.filter(function () {
      return jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).find(".sortable-handle").length === 0;
    });
    var $handles = jquery__WEBPACK_IMPORTED_MODULE_0___default()('<a href="#" class="sortable-handle">⇕</a>').appendTo($sortables_without_handles);

    if ("draggable" in document.createElement("span")) {
      $handles.attr("draggable", true);
    } else {
      $handles.on("selectstart", function (ev) {
        ev.preventDefault();
      });
    }

    $handles.on("dragstart", this.onDragStart.bind(this));
    $handles.on("dragend", this.onDragEnd.bind(this));
    return this;
  },
  initScrolling: function initScrolling() {
    // invisible scroll activation areas
    var scrollup = jquery__WEBPACK_IMPORTED_MODULE_0___default()('<div id="pat-scroll-up">&nbsp;</div>'),
        scrolldn = jquery__WEBPACK_IMPORTED_MODULE_0___default()('<div id="pat-scroll-dn">&nbsp;</div>'),
        scroll = jquery__WEBPACK_IMPORTED_MODULE_0___default()().add(scrollup).add(scrolldn);
    scrollup.css({
      top: 0
    });
    scrolldn.css({
      bottom: 0
    });
    scroll.css({
      position: "fixed",
      zIndex: 999999,
      height: 32,
      left: 0,
      right: 0
    });
    scroll.on("dragover", function (ev) {
      ev.preventDefault();

      if (jquery__WEBPACK_IMPORTED_MODULE_0___default()("html,body").is(":animated")) {
        return;
      }

      var newpos = jquery__WEBPACK_IMPORTED_MODULE_0___default()(window).scrollTop() + (jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).attr("id") === "pat-scroll-up" ? -32 : 32);
      jquery__WEBPACK_IMPORTED_MODULE_0___default()("html,body").animate({
        scrollTop: newpos
      }, 50, "linear");
    });
    return this;
  },
  onDragEnd: function onDragEnd(ev) {
    var $dragged = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target).parent();
    $dragged.removeClass(this.options.dragClass);
    this.$sortables.off(".pat-sortable");
    this.$el.off(".pat-sortable");
    jquery__WEBPACK_IMPORTED_MODULE_0___default()("#pat-scroll-up, #pat-scroll-dn").detach();
    var change = this.submitChangedAmount(jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target).closest(".sortable")); // Call the optionally passed-in callback function

    if (this.options.drop) {
      this.options.drop($dragged, change);
    }
  },
  submitChangedAmount: function submitChangedAmount($dragged) {
    /* If we are in a form, then submit the form with the right amount
     * that the sortable element was moved up or down.
     */
    var $amount_input = this.$form.find(".sortable-amount");

    if ($amount_input.length === 0) {
      return;
    }

    var old_position = $dragged.data("patterns.sortable").position;
    this.recordPositions();
    var new_position = $dragged.data("patterns.sortable").position;
    var change = Math.abs(new_position - old_position);
    var direction = new_position > old_position && "down" || "up";

    if (this.$form.length > 0) {
      $amount_input.val(change);

      if (direction == "up") {
        $dragged.find(".sortable-button-up").click();
      } else {
        $dragged.find(".sortable-button-down").click();
      }
    }

    return change;
  },
  onDragStart: function onDragStart(ev) {
    var $handle = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target),
        $dragged = $handle.parent(),
        that = this;

    if (typeof ev.originalEvent !== "undefined") {
      // Firefox seems to need this set to any value
      ev.originalEvent.dataTransfer.setData("Text", "");
      ev.originalEvent.dataTransfer.effectAllowed = ["move"];

      if ("setDragImage" in ev.originalEvent.dataTransfer) {
        ev.originalEvent.dataTransfer.setDragImage($dragged[0], 0, 0);
      }
    }

    $dragged.addClass(this.options.dragClass); // Scroll the list if near the borders

    this.$el.on("dragover.pat-sortable", function (ev) {
      ev.preventDefault();
      if (this.$el.is(":animated")) return;
      var pos = ev.originalEvent.clientY + jquery__WEBPACK_IMPORTED_MODULE_0___default()("body").scrollTop();
      if (pos - this.$el.safeOffset().top < 32) this.$el.animate({
        scrollTop: this.$el.scrollTop() - 32
      }, 50, "linear");else if (this.$el.safeOffset().top + this.$el.height() - pos < 32) this.$el.animate({
        scrollTop: this.$el.scrollTop() + 32
      }, 50, "linear");
    }.bind(this));
    this.$sortables.on("dragover.pat-sortable", function (ev) {
      // list elements are only drop targets when one element of the
      // list is being dragged. avoids dragging between lists.
      var $dropTarget = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target).closest(that.options.selector),
          midlineY = $dropTarget.safeOffset().top - jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).scrollTop() + $dropTarget.height() / 2;

      if ($dropTarget.is($dragged)) {
        return;
      }

      $dropTarget.removeClass("drop-target-above drop-target-below");
      if (ev.originalEvent.clientY > midlineY) $dropTarget.addClass("drop-target-below");else $dropTarget.addClass("drop-target-above");
      ev.preventDefault();
    }.bind(this));
    this.$sortables.on("dragleave.pat-sortable", function () {
      this.$sortables.removeClass("drop-target-above drop-target-below");
    }.bind(this));
    this.$sortables.on("drop.pat-sortable", function (ev) {
      var $dropTarget = jquery__WEBPACK_IMPORTED_MODULE_0___default()(ev.target).closest(that.options.selector);

      if ($dropTarget.is($dragged)) {
        return;
      }

      if ($dropTarget.hasClass("drop-target-below")) {
        $dropTarget.after($dragged);
      } else {
        $dropTarget.before($dragged);
      }

      $dropTarget.removeClass("drop-target-above drop-target-below");
      ev.preventDefault();
    });
  }
}));

/***/ }),

/***/ 19:
/***/ (function(module, exports, __webpack_require__) {

/**
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

var runtime = (function (exports) {
  "use strict";

  var Op = Object.prototype;
  var hasOwn = Op.hasOwnProperty;
  var undefined; // More compressible than void 0.
  var $Symbol = typeof Symbol === "function" ? Symbol : {};
  var iteratorSymbol = $Symbol.iterator || "@@iterator";
  var asyncIteratorSymbol = $Symbol.asyncIterator || "@@asyncIterator";
  var toStringTagSymbol = $Symbol.toStringTag || "@@toStringTag";

  function define(obj, key, value) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
    return obj[key];
  }
  try {
    // IE 8 has a broken Object.defineProperty that only works on DOM objects.
    define({}, "");
  } catch (err) {
    define = function(obj, key, value) {
      return obj[key] = value;
    };
  }

  function wrap(innerFn, outerFn, self, tryLocsList) {
    // If outerFn provided and outerFn.prototype is a Generator, then outerFn.prototype instanceof Generator.
    var protoGenerator = outerFn && outerFn.prototype instanceof Generator ? outerFn : Generator;
    var generator = Object.create(protoGenerator.prototype);
    var context = new Context(tryLocsList || []);

    // The ._invoke method unifies the implementations of the .next,
    // .throw, and .return methods.
    generator._invoke = makeInvokeMethod(innerFn, self, context);

    return generator;
  }
  exports.wrap = wrap;

  // Try/catch helper to minimize deoptimizations. Returns a completion
  // record like context.tryEntries[i].completion. This interface could
  // have been (and was previously) designed to take a closure to be
  // invoked without arguments, but in all the cases we care about we
  // already have an existing method we want to call, so there's no need
  // to create a new function object. We can even get away with assuming
  // the method takes exactly one argument, since that happens to be true
  // in every case, so we don't have to touch the arguments object. The
  // only additional allocation required is the completion record, which
  // has a stable shape and so hopefully should be cheap to allocate.
  function tryCatch(fn, obj, arg) {
    try {
      return { type: "normal", arg: fn.call(obj, arg) };
    } catch (err) {
      return { type: "throw", arg: err };
    }
  }

  var GenStateSuspendedStart = "suspendedStart";
  var GenStateSuspendedYield = "suspendedYield";
  var GenStateExecuting = "executing";
  var GenStateCompleted = "completed";

  // Returning this object from the innerFn has the same effect as
  // breaking out of the dispatch switch statement.
  var ContinueSentinel = {};

  // Dummy constructor functions that we use as the .constructor and
  // .constructor.prototype properties for functions that return Generator
  // objects. For full spec compliance, you may wish to configure your
  // minifier not to mangle the names of these two functions.
  function Generator() {}
  function GeneratorFunction() {}
  function GeneratorFunctionPrototype() {}

  // This is a polyfill for %IteratorPrototype% for environments that
  // don't natively support it.
  var IteratorPrototype = {};
  IteratorPrototype[iteratorSymbol] = function () {
    return this;
  };

  var getProto = Object.getPrototypeOf;
  var NativeIteratorPrototype = getProto && getProto(getProto(values([])));
  if (NativeIteratorPrototype &&
      NativeIteratorPrototype !== Op &&
      hasOwn.call(NativeIteratorPrototype, iteratorSymbol)) {
    // This environment has a native %IteratorPrototype%; use it instead
    // of the polyfill.
    IteratorPrototype = NativeIteratorPrototype;
  }

  var Gp = GeneratorFunctionPrototype.prototype =
    Generator.prototype = Object.create(IteratorPrototype);
  GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
  GeneratorFunctionPrototype.constructor = GeneratorFunction;
  GeneratorFunction.displayName = define(
    GeneratorFunctionPrototype,
    toStringTagSymbol,
    "GeneratorFunction"
  );

  // Helper for defining the .next, .throw, and .return methods of the
  // Iterator interface in terms of a single ._invoke method.
  function defineIteratorMethods(prototype) {
    ["next", "throw", "return"].forEach(function(method) {
      define(prototype, method, function(arg) {
        return this._invoke(method, arg);
      });
    });
  }

  exports.isGeneratorFunction = function(genFun) {
    var ctor = typeof genFun === "function" && genFun.constructor;
    return ctor
      ? ctor === GeneratorFunction ||
        // For the native GeneratorFunction constructor, the best we can
        // do is to check its .name property.
        (ctor.displayName || ctor.name) === "GeneratorFunction"
      : false;
  };

  exports.mark = function(genFun) {
    if (Object.setPrototypeOf) {
      Object.setPrototypeOf(genFun, GeneratorFunctionPrototype);
    } else {
      genFun.__proto__ = GeneratorFunctionPrototype;
      define(genFun, toStringTagSymbol, "GeneratorFunction");
    }
    genFun.prototype = Object.create(Gp);
    return genFun;
  };

  // Within the body of any async function, `await x` is transformed to
  // `yield regeneratorRuntime.awrap(x)`, so that the runtime can test
  // `hasOwn.call(value, "__await")` to determine if the yielded value is
  // meant to be awaited.
  exports.awrap = function(arg) {
    return { __await: arg };
  };

  function AsyncIterator(generator, PromiseImpl) {
    function invoke(method, arg, resolve, reject) {
      var record = tryCatch(generator[method], generator, arg);
      if (record.type === "throw") {
        reject(record.arg);
      } else {
        var result = record.arg;
        var value = result.value;
        if (value &&
            typeof value === "object" &&
            hasOwn.call(value, "__await")) {
          return PromiseImpl.resolve(value.__await).then(function(value) {
            invoke("next", value, resolve, reject);
          }, function(err) {
            invoke("throw", err, resolve, reject);
          });
        }

        return PromiseImpl.resolve(value).then(function(unwrapped) {
          // When a yielded Promise is resolved, its final value becomes
          // the .value of the Promise<{value,done}> result for the
          // current iteration.
          result.value = unwrapped;
          resolve(result);
        }, function(error) {
          // If a rejected Promise was yielded, throw the rejection back
          // into the async generator function so it can be handled there.
          return invoke("throw", error, resolve, reject);
        });
      }
    }

    var previousPromise;

    function enqueue(method, arg) {
      function callInvokeWithMethodAndArg() {
        return new PromiseImpl(function(resolve, reject) {
          invoke(method, arg, resolve, reject);
        });
      }

      return previousPromise =
        // If enqueue has been called before, then we want to wait until
        // all previous Promises have been resolved before calling invoke,
        // so that results are always delivered in the correct order. If
        // enqueue has not been called before, then it is important to
        // call invoke immediately, without waiting on a callback to fire,
        // so that the async generator function has the opportunity to do
        // any necessary setup in a predictable way. This predictability
        // is why the Promise constructor synchronously invokes its
        // executor callback, and why async functions synchronously
        // execute code before the first await. Since we implement simple
        // async functions in terms of async generators, it is especially
        // important to get this right, even though it requires care.
        previousPromise ? previousPromise.then(
          callInvokeWithMethodAndArg,
          // Avoid propagating failures to Promises returned by later
          // invocations of the iterator.
          callInvokeWithMethodAndArg
        ) : callInvokeWithMethodAndArg();
    }

    // Define the unified helper method that is used to implement .next,
    // .throw, and .return (see defineIteratorMethods).
    this._invoke = enqueue;
  }

  defineIteratorMethods(AsyncIterator.prototype);
  AsyncIterator.prototype[asyncIteratorSymbol] = function () {
    return this;
  };
  exports.AsyncIterator = AsyncIterator;

  // Note that simple async functions are implemented on top of
  // AsyncIterator objects; they just return a Promise for the value of
  // the final result produced by the iterator.
  exports.async = function(innerFn, outerFn, self, tryLocsList, PromiseImpl) {
    if (PromiseImpl === void 0) PromiseImpl = Promise;

    var iter = new AsyncIterator(
      wrap(innerFn, outerFn, self, tryLocsList),
      PromiseImpl
    );

    return exports.isGeneratorFunction(outerFn)
      ? iter // If outerFn is a generator, return the full iterator.
      : iter.next().then(function(result) {
          return result.done ? result.value : iter.next();
        });
  };

  function makeInvokeMethod(innerFn, self, context) {
    var state = GenStateSuspendedStart;

    return function invoke(method, arg) {
      if (state === GenStateExecuting) {
        throw new Error("Generator is already running");
      }

      if (state === GenStateCompleted) {
        if (method === "throw") {
          throw arg;
        }

        // Be forgiving, per 25.3.3.3.3 of the spec:
        // https://people.mozilla.org/~jorendorff/es6-draft.html#sec-generatorresume
        return doneResult();
      }

      context.method = method;
      context.arg = arg;

      while (true) {
        var delegate = context.delegate;
        if (delegate) {
          var delegateResult = maybeInvokeDelegate(delegate, context);
          if (delegateResult) {
            if (delegateResult === ContinueSentinel) continue;
            return delegateResult;
          }
        }

        if (context.method === "next") {
          // Setting context._sent for legacy support of Babel's
          // function.sent implementation.
          context.sent = context._sent = context.arg;

        } else if (context.method === "throw") {
          if (state === GenStateSuspendedStart) {
            state = GenStateCompleted;
            throw context.arg;
          }

          context.dispatchException(context.arg);

        } else if (context.method === "return") {
          context.abrupt("return", context.arg);
        }

        state = GenStateExecuting;

        var record = tryCatch(innerFn, self, context);
        if (record.type === "normal") {
          // If an exception is thrown from innerFn, we leave state ===
          // GenStateExecuting and loop back for another invocation.
          state = context.done
            ? GenStateCompleted
            : GenStateSuspendedYield;

          if (record.arg === ContinueSentinel) {
            continue;
          }

          return {
            value: record.arg,
            done: context.done
          };

        } else if (record.type === "throw") {
          state = GenStateCompleted;
          // Dispatch the exception by looping back around to the
          // context.dispatchException(context.arg) call above.
          context.method = "throw";
          context.arg = record.arg;
        }
      }
    };
  }

  // Call delegate.iterator[context.method](context.arg) and handle the
  // result, either by returning a { value, done } result from the
  // delegate iterator, or by modifying context.method and context.arg,
  // setting context.delegate to null, and returning the ContinueSentinel.
  function maybeInvokeDelegate(delegate, context) {
    var method = delegate.iterator[context.method];
    if (method === undefined) {
      // A .throw or .return when the delegate iterator has no .throw
      // method always terminates the yield* loop.
      context.delegate = null;

      if (context.method === "throw") {
        // Note: ["return"] must be used for ES3 parsing compatibility.
        if (delegate.iterator["return"]) {
          // If the delegate iterator has a return method, give it a
          // chance to clean up.
          context.method = "return";
          context.arg = undefined;
          maybeInvokeDelegate(delegate, context);

          if (context.method === "throw") {
            // If maybeInvokeDelegate(context) changed context.method from
            // "return" to "throw", let that override the TypeError below.
            return ContinueSentinel;
          }
        }

        context.method = "throw";
        context.arg = new TypeError(
          "The iterator does not provide a 'throw' method");
      }

      return ContinueSentinel;
    }

    var record = tryCatch(method, delegate.iterator, context.arg);

    if (record.type === "throw") {
      context.method = "throw";
      context.arg = record.arg;
      context.delegate = null;
      return ContinueSentinel;
    }

    var info = record.arg;

    if (! info) {
      context.method = "throw";
      context.arg = new TypeError("iterator result is not an object");
      context.delegate = null;
      return ContinueSentinel;
    }

    if (info.done) {
      // Assign the result of the finished delegate to the temporary
      // variable specified by delegate.resultName (see delegateYield).
      context[delegate.resultName] = info.value;

      // Resume execution at the desired location (see delegateYield).
      context.next = delegate.nextLoc;

      // If context.method was "throw" but the delegate handled the
      // exception, let the outer generator proceed normally. If
      // context.method was "next", forget context.arg since it has been
      // "consumed" by the delegate iterator. If context.method was
      // "return", allow the original .return call to continue in the
      // outer generator.
      if (context.method !== "return") {
        context.method = "next";
        context.arg = undefined;
      }

    } else {
      // Re-yield the result returned by the delegate method.
      return info;
    }

    // The delegate iterator is finished, so forget it and continue with
    // the outer generator.
    context.delegate = null;
    return ContinueSentinel;
  }

  // Define Generator.prototype.{next,throw,return} in terms of the
  // unified ._invoke helper method.
  defineIteratorMethods(Gp);

  define(Gp, toStringTagSymbol, "Generator");

  // A Generator should always return itself as the iterator object when the
  // @@iterator function is called on it. Some browsers' implementations of the
  // iterator prototype chain incorrectly implement this, causing the Generator
  // object to not be returned from this call. This ensures that doesn't happen.
  // See https://github.com/facebook/regenerator/issues/274 for more details.
  Gp[iteratorSymbol] = function() {
    return this;
  };

  Gp.toString = function() {
    return "[object Generator]";
  };

  function pushTryEntry(locs) {
    var entry = { tryLoc: locs[0] };

    if (1 in locs) {
      entry.catchLoc = locs[1];
    }

    if (2 in locs) {
      entry.finallyLoc = locs[2];
      entry.afterLoc = locs[3];
    }

    this.tryEntries.push(entry);
  }

  function resetTryEntry(entry) {
    var record = entry.completion || {};
    record.type = "normal";
    delete record.arg;
    entry.completion = record;
  }

  function Context(tryLocsList) {
    // The root entry object (effectively a try statement without a catch
    // or a finally block) gives us a place to store values thrown from
    // locations where there is no enclosing try statement.
    this.tryEntries = [{ tryLoc: "root" }];
    tryLocsList.forEach(pushTryEntry, this);
    this.reset(true);
  }

  exports.keys = function(object) {
    var keys = [];
    for (var key in object) {
      keys.push(key);
    }
    keys.reverse();

    // Rather than returning an object with a next method, we keep
    // things simple and return the next function itself.
    return function next() {
      while (keys.length) {
        var key = keys.pop();
        if (key in object) {
          next.value = key;
          next.done = false;
          return next;
        }
      }

      // To avoid creating an additional object, we just hang the .value
      // and .done properties off the next function object itself. This
      // also ensures that the minifier will not anonymize the function.
      next.done = true;
      return next;
    };
  };

  function values(iterable) {
    if (iterable) {
      var iteratorMethod = iterable[iteratorSymbol];
      if (iteratorMethod) {
        return iteratorMethod.call(iterable);
      }

      if (typeof iterable.next === "function") {
        return iterable;
      }

      if (!isNaN(iterable.length)) {
        var i = -1, next = function next() {
          while (++i < iterable.length) {
            if (hasOwn.call(iterable, i)) {
              next.value = iterable[i];
              next.done = false;
              return next;
            }
          }

          next.value = undefined;
          next.done = true;

          return next;
        };

        return next.next = next;
      }
    }

    // Return an iterator with no values.
    return { next: doneResult };
  }
  exports.values = values;

  function doneResult() {
    return { value: undefined, done: true };
  }

  Context.prototype = {
    constructor: Context,

    reset: function(skipTempReset) {
      this.prev = 0;
      this.next = 0;
      // Resetting context._sent for legacy support of Babel's
      // function.sent implementation.
      this.sent = this._sent = undefined;
      this.done = false;
      this.delegate = null;

      this.method = "next";
      this.arg = undefined;

      this.tryEntries.forEach(resetTryEntry);

      if (!skipTempReset) {
        for (var name in this) {
          // Not sure about the optimal order of these conditions:
          if (name.charAt(0) === "t" &&
              hasOwn.call(this, name) &&
              !isNaN(+name.slice(1))) {
            this[name] = undefined;
          }
        }
      }
    },

    stop: function() {
      this.done = true;

      var rootEntry = this.tryEntries[0];
      var rootRecord = rootEntry.completion;
      if (rootRecord.type === "throw") {
        throw rootRecord.arg;
      }

      return this.rval;
    },

    dispatchException: function(exception) {
      if (this.done) {
        throw exception;
      }

      var context = this;
      function handle(loc, caught) {
        record.type = "throw";
        record.arg = exception;
        context.next = loc;

        if (caught) {
          // If the dispatched exception was caught by a catch block,
          // then let that catch block handle the exception normally.
          context.method = "next";
          context.arg = undefined;
        }

        return !! caught;
      }

      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        var record = entry.completion;

        if (entry.tryLoc === "root") {
          // Exception thrown outside of any try block that could handle
          // it, so set the completion value of the entire function to
          // throw the exception.
          return handle("end");
        }

        if (entry.tryLoc <= this.prev) {
          var hasCatch = hasOwn.call(entry, "catchLoc");
          var hasFinally = hasOwn.call(entry, "finallyLoc");

          if (hasCatch && hasFinally) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            } else if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else if (hasCatch) {
            if (this.prev < entry.catchLoc) {
              return handle(entry.catchLoc, true);
            }

          } else if (hasFinally) {
            if (this.prev < entry.finallyLoc) {
              return handle(entry.finallyLoc);
            }

          } else {
            throw new Error("try statement without catch or finally");
          }
        }
      }
    },

    abrupt: function(type, arg) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc <= this.prev &&
            hasOwn.call(entry, "finallyLoc") &&
            this.prev < entry.finallyLoc) {
          var finallyEntry = entry;
          break;
        }
      }

      if (finallyEntry &&
          (type === "break" ||
           type === "continue") &&
          finallyEntry.tryLoc <= arg &&
          arg <= finallyEntry.finallyLoc) {
        // Ignore the finally entry if control is not jumping to a
        // location outside the try/catch block.
        finallyEntry = null;
      }

      var record = finallyEntry ? finallyEntry.completion : {};
      record.type = type;
      record.arg = arg;

      if (finallyEntry) {
        this.method = "next";
        this.next = finallyEntry.finallyLoc;
        return ContinueSentinel;
      }

      return this.complete(record);
    },

    complete: function(record, afterLoc) {
      if (record.type === "throw") {
        throw record.arg;
      }

      if (record.type === "break" ||
          record.type === "continue") {
        this.next = record.arg;
      } else if (record.type === "return") {
        this.rval = this.arg = record.arg;
        this.method = "return";
        this.next = "end";
      } else if (record.type === "normal" && afterLoc) {
        this.next = afterLoc;
      }

      return ContinueSentinel;
    },

    finish: function(finallyLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.finallyLoc === finallyLoc) {
          this.complete(entry.completion, entry.afterLoc);
          resetTryEntry(entry);
          return ContinueSentinel;
        }
      }
    },

    "catch": function(tryLoc) {
      for (var i = this.tryEntries.length - 1; i >= 0; --i) {
        var entry = this.tryEntries[i];
        if (entry.tryLoc === tryLoc) {
          var record = entry.completion;
          if (record.type === "throw") {
            var thrown = record.arg;
            resetTryEntry(entry);
          }
          return thrown;
        }
      }

      // The context.catch method must only be called with a location
      // argument that corresponds to a known catch block.
      throw new Error("illegal catch attempt");
    },

    delegateYield: function(iterable, resultName, nextLoc) {
      this.delegate = {
        iterator: values(iterable),
        resultName: resultName,
        nextLoc: nextLoc
      };

      if (this.method === "next") {
        // Deliberately forget the last sent value so that we don't
        // accidentally pass it on to the delegate.
        this.arg = undefined;
      }

      return ContinueSentinel;
    }
  };

  // Regardless of whether this script is executing as a CommonJS module
  // or not, return the runtime object so that we can declare the variable
  // regeneratorRuntime in the outer scope, which allows this module to be
  // injected easily by `bin/regenerator --include-runtime script.js`.
  return exports;

}(
  // If this script is executing as a CommonJS module, use module.exports
  // as the regeneratorRuntime namespace. Otherwise create a new empty
  // object. Either way, the resulting object will be used to initialize
  // the regeneratorRuntime variable at the top of this file.
   true ? module.exports : undefined
));

try {
  regeneratorRuntime = runtime;
} catch (accidentalStrictMode) {
  // This module should not be running in strict mode, so the above
  // assignment should always work unless something is misconfigured. Just
  // in case runtime.js accidentally runs in strict mode, we can escape
  // strict mode using a global Function call. This could conceivably fail
  // if a Content Security Policy forbids using Function, but in that case
  // the proper solution is to fix the accidental strict mode problem. If
  // you've misconfigured your bundler to force strict mode and applied a
  // CSP to forbid Function, and you're not willing to fix either of those
  // problems, please detail your unique predicament in a GitHub issue.
  Function("r", "regeneratorRuntime = r")(runtime);
}


/***/ }),

/***/ 2:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(7);
/* harmony import */ var _dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(11);
function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }





jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.safeClone = function () {
  var $clone = this.clone(); // IE BUG : Placeholder text becomes actual value after deep clone on textarea
  // https://connect.microsoft.com/IE/feedback/details/781612/placeholder-text-becomes-actual-value-after-deep-clone-on-textarea

  if (window.document.documentMode) {
    $clone.findInclusive(":input[placeholder]").each(function (i, item) {
      var $item = jquery__WEBPACK_IMPORTED_MODULE_0___default()(item);

      if ($item.attr("placeholder") === $item.val()) {
        $item.val("");
      }
    });
  }

  return $clone;
}; // Production steps of ECMA-262, Edition 5, 15.4.4.18
// Reference: http://es5.github.io/#x15.4.4.18


if (!Array.prototype.forEach) {
  Array.prototype.forEach = function (callback, thisArg) {
    var T, k;

    if (this === null) {
      throw new TypeError(" this is null or not defined");
    } // 1. Let O be the result of calling ToObject passing the |this| value as the argument.


    var O = Object(this); // 2. Let lenValue be the result of calling the Get internal method of O with the argument "length".
    // 3. Let len be ToUint32(lenValue).

    var len = O.length >>> 0; // 4. If IsCallable(callback) is false, throw a TypeError exception.
    // See: http://es5.github.com/#x9.11

    if (typeof callback !== "function") {
      throw new TypeError(callback + " is not a function");
    } // 5. If thisArg was supplied, let T be thisArg; else let T be undefined.


    if (arguments.length > 1) {
      T = thisArg;
    } // 6. Let k be 0


    k = 0; // 7. Repeat, while k < len

    while (k < len) {
      var kValue; // a. Let Pk be ToString(k).
      //   This is implicit for LHS operands of the in operator
      // b. Let kPresent be the result of calling the HasProperty internal method of O with argument Pk.
      //   This step can be combined with c
      // c. If kPresent is true, then

      if (k in O) {
        // i. Let kValue be the result of calling the Get internal method of O with argument Pk.
        kValue = O[k]; // ii. Call the Call internal method of callback with T as the this value and
        // argument list containing kValue, k, and O.

        callback.call(T, kValue, k, O);
      } // d. Increase k by 1.


      k++;
    } // 8. return undefined

  };
}

var singleBoundJQueryPlugin = function singleBoundJQueryPlugin(pattern, method, options) {
  /* This is a jQuery plugin for patterns which are invoked ONCE FOR EACH
   * matched element in the DOM.
   *
   * This is how the Mockup-type patterns behave. They are constructor
   * functions which need to be invoked once per jQuery-wrapped DOM node
   * for all DOM nodes on which the pattern applies.
   */
  var $this = this;
  $this.each(function () {
    var pat,
        $el = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this);
    pat = pattern.init($el, options);

    if (method) {
      if (pat[method] === undefined) {
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.error("Method " + method + " does not exist on jQuery." + pattern.name);
        return false;
      }

      if (method.charAt(0) === "_") {
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.error("Method " + method + " is private on jQuery." + pattern.name);
        return false;
      }

      pat[method].apply(pat, [options]);
    }
  });
  return $this;
};

var pluralBoundJQueryPlugin = function pluralBoundJQueryPlugin(pattern, method, options) {
  /* This is a jQuery plugin for patterns which are invoked ONCE FOR ALL
   * matched elements in the DOM.
   *
   * This is how the vanilla Patternslib-type patterns behave. They are
   * simple objects with an init method and this method gets called once
   * with a list of jQuery-wrapped DOM nodes on which the pattern
   * applies.
   */
  var $this = this;

  if (method) {
    if (pattern[method]) {
      return pattern[method].apply($this, [$this].concat([options]));
    } else {
      jquery__WEBPACK_IMPORTED_MODULE_0___default.a.error("Method " + method + " does not exist on jQuery." + pattern.name);
    }
  } else {
    pattern.init.apply($this, [$this].concat([options]));
  }

  return $this;
};

var jqueryPlugin = function jqueryPlugin(pattern) {
  return function (method, options) {
    var $this = this;

    if ($this.length === 0) {
      return $this;
    }

    if (_typeof(method) === "object") {
      options = method;
      method = undefined;
    }

    if (typeof pattern === "function") {
      return singleBoundJQueryPlugin.call(this, pattern, method, options);
    } else {
      return pluralBoundJQueryPlugin.call(this, pattern, method, options);
    }
  };
}; // Is a given variable an object?


function isObject(obj) {
  var type = _typeof(obj);

  return type === "function" || type === "object" && !!obj;
} // Extend a given object with all the properties in passed-in object(s).


function extend(obj) {
  if (!isObject(obj)) return obj;
  var source, prop;

  for (var i = 1, length = arguments.length; i < length; i++) {
    source = arguments[i];

    for (prop in source) {
      if (hasOwnProperty.call(source, prop)) {
        obj[prop] = source[prop];
      }
    }
  }

  return obj;
} // END: Taken from Underscore.js until here.


function rebaseURL(base, url) {
  base = new URL(base, window.location).href; // If base is relative make it absolute.

  if (url.indexOf("://") !== -1 || url[0] === "/" || url.indexOf("data:") === 0) {
    return url;
  }

  return base.slice(0, base.lastIndexOf("/") + 1) + url;
}

function findLabel(input) {
  var $label;

  for (var label = input.parentNode; label && label.nodeType !== 11; label = label.parentNode) {
    if (label.tagName === "LABEL") {
      return label;
    }
  }

  if (input.id) {
    $label = jquery__WEBPACK_IMPORTED_MODULE_0___default()('label[for="' + input.id + '"]');
  }

  if ($label && $label.length === 0 && input.form) {
    $label = jquery__WEBPACK_IMPORTED_MODULE_0___default()('label[for="' + input.name + '"]', input.form);
  }

  if ($label && $label.length) {
    return $label[0];
  } else {
    return null;
  }
} // Taken from http://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport


function elementInViewport(el) {
  var rect = el.getBoundingClientRect(),
      docEl = document.documentElement,
      vWidth = window.innerWidth || docEl.clientWidth,
      vHeight = window.innerHeight || docEl.clientHeight;
  if (rect.right < 0 || rect.bottom < 0 || rect.left > vWidth || rect.top > vHeight) return false;
  return true;
} // Taken from http://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex


function escapeRegExp(str) {
  return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
}

function removeWildcardClass($targets, classes) {
  if (classes.indexOf("*") === -1) $targets.removeClass(classes);else {
    var matcher = classes.replace(/[\-\[\]{}()+?.,\\\^$|#\s]/g, "\\$&");
    matcher = matcher.replace(/[*]/g, ".*");
    matcher = new RegExp("^" + matcher + "$");
    $targets.filter("[class]").each(function () {
      var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
          classes = $this.attr("class").split(/\s+/),
          ok = [];

      for (var i = 0; i < classes.length; i++) {
        if (!matcher.test(classes[i])) ok.push(classes[i]);
      }

      if (ok.length) $this.attr("class", ok.join(" "));else $this.removeAttr("class");
    });
  }
}

function hasValue(el) {
  if (el.tagName === "INPUT") {
    if (el.type === "checkbox" || el.type === "radio") {
      return el.checked;
    }

    return el.value !== "";
  }

  if (el.tagName === "SELECT") {
    return el.selectedIndex !== -1;
  }

  if (el.tagName === "TEXTAREA") {
    return el.value !== "";
  }

  return false;
}

var hideOrShow = function hideOrShow(nodes, visible, options, pattern_name) {
  nodes = _dom__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].toNodeArray(nodes);
  var transitions = {
    none: {
      hide: "hide",
      show: "show"
    },
    fade: {
      hide: "fadeOut",
      show: "fadeIn"
    },
    slide: {
      hide: "slideUp",
      show: "slideDown"
    }
  };
  var duration = options.transition === "css" || options.transition === "none" ? null : options.effect.duration;

  var on_complete = function on_complete(el) {
    el.classList.remove("in-progress");
    el.classList.add(visible ? "visible" : "hidden");
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(el).trigger("pat-update", {
      pattern: pattern_name,
      transition: "complete"
    });
  };

  var _iterator = _createForOfIteratorHelper(nodes),
      _step;

  try {
    var _loop = function _loop() {
      var el = _step.value;
      el.classList.remove("visible");
      el.classList.remove("hidden");
      el.classList.remove("in-progress");

      if (duration) {
        var t = transitions[options.transition];
        el.classList.add("in-progress");
        jquery__WEBPACK_IMPORTED_MODULE_0___default()(el).trigger("pat-update", {
          pattern: pattern_name,
          transition: "start"
        });
        jquery__WEBPACK_IMPORTED_MODULE_0___default()(el)[visible ? t.show : t.hide]({
          duration: duration,
          easing: options.effect.easing,
          complete: function complete() {
            return on_complete(el);
          }
        });
      } else {
        if (options.transition !== "css") {
          _dom__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"][visible ? "show" : "hide"](el);
        }

        on_complete(el);
      }
    };

    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      _loop();
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
};

function addURLQueryParameter(fullURL, param, value) {
  /* Using a positive lookahead (?=\=) to find the given parameter,
   * preceded by a ? or &, and followed by a = with a value after
   * than (using a non-greedy selector) and then followed by
   * a & or the end of the string.
   *
   * Taken from http://stackoverflow.com/questions/7640270/adding-modify-query-string-get-variables-in-a-url-with-javascript
   */
  var val = new RegExp("(\\?|\\&)" + param + "=.*?(?=(&|$))"),
      parts = fullURL.toString().split("#"),
      url = parts[0],
      hash = parts[1],
      qstring = /\?.+$/,
      newURL = url; // Check if the parameter exists

  if (val.test(url)) {
    // if it does, replace it, using the captured group
    // to determine & or ? at the beginning
    newURL = url.replace(val, "$1" + param + "=" + value);
  } else if (qstring.test(url)) {
    // otherwise, if there is a query string at all
    // add the param to the end of it
    newURL = url + "&" + param + "=" + value;
  } else {
    // if there's no query string, add one
    newURL = url + "?" + param + "=" + value;
  }

  if (hash) {
    newURL += "#" + hash;
  }

  return newURL;
}

function removeDuplicateObjects(objs) {
  /* Given an array of objects, remove any duplicate objects which might
   * be present.
   */
  var comparator = function comparator(v, k) {
    return this[k] === v;
  };

  return underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].reduce(objs, function (list, next_obj) {
    var is_duplicate = false;

    underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].each(list, function (obj) {
      is_duplicate = underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].keys(obj).length === underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].keys(next_obj).length && !underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].chain(obj).omit(comparator.bind(next_obj)).keys().value().length;
    });

    if (!is_duplicate) {
      list.push(next_obj);
    }

    return list;
  }, []);
}

function mergeStack(stack, length) {
  /* Given a list of lists of objects (which for brevity we call a stack),
   * return a list of objects where each object is the merge of all the
   * corresponding original objects at that particular index.
   *
   * If a certain sub-list doesn't have an object at that particular
   * index, the last object in that list is merged.
   */
  var results = [];

  for (var i = 0; i < length; i++) {
    results.push({});
  }

  underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].each(stack, function (frame) {
    var frame_length = frame.length - 1;

    for (var x = 0; x < length; x++) {
      results[x] = jquery__WEBPACK_IMPORTED_MODULE_0___default.a.extend(results[x] || {}, frame[x > frame_length ? frame_length : x]);
    }
  });

  return results;
}

function isElementInViewport(el, partial, offset) {
  /* returns true if element is visible to the user ie. is in the viewport.
   * Setting partial parameter to true, will only check if a part of the element is visible
   * in the viewport, specifically that some part of that element is touching the top part
   * of the viewport. This only applies to the vertical direction, ie. doesnt check partial
   * visibility for horizontal scrolling
   * some code taken from:
   * http://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport/7557433#7557433
   */
  if (el === []) {
    return false;
  }

  if (el instanceof jquery__WEBPACK_IMPORTED_MODULE_0___default.a) {
    el = el[0];
  }

  var rec = el.getBoundingClientRect(),
      rec_values = [rec.top, rec.bottom, rec.left, rec.right];

  if (underscore__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].every(rec_values, function zero(v) {
    if (v === 0) {
      return true;
    }
  })) {
    // if every property of rec is 0, the element is invisible;
    return false;
  } else if (partial) {
    // when using getBoundingClientRect() (in the vertical case)
    // negative means above top of viewport, positive means below top of viewport
    // therefore for part of the element to be touching or crossing the top of the viewport
    // rec.top must <= 0 and rec.bottom must >= 0
    // an optional tolerance offset can be added for when the desired element is not exactly
    // toucing the top of the viewport but needs to be considered as touching.
    if (offset === undefined) {
      offset = 0;
    }

    return rec.top <= 0 + offset && rec.bottom >= 0 + offset //(rec.top >= 0+offset && rec.top <= window.innerHeight) // this checks if the element
    // touches bottom part of viewport
    // XXX do we want to include a check for the padding of an element?
    // using window.getComputedStyle(target).paddingTop
    ;
  } else {
    // this will return true if the entire element is completely in the viewport
    return rec.top >= 0 && rec.left >= 0 && rec.bottom <= (window.innerHeight || document.documentElement.clientHeight)
    /*or $(window).height() */
    && rec.right <= (window.innerWidth || document.documentElement.clientWidth)
    /*or $(window).width() */
    ;
  }
}

function parseTime(time) {
  var m = /^(\d+(?:\.\d+)?)\s*(\w*)/.exec(time);

  if (!m) {
    throw new Error("Invalid time");
  }

  var amount = parseFloat(m[1]);

  switch (m[2]) {
    case "s":
      return Math.round(amount * 1000);

    case "m":
      return Math.round(amount * 1000 * 60);

    case "ms":
    default:
      return Math.round(amount);
  }
} // Return a jQuery object with elements related to an input element.


function findRelatives(el) {
  var $el = jquery__WEBPACK_IMPORTED_MODULE_0___default()(el),
      $relatives = jquery__WEBPACK_IMPORTED_MODULE_0___default()(el),
      $label = jquery__WEBPACK_IMPORTED_MODULE_0___default()();
  $relatives = $relatives.add($el.closest("label"));
  $relatives = $relatives.add($el.closest("fieldset"));
  if (el.id) $label = jquery__WEBPACK_IMPORTED_MODULE_0___default()("label[for='" + el.id + "']");

  if (!$label.length) {
    var $form = $el.closest("form");
    if (!$form.length) $form = jquery__WEBPACK_IMPORTED_MODULE_0___default()(document.body);
    $label = $form.find("label[for='" + el.name + "']");
  }

  $relatives = $relatives.add($label);
  return $relatives;
}

function getCSSValue(el, property, asPixels) {
  /* Return a CSS property value for a given DOM node.
   * For length-values, relative values are converted to pixels.
   * Optionally parse as pixels, if applicable.
   */
  var value = window.getComputedStyle(el).getPropertyValue(property);

  if (asPixels) {
    value = parseFloat(value) || 0.0;
  }

  return value;
}

function checkInputSupport(type, invalid_value) {
  /* Check input type support.
   *  See: https://stackoverflow.com/a/10199306/1337474
   */
  var support = false;
  var input = document.createElement("input");
  input.setAttribute("type", type);
  support = input.type == type;

  if (invalid_value !== undefined) {
    // Check for input type UI support
    input.setAttribute("value", invalid_value);
    support = input.value !== invalid_value;
  }

  return support;
}

var checkCSSFeature = function checkCSSFeature(attribute, value) {
  var tag = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "div";

  /* Check for browser support of specific CSS feature.
   */
  tag = document.createElement(tag);
  var supported = tag.style[attribute] !== undefined;

  if (supported && value !== undefined) {
    tag.style[attribute] = value;
    supported = tag.style[attribute] === value;
  }

  return supported;
};

var timeout = function timeout(ms) {
  return new Promise(function (resolve) {
    return setTimeout(resolve, ms);
  });
};

var debounce = function debounce(func, ms) {
  // Returns a function, that, as long as it continues to be invoked, will not
  // be triggered. The function will be called after it stops being called for
  // N milliseconds.
  // From: https://underscorejs.org/#debounce
  var timer = null;
  return function () {
    var _this = this;

    clearTimeout(timer);
    var args = arguments;
    timer = setTimeout(function () {
      func.apply(_this, args);
    }, ms);
  };
};

var isIE = function isIE() {
  // See: https://stackoverflow.com/a/9851769/1337474
  // Internet Explorer 6-11
  return (
    /*@cc_on!@*/
     false || !!document.documentMode
  );
};

var jqToNode = function jqToNode(el) {
  // Return a DOM node if a jQuery node was passed.
  if (el.jquery) {
    el = el[0];
  }

  return el;
};

var ensureArray = function ensureArray(it) {
  // Ensure to return always an array
  return Array.isArray(it) || it.jquery ? it : [it];
};

var utils = {
  // pattern pimping - own module?
  jqueryPlugin: jqueryPlugin,
  escapeRegExp: escapeRegExp,
  isObject: isObject,
  extend: extend,
  rebaseURL: rebaseURL,
  findLabel: findLabel,
  elementInViewport: elementInViewport,
  removeWildcardClass: removeWildcardClass,
  hideOrShow: hideOrShow,
  addURLQueryParameter: addURLQueryParameter,
  removeDuplicateObjects: removeDuplicateObjects,
  mergeStack: mergeStack,
  isElementInViewport: isElementInViewport,
  hasValue: hasValue,
  parseTime: parseTime,
  findRelatives: findRelatives,
  getCSSValue: getCSSValue,
  checkInputSupport: checkInputSupport,
  checkCSSFeature: checkCSSFeature,
  timeout: timeout,
  debounce: debounce,
  isIE: isIE,
  jqToNode: jqToNode,
  ensureArray: ensureArray
};
/* harmony default export */ __webpack_exports__["a"] = (utils);

/***/ }),

/***/ 22:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _logging__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(6);
/**
 * Patterns store - store pattern state locally in the browser
 *
 * Copyright 2008-2012 Simplon B.V.
 * Copyright 2011 Humberto Sermeño
 * Copyright 2011 Florian Friesdorf
 */

var log = _logging__WEBPACK_IMPORTED_MODULE_0__[/* default */ "a"].getLogger("Patternslib Store");

function Storage(backend, prefix) {
  this.prefix = prefix;
  this.backend = backend;
}

Storage.prototype._key = function Storage_key(name) {
  return this.prefix + ":" + name;
};

Storage.prototype._allKeys = function Storage_allKeys() {
  var keys = [],
      prefix = this.prefix + ":",
      prefix_length = prefix.length,
      key,
      i;

  for (i = 0; i < this.backend.length; i++) {
    key = this.backend.key(i);
    if (key.slice(0, prefix_length) === prefix) keys.push(key);
  }

  return keys;
};

Storage.prototype.get = function Storage_get(name) {
  var key = this._key(name),
      value = this.backend.getItem(key);

  if (value !== null) {
    try {
      value = JSON.parse(value);
    } catch (_unused) {
      log.warn("Cannot parse storage value for key ".concat(key));
      return;
    }
  }

  return value;
};

Storage.prototype.set = function Storage_set(name, value) {
  var key = this._key(name);

  return this.backend.setItem(key, JSON.stringify(value));
};

Storage.prototype.remove = function Storage_remove(name) {
  var key = this._key(name);

  return this.backend.removeItem(key);
};

Storage.prototype.clear = function Storage_clear() {
  var keys = this._allKeys();

  for (var i = 0; i < keys.length; i++) {
    this.backend.removeItem(keys[i]);
  }
};

Storage.prototype.all = function Storage_all() {
  var keys = this._allKeys(),
      prefix_length = this.prefix.length + 1,
      lk,
      data = {};

  for (var i = 0; i < keys.length; i++) {
    lk = keys[i].slice(prefix_length);
    data[lk] = JSON.parse(this.backend.getItem(keys[i]));
  }

  return data;
};

function ValueStorage(store, name) {
  this.store = store;
  this.name = name;
}

ValueStorage.prototype.get = function ValueStorage_get() {
  return this.store.get(this.name);
};

ValueStorage.prototype.set = function ValueStorage_get(value) {
  return this.store.set(this.name, value);
};

ValueStorage.prototype.remove = function ValueStorage_remove() {
  return this.store.remove(this.name);
};

var store = {
  supported: false,
  local: function local(name) {
    return new Storage(window.localStorage, name);
  },
  session: function session(name) {
    return new Storage(window.sessionStorage, name);
  },
  ValueStorage: ValueStorage,
  // Update storage options for a given element.
  updateOptions: function store_updateOptions(trigger, options) {
    if (options.store !== "none") {
      if (!trigger.id) {
        log.warn("state persistance requested, but element has no id");
        options.store = "none";
      } else if (!store.supported) {
        log.warn("state persistance requested, but browser does not support webstorage");
        options.store = "none";
      }
    }

    return options;
  }
}; // Perform the test separately since this may throw a SecurityError as
// reported in #326

try {
  store.supported = typeof window.sessionStorage !== "undefined";
} catch (e) {// just ignore.
}

/* harmony default export */ __webpack_exports__["a"] = (store);

/***/ }),

/***/ 23:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var _core_jquery_ext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(38);
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(19);
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7);
/* harmony import */ var _ajax_ajax__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(35);
/* harmony import */ var _core_dom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(11);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(6);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(4);
/* harmony import */ var _core_registry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(9);
/* harmony import */ var _core_utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(2);
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

 // for :scrollable for autoLoading-visible

 // needed for ``await`` support









var log = _core_logging__WEBPACK_IMPORTED_MODULE_6__[/* default */ "a"].getLogger("pat.inject");
var TEXT_NODE = 3;
var COMMENT_NODE = 8;
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_7__[/* default */ "a"]("inject");
parser.addArgument("default-selector");
parser.addArgument("target");
parser.addArgument("data-type", "html");
parser.addArgument("next-href");
parser.addArgument("source");
parser.addArgument("trigger", "default", ["default", "autoload", "autoload-visible", "idle"]);
parser.addArgument("delay"); // only used in autoload

parser.addArgument("confirm", "class", ["never", "always", "form-data", "class"]);
parser.addArgument("confirm-message", "Are you sure you want to leave this page?");
parser.addArgument("hooks", [], ["raptor"], true); // After injection, pat-inject will trigger an event for each hook: pat-inject-hook-$(hook)

parser.addArgument("loading-class", "injecting"); // Add a class to the target while content is still loading.

parser.addArgument("executing-class", "executing"); // Add a class to the element while content is still loading.

parser.addArgument("executed-class", "executed"); // Add a class to the element when content is loaded.

parser.addArgument("class"); // Add a class to the injected content.

parser.addArgument("history");
parser.addArgument("push-marker");
parser.addArgument("scroll"); // XXX: this should not be here but the parser would bail on
// unknown parameters and expand/collapsible need to pass the url
// to us

parser.addArgument("url");
var inject = {
  name: "inject",
  trigger: ".raptor-ui .ui-button.pat-inject, a.pat-inject, form.pat-inject, .pat-subform.pat-inject",
  parser: parser,
  init: function init($el, opts) {
    var _this = this;

    var cfgs = this.extractConfig($el, opts);

    if (cfgs.some(function (e) {
      return e.history === "record";
    }) && !("pushState" in history)) {
      // if the injection shall add a history entry and HTML5 pushState
      // is missing, then don't initialize the injection.
      return $el;
    }

    $el.data("pat-inject", cfgs);

    if (cfgs[0].nextHref && cfgs[0].nextHref.indexOf("#") === 0) {
      // In case the next href is an anchor, and it already
      // exists in the page, we do not activate the injection
      // but instead just change the anchors href.
      // XXX: This is used in only one project for linked
      // fullcalendars, it's sanity is wonky and we should
      // probably solve it differently.
      if ($el.is("a") && jquery__WEBPACK_IMPORTED_MODULE_2___default()(cfgs[0].nextHref).length > 0) {
        log.debug("Skipping as next href is anchor, which already exists", cfgs[0].nextHref); // XXX: reconsider how the injection enters exhausted state

        return $el.attr({
          href: (window.location.href.split("#")[0] || "") + cfgs[0].nextHref
        });
      }
    }

    if (cfgs[0].pushMarker) {
      jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").on("push", function (event, data) {
        log.debug("received push message: " + data);

        if (data == cfgs[0].pushMarker) {
          log.debug("re-injecting " + data);

          _this.onTrigger({
            currentTarget: $el[0]
          });
        }
      });
    }

    if (cfgs[0].idleTrigger) {
      this._initIdleTrigger($el, cfgs[0].idleTrigger);
    } else {
      switch (cfgs[0].trigger) {
        case "default":
          cfgs.forEach(function (cfg) {
            if (cfg.delay) {
              cfg.processDelay = cfg.delay;
            }
          }); // setup event handlers

          if ($el.is("form")) {
            $el.on("submit.pat-inject", this.onTrigger.bind(this)).on("click.pat-inject", "[type=submit]", _ajax_ajax__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].onClickSubmit).on("click.pat-inject", "[type=submit][formaction], [type=image][formaction]", this.onFormActionSubmit.bind(this));
          } else if ($el.is(".pat-subform")) {
            log.debug("Initializing subform with injection");
          } else {
            $el.on("click.pat-inject", this.onTrigger.bind(this));
          }

          break;

        case "autoload":
          if (!cfgs[0].delay) {
            this.onTrigger({
              currentTarget: $el[0]
            });
          } else {
            // generate UID
            var uid = Math.random().toString(36);
            $el.attr("data-pat-inject-uid", uid); // function to trigger the autoload and mark as triggered

            var delayed_trigger = function delayed_trigger(uid_) {
              // Check if the element has been removed from the dom
              var still_there = jquery__WEBPACK_IMPORTED_MODULE_2___default()("[data-pat-inject-uid='" + uid_ + "']");
              if (still_there.length == 0) return false;
              $el.data("pat-inject-autoloaded", true);

              _this.onTrigger({
                currentTarget: $el[0]
              });

              return true;
            };

            window.setTimeout(delayed_trigger.bind(null, uid), cfgs[0].delay);
          }

          break;

        case "autoload-visible":
          this._initAutoloadVisible($el, cfgs);

          break;

        case "idle":
          this._initIdleTrigger($el, cfgs[0].delay);

          break;
      }
    }

    log.debug("initialised:", $el);
    return $el;
  },
  destroy: function destroy($el) {
    $el.off(".pat-inject");
    $el.data("pat-inject", null);
    return $el;
  },
  onTrigger: function onTrigger(e) {
    /* Injection has been triggered, either via form submission or a
     * link has been clicked.
     */
    var $el = jquery__WEBPACK_IMPORTED_MODULE_2___default()(e.currentTarget);
    var cfgs = $el.data("pat-inject");

    if ($el.is("form")) {
      jquery__WEBPACK_IMPORTED_MODULE_2___default()(cfgs).each(function (i, v) {
        v.params = jquery__WEBPACK_IMPORTED_MODULE_2___default.a.param($el.serializeArray());
      });
    }

    e.preventDefault && e.preventDefault();
    $el.trigger("patterns-inject-triggered");
    this.execute(cfgs, $el);
  },
  onFormActionSubmit: function onFormActionSubmit(e) {
    _ajax_ajax__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].onClickSubmit(e); // make sure the submitting button is sent with the form

    var $button = jquery__WEBPACK_IMPORTED_MODULE_2___default()(e.target);
    var formaction = $button.attr("formaction");
    var $form = $button.parents(".pat-inject").first();
    var opts = {
      url: formaction
    };
    var $cfg_node = $button.closest("[data-pat-inject]");
    var cfgs = this.extractConfig($cfg_node, opts);
    jquery__WEBPACK_IMPORTED_MODULE_2___default()(cfgs).each(function (i, v) {
      v.params = jquery__WEBPACK_IMPORTED_MODULE_2___default.a.param($form.serializeArray());
    });
    e.preventDefault();
    $form.trigger("patterns-inject-triggered");
    this.execute(cfgs, $form);
  },
  submitSubform: function submitSubform($sub) {
    /* This method is called from pat-subform
     */
    var $el = $sub.parents("form");
    var cfgs = $sub.data("pat-inject"); // store the params of the subform in the config, to be used by history

    jquery__WEBPACK_IMPORTED_MODULE_2___default()(cfgs).each(function (i, v) {
      v.params = jquery__WEBPACK_IMPORTED_MODULE_2___default.a.param($sub.serializeArray());
    });

    try {
      $el.trigger("patterns-inject-triggered");
    } catch (e) {
      log.error("patterns-inject-triggered", e);
    }

    this.execute(cfgs, $el);
  },
  extractConfig: function extractConfig($el, opts) {
    opts = jquery__WEBPACK_IMPORTED_MODULE_2___default.a.extend({}, opts);
    var cfgs = parser.parse($el, opts, true);
    cfgs.forEach(function (cfg) {
      cfg.$context = $el; // opts and cfg have priority, fallback to href/action

      cfg.url = opts.url || cfg.url || $el.attr("href") || $el.attr("action") || $el.parents("form").attr("action") || ""; // separate selector from url

      var urlparts = cfg.url.split("#");
      cfg.url = urlparts[0];

      if (urlparts.length > 2) {
        log.warn("Ignoring additional source ids:", urlparts.slice(2));
      }

      if (!cfg.defaultSelector) {
        // if no selector, check for selector as part of original url
        cfg.defaultSelector = urlparts[1] && "#" + urlparts[1] || "body";
      }

      if (cfg.delay) {
        try {
          cfg.delay = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].parseTime(cfg.delay);
        } catch (e) {
          log.warn("Invalid delay value: ", cfg.delay);
          cfg.delay = null;
        }
      }

      cfg.processDelay = 0;
    });
    return cfgs;
  },
  elementIsDirty: function elementIsDirty(m) {
    /* Check whether the passed in form element contains a value.
     */
    var data = jquery__WEBPACK_IMPORTED_MODULE_2___default.a.map(m.find(":input:not(select)"), function (i) {
      var val = jquery__WEBPACK_IMPORTED_MODULE_2___default()(i).val();
      return Boolean(val) && val !== jquery__WEBPACK_IMPORTED_MODULE_2___default()(i).attr("placeholder");
    });
    return jquery__WEBPACK_IMPORTED_MODULE_2___default.a.inArray(true, data) !== -1;
  },
  askForConfirmation: function askForConfirmation(cfgs) {
    var _this2 = this;

    /* If configured to do so, show a confirmation dialog to the user.
     * This is done before attempting to perform injection.
     */
    var should_confirm = false;
    var message;

    underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].each(cfgs, function (cfg) {
      var _confirm = false;

      if (cfg.confirm == "always") {
        _confirm = true;
      } else if (cfg.confirm === "form-data") {
        if (cfg.target != "none") _confirm = _this2.elementIsDirty(cfg.$target);
      } else if (cfg.confirm === "class") {
        if (cfg.target != "none") _confirm = cfg.$target.hasClass("is-dirty");
      }

      if (_confirm) {
        should_confirm = true;
        message = cfg.confirmMessage;
      }
    });

    if (should_confirm) {
      if (!window.confirm(message)) {
        return false;
      }
    }

    return true;
  },
  ensureTarget: function ensureTarget(cfg) {
    /* Make sure that a target element exists and that it's assigned to
     * cfg.$target.
     */
    // make sure target exist
    if (cfg.target === "none") {
      // special case, we don't want to inject anything
      return true;
    }

    cfg.$target = cfg.$target || (cfg.target === "self" ? cfg.$context : jquery__WEBPACK_IMPORTED_MODULE_2___default()(cfg.target));

    if (cfg.$target.length === 0) {
      if (!cfg.target) {
        log.error("Need target selector", cfg);
        return false;
      }

      cfg.$target = this.createTarget(cfg.target);
      cfg.$injected = cfg.$target;
    }

    return true;
  },
  verifySingleConfig: function verifySingleConfig(url, cfg) {
    /* Verify one of potentially multiple configs (i.e. argument lists).
     *
     * Extract modifiers such as ::element or ::after.
     * Ensure that a target element exists.
     */
    if (cfg.url !== url) {
      // in case of multi-injection, all injections need to use
      // the same url
      log.error("Unsupported different urls for multi-inject");
      return false;
    } // defaults


    cfg.source = cfg.source || cfg.defaultSelector;
    cfg.target = cfg.target || cfg.defaultSelector;

    if (!this.extractModifiers(cfg)) {
      return false;
    }

    if (!this.ensureTarget(cfg)) {
      return false;
    }

    this.listenForFormReset(cfg);
    return true;
  },
  verifyConfig: function verifyConfig(cfgs) {
    /* Verify and post-process all the configurations.
     * Each "config" is an arguments list separated by the &&
     * combination operator.
     *
     * In case of multi-injection, only one URL is allowed, which
     * should be specified in the first config (i.e. arguments list).
     *
     * Verification for each cfg in the array needs to succeed.
     */
    return cfgs.every(underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].partial(this.verifySingleConfig.bind(this), cfgs[0].url));
  },
  listenForFormReset: function listenForFormReset(cfg) {
    /* if pat-inject is used to populate target in some form and when
     * Cancel button is pressed (this triggers reset event on the
     * form) you would expect to populate with initial placeholder
     */
    if (cfg.target === "none") // Special case, we don't want to display any return value.
      return;
    var $form = cfg.$target.parents("form");

    if ($form.length !== 0 && cfg.$target.data("initial-value") === undefined) {
      cfg.$target.data("initial-value", cfg.$target.html());
      $form.on("reset", function () {
        cfg.$target.html(cfg.$target.data("initial-value"));
      });
    }
  },
  extractModifiers: function extractModifiers(cfg) {
    /* The user can add modifiers to the source and target arguments.
     * Modifiers such as ::element, ::before and ::after.
     * We identifiy and extract these modifiers here.
     */
    var source_re = /^(.*?)(::element)?$/;
    var target_re = /^(.*?)(::element)?(::after|::before)?$/;
    var source_match = source_re.exec(cfg.source);
    var target_match = target_re.exec(cfg.target);
    cfg.source = source_match[1];
    cfg.sourceMod = source_match[2] ? "element" : "content";
    cfg.target = target_match[1];
    var targetMod = target_match[2] ? "element" : "content";
    var targetPosition = (target_match[3] || "::").slice(2); // position relative to target

    if (cfg.loadingClass) {
      cfg.loadingClass += " " + cfg.loadingClass + "-" + targetMod;

      if (targetPosition && cfg.loadingClass) {
        cfg.loadingClass += " " + cfg.loadingClass + "-" + targetPosition;
      }
    }

    cfg.action = targetMod + targetPosition; // Once we start detecting illegal combinations, we'll
    // return false in case of error

    return true;
  },
  createTarget: function createTarget(selector) {
    /* create a target that matches the selector
     *
     * XXX: so far we only support #target and create a div with
     * that id appended to the body.
     */
    if (selector.slice(0, 1) !== "#") {
      log.error("only id supported for non-existing target");
      return null;
    }

    var $target = jquery__WEBPACK_IMPORTED_MODULE_2___default()("<div />").attr({
      id: selector.slice(1)
    });
    jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").append($target);
    return $target;
  },
  stopBubblingFromRemovedElement: function stopBubblingFromRemovedElement($el, cfgs, ev) {
    /* IE8 fix. Stop event from propagating IF $el will be removed
     * from the DOM. With pat-inject, often $el is the target that
     * will itself be replaced with injected content.
     *
     * IE8 cannot handle events bubbling up from an element removed
     * from the DOM.
     *
     * See: http://stackoverflow.com/questions/7114368/why-is-jquery-remove-throwing-attr-exception-in-ie8
     */
    var _iterator = _createForOfIteratorHelper(cfgs),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var cfg = _step.value;
        var sel = cfg.target;

        if ($el.parents(sel).addBack(sel) && !ev.isPropagationStopped()) {
          ev.stopPropagation();
          return;
        }
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }
  },
  _performInjection: function _performInjection(target, $el, $source, cfg, trigger, title) {
    /* Called after the XHR has succeeded and we have a new $source
     * element to inject.
     */
    if (cfg.sourceMod === "content") {
      $source = $source.contents();
    }

    var $src; // $source.clone() does not work with shived elements in IE8

    if (document.all && document.querySelector && !document.addEventListener) {
      $src = $source.map(function (idx, el) {
        return jquery__WEBPACK_IMPORTED_MODULE_2___default()(el.outerHTML)[0];
      });
    } else {
      $src = $source.safeClone();
    }

    $src.findInclusive("img").on("load", function (e) {
      jquery__WEBPACK_IMPORTED_MODULE_2___default()(e.currentTarget).trigger("pat-inject-content-loaded");
    });
    var $injected = cfg.$injected || $src; // Now the injection actually happens.

    if (this._inject(trigger, $src, jquery__WEBPACK_IMPORTED_MODULE_2___default()(target), cfg)) {
      this._afterInjection($el, $injected, cfg);
    } // History support. if subform is submitted, append form params


    var glue = cfg.url.indexOf("?") > -1 ? "&" : "?";

    if (cfg.history === "record" && "pushState" in history) {
      if (cfg.params) {
        history.pushState({
          url: cfg.url + glue + cfg.params
        }, "", cfg.url + glue + cfg.params);
      } else {
        history.pushState({
          url: cfg.url
        }, "", cfg.url);
      } // Also inject title element if we have one


      if (title) this._inject(trigger, title, jquery__WEBPACK_IMPORTED_MODULE_2___default()("title"), {
        action: "element"
      });
    }
  },
  _afterInjection: function _afterInjection($el, $injected, cfg) {
    /* Set a class on the injected elements and fire the
     * patterns-injected event.
     */
    $injected.filter(function (idx, el_) {
      // setting data on textnode fails in IE8
      return el_.nodeType !== TEXT_NODE;
    }).data("pat-injected", {
      origin: cfg.url
    });

    if ($injected.length === 1 && $injected[0].nodeType == TEXT_NODE) {
      // Only one element injected, and it was a text node.
      // So we trigger "patterns-injected" on the parent.
      // The event handler should check whether the
      // injected element and the triggered element are
      // the same.
      $injected.parent().trigger("patterns-injected", [cfg, $el[0], $injected[0]]);
    } else {
      $injected.each(function (idx, el_) {
        // patterns-injected event will be triggered for each injected (non-text) element.
        if (el_.nodeType !== TEXT_NODE) {
          jquery__WEBPACK_IMPORTED_MODULE_2___default()(el_).addClass(cfg["class"]).trigger("patterns-injected", [cfg, $el[0], el_]);
        }
      });
    }

    if (cfg.scroll && cfg.scroll !== "none") {
      var scroll_container = cfg.$target.parents().addBack().filter(":scrollable");
      scroll_container = scroll_container.length ? scroll_container[0] : window; // default for scroll===top

      var top = 0;
      var left = 0;

      if (cfg.scroll !== "top") {
        var scroll_target = cfg.scroll === "target" ? cfg.$target[0] : $injected.filter(cfg.scroll)[0]; // Get the reference element to which against we calculate
        // the relative position of the target.
        // In case of a scroll container of window, we do not have
        // getBoundingClientRect method, so get the body instead.

        var scroll_container_ref = scroll_container === window ? document.body : scroll_container; // Calculate absolute [¹] position difference between
        // scroll_container and scroll_target.
        // Substract the container's border from the scrolling
        // value, as this one isn't respected by
        // getBoundingClientRect [²] and would lead to covered
        // items [³].
        // ¹) so that it doesn't make a difference, if the element
        // is below or above the scrolling container. We just need
        // to know the absolute difference.
        // ²) Calculations are based from the viewport.
        // ³) See:
        //      https://docs.microsoft.com/en-us/previous-versions//hh781509(v=vs.85)
        //      https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect

        left = Math.abs(scroll_target.getBoundingClientRect().left + scroll_container_ref.scrollLeft - scroll_container_ref.getBoundingClientRect().left - _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].getCSSValue(scroll_container_ref, "border-left-width", true));
        top = Math.abs(scroll_target.getBoundingClientRect().top + scroll_container_ref.scrollTop - scroll_container_ref.getBoundingClientRect().top - _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].getCSSValue(scroll_container_ref, "border-top-width", true));
      }

      if (scroll_container === window) {
        scroll_container.scrollTo(left, top);
      } else {
        scroll_container.scrollLeft = left;
        scroll_container.scrollTop = top;
      }
    }

    $el.trigger("pat-inject-success");
  },
  _onInjectSuccess: function _onInjectSuccess($el, cfgs, ev) {
    var _this3 = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var data, sources$, title;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              data = ev && ev.jqxhr && ev.jqxhr.responseText;

              if (data) {
                _context.next = 4;
                break;
              }

              log.warn("No response content, aborting", ev);
              return _context.abrupt("return");

            case 4:
              if (cfgs[0].source === "none") {
                // Special case, we want to call something, but we don't want to inject anything
                data = "";
              }

              jquery__WEBPACK_IMPORTED_MODULE_2___default.a.each(cfgs[0].hooks || [], function (idx, hook) {
                return $el.trigger("pat-inject-hook-" + hook);
              });

              _this3.stopBubblingFromRemovedElement($el, cfgs, ev);

              _context.next = 9;
              return _this3.callTypeHandler(cfgs[0].dataType, "sources", $el, [cfgs, data, ev]);

            case 9:
              sources$ = _context.sent;

              if (sources$ && sources$[sources$.length - 1] && sources$[sources$.length - 1][0] && sources$[sources$.length - 1][0].nodeName == "TITLE") {
                title = sources$[sources$.length - 1];
              }

              cfgs.forEach(function (cfg, idx1) {
                var perform_inject = function perform_inject() {
                  if (cfg.target != "none") cfg.$target.each(function (idx2, target) {
                    _this3._performInjection(target, $el, sources$[idx1], cfg, ev.target, title);
                  });
                };

                if (cfg.processDelay) {
                  setTimeout(function () {
                    return perform_inject();
                  }, cfg.processDelay);
                } else {
                  perform_inject();
                }
              });

              if (cfgs[0].nextHref && $el.is("a")) {
                // In case next-href is specified the anchor's href will
                // be set to it after the injection is triggered.
                $el.attr({
                  href: cfgs[0].nextHref.replace(/&amp;/g, "&")
                });

                _this3.destroy($el);
              }

              $el.off("pat-ajax-success.pat-inject");
              $el.off("pat-ajax-error.pat-inject");

            case 15:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }))();
  },
  _onInjectError: function _onInjectError($el, cfgs, event) {
    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
      var _document$querySelect;

      var explanation, fallback, status, timestamp, url_params, fallback_url, fallback_response, msg_attr;
      return regeneratorRuntime.wrap(function _callee2$(_context2) {
        while (1) {
          switch (_context2.prev = _context2.next) {
            case 0:
              explanation = "";
              status = event.jqxhr.status;
              timestamp = new Date();

              if (status % 100 == 4) {
                explanation = "Sorry! We couldn't find the page to load. Please make a screenshot and send it to support. Thank you!";
              } else if (status % 100 == 5) {
                explanation = "I am very sorry! There was an error at the server. Please make a screenshot and contact support. Thank you!";
              } else if (status == 0) {
                explanation = "It seems, the server is down. Please make a screenshot and contact support. Thank you!";
              }

              url_params = new URLSearchParams(window.location.search);
              fallback_url = (_document$querySelect = document.querySelector("meta[name=pat-inject-status-".concat(status, "]"))) === null || _document$querySelect === void 0 ? void 0 : _document$querySelect.getAttribute("content", false);

              if (!(fallback_url && url_params.get("pat-inject-errorhandler.off") === null)) {
                _context2.next = 20;
                break;
              }

              _context2.prev = 7;
              _context2.next = 10;
              return fetch(fallback_url, {
                method: "GET"
              });

            case 10:
              fallback_response = _context2.sent;
              fallback = document.createElement("html");
              _context2.next = 14;
              return fallback_response.text();

            case 14:
              fallback.innerHTML = _context2.sent;
              fallback = fallback.querySelector("body");
              _context2.next = 20;
              break;

            case 18:
              _context2.prev = 18;
              _context2.t0 = _context2["catch"](7);

            case 20:
              // clean up
              cfgs.forEach(function (cfg) {
                if ("$injected" in cfg) cfg.$injected.remove();
              });
              $el.off("pat-ajax-success.pat-inject");
              $el.off("pat-ajax-error.pat-inject");

              if (fallback) {
                document.body.innerHTML = fallback.innerHTML;
              } else {
                msg_attr = fallback || "".concat(explanation, " Status is ").concat(status, " ").concat(event.jqxhr.statusText, ", time was ").concat(timestamp, ". You can click to close this.");
                jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").attr("data-error-message", msg_attr);
                jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").on("click", function () {
                  jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").removeAttr("data-error-message");
                  window.location.href = window.location.href; // reload
                });
              }

            case 24:
            case "end":
              return _context2.stop();
          }
        }
      }, _callee2, null, [[7, 18]]);
    }))();
  },
  execute: function execute(cfgs, $el) {
    /* Actually execute the injection.
     *
     * Either by making an ajax request or by spoofing an ajax
     * request when the content is readily available in the current page.
     */
    // get a kinda deep copy, we scribble on it
    cfgs = cfgs.map(function (cfg) {
      return jquery__WEBPACK_IMPORTED_MODULE_2___default.a.extend({}, cfg);
    });

    if (!this.verifyConfig(cfgs)) {
      return;
    }

    if (!this.askForConfirmation(cfgs)) {
      return;
    }

    if ($el.data("pat-inject-triggered")) {
      // Prevent double triggers;
      return;
    }

    $el.data("pat-inject-triggered", true); // possibility for spinners on targets

    underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].chain(cfgs).filter(underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].property("loadingClass")).each(function (cfg) {
      if (cfg.target != "none") cfg.$target.addClass(cfg.loadingClass);
    }); // Put the execute class on the elem that has pat inject on it


    underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].chain(cfgs).filter(underscore__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].property("loadingClass")).each(function (cfg) {
      return $el.addClass(cfg.executingClass);
    });

    $el.on("pat-ajax-success.pat-inject", this._onInjectSuccess.bind(this, $el, cfgs));
    $el.on("pat-ajax-error.pat-inject", this._onInjectError.bind(this, $el, cfgs));
    $el.on("pat-ajax-success.pat-inject pat-ajax-error.pat-inject", function () {
      return $el.removeData("pat-inject-triggered");
    });

    if (cfgs[0].url.length) {
      _ajax_ajax__WEBPACK_IMPORTED_MODULE_4__[/* default */ "a"].request($el, {
        url: cfgs[0].url
      });
    } else {
      // If there is no url specified, then content is being fetched
      // from the same page.
      // No need to do an ajax request for this, so we spoof the ajax
      // event.
      $el.trigger({
        type: "pat-ajax-success",
        jqxhr: {
          responseText: jquery__WEBPACK_IMPORTED_MODULE_2___default()("body").html()
        }
      });
    }
  },
  _inject: function _inject(trigger, $source, $target, cfg) {
    // action to jquery method mapping, except for "content"
    // and "element"
    var method = {
      contentbefore: "prepend",
      contentafter: "append",
      elementbefore: "before",
      elementafter: "after"
    }[cfg.action];

    if (cfg.source === "none") {
      $target.replaceWith("");
      return true;
    }

    if ($source.length === 0) {
      log.warn("Aborting injection, source not found:", $source);
      jquery__WEBPACK_IMPORTED_MODULE_2___default()(trigger).trigger("pat-inject-missingSource", {
        url: cfg.url,
        selector: cfg.source
      });
      return false;
    }

    if (cfg.target === "none") // Special case. Don't do anything, we don't want any result
      return true;

    if ($target.length === 0) {
      log.warn("Aborting injection, target not found:", $target);
      jquery__WEBPACK_IMPORTED_MODULE_2___default()(trigger).trigger("pat-inject-missingTarget", {
        selector: cfg.target
      });
      return false;
    }

    if (cfg.action === "content") {
      $target.empty().append($source);
    } else if (cfg.action === "element") {
      $target.replaceWith($source);
    } else {
      $target[method]($source);
    }

    return true;
  },
  _sourcesFromHtml: function _sourcesFromHtml(html, url, sources) {
    var $html = this._parseRawHtml(html, url);

    return sources.map(function (source) {
      if (source === "body") {
        source = "#__original_body";
      }

      if (source === "none") {
        return jquery__WEBPACK_IMPORTED_MODULE_2___default()("<!-- -->");
      }

      var $source = $html.find(source);

      if ($source.length === 0) {
        if (source != "title") {
          log.warn("No source elements for selector:", source, $html);
        }
      }

      $source.find('a[href^="#"]').each(function (idx, el_) {
        var href = el_.getAttribute("href");

        if (href.indexOf("#{1}") !== -1) {
          // We ignore hrefs containing #{1} because they're not
          // valid and only applicable in the context of
          // pat-clone.
          return;
        } // Skip in-document links pointing to an id that is inside
        // this fragment.


        if (href.length === 1) {
          // Special case for top-of-page links
          el_.href = url;
        } else if (!$source.find(href).length) {
          el_.href = url + href;
        }
      });
      return $source;
    });
  },
  _rebaseAttrs: {
    A: "href",
    FORM: "action",
    IMG: "data-pat-inject-rebase-src",
    OBJECT: "data",
    SOURCE: "data-pat-inject-rebase-src",
    VIDEO: "data-pat-inject-rebase-src"
  },
  _rebaseOptions: {
    "calendar": ["url", "event-sources"],
    "collapsible": ["load-content"],
    "date-picker": ["i18n"],
    "datetime-picker": ["i18n"],
    "inject": ["url"]
  },
  _rebaseHTML: function _rebaseHTML(base, html) {
    var _this4 = this;

    if (html === "") {
      // Special case, source is none
      return "";
    }

    var $page = jquery__WEBPACK_IMPORTED_MODULE_2___default()(html.replace(/(\s)(src\s*)=/gi, '$1src="" data-pat-inject-rebase-$2=').trim()).wrapAll("<div>").parent();
    $page.find(Object.keys(this._rebaseAttrs).join(",")).each(function (idx, el_) {
      var $el_ = jquery__WEBPACK_IMPORTED_MODULE_2___default()(el_);
      var attrName = _this4._rebaseAttrs[el_.tagName];
      var value = $el_.attr(attrName);

      if (value && value.slice(0, 2) !== "@@" && value[0] !== "#" && value.slice(0, 7) !== "mailto:" && value.slice(0, 4) !== "tel:" && value.slice(0, 4) !== "fax:" && value.slice(0, 7) !== "callto:" && value.slice(0, 10) !== "ts3server:" && value.slice(0, 6) !== "teams:" && value.slice(0, 11) !== "javascript:") {
        value = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].rebaseURL(base, value);
        $el_.attr(attrName, value);
      }
    });

    for (var _i = 0, _Object$entries = Object.entries(this._rebaseOptions); _i < _Object$entries.length; _i++) {
      var _Object$entries$_i = _slicedToArray(_Object$entries[_i], 2),
          pattern_name = _Object$entries$_i[0],
          opts = _Object$entries$_i[1];

      var _iterator2 = _createForOfIteratorHelper(_core_dom__WEBPACK_IMPORTED_MODULE_5__[/* default */ "a"].querySelectorAllAndMe($page[0], "[data-pat-".concat(pattern_name, "]"))),
          _step2;

      try {
        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          var el_ = _step2.value;
          var val = el_.getAttribute("data-pat-".concat(pattern_name), false);

          if (val) {
            var pattern = _core_registry__WEBPACK_IMPORTED_MODULE_8__[/* default */ "a"].patterns[pattern_name];
            var pattern_parser = pattern === null || pattern === void 0 ? void 0 : pattern.parser;

            if (!pattern_parser) {
              continue;
            }

            var options = pattern_parser._parse(val);

            var changed = false;

            var _iterator3 = _createForOfIteratorHelper(opts),
                _step3;

            try {
              for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
                var opt = _step3.value;
                var _val = options[opt];

                if (!_val) {
                  continue;
                }

                changed = true;

                if (Array.isArray(_val)) {
                  options[opt] = _val.map(function (it) {
                    return _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].rebaseURL(base, it);
                  });
                } else {
                  options[opt] = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].rebaseURL(base, _val);
                }
              }
            } catch (err) {
              _iterator3.e(err);
            } finally {
              _iterator3.f();
            }

            if (changed) {
              el_.setAttribute("data-pat-".concat(pattern_name), JSON.stringify(options));
            }
          }
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }
    } // XXX: IE8 changes the order of attributes in html. The following
    // lines move data-pat-inject-rebase-src to src.


    $page.find("[data-pat-inject-rebase-src]").each(function (id, el_) {
      var $el = jquery__WEBPACK_IMPORTED_MODULE_2___default()(el_);
      $el.attr("src", $el.attr("data-pat-inject-rebase-src")).removeAttr("data-pat-inject-rebase-src");
    });
    return $page.html().replace(/src="" data-pat-inject-rebase-/g, "").trim();
  },
  _parseRawHtml: function _parseRawHtml(html, url) {
    url = url || ""; // remove script tags and head and replace body by a div

    var title = html.match(/\<title\>(.*)\<\/title\>/);
    var clean_html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "").replace(/<head\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/head>/gi, "").replace(/<body([^>]*?)>/gi, '<div id="__original_body">').replace(/<\/body([^>]*?)>/gi, "</div>");

    if (title && title.length == 2) {
      clean_html = title[0] + clean_html;
    }

    try {
      clean_html = this._rebaseHTML(url, clean_html);
    } catch (e) {
      log.error("Error rebasing urls", e);
    }

    var $html = jquery__WEBPACK_IMPORTED_MODULE_2___default()("<div/>").html(clean_html);

    if ($html.children().length === 0) {
      log.warn("Parsing html resulted in empty jquery object:", clean_html);
    }

    return $html;
  },
  // XXX: hack
  _initAutoloadVisible: function _initAutoloadVisible($el, cfgs) {
    var _this5 = this;

    if ($el.data("pat-inject-autoloaded")) {
      // ignore executed autoloads
      return false;
    }

    var $scrollable = $el.parents(":scrollable"); // function to trigger the autoload and mark as triggered

    var trigger = function trigger(event) {
      if ($el.data("pat-inject-autoloaded")) {
        return false;
      }

      $el.data("pat-inject-autoloaded", true);

      _this5.onTrigger({
        currentTarget: $el[0]
      });

      event && event.preventDefault();
      return true;
    };

    $el.click(trigger); // Use case 1: a (heigh-constrained) scrollable parent

    if ($scrollable.length) {
      // if scrollable parent and visible -> trigger it
      // we only look at the closest scrollable parent, no nesting
      // Check visibility for scrollable
      var checkVisibility = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].debounce(function () {
        if ($el.data("patterns.autoload") || !jquery__WEBPACK_IMPORTED_MODULE_2___default.a.contains(document, $el[0])) {
          return false;
        }

        if (!$el.is(":visible")) {
          return false;
        } // check if the target element still exists. Otherwise halt and catch fire


        var target = ($el.data("pat-inject")[0].target || cfgs[0].defaultSelector).replace(/::element/, "");

        if (target && target !== "self" && jquery__WEBPACK_IMPORTED_MODULE_2___default()(target).length === 0) {
          return false;
        }

        var reltop = $el.safeOffset().top - $scrollable.safeOffset().top - 1000,
            doTrigger = reltop <= $scrollable.innerHeight();

        if (doTrigger) {
          // checkVisibility was possibly installed as a scroll
          // handler and has now served its purpose -> remove
          jquery__WEBPACK_IMPORTED_MODULE_2___default()($scrollable[0]).off("scroll", checkVisibility);
          jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).off("resize.pat-autoload", checkVisibility);
          return trigger();
        }

        return false;
      }, 100);

      if (checkVisibility()) {
        return true;
      } // wait to become visible - again only immediate scrollable parent


      jquery__WEBPACK_IMPORTED_MODULE_2___default()($scrollable[0]).on("scroll", checkVisibility);
      jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).on("resize.pat-autoload", checkVisibility);
    } else {
      // Use case 2: scrolling the entire page
      // Check visibility for non-scrollable
      var _checkVisibility = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].debounce(function () {
        if ($el.parents(":scrollable").length) {
          // Because of a resize the element has now a scrollable parent
          // and we should reset the correct event
          jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).off(".pat-autoload", _checkVisibility);
          return _this5._initAutoloadVisible($el);
        }

        if ($el.data("patterns.autoload")) {
          return false;
        }

        if (!$el.is(":visible")) {
          return false;
        }

        if (!_core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].elementInViewport($el[0])) {
          return false;
        } // check if the target element still exists. Otherwise halt and catch fire


        var target = ($el.data("pat-inject")[0].target || cfgs[0].defaultSelector).replace(/::element/, "");

        if (target && target !== "self" && jquery__WEBPACK_IMPORTED_MODULE_2___default()(target).length === 0) {
          return false;
        }

        jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).off(".pat-autoload", _checkVisibility);
        return trigger();
      }, 100);

      if (_checkVisibility()) {
        return true;
      } // https://github.com/w3c/IntersectionObserver/tree/master/polyfill


      if (IntersectionObserver) {
        var observer = new IntersectionObserver(_checkVisibility);
        $el.each(function (idx, el) {
          return observer.observe(el);
        });
      } else {
        jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).on("resize.pat-autoload scroll.pat-autoload", _checkVisibility);
      }
    }

    return false;
  },
  _initIdleTrigger: function _initIdleTrigger($el, delay) {
    var _this6 = this;

    // XXX TODO: handle item removed from DOM
    var timeout = parseInt(delay, 10);
    var timer;

    var onTimeout = function onTimeout() {
      _this6.onTrigger({
        currentTarget: $el[0]
      });

      unsub();
      clearTimeout(timer);
    };

    var onInteraction = _core_utils__WEBPACK_IMPORTED_MODULE_9__[/* default */ "a"].debounce(function () {
      if (!document.body.contains($el[0])) {
        unsub();
        return;
      }

      clearTimeout(timer);
      timer = setTimeout(onTimeout, timeout);
    }, timeout);

    var unsub = function unsub() {
      ["scroll", "resize"].forEach(function (e) {
        return window.removeEventListener(e, onInteraction);
      });
      ["click", "keypress", "keyup", "mousemove", "touchstart", "touchend"].forEach(function (e) {
        return document.removeEventListener(e, onInteraction);
      });
    };

    onInteraction();
    ["scroll", "resize"].forEach(function (e) {
      return window.addEventListener(e, onInteraction);
    });
    ["click", "keypress", "keyup", "mousemove", "touchstart", "touchend"].forEach(function (e) {
      return document.addEventListener(e, onInteraction);
    });
  },
  // XXX: simple so far to see what the team thinks of the idea
  registerTypeHandler: function registerTypeHandler(type, handler) {
    this.handlers[type] = handler;
  },
  callTypeHandler: function callTypeHandler(type, fn, context, params) {
    var _this7 = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
      return regeneratorRuntime.wrap(function _callee3$(_context3) {
        while (1) {
          switch (_context3.prev = _context3.next) {
            case 0:
              type = type || "html";

              if (!(_this7.handlers[type] && jquery__WEBPACK_IMPORTED_MODULE_2___default.a.isFunction(_this7.handlers[type][fn]))) {
                _context3.next = 7;
                break;
              }

              _context3.next = 4;
              return _this7.handlers[type][fn].bind(_this7).apply(void 0, _toConsumableArray(params));

            case 4:
              return _context3.abrupt("return", _context3.sent);

            case 7:
              return _context3.abrupt("return", null);

            case 8:
            case "end":
              return _context3.stop();
          }
        }
      }, _callee3);
    }))();
  },
  handlers: {
    html: {
      sources: function sources(cfgs, data) {
        var sources = cfgs.map(function (cfg) {
          return cfg.source;
        });
        sources.push("title");
        return this._sourcesFromHtml(data, cfgs[0].url, sources);
      }
    }
  }
};
jquery__WEBPACK_IMPORTED_MODULE_2___default()(document).on("patterns-injected.inject", function (ev, cfg, trigger, injected) {
  /* Listen for the patterns-injected event.
   *
   * Remove the "loading-class" classes from all injection targets and
   * then scan the injected content for new patterns.
   */
  if (cfg && cfg.skipPatInjectHandler) {
    // Allow skipping this handler but still have other handlers in other
    // patterns listen to ``patterns-injected``.
    return;
  }

  if (cfg) {
    cfg.$target.removeClass(cfg.loadingClass); // Remove the executing class, add the executed class to the element with pat.inject on it.

    jquery__WEBPACK_IMPORTED_MODULE_2___default()(trigger).removeClass(cfg.executingClass).addClass(cfg.executedClass);
  }

  if (injected.nodeType !== TEXT_NODE && injected !== COMMENT_NODE) {
    _core_registry__WEBPACK_IMPORTED_MODULE_8__[/* default */ "a"].scan(injected, null, {
      type: "injection",
      element: trigger
    });
    jquery__WEBPACK_IMPORTED_MODULE_2___default()(injected).trigger("patterns-injected-scanned");
  }
});
jquery__WEBPACK_IMPORTED_MODULE_2___default()(window).on("popstate", function (event) {
  // popstate also triggers on traditional anchors
  if (!event.originalEvent.state && "replaceState" in history) {
    try {
      history.replaceState("anchor", "", document.location.href);
    } catch (e) {
      log.debug(e);
    }

    return;
  } // Not only change the URL, also reload the page.


  window.location.reload();
}); // this entry ensures that the initally loaded page can be reached with
// the back button

if ("replaceState" in history) {
  try {
    history.replaceState("pageload", "", document.location.href);
  } catch (e) {
    log.debug(e);
  }
}

_core_registry__WEBPACK_IMPORTED_MODULE_8__[/* default */ "a"].register(inject);
/* harmony default export */ __webpack_exports__["a"] = (inject);

/***/ }),

/***/ 29:
/***/ (function(module, exports) {

var g;

// This works in non-strict mode
g = (function() {
	return this;
})();

try {
	// This works if eval is allowed (see CSP)
	g = g || new Function("return this")();
} catch (e) {
	// This works if the window reference is available
	if (typeof window === "object") g = window;
}

// g can still be undefined, but nothing to do about it...
// We return undefined, instead of nothing here, so it's
// easier to handle this case. if(!global) { ...}

module.exports = g;


/***/ }),

/***/ 318:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _public_path__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(98);
/* harmony import */ var _public_path__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_public_path__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var modernizr__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(99);
/* harmony import */ var modernizr__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(modernizr__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var patternslib_src_core_registry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(9);
/* harmony import */ var patternslib_src_pat_ajax_ajax__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(35);
/* harmony import */ var patternslib_src_pat_auto_scale_auto_scale__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(102);
/* harmony import */ var patternslib_src_pat_checklist_checklist__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(103);
/* harmony import */ var patternslib_src_pat_collapsible_collapsible__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(104);
/* harmony import */ var patternslib_src_pat_depends_depends__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(106);
/* harmony import */ var patternslib_src_pat_display_time_display_time__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(74);
/* harmony import */ var patternslib_src_pat_equaliser_equaliser__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(107);
/* harmony import */ var patternslib_src_pat_inject_inject__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(23);
/* harmony import */ var patternslib_src_pat_legend_legend__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(108);
/* harmony import */ var patternslib_src_pat_masonry_masonry__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(109);
/* harmony import */ var patternslib_src_pat_navigation_navigation__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(110);
/* harmony import */ var patternslib_src_pat_sortable_sortable__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(111);
 // first import

 // Core


 // Pattern imports













window.jQuery = jquery__WEBPACK_IMPORTED_MODULE_2___default.a;
patternslib_src_core_registry__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].init();

/***/ }),

/***/ 35:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(6);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(4);
/* harmony import */ var _core_registry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(9);
/**
 * Patterns ajax - AJAX injection for forms and anchors
 *
 * Copyright 2012-2013 Florian Friesdorf
 * Copyright 2012-2013 Marko Durkovic
 */




var log = _core_logging__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].getLogger("pat.ajax");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"]("ajax");
parser.addArgument("url", function ($el) {
  return ($el.is("a") ? $el.attr("href") : $el.is("form") ? $el.attr("action") : "").split("#")[0];
});
jquery__WEBPACK_IMPORTED_MODULE_0___default.a.ajaxSetup({
  // Disable caching of AJAX responses
  cache: false
});
var xhrCount = {};

xhrCount.get = function (a) {
  return this[a] !== undefined ? this[a] : 0;
};

xhrCount.inc = function (a) {
  this[a] = this.get(a) + 1;
  return this.get(a);
};

var _ = {
  name: "ajax",
  trigger: ".pat-ajax",
  parser: parser,
  init: function init($el) {
    $el.off(".pat-ajax");
    $el.filter("a").on("click.pat-ajax", _.onTriggerEvents);
    $el.filter("form").on("submit.pat-ajax", _.onTriggerEvents).on("click.pat-ajax", "[type=submit]", _.onClickSubmit);
    $el.filter(":not(form,a)").each(function () {
      log.warn("Unsupported element:", this);
    });
    return $el;
  },
  destroy: function destroy($el) {
    $el.off(".pat-ajax");
  },
  onClickSubmit: function onClickSubmit(event) {
    var $form = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.target).parents("form").first(),
        name = event.target.name,
        value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.target).val(),
        data = {};

    if (name) {
      data[name] = value;
    }

    $form.data("pat-ajax.clicked-data", data);
  },
  onTriggerEvents: function onTriggerEvents(event) {
    if (event) {
      event.preventDefault();
    }

    _.request(jquery__WEBPACK_IMPORTED_MODULE_0___default()(this));
  },
  request: function request($el, opts) {
    return $el.each(function () {
      _._request(jquery__WEBPACK_IMPORTED_MODULE_0___default()(this), opts);
    });
  },
  _request: function _request($el, opts) {
    var cfg = _.parser.parse($el, opts),
        onError = function onError(jqxhr, status, error) {
      // error can also stem from a javascript
      // exception, not only errors described in the
      // jqxhr.
      log.error("load error for " + cfg.url + ":", error, jqxhr);
      $el.trigger({
        type: "pat-ajax-error",
        jqxhr: jqxhr
      });
    },
        seqNumber = xhrCount.inc(cfg.url),
        onSuccess = function onSuccess(data, status, jqxhr) {
      log.debug("success: jqxhr:", jqxhr);

      if (seqNumber === xhrCount.get(cfg.url)) {
        // if this url is requested multiple time, only return the last result
        $el.trigger({
          type: "pat-ajax-success",
          jqxhr: jqxhr
        });
      } else {// ignore
      }
    },
        temp = $el.data("pat-ajax.clicked-data"),
        clickedData = temp ? jquery__WEBPACK_IMPORTED_MODULE_0___default.a.param(temp) : "",
        args = {
      context: $el,
      data: [$el.serialize(), clickedData].filter(Boolean).join("&"),
      url: cfg.url,
      method: $el.attr("method") ? $el.attr("method") : "GET"
    };

    if ($el.is("form") && $el.attr("method") && $el.attr("method").toUpperCase() == "POST") {
      var formdata = new FormData($el[0]);

      for (var key in temp) {
        formdata.append(key, temp[key]);
      }

      args["method"] = "POST";
      args["data"] = formdata;
      args["cache"] = false;
      args["contentType"] = false;
      args["processData"] = false;
      args["type"] = "POST";
    }

    $el.removeData("pat-ajax.clicked-data");
    log.debug("request:", args, $el[0]); // Make it happen

    var ajax_deferred = jquery__WEBPACK_IMPORTED_MODULE_0___default.a.ajax(args);
    if (ajax_deferred) ajax_deferred.done(onSuccess).fail(onError);
  }
};
_core_registry__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].register(_);
/* harmony default export */ __webpack_exports__["a"] = (_);

/***/ }),

/***/ 38:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

/**
 * @license
 * Patterns @VERSION@ jquery-ext - various jQuery extensions
 *
 * Copyright 2011 Humberto Sermeño
 */

var methods = {
  init: function init(options) {
    var settings = {
      time: 3
      /* time it will wait before moving to "timeout" after a move event */
      ,
      initialTime: 8
      /* time it will wait before first adding the "timeout" class */
      ,
      exceptionAreas: []
      /* IDs of elements that, if the mouse is over them, will reset the timer */

    };
    return this.each(function () {
      var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
          data = $this.data("timeout");

      if (!data) {
        if (options) {
          jquery__WEBPACK_IMPORTED_MODULE_0___default.a.extend(settings, options);
        }

        $this.data("timeout", {
          lastEvent: new Date(),
          trueTime: settings.time,
          time: settings.initialTime,
          untouched: true,
          inExceptionArea: false
        });
        $this.on("mouseover.timeout", methods.mouseMoved);
        $this.on("mouseenter.timeout", methods.mouseMoved);
        jquery__WEBPACK_IMPORTED_MODULE_0___default()(settings.exceptionAreas).each(function () {
          $this.find(this).live("mouseover.timeout", {
            parent: $this
          }, methods.enteredException).live("mouseleave.timeout", {
            parent: $this
          }, methods.leftException);
        });
        if (settings.initialTime > 0) $this.timeout("startTimer");else $this.addClass("timeout");
      }
    });
  },
  enteredException: function enteredException(event) {
    var data = event.data.parent.data("timeout");
    data.inExceptionArea = true;
    event.data.parent.data("timeout", data);
    event.data.parent.trigger("mouseover");
  },
  leftException: function leftException(event) {
    var data = event.data.parent.data("timeout");
    data.inExceptionArea = false;
    event.data.parent.data("timeout", data);
  },
  destroy: function destroy() {
    return this.each(function () {
      var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
          data = $this.data("timeout");
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(window).off(".timeout");
      data.timeout.remove();
      $this.removeData("timeout");
    });
  },
  mouseMoved: function mouseMoved() {
    var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
        data = $this.data("timeout");

    if ($this.hasClass("timeout")) {
      $this.removeClass("timeout");
      $this.timeout("startTimer");
    } else if (data.untouched) {
      data.untouched = false;
      data.time = data.trueTime;
    }

    data.lastEvent = new Date();
    $this.data("timeout", data);
  },
  startTimer: function startTimer() {
    var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
        data = $this.data("timeout");

    var fn = function fn() {
      var data = $this.data("timeout");

      if (data && data.lastEvent) {
        if (data.inExceptionArea) {
          setTimeout(fn, Math.floor(data.time * 1000));
        } else {
          var now = new Date();
          var diff = Math.floor(data.time * 1000) - (now - data.lastEvent);

          if (diff > 0) {
            // the timeout has not ocurred, so set the timeout again
            setTimeout(fn, diff + 100);
          } else {
            // timeout ocurred, so set the class
            $this.addClass("timeout");
          }
        }
      }
    };

    setTimeout(fn, Math.floor(data.time * 1000));
  }
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.timeout = function (method) {
  if (methods[method]) {
    return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
  } else if (_typeof(method) === "object" || !method) {
    return methods.init.apply(this, arguments);
  } else {
    jquery__WEBPACK_IMPORTED_MODULE_0___default.a.error("Method " + method + " does not exist on jQuery.timeout");
  }
}; // Custom jQuery selector to find elements with scrollbars


jquery__WEBPACK_IMPORTED_MODULE_0___default.a.extend(jquery__WEBPACK_IMPORTED_MODULE_0___default.a.expr[":"], {
  scrollable: function scrollable(element) {
    var vertically_scrollable, horizontally_scrollable;
    if (jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflow") === "scroll" || jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflowX") === "scroll" || jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflowY") === "scroll") return true;
    vertically_scrollable = element.clientHeight < element.scrollHeight && (jquery__WEBPACK_IMPORTED_MODULE_0___default.a.inArray(jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflowY"), ["scroll", "auto"]) !== -1 || jquery__WEBPACK_IMPORTED_MODULE_0___default.a.inArray(jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflow"), ["scroll", "auto"]) !== -1);
    if (vertically_scrollable) return true;
    horizontally_scrollable = element.clientWidth < element.scrollWidth && (jquery__WEBPACK_IMPORTED_MODULE_0___default.a.inArray(jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflowX"), ["scroll", "auto"]) !== -1 || jquery__WEBPACK_IMPORTED_MODULE_0___default.a.inArray(jquery__WEBPACK_IMPORTED_MODULE_0___default()(element).css("overflow"), ["scroll", "auto"]) !== -1);
    return horizontally_scrollable;
  }
}); // Make Visible in scroll

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.makeVisibleInScroll = function (parent_id) {
  var absoluteParent = null;

  if (typeof parent_id === "string") {
    absoluteParent = jquery__WEBPACK_IMPORTED_MODULE_0___default()("#" + parent_id);
  } else if (parent_id) {
    absoluteParent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(parent_id);
  }

  return this.each(function () {
    var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this),
        parent;

    if (!absoluteParent) {
      parent = $this.parents(":scrollable");

      if (parent.length > 0) {
        parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(parent[0]);
      } else {
        parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(window);
      }
    } else {
      parent = absoluteParent;
    }

    var elemTop = $this.position().top;
    var elemBottom = $this.height() + elemTop;
    var viewTop = parent.scrollTop();
    var viewBottom = parent.height() + viewTop;

    if (elemTop < viewTop) {
      parent.scrollTop(elemTop);
    } else if (elemBottom > viewBottom - parent.height() / 2) {
      parent.scrollTop(elemTop - (parent.height() - $this.height()) / 2);
    }
  });
}; //Work around warning for jQuery 3.x:
//JQMIGRATE: jQuery.fn.offset() requires an element connected to a document


jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.safeOffset = function () {
  var docElem,
      elem = this[0],
      origin = {
    top: 0,
    left: 0
  };

  if (!elem || !elem.nodeType) {
    return origin;
  }

  docElem = (elem.ownerDocument || document).documentElement;

  if (!jquery__WEBPACK_IMPORTED_MODULE_0___default.a.contains(docElem, elem)) {
    return origin;
  }

  return jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.offset.apply(this, arguments);
}; //Make absolute location


jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.setPositionAbsolute = function (element, offsettop, offsetleft) {
  return this.each(function () {
    // set absolute location for based on the element passed
    // dynamically since every browser has different settings
    var $this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this);
    var thiswidth = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).width();
    var pos = element.safeOffset();
    var width = element.width();
    var height = element.height();
    var setleft = pos.left + width - thiswidth + offsetleft;
    var settop = pos.top + height + offsettop;
    $this.css({
      "z-index": 1,
      "position": "absolute",
      "marginLeft": 0,
      "marginTop": 0,
      "left": setleft + "px",
      "top": settop + "px",
      "width": thiswidth
    });
    $this.remove().appendTo("body").show();
  });
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.positionAncestor = function (selector) {
  var left = 0;
  var top = 0;
  this.each(function () {
    // check if current element has an ancestor matching a selector
    // and that ancestor is positioned
    var $ancestor = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).closest(selector);

    if ($ancestor.length && $ancestor.css("position") !== "static") {
      var $child = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this);
      var childMarginEdgeLeft = $child.safeOffset().left - parseInt($child.css("marginLeft"), 10);
      var childMarginEdgeTop = $child.safeOffset().top - parseInt($child.css("marginTop"), 10);
      var ancestorPaddingEdgeLeft = $ancestor.safeOffset().left + parseInt($ancestor.css("borderLeftWidth"), 10);
      var ancestorPaddingEdgeTop = $ancestor.safeOffset().top + parseInt($ancestor.css("borderTopWidth"), 10);
      left = childMarginEdgeLeft - ancestorPaddingEdgeLeft;
      top = childMarginEdgeTop - ancestorPaddingEdgeTop; // we have found the ancestor and computed the position
      // stop iterating

      return false;
    }
  });
  return {
    left: left,
    top: top
  };
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.findInclusive = function (selector) {
  return this.find("*").addBack().filter(selector);
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.slideIn = function (speed, easing, callback) {
  return this.animate({
    width: "show"
  }, speed, easing, callback);
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.slideOut = function (speed, easing, callback) {
  return this.animate({
    width: "hide"
  }, speed, easing, callback);
}; // case-insensitive :contains


jquery__WEBPACK_IMPORTED_MODULE_0___default.a.expr[":"].Contains = function (a, i, m) {
  return jquery__WEBPACK_IMPORTED_MODULE_0___default()(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};

jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn.scopedFind = function (selector) {
  /*  If the selector starts with an object id do a global search,
   *  otherwise do a local search.
   */
  if (selector.indexOf("#") === 0) {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()(selector);
  } else {
    return this.find(selector);
  }
};

/* unused harmony default export */ var _unused_webpack_default_export = (undefined);

/***/ }),

/***/ 4:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(2);
/* harmony import */ var _logging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6);
function _typeof2(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof2 = function _typeof2(obj) { return typeof obj; }; } else { _typeof2 = function _typeof2(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof2(obj); }

function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// Patterns argument parser




var ArgumentParser = /*#__PURE__*/function () {
  function ArgumentParser(name) {
    _classCallCheck(this, ArgumentParser);

    this.order = [];
    this.parameters = {};
    this.attribute = "data-pat-" + name;
    this.enum_values = {};
    this.enum_conflicts = [];
    this.groups = {};
    this.possible_groups = {};
    this.log = _logging__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].getLogger(name + ".parser");
    this.group_pattern = /([a-z][a-z0-9]*)-([A-Z][a-z0-0\-]*)/i;
    this.json_param_pattern = /^\s*{/i;
    this.named_param_pattern = /^\s*([a-z][a-z0-9\-]*)\s*:(.*)/i;
    this.token_pattern = /((["']).*?(?!\\)\2)|\s*(\S+)\s*/g;
  }

  _createClass(ArgumentParser, [{
    key: "_camelCase",
    value: function _camelCase(str) {
      return str.replace(/\-([a-z])/g, function (__, p1) {
        return p1.toUpperCase();
      });
    }
  }, {
    key: "addAlias",
    value: function addAlias(alias, original) {
      /* Add an alias for a previously added parser argument.
       *
       * Useful when you want to support both US and UK english argument
       * names.
       */
      if (this.parameters[original]) {
        this.parameters[original].alias = alias;
      } else {
        throw 'Attempted to add an alias "' + alias + '" for a non-existing parser argument "' + original + '".';
      }
    }
  }, {
    key: "addGroupToSpec",
    value: function addGroupToSpec(spec) {
      /* Determine wether an argument being parsed can be grouped and
       * update its specifications object accordingly.
       *
       * Internal method used by addArgument and addJSONArgument
       */
      var m = spec.name.match(this.group_pattern);

      if (m) {
        var group = m[1];
        var field = m[2];

        if (group in this.possible_groups) {
          var first_spec = this.possible_groups[group];
          var first_name = first_spec.name.match(this.group_pattern)[2];
          first_spec.group = group;
          first_spec.dest = first_name;
          this.groups[group] = new ArgumentParser();
          this.groups[group].addArgument(first_name, first_spec.value, first_spec.choices, first_spec.multiple);
          delete this.possible_groups[group];
        }

        if (group in this.groups) {
          this.groups[group].addArgument(field, spec.value, spec.choices, spec.multiple);
          spec.group = group;
          spec.dest = field;
        } else {
          this.possible_groups[group] = spec;
          spec.dest = this._camelCase(spec.name);
        }
      }

      return spec;
    }
  }, {
    key: "addJSONArgument",
    value: function addJSONArgument(name, default_value) {
      /* Add an argument where the value is provided in JSON format.
       *
       * This is a different usecase than specifying all arguments to
       * the data-pat-... attributes in JSON format, and instead is part
       * of the normal notation except that a value is in JSON instead of
       * for example a string.
       */
      this.order.push(name);
      this.parameters[name] = this.addGroupToSpec({
        name: name,
        value: default_value,
        dest: name,
        group: null,
        type: "json"
      });
    }
  }, {
    key: "addArgument",
    value: function addArgument(name, default_value, choices, multiple) {
      var spec = {
        name: name,
        value: multiple && !Array.isArray(default_value) ? [default_value] : default_value,
        multiple: multiple,
        dest: name,
        group: null
      };

      if (choices && Array.isArray(choices) && choices.length) {
        spec.choices = choices;
        spec.type = this._typeof(choices[0]);

        var _iterator = _createForOfIteratorHelper(choices),
            _step;

        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var choice = _step.value;

            if (this.enum_conflicts.indexOf(choice) !== -1) {
              continue;
            } else if (choice in this.enum_values) {
              this.enum_conflicts.push(choice);
              delete this.enum_values[choice];
            } else {
              this.enum_values[choice] = name;
            }
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }
      } else if (typeof spec.value === "string" && spec.value.slice(0, 1) === "$") {
        spec.type = this.parameters[spec.value.slice(1)].type;
      } else {
        // Note that this will get reset by _defaults if default_value is a function.
        spec.type = this._typeof(multiple ? spec.value[0] : spec.value);
      }

      this.order.push(name);
      this.parameters[name] = this.addGroupToSpec(spec);
    }
  }, {
    key: "_typeof",
    value: function _typeof(obj) {
      if (obj === null) {
        return "null";
      }

      return _typeof2(obj);
    }
  }, {
    key: "_coerce",
    value: function _coerce(name, value) {
      var spec = this.parameters[name];
      if (_typeof2(value) !== spec.type) try {
        switch (spec.type) {
          case "json":
            value = JSON.parse(value);
            break;

          case "boolean":
            if (typeof value === "string") {
              value = value.toLowerCase();
              var num = parseInt(value, 10);
              if (!isNaN(num)) value = !!num;else value = value === "true" || value === "y" || value === "yes" || value === "y";
            } else if (typeof value === "number") {
              value = !!value;
            } else {
              throw "Cannot convert value for " + name + " to boolean";
            }

            break;

          case "number":
            if (typeof value === "string") {
              value = parseInt(value, 10);

              if (isNaN(value)) {
                throw "Cannot convert value for " + name + " to number";
              }
            } else if (typeof value === "boolean") {
              value = value + 0;
            } else {
              throw "Cannot convert value for " + name + " to number";
            }

            break;

          case "string":
            value = value.toString();
            break;

          case "null": // Missing default values

          case "undefined":
            break;

          default:
            throw "Do not know how to convert value for " + name + " to " + spec.type;
        }
      } catch (e) {
        this.log.warn(e);
        return null;
      }

      if (spec.choices && spec.choices.indexOf(value) === -1) {
        this.log.warn("Illegal value for " + name + ": " + value);
        return null;
      }

      return value;
    }
  }, {
    key: "_set",
    value: function _set(opts, name, value) {
      if (!(name in this.parameters)) {
        this.log.debug("Ignoring value for unknown argument " + name);
        return;
      }

      var spec = this.parameters[name];
      var parts;

      if (spec.multiple) {
        if (typeof value === "string") {
          parts = value.split(/,+/);
        } else {
          parts = value;
        }

        value = [];

        var _iterator2 = _createForOfIteratorHelper(parts),
            _step2;

        try {
          for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
            var part = _step2.value;

            var v = this._coerce(name, part.trim());

            if (v !== null) {
              value.push(v);
            }
          }
        } catch (err) {
          _iterator2.e(err);
        } finally {
          _iterator2.f();
        }
      } else {
        value = this._coerce(name, value);

        if (value === null) {
          return;
        }
      }

      opts[name] = value;
    }
  }, {
    key: "_split",
    value: function _split(text) {
      var tokens = [];
      text.replace(this.token_pattern, function (match, quoted, __, simple) {
        if (quoted) {
          tokens.push(quoted);
        } else if (simple) {
          tokens.push(simple);
        }
      });
      return tokens;
    }
  }, {
    key: "_parseExtendedNotation",
    value: function _parseExtendedNotation(argstring) {
      var _this = this;

      var opts = {};
      var parts = argstring.replace(/;;/g, "\0x1f").replace(/&amp;/g, "&amp\0x1f").split(/;/).map(function (el) {
        return el.replace(new RegExp("\0x1f", "g"), ";");
      });

      var _iterator3 = _createForOfIteratorHelper(parts),
          _step3;

      try {
        var _loop = function _loop() {
          var part = _step3.value;

          if (!part) {
            return "continue";
          }

          var matches = part.match(_this.named_param_pattern);

          if (!matches) {
            _this.log.warn("Invalid parameter: " + part + ": " + argstring);

            return "continue";
          }

          var name = matches[1];
          var value = matches[2].trim();
          var arg = Object.values(_this.parameters).filter(function (it) {
            return it.alias === name;
          });
          var is_alias = arg.length === 1;

          if (is_alias) {
            _this._set(opts, arg[0].name, value);
          } else if (name in _this.parameters) {
            _this._set(opts, name, value);
          } else if (name in _this.groups) {
            var subopt = _this.groups[name]._parseShorthandNotation(value);

            for (var field in subopt) {
              _this._set(opts, name + "-" + field, subopt[field]);
            }
          } else {
            _this.log.warn("Unknown named parameter " + matches[1]);

            return "continue";
          }
        };

        for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
          var _ret = _loop();

          if (_ret === "continue") continue;
        }
      } catch (err) {
        _iterator3.e(err);
      } finally {
        _iterator3.f();
      }

      return opts;
    }
  }, {
    key: "_parseShorthandNotation",
    value: function _parseShorthandNotation(parameter) {
      var parts = this._split(parameter);

      var opts = {};
      var i = 0;

      while (parts.length) {
        var part = parts.shift().trim();
        var sense = void 0;
        var flag = void 0;
        var positional = true;

        if (part.slice(0, 3) === "no-") {
          sense = false;
          flag = part.slice(3);
        } else {
          sense = true;
          flag = part;
        }

        if (flag in this.parameters && this.parameters[flag].type === "boolean") {
          positional = false;

          this._set(opts, flag, sense);
        } else if (flag in this.enum_values) {
          positional = false;

          this._set(opts, this.enum_values[flag], flag);
        } else if (positional) this._set(opts, this.order[i], part);else {
          parts.unshift(part);
          break;
        }

        i++;

        if (i >= this.order.length) {
          break;
        }
      }

      if (parts.length) this.log.warn("Ignore extra arguments: " + parts.join(" "));
      return opts;
    }
  }, {
    key: "_parse",
    value: function _parse(parameter) {
      if (!parameter) {
        return {};
      }

      if (parameter.match(this.json_param_pattern)) {
        try {
          return JSON.parse(parameter);
        } catch (e) {
          this.log.warn("Invalid JSON argument found: " + parameter);
        }
      }

      if (parameter.match(this.named_param_pattern)) {
        return this._parseExtendedNotation(parameter);
      }

      var sep = parameter.indexOf(";");

      if (sep === -1) {
        return this._parseShorthandNotation(parameter);
      }

      var opts = this._parseShorthandNotation(parameter.slice(0, sep));

      var extended = this._parseExtendedNotation(parameter.slice(sep + 1));

      for (var name in extended) {
        opts[name] = extended[name];
      }

      return opts;
    }
  }, {
    key: "_defaults",
    value: function _defaults($el) {
      var result = {};

      for (var name in this.parameters) {
        if (typeof this.parameters[name].value === "function") try {
          result[name] = this.parameters[name].value($el, name);
          this.parameters[name].type = _typeof2(result[name]);
        } catch (e) {
          this.log.error("Default function for " + name + " failed.");
        } else result[name] = this.parameters[name].value;
      }

      return result;
    }
  }, {
    key: "_cleanupOptions",
    value: function _cleanupOptions(options) {
      // Resolve references
      for (var _i = 0, _Object$keys = Object.keys(options); _i < _Object$keys.length; _i++) {
        var name = _Object$keys[_i];
        var spec = this.parameters[name];
        if (spec === undefined) continue;
        if (options[name] === spec.value && typeof spec.value === "string" && spec.value.slice(0, 1) === "$") options[name] = options[spec.value.slice(1)];
      } // Move options into groups and do renames


      for (var _i2 = 0, _Object$keys2 = Object.keys(options); _i2 < _Object$keys2.length; _i2++) {
        var _name = _Object$keys2[_i2];
        var _spec = this.parameters[_name];
        var target = void 0;
        if (_spec === undefined) continue;

        if (_spec.group) {
          if (_typeof2(options[_spec.group]) !== "object") options[_spec.group] = {};
          target = options[_spec.group];
        } else {
          target = options;
        }

        if (_spec.dest !== _name) {
          target[_spec.dest] = options[_name];
          delete options[_name];
        }
      }

      return options;
    }
  }, {
    key: "parse",
    value: function parse($el, options, multiple, inherit) {
      if (!$el.jquery) {
        $el = jquery__WEBPACK_IMPORTED_MODULE_0___default()($el);
      }

      if (typeof options === "boolean" && multiple === undefined) {
        // Fix argument order: ``multiple`` passed instead of ``options``.
        multiple = options;
        options = {};
      }

      inherit = inherit !== false;
      var stack = inherit ? [[this._defaults($el)]] : [[{}]];
      var $possible_config_providers;
      var final_length = 1;
      /*
       * XXX this is a workaround for:
       * - https://github.com/Patternslib/Patterns/issues/393
       *
       * Prevents the parser to pollute the pat-modal configuration
       * with data-pat-inject elements define in a `.pat-modal` parent element.
       *
       *  Probably this function should be completely revisited, see:
       * - https://github.com/Patternslib/Patterns/issues/627
       *
       */

      if (!inherit || $el.hasClass("pat-modal") && this.attribute === "data-pat-inject") {
        $possible_config_providers = $el;
      } else {
        $possible_config_providers = $el.parents("[" + this.attribute + "]").addBack();
      }

      var _iterator4 = _createForOfIteratorHelper($possible_config_providers),
          _step4;

      try {
        for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
          var provider = _step4.value;
          var frame = void 0;
          var data = jquery__WEBPACK_IMPORTED_MODULE_0___default()(provider).attr(this.attribute);

          if (!data) {
            continue;
          }

          var _parse = this._parse.bind(this);

          if (data.match(/&&/)) {
            frame = data.split(/\s*&&\s*/).map(_parse);
          } else {
            frame = [_parse(data)];
          }

          final_length = Math.max(frame.length, final_length);
          stack.push(frame);
        }
      } catch (err) {
        _iterator4.e(err);
      } finally {
        _iterator4.f();
      }

      if (_typeof2(options) === "object") {
        if (Array.isArray(options)) {
          stack.push(options);
          final_length = Math.max(options.length, final_length);
        } else stack.push([options]);
      }

      if (!multiple) {
        final_length = 1;
      }

      var results = _utils_js__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].removeDuplicateObjects(_utils_js__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].mergeStack(stack, final_length)).map(this._cleanupOptions.bind(this));
      return multiple ? results : results[0];
    }
  }]);

  return ArgumentParser;
}(); // BBB


ArgumentParser.prototype.add_argument = ArgumentParser.prototype.addArgument;
/* harmony default export */ __webpack_exports__["a"] = (ArgumentParser);

/***/ }),

/***/ 5:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXTERNAL MODULE: ./node_modules/regenerator-runtime/runtime.js
var runtime = __webpack_require__(19);

// EXTERNAL MODULE: ./node_modules/jquery/dist/jquery.js-exposed
var jquery_js_exposed = __webpack_require__(0);
var jquery_js_exposed_default = /*#__PURE__*/__webpack_require__.n(jquery_js_exposed);

// EXTERNAL MODULE: ./src/patternslib/src/core/registry.js
var registry = __webpack_require__(9);

// EXTERNAL MODULE: ./src/patternslib/src/core/logging.js
var logging = __webpack_require__(6);

// CONCATENATED MODULE: ./src/patternslib/src/core/mockup-parser.js

var parser = {
  getOptions: function getOptions($el, patternName, options) {
    /* This is the Mockup parser. An alternative parser for Patternslib
     * patterns.
     *
     * NOTE: Use of the Mockup parser is discouraged and is added here for
     * legacy support for the Plone Mockup project.
     *
     * It parses a DOM element for pattern configuration options.
     */
    options = options || {}; // get options from parent element first, stop if element tag name is 'body'

    if ($el.length !== 0 && !jquery_js_exposed_default.a.nodeName($el[0], "body")) {
      options = this.getOptions($el.parent(), patternName, options);
    } // collect all options from element


    var elOptions = {};

    if ($el.length !== 0) {
      elOptions = $el.data("pat-" + patternName);

      if (elOptions) {
        // parse options if string
        if (typeof elOptions === "string") {
          var tmpOptions = {};
          jquery_js_exposed_default.a.each(elOptions.split(";"), function (i, item) {
            item = item.split(":");
            item.reverse();
            var key = item.pop();
            key = key.replace(/^\s+|\s+$/g, ""); // trim

            item.reverse();
            var value = item.join(":");
            value = value.replace(/^\s+|\s+$/g, ""); // trim

            tmpOptions[key] = value;
          });
          elOptions = tmpOptions;
        }
      }
    }

    return jquery_js_exposed_default.a.extend(true, {}, options, elOptions);
  }
};
/* harmony default export */ var mockup_parser = (parser);
// CONCATENATED MODULE: ./src/patternslib/src/core/base.js
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

/**
 * A Base pattern for creating scoped patterns. It's similar to Backbone's
 * Model class. The advantage of this approach is that each instance of a
 * pattern has its own local scope (closure).
 *
 * A new instance is created for each DOM element on which a pattern applies.
 *
 * You can assign values, such as $el, to `this` for an instance and they
 * will remain unique to that instance.
 *
 * Older Patternslib patterns on the other hand have a single global scope for
 * all DOM elements.
 */
 // needed for ``await`` support





var log = logging["a" /* default */].getLogger("Patternslib Base");

var base_initBasePattern = function initBasePattern($el, options, trigger) {
  if (!$el.jquery) {
    $el = jquery_js_exposed_default()($el);
  }

  var name = this.prototype.name;
  var plog = logging["a" /* default */].getLogger("pat.".concat(name));
  var pattern = $el.data("pattern-".concat(name));

  if (pattern === undefined && registry["a" /* default */].patterns[name]) {
    try {
      options = this.prototype.parser === "mockup" ? mockup_parser.getOptions($el, name, options) : options;
      pattern = new registry["a" /* default */].patterns[name]($el, options, trigger);
    } catch (e) {
      plog.error("Failed while initializing ".concat(name, " pattern."), e);
    }

    $el.data("pattern-".concat(name), pattern);
  }

  return pattern;
};

var Base = /*#__PURE__*/function () {
  var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee($el, options, trigger) {
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            if (!$el.jquery) {
              $el = jquery_js_exposed_default()($el);
            }

            this.$el = $el;
            this.el = $el[0];
            this.options = jquery_js_exposed_default.a.extend(true, {}, this.defaults || {}, options || {});
            _context.next = 6;
            return this.init($el, options, trigger);

          case 6:
            this.emit("init");

          case 7:
          case "end":
            return _context.stop();
        }
      }
    }, _callee, this);
  }));

  return function Base(_x, _x2, _x3) {
    return _ref.apply(this, arguments);
  };
}();

Base.prototype = {
  constructor: Base,
  on: function on(eventName, eventCallback) {
    this.$el.on("".concat(eventName, ".").concat(this.name, ".patterns"), eventCallback);
  },
  emit: function emit(eventName, args) {
    // args should be a list
    if (args === undefined) {
      args = [];
    }

    this.$el.trigger("".concat(eventName, ".").concat(this.name, ".patterns"), args);
  }
};

Base.extend = function (patternProps) {
  /* Helper function to correctly set up the prototype chain for new patterns.
   */
  var parent = this;
  var child; // Check that the required configuration properties are given.

  if (!patternProps) {
    throw new Error("Pattern configuration properties required when calling Base.extend");
  } // The constructor function for the new subclass is either defined by you
  // (the "constructor" property in your `extend` definition), or defaulted
  // by us to simply call the parent's constructor.


  if (Object.hasOwnProperty.call(patternProps, "constructor")) {
    child = patternProps.constructor;
  } else {
    child = function child() {
      parent.apply(this, arguments);
    };
  } // Allow patterns to be extended indefinitely


  child.extend = Base.extend; // Static properties required by the Patternslib registry

  child.init = base_initBasePattern;
  child.jquery_plugin = true;
  child.trigger = patternProps.trigger;
  child.parser = (patternProps === null || patternProps === void 0 ? void 0 : patternProps.parser) || null; // Set the prototype chain to inherit from `parent`, without calling
  // `parent`'s constructor function.

  var Surrogate = function Surrogate() {
    this.constructor = child;
  };

  Surrogate.prototype = parent.prototype;
  child.prototype = new Surrogate(); // Add pattern's configuration properties (instance properties) to the subclass,

  jquery_js_exposed_default.a.extend(true, child.prototype, patternProps); // Set a convenience property in case the parent's prototype is needed
  // later.

  child.__super__ = parent.prototype; // Register the pattern in the Patternslib registry.

  if (!patternProps.name) {
    log.warn("This pattern without a name attribute will not be registered!");
  } else if (!patternProps.trigger) {
    log.warn("The pattern ".concat(patternProps.name, " does not have a trigger attribute, it will not be registered."));
  } else {
    registry["a" /* default */].register(child, patternProps.name);
  }

  return child;
};

/* harmony default export */ var base = __webpack_exports__["a"] = (Base);

/***/ }),

/***/ 6:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

/**
 * Patterns logging - minimal logging framework
 *
 * Copyright 2012 Simplon B.V.
 */
// source: https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Function/bind
if (!Function.prototype.bind) {
  Function.prototype.bind = function (oThis) {
    if (typeof this !== "function") {
      // closest thing possible to the ECMAScript 5 internal IsCallable function
      throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
    }

    var aArgs = Array.prototype.slice.call(arguments, 1),
        fToBind = this,
        fNOP = function fNOP() {},
        fBound = function fBound() {
      return fToBind.apply(this instanceof fNOP && oThis ? this : oThis, aArgs.concat(Array.prototype.slice.call(arguments)));
    };

    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();
    return fBound;
  };
}

var root, // root logger instance
writer; // writer instance, used to output log entries

var Level = {
  DEBUG: 10,
  INFO: 20,
  WARN: 30,
  ERROR: 40,
  FATAL: 50
};

function IEConsoleWriter() {}

IEConsoleWriter.prototype = {
  output: function output(log_name, level, messages) {
    // console.log will magically appear in IE8 when the user opens the
    // F12 Developer Tools, so we have to test for it every time.
    if (typeof window.console === "undefined" || typeof console.log === "undefined") return;
    if (log_name) messages.unshift(log_name + ":");
    var message = messages.join(" "); // Under some conditions console.log will be available but the
    // other functions are missing.

    if (_typeof(console.info) === undefined) {
      var level_name;
      if (level <= Level.DEBUG) level_name = "DEBUG";else if (level <= Level.INFO) level_name = "INFO";else if (level <= Level.WARN) level_name = "WARN";else if (level <= Level.ERROR) level_name = "ERROR";else level_name = "FATAL";
      console.log("[" + level_name + "] " + message);
    } else {
      if (level <= Level.DEBUG) {
        // console.debug exists but is deprecated
        message = "[DEBUG] " + message;
        console.log(message);
      } else if (level <= Level.INFO) console.info(message);else if (level <= Level.WARN) console.warn(message);else console.error(message);
    }
  }
};

function ConsoleWriter() {}

ConsoleWriter.prototype = {
  output: function output(log_name, level, messages) {
    if (log_name) messages.unshift(log_name + ":");

    if (level <= Level.DEBUG) {
      // console.debug exists but is deprecated
      messages.unshift("[DEBUG]");
      console.log.apply(console, messages);
    } else if (level <= Level.INFO) console.info.apply(console, messages);else if (level <= Level.WARN) console.warn.apply(console, messages);else console.error.apply(console, messages);
  }
};

function Logger(name, parent) {
  this._loggers = {};
  this.name = name || "";
  this._parent = parent || null;

  if (!parent) {
    this._enabled = true;
    this._level = Level.WARN;
  }
}

Logger.prototype = {
  getLogger: function getLogger(name) {
    var path = name.split("."),
        root = this,
        route = this.name ? [this.name] : [];

    while (path.length) {
      var entry = path.shift();
      route.push(entry);
      if (!(entry in root._loggers)) root._loggers[entry] = new Logger(route.join("."), root);
      root = root._loggers[entry];
    }

    return root;
  },
  _getFlag: function _getFlag(flag) {
    var context = this;
    flag = "_" + flag;

    while (context !== null) {
      if (context[flag] !== undefined) return context[flag];
      context = context._parent;
    }

    return null;
  },
  setEnabled: function setEnabled(state) {
    this._enabled = !!state;
  },
  isEnabled: function isEnabled() {
    this._getFlag("enabled");
  },
  setLevel: function setLevel(level) {
    if (typeof level === "number") this._level = level;else if (typeof level === "string") {
      level = level.toUpperCase();
      if (level in Level) this._level = Level[level];
    }
  },
  getLevel: function getLevel() {
    return this._getFlag("level");
  },
  log: function log(level, messages) {
    if (!messages.length || !this._getFlag("enabled") || level < this._getFlag("level")) return;
    messages = Array.prototype.slice.call(messages);
    writer.output(this.name, level, messages);
  },
  debug: function debug() {
    this.log(Level.DEBUG, arguments);
  },
  info: function info() {
    this.log(Level.INFO, arguments);
  },
  warn: function warn() {
    this.log(Level.WARN, arguments);
  },
  error: function error() {
    this.log(Level.ERROR, arguments);
  },
  fatal: function fatal() {
    this.log(Level.FATAL, arguments);
  }
};

function getWriter() {
  return writer;
}

function setWriter(w) {
  writer = w;
}

if (!window.console || !window.console.log || typeof window.console.log.apply !== "function") {
  setWriter(new IEConsoleWriter());
} else {
  setWriter(new ConsoleWriter());
}

root = new Logger();
var logconfig = /loglevel(|-[^=]+)=([^&]+)/g,
    match;

while ((match = logconfig.exec(window.location.search)) !== null) {
  var logger = match[1] === "" ? root : root.getLogger(match[1].slice(1));
  logger.setLevel(match[2].toUpperCase());
}

var api = {
  Level: Level,
  getLogger: root.getLogger.bind(root),
  setEnabled: root.setEnabled.bind(root),
  isEnabled: root.isEnabled.bind(root),
  setLevel: root.setLevel.bind(root),
  getLevel: root.getLevel.bind(root),
  debug: root.debug.bind(root),
  info: root.info.bind(root),
  warn: root.warn.bind(root),
  error: root.error.bind(root),
  fatal: root.fatal.bind(root),
  getWriter: getWriter,
  setWriter: setWriter
};
/* harmony default export */ __webpack_exports__["a"] = (api);

/***/ }),

/***/ 7:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXPORTS
__webpack_require__.d(__webpack_exports__, "a", function() { return /* reexport */ index_default; });

// UNUSED EXPORTS: VERSION, restArguments, isObject, isNull, isUndefined, isBoolean, isElement, isString, isNumber, isDate, isRegExp, isError, isSymbol, isArrayBuffer, isDataView, isArray, isFunction, isArguments, isFinite, isNaN, isTypedArray, isEmpty, isMatch, isEqual, isMap, isWeakMap, isSet, isWeakSet, keys, allKeys, values, pairs, invert, functions, methods, extend, extendOwn, assign, defaults, create, clone, tap, get, has, mapObject, identity, constant, noop, toPath, property, propertyOf, matcher, matches, times, random, now, escape, unescape, templateSettings, template, result, uniqueId, chain, iteratee, partial, bind, bindAll, memoize, delay, defer, throttle, debounce, wrap, negate, compose, after, before, once, findKey, findIndex, findLastIndex, sortedIndex, indexOf, lastIndexOf, find, detect, findWhere, each, forEach, map, collect, reduce, foldl, inject, reduceRight, foldr, filter, select, reject, every, all, some, any, contains, includes, include, invoke, pluck, where, max, min, shuffle, sample, sortBy, groupBy, indexBy, countBy, partition, toArray, size, pick, omit, first, head, take, initial, last, rest, tail, drop, compact, flatten, without, uniq, unique, union, intersection, difference, unzip, transpose, zip, object, range, chunk, mixin

// NAMESPACE OBJECT: ./node_modules/underscore/modules/index.js
var modules_namespaceObject = {};
__webpack_require__.r(modules_namespaceObject);
__webpack_require__.d(modules_namespaceObject, "VERSION", function() { return _setup["e" /* VERSION */]; });
__webpack_require__.d(modules_namespaceObject, "restArguments", function() { return restArguments; });
__webpack_require__.d(modules_namespaceObject, "isObject", function() { return isObject; });
__webpack_require__.d(modules_namespaceObject, "isNull", function() { return isNull; });
__webpack_require__.d(modules_namespaceObject, "isUndefined", function() { return isUndefined; });
__webpack_require__.d(modules_namespaceObject, "isBoolean", function() { return isBoolean; });
__webpack_require__.d(modules_namespaceObject, "isElement", function() { return isElement; });
__webpack_require__.d(modules_namespaceObject, "isString", function() { return isString; });
__webpack_require__.d(modules_namespaceObject, "isNumber", function() { return isNumber; });
__webpack_require__.d(modules_namespaceObject, "isDate", function() { return isDate; });
__webpack_require__.d(modules_namespaceObject, "isRegExp", function() { return isRegExp; });
__webpack_require__.d(modules_namespaceObject, "isError", function() { return isError; });
__webpack_require__.d(modules_namespaceObject, "isSymbol", function() { return isSymbol; });
__webpack_require__.d(modules_namespaceObject, "isArrayBuffer", function() { return isArrayBuffer; });
__webpack_require__.d(modules_namespaceObject, "isDataView", function() { return modules_isDataView; });
__webpack_require__.d(modules_namespaceObject, "isArray", function() { return isArray; });
__webpack_require__.d(modules_namespaceObject, "isFunction", function() { return modules_isFunction; });
__webpack_require__.d(modules_namespaceObject, "isArguments", function() { return modules_isArguments; });
__webpack_require__.d(modules_namespaceObject, "isFinite", function() { return isFinite_isFinite; });
__webpack_require__.d(modules_namespaceObject, "isNaN", function() { return isNaN_isNaN; });
__webpack_require__.d(modules_namespaceObject, "isTypedArray", function() { return modules_isTypedArray; });
__webpack_require__.d(modules_namespaceObject, "isEmpty", function() { return isEmpty; });
__webpack_require__.d(modules_namespaceObject, "isMatch", function() { return isMatch; });
__webpack_require__.d(modules_namespaceObject, "isEqual", function() { return isEqual; });
__webpack_require__.d(modules_namespaceObject, "isMap", function() { return isMap; });
__webpack_require__.d(modules_namespaceObject, "isWeakMap", function() { return isWeakMap; });
__webpack_require__.d(modules_namespaceObject, "isSet", function() { return isSet; });
__webpack_require__.d(modules_namespaceObject, "isWeakSet", function() { return isWeakSet; });
__webpack_require__.d(modules_namespaceObject, "keys", function() { return keys_keys; });
__webpack_require__.d(modules_namespaceObject, "allKeys", function() { return allKeys; });
__webpack_require__.d(modules_namespaceObject, "values", function() { return values_values; });
__webpack_require__.d(modules_namespaceObject, "pairs", function() { return pairs_pairs; });
__webpack_require__.d(modules_namespaceObject, "invert", function() { return invert; });
__webpack_require__.d(modules_namespaceObject, "functions", function() { return functions; });
__webpack_require__.d(modules_namespaceObject, "methods", function() { return functions; });
__webpack_require__.d(modules_namespaceObject, "extend", function() { return extend; });
__webpack_require__.d(modules_namespaceObject, "extendOwn", function() { return extendOwn; });
__webpack_require__.d(modules_namespaceObject, "assign", function() { return extendOwn; });
__webpack_require__.d(modules_namespaceObject, "defaults", function() { return defaults; });
__webpack_require__.d(modules_namespaceObject, "create", function() { return create; });
__webpack_require__.d(modules_namespaceObject, "clone", function() { return clone; });
__webpack_require__.d(modules_namespaceObject, "tap", function() { return tap; });
__webpack_require__.d(modules_namespaceObject, "get", function() { return get; });
__webpack_require__.d(modules_namespaceObject, "has", function() { return has_has; });
__webpack_require__.d(modules_namespaceObject, "mapObject", function() { return mapObject; });
__webpack_require__.d(modules_namespaceObject, "identity", function() { return identity; });
__webpack_require__.d(modules_namespaceObject, "constant", function() { return constant; });
__webpack_require__.d(modules_namespaceObject, "noop", function() { return noop; });
__webpack_require__.d(modules_namespaceObject, "toPath", function() { return toPath; });
__webpack_require__.d(modules_namespaceObject, "property", function() { return property; });
__webpack_require__.d(modules_namespaceObject, "propertyOf", function() { return propertyOf; });
__webpack_require__.d(modules_namespaceObject, "matcher", function() { return matcher_matcher; });
__webpack_require__.d(modules_namespaceObject, "matches", function() { return matcher_matcher; });
__webpack_require__.d(modules_namespaceObject, "times", function() { return times; });
__webpack_require__.d(modules_namespaceObject, "random", function() { return random; });
__webpack_require__.d(modules_namespaceObject, "now", function() { return now; });
__webpack_require__.d(modules_namespaceObject, "escape", function() { return modules_escape; });
__webpack_require__.d(modules_namespaceObject, "unescape", function() { return modules_unescape; });
__webpack_require__.d(modules_namespaceObject, "templateSettings", function() { return templateSettings; });
__webpack_require__.d(modules_namespaceObject, "template", function() { return template_template; });
__webpack_require__.d(modules_namespaceObject, "result", function() { return result_result; });
__webpack_require__.d(modules_namespaceObject, "uniqueId", function() { return uniqueId; });
__webpack_require__.d(modules_namespaceObject, "chain", function() { return chain; });
__webpack_require__.d(modules_namespaceObject, "iteratee", function() { return iteratee_iteratee; });
__webpack_require__.d(modules_namespaceObject, "partial", function() { return modules_partial; });
__webpack_require__.d(modules_namespaceObject, "bind", function() { return bind; });
__webpack_require__.d(modules_namespaceObject, "bindAll", function() { return bindAll; });
__webpack_require__.d(modules_namespaceObject, "memoize", function() { return memoize_memoize; });
__webpack_require__.d(modules_namespaceObject, "delay", function() { return delay; });
__webpack_require__.d(modules_namespaceObject, "defer", function() { return defer; });
__webpack_require__.d(modules_namespaceObject, "throttle", function() { return throttle; });
__webpack_require__.d(modules_namespaceObject, "debounce", function() { return debounce; });
__webpack_require__.d(modules_namespaceObject, "wrap", function() { return wrap; });
__webpack_require__.d(modules_namespaceObject, "negate", function() { return negate; });
__webpack_require__.d(modules_namespaceObject, "compose", function() { return compose; });
__webpack_require__.d(modules_namespaceObject, "after", function() { return after; });
__webpack_require__.d(modules_namespaceObject, "before", function() { return before; });
__webpack_require__.d(modules_namespaceObject, "once", function() { return once; });
__webpack_require__.d(modules_namespaceObject, "findKey", function() { return findKey; });
__webpack_require__.d(modules_namespaceObject, "findIndex", function() { return findIndex; });
__webpack_require__.d(modules_namespaceObject, "findLastIndex", function() { return findLastIndex; });
__webpack_require__.d(modules_namespaceObject, "sortedIndex", function() { return sortedIndex_sortedIndex; });
__webpack_require__.d(modules_namespaceObject, "indexOf", function() { return indexOf; });
__webpack_require__.d(modules_namespaceObject, "lastIndexOf", function() { return lastIndexOf; });
__webpack_require__.d(modules_namespaceObject, "find", function() { return find; });
__webpack_require__.d(modules_namespaceObject, "detect", function() { return find; });
__webpack_require__.d(modules_namespaceObject, "findWhere", function() { return findWhere; });
__webpack_require__.d(modules_namespaceObject, "each", function() { return each; });
__webpack_require__.d(modules_namespaceObject, "forEach", function() { return each; });
__webpack_require__.d(modules_namespaceObject, "map", function() { return map_map; });
__webpack_require__.d(modules_namespaceObject, "collect", function() { return map_map; });
__webpack_require__.d(modules_namespaceObject, "reduce", function() { return reduce; });
__webpack_require__.d(modules_namespaceObject, "foldl", function() { return reduce; });
__webpack_require__.d(modules_namespaceObject, "inject", function() { return reduce; });
__webpack_require__.d(modules_namespaceObject, "reduceRight", function() { return reduceRight; });
__webpack_require__.d(modules_namespaceObject, "foldr", function() { return reduceRight; });
__webpack_require__.d(modules_namespaceObject, "filter", function() { return filter; });
__webpack_require__.d(modules_namespaceObject, "select", function() { return filter; });
__webpack_require__.d(modules_namespaceObject, "reject", function() { return reject; });
__webpack_require__.d(modules_namespaceObject, "every", function() { return every; });
__webpack_require__.d(modules_namespaceObject, "all", function() { return every; });
__webpack_require__.d(modules_namespaceObject, "some", function() { return some; });
__webpack_require__.d(modules_namespaceObject, "any", function() { return some; });
__webpack_require__.d(modules_namespaceObject, "contains", function() { return contains; });
__webpack_require__.d(modules_namespaceObject, "includes", function() { return contains; });
__webpack_require__.d(modules_namespaceObject, "include", function() { return contains; });
__webpack_require__.d(modules_namespaceObject, "invoke", function() { return invoke; });
__webpack_require__.d(modules_namespaceObject, "pluck", function() { return pluck; });
__webpack_require__.d(modules_namespaceObject, "where", function() { return where; });
__webpack_require__.d(modules_namespaceObject, "max", function() { return max; });
__webpack_require__.d(modules_namespaceObject, "min", function() { return min; });
__webpack_require__.d(modules_namespaceObject, "shuffle", function() { return shuffle; });
__webpack_require__.d(modules_namespaceObject, "sample", function() { return sample_sample; });
__webpack_require__.d(modules_namespaceObject, "sortBy", function() { return sortBy; });
__webpack_require__.d(modules_namespaceObject, "groupBy", function() { return groupBy; });
__webpack_require__.d(modules_namespaceObject, "indexBy", function() { return indexBy; });
__webpack_require__.d(modules_namespaceObject, "countBy", function() { return countBy; });
__webpack_require__.d(modules_namespaceObject, "partition", function() { return modules_partition; });
__webpack_require__.d(modules_namespaceObject, "toArray", function() { return toArray; });
__webpack_require__.d(modules_namespaceObject, "size", function() { return size; });
__webpack_require__.d(modules_namespaceObject, "pick", function() { return pick; });
__webpack_require__.d(modules_namespaceObject, "omit", function() { return omit; });
__webpack_require__.d(modules_namespaceObject, "first", function() { return first; });
__webpack_require__.d(modules_namespaceObject, "head", function() { return first; });
__webpack_require__.d(modules_namespaceObject, "take", function() { return first; });
__webpack_require__.d(modules_namespaceObject, "initial", function() { return initial_initial; });
__webpack_require__.d(modules_namespaceObject, "last", function() { return last_last; });
__webpack_require__.d(modules_namespaceObject, "rest", function() { return rest_rest; });
__webpack_require__.d(modules_namespaceObject, "tail", function() { return rest_rest; });
__webpack_require__.d(modules_namespaceObject, "drop", function() { return rest_rest; });
__webpack_require__.d(modules_namespaceObject, "compact", function() { return compact; });
__webpack_require__.d(modules_namespaceObject, "flatten", function() { return flatten_flatten; });
__webpack_require__.d(modules_namespaceObject, "without", function() { return without; });
__webpack_require__.d(modules_namespaceObject, "uniq", function() { return uniq; });
__webpack_require__.d(modules_namespaceObject, "unique", function() { return uniq; });
__webpack_require__.d(modules_namespaceObject, "union", function() { return union; });
__webpack_require__.d(modules_namespaceObject, "intersection", function() { return intersection; });
__webpack_require__.d(modules_namespaceObject, "difference", function() { return difference; });
__webpack_require__.d(modules_namespaceObject, "unzip", function() { return unzip; });
__webpack_require__.d(modules_namespaceObject, "transpose", function() { return unzip; });
__webpack_require__.d(modules_namespaceObject, "zip", function() { return zip; });
__webpack_require__.d(modules_namespaceObject, "object", function() { return object_object; });
__webpack_require__.d(modules_namespaceObject, "range", function() { return range; });
__webpack_require__.d(modules_namespaceObject, "chunk", function() { return chunk; });
__webpack_require__.d(modules_namespaceObject, "mixin", function() { return mixin; });
__webpack_require__.d(modules_namespaceObject, "default", function() { return underscore_array_methods; });

// EXTERNAL MODULE: ./node_modules/underscore/modules/_setup.js
var _setup = __webpack_require__(1);

// CONCATENATED MODULE: ./node_modules/underscore/modules/restArguments.js
// Some functions take a variable number of arguments, or a few expected
// arguments at the beginning and then a variable number of values to operate
// on. This helper accumulates all remaining arguments past the function’s
// argument length (or an explicit `startIndex`), into an array that becomes
// the last argument. Similar to ES6’s "rest parameter".
function restArguments(func, startIndex) {
  startIndex = startIndex == null ? func.length - 1 : +startIndex;
  return function() {
    var length = Math.max(arguments.length - startIndex, 0),
        rest = Array(length),
        index = 0;
    for (; index < length; index++) {
      rest[index] = arguments[index + startIndex];
    }
    switch (startIndex) {
      case 0: return func.call(this, rest);
      case 1: return func.call(this, arguments[0], rest);
      case 2: return func.call(this, arguments[0], arguments[1], rest);
    }
    var args = Array(startIndex + 1);
    for (index = 0; index < startIndex; index++) {
      args[index] = arguments[index];
    }
    args[startIndex] = rest;
    return func.apply(this, args);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isObject.js
// Is a given variable an object?
function isObject(obj) {
  var type = typeof obj;
  return type === 'function' || type === 'object' && !!obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isNull.js
// Is a given value equal to null?
function isNull(obj) {
  return obj === null;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isUndefined.js
// Is a given variable undefined?
function isUndefined(obj) {
  return obj === void 0;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isBoolean.js


// Is a given value a boolean?
function isBoolean(obj) {
  return obj === true || obj === false || _setup["t" /* toString */].call(obj) === '[object Boolean]';
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isElement.js
// Is a given value a DOM element?
function isElement(obj) {
  return !!(obj && obj.nodeType === 1);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_tagTester.js


// Internal function for creating a `toString`-based type tester.
function tagTester(name) {
  var tag = '[object ' + name + ']';
  return function(obj) {
    return _setup["t" /* toString */].call(obj) === tag;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isString.js


/* harmony default export */ var isString = (tagTester('String'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isNumber.js


/* harmony default export */ var isNumber = (tagTester('Number'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isDate.js


/* harmony default export */ var isDate = (tagTester('Date'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isRegExp.js


/* harmony default export */ var isRegExp = (tagTester('RegExp'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isError.js


/* harmony default export */ var isError = (tagTester('Error'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isSymbol.js


/* harmony default export */ var isSymbol = (tagTester('Symbol'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isArrayBuffer.js


/* harmony default export */ var isArrayBuffer = (tagTester('ArrayBuffer'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isFunction.js



var isFunction = tagTester('Function');

// Optimize `isFunction` if appropriate. Work around some `typeof` bugs in old
// v8, IE 11 (#1621), Safari 8 (#1929), and PhantomJS (#2236).
var nodelist = _setup["p" /* root */].document && _setup["p" /* root */].document.childNodes;
if ( true && typeof Int8Array != 'object' && typeof nodelist != 'function') {
  isFunction = function(obj) {
    return typeof obj == 'function' || false;
  };
}

/* harmony default export */ var modules_isFunction = (isFunction);

// CONCATENATED MODULE: ./node_modules/underscore/modules/_hasObjectTag.js


/* harmony default export */ var _hasObjectTag = (tagTester('Object'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_stringTagBug.js



// In IE 10 - Edge 13, `DataView` has string tag `'[object Object]'`.
// In IE 11, the most common among them, this problem also applies to
// `Map`, `WeakMap` and `Set`.
var hasStringTagBug = (
      _setup["s" /* supportsDataView */] && _hasObjectTag(new DataView(new ArrayBuffer(8)))
    ),
    isIE11 = (typeof Map !== 'undefined' && _hasObjectTag(new Map));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isDataView.js





var isDataView = tagTester('DataView');

// In IE 10 - Edge 13, we need a different heuristic
// to determine whether an object is a `DataView`.
function ie10IsDataView(obj) {
  return obj != null && modules_isFunction(obj.getInt8) && isArrayBuffer(obj.buffer);
}

/* harmony default export */ var modules_isDataView = (hasStringTagBug ? ie10IsDataView : isDataView);

// CONCATENATED MODULE: ./node_modules/underscore/modules/isArray.js



// Is a given value an array?
// Delegates to ECMA5's native `Array.isArray`.
/* harmony default export */ var isArray = (_setup["k" /* nativeIsArray */] || tagTester('Array'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_has.js


// Internal function to check whether `key` is an own property name of `obj`.
function has(obj, key) {
  return obj != null && _setup["i" /* hasOwnProperty */].call(obj, key);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isArguments.js



var isArguments = tagTester('Arguments');

// Define a fallback version of the method in browsers (ahem, IE < 9), where
// there isn't any inspectable "Arguments" type.
(function() {
  if (!isArguments(arguments)) {
    isArguments = function(obj) {
      return has(obj, 'callee');
    };
  }
}());

/* harmony default export */ var modules_isArguments = (isArguments);

// CONCATENATED MODULE: ./node_modules/underscore/modules/isFinite.js



// Is a given object a finite number?
function isFinite_isFinite(obj) {
  return !isSymbol(obj) && Object(_setup["f" /* _isFinite */])(obj) && !isNaN(parseFloat(obj));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isNaN.js



// Is the given value `NaN`?
function isNaN_isNaN(obj) {
  return isNumber(obj) && Object(_setup["g" /* _isNaN */])(obj);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/constant.js
// Predicate-generating function. Often useful outside of Underscore.
function constant(value) {
  return function() {
    return value;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createSizePropertyCheck.js


// Common internal logic for `isArrayLike` and `isBufferLike`.
function createSizePropertyCheck(getSizeProperty) {
  return function(collection) {
    var sizeProperty = getSizeProperty(collection);
    return typeof sizeProperty == 'number' && sizeProperty >= 0 && sizeProperty <= _setup["b" /* MAX_ARRAY_INDEX */];
  }
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_shallowProperty.js
// Internal helper to generate a function to obtain property `key` from `obj`.
function shallowProperty(key) {
  return function(obj) {
    return obj == null ? void 0 : obj[key];
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_getByteLength.js


// Internal helper to obtain the `byteLength` property of an object.
/* harmony default export */ var _getByteLength = (shallowProperty('byteLength'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_isBufferLike.js



// Internal helper to determine whether we should spend extensive checks against
// `ArrayBuffer` et al.
/* harmony default export */ var _isBufferLike = (createSizePropertyCheck(_getByteLength));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isTypedArray.js





// Is a given value a typed array?
var typedArrayPattern = /\[object ((I|Ui)nt(8|16|32)|Float(32|64)|Uint8Clamped|Big(I|Ui)nt64)Array\]/;
function isTypedArray(obj) {
  // `ArrayBuffer.isView` is the most future-proof, so use it when available.
  // Otherwise, fall back on the above regular expression.
  return _setup["l" /* nativeIsView */] ? (Object(_setup["l" /* nativeIsView */])(obj) && !modules_isDataView(obj)) :
                _isBufferLike(obj) && typedArrayPattern.test(_setup["t" /* toString */].call(obj));
}

/* harmony default export */ var modules_isTypedArray = (_setup["r" /* supportsArrayBuffer */] ? isTypedArray : constant(false));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_getLength.js


// Internal helper to obtain the `length` property of an object.
/* harmony default export */ var _getLength = (shallowProperty('length'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_collectNonEnumProps.js




// Internal helper to create a simple lookup structure.
// `collectNonEnumProps` used to depend on `_.contains`, but this led to
// circular imports. `emulatedSet` is a one-off solution that only works for
// arrays of strings.
function emulatedSet(keys) {
  var hash = {};
  for (var l = keys.length, i = 0; i < l; ++i) hash[keys[i]] = true;
  return {
    contains: function(key) { return hash[key]; },
    push: function(key) {
      hash[key] = true;
      return keys.push(key);
    }
  };
}

// Internal helper. Checks `keys` for the presence of keys in IE < 9 that won't
// be iterated by `for key in ...` and thus missed. Extends `keys` in place if
// needed.
function collectNonEnumProps(obj, keys) {
  keys = emulatedSet(keys);
  var nonEnumIdx = _setup["n" /* nonEnumerableProps */].length;
  var constructor = obj.constructor;
  var proto = modules_isFunction(constructor) && constructor.prototype || _setup["c" /* ObjProto */];

  // Constructor is a special case.
  var prop = 'constructor';
  if (has(obj, prop) && !keys.contains(prop)) keys.push(prop);

  while (nonEnumIdx--) {
    prop = _setup["n" /* nonEnumerableProps */][nonEnumIdx];
    if (prop in obj && obj[prop] !== proto[prop] && !keys.contains(prop)) {
      keys.push(prop);
    }
  }
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/keys.js





// Retrieve the names of an object's own properties.
// Delegates to **ECMAScript 5**'s native `Object.keys`.
function keys_keys(obj) {
  if (!isObject(obj)) return [];
  if (_setup["m" /* nativeKeys */]) return Object(_setup["m" /* nativeKeys */])(obj);
  var keys = [];
  for (var key in obj) if (has(obj, key)) keys.push(key);
  // Ahem, IE < 9.
  if (_setup["h" /* hasEnumBug */]) collectNonEnumProps(obj, keys);
  return keys;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isEmpty.js






// Is a given array, string, or object empty?
// An "empty" object has no enumerable own-properties.
function isEmpty(obj) {
  if (obj == null) return true;
  // Skip the more expensive `toString`-based type checks if `obj` has no
  // `.length`.
  var length = _getLength(obj);
  if (typeof length == 'number' && (
    isArray(obj) || isString(obj) || modules_isArguments(obj)
  )) return length === 0;
  return _getLength(keys_keys(obj)) === 0;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isMatch.js


// Returns whether an object has a given set of `key:value` pairs.
function isMatch(object, attrs) {
  var _keys = keys_keys(attrs), length = _keys.length;
  if (object == null) return !length;
  var obj = Object(object);
  for (var i = 0; i < length; i++) {
    var key = _keys[i];
    if (attrs[key] !== obj[key] || !(key in obj)) return false;
  }
  return true;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/underscore.js


// If Underscore is called as a function, it returns a wrapped object that can
// be used OO-style. This wrapper holds altered versions of all functions added
// through `_.mixin`. Wrapped objects may be chained.
function _(obj) {
  if (obj instanceof _) return obj;
  if (!(this instanceof _)) return new _(obj);
  this._wrapped = obj;
}

_.VERSION = _setup["e" /* VERSION */];

// Extracts the result from a wrapped and chained object.
_.prototype.value = function() {
  return this._wrapped;
};

// Provide unwrapping proxies for some methods used in engine operations
// such as arithmetic and JSON stringification.
_.prototype.valueOf = _.prototype.toJSON = _.prototype.value;

_.prototype.toString = function() {
  return String(this._wrapped);
};

// CONCATENATED MODULE: ./node_modules/underscore/modules/_toBufferView.js


// Internal function to wrap or shallow-copy an ArrayBuffer,
// typed array or DataView to a new view, reusing the buffer.
function toBufferView(bufferSource) {
  return new Uint8Array(
    bufferSource.buffer || bufferSource,
    bufferSource.byteOffset || 0,
    _getByteLength(bufferSource)
  );
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/isEqual.js











// We use this string twice, so give it a name for minification.
var tagDataView = '[object DataView]';

// Internal recursive comparison function for `_.isEqual`.
function eq(a, b, aStack, bStack) {
  // Identical objects are equal. `0 === -0`, but they aren't identical.
  // See the [Harmony `egal` proposal](https://wiki.ecmascript.org/doku.php?id=harmony:egal).
  if (a === b) return a !== 0 || 1 / a === 1 / b;
  // `null` or `undefined` only equal to itself (strict comparison).
  if (a == null || b == null) return false;
  // `NaN`s are equivalent, but non-reflexive.
  if (a !== a) return b !== b;
  // Exhaust primitive checks
  var type = typeof a;
  if (type !== 'function' && type !== 'object' && typeof b != 'object') return false;
  return deepEq(a, b, aStack, bStack);
}

// Internal recursive comparison function for `_.isEqual`.
function deepEq(a, b, aStack, bStack) {
  // Unwrap any wrapped objects.
  if (a instanceof _) a = a._wrapped;
  if (b instanceof _) b = b._wrapped;
  // Compare `[[Class]]` names.
  var className = _setup["t" /* toString */].call(a);
  if (className !== _setup["t" /* toString */].call(b)) return false;
  // Work around a bug in IE 10 - Edge 13.
  if (hasStringTagBug && className == '[object Object]' && modules_isDataView(a)) {
    if (!modules_isDataView(b)) return false;
    className = tagDataView;
  }
  switch (className) {
    // These types are compared by value.
    case '[object RegExp]':
      // RegExps are coerced to strings for comparison (Note: '' + /a/i === '/a/i')
    case '[object String]':
      // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
      // equivalent to `new String("5")`.
      return '' + a === '' + b;
    case '[object Number]':
      // `NaN`s are equivalent, but non-reflexive.
      // Object(NaN) is equivalent to NaN.
      if (+a !== +a) return +b !== +b;
      // An `egal` comparison is performed for other numeric values.
      return +a === 0 ? 1 / +a === 1 / b : +a === +b;
    case '[object Date]':
    case '[object Boolean]':
      // Coerce dates and booleans to numeric primitive values. Dates are compared by their
      // millisecond representations. Note that invalid dates with millisecond representations
      // of `NaN` are not equivalent.
      return +a === +b;
    case '[object Symbol]':
      return _setup["d" /* SymbolProto */].valueOf.call(a) === _setup["d" /* SymbolProto */].valueOf.call(b);
    case '[object ArrayBuffer]':
    case tagDataView:
      // Coerce to typed array so we can fall through.
      return deepEq(toBufferView(a), toBufferView(b), aStack, bStack);
  }

  var areArrays = className === '[object Array]';
  if (!areArrays && modules_isTypedArray(a)) {
      var byteLength = _getByteLength(a);
      if (byteLength !== _getByteLength(b)) return false;
      if (a.buffer === b.buffer && a.byteOffset === b.byteOffset) return true;
      areArrays = true;
  }
  if (!areArrays) {
    if (typeof a != 'object' || typeof b != 'object') return false;

    // Objects with different constructors are not equivalent, but `Object`s or `Array`s
    // from different frames are.
    var aCtor = a.constructor, bCtor = b.constructor;
    if (aCtor !== bCtor && !(modules_isFunction(aCtor) && aCtor instanceof aCtor &&
                             modules_isFunction(bCtor) && bCtor instanceof bCtor)
                        && ('constructor' in a && 'constructor' in b)) {
      return false;
    }
  }
  // Assume equality for cyclic structures. The algorithm for detecting cyclic
  // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.

  // Initializing stack of traversed objects.
  // It's done here since we only need them for objects and arrays comparison.
  aStack = aStack || [];
  bStack = bStack || [];
  var length = aStack.length;
  while (length--) {
    // Linear search. Performance is inversely proportional to the number of
    // unique nested structures.
    if (aStack[length] === a) return bStack[length] === b;
  }

  // Add the first object to the stack of traversed objects.
  aStack.push(a);
  bStack.push(b);

  // Recursively compare objects and arrays.
  if (areArrays) {
    // Compare array lengths to determine if a deep comparison is necessary.
    length = a.length;
    if (length !== b.length) return false;
    // Deep compare the contents, ignoring non-numeric properties.
    while (length--) {
      if (!eq(a[length], b[length], aStack, bStack)) return false;
    }
  } else {
    // Deep compare objects.
    var _keys = keys_keys(a), key;
    length = _keys.length;
    // Ensure that both objects contain the same number of properties before comparing deep equality.
    if (keys_keys(b).length !== length) return false;
    while (length--) {
      // Deep compare each member
      key = _keys[length];
      if (!(has(b, key) && eq(a[key], b[key], aStack, bStack))) return false;
    }
  }
  // Remove the first object from the stack of traversed objects.
  aStack.pop();
  bStack.pop();
  return true;
}

// Perform a deep comparison to check if two objects are equal.
function isEqual(a, b) {
  return eq(a, b);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/allKeys.js




// Retrieve all the enumerable property names of an object.
function allKeys(obj) {
  if (!isObject(obj)) return [];
  var keys = [];
  for (var key in obj) keys.push(key);
  // Ahem, IE < 9.
  if (_setup["h" /* hasEnumBug */]) collectNonEnumProps(obj, keys);
  return keys;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_methodFingerprint.js




// Since the regular `Object.prototype.toString` type tests don't work for
// some types in IE 11, we use a fingerprinting heuristic instead, based
// on the methods. It's not great, but it's the best we got.
// The fingerprint method lists are defined below.
function ie11fingerprint(methods) {
  var length = _getLength(methods);
  return function(obj) {
    if (obj == null) return false;
    // `Map`, `WeakMap` and `Set` have no enumerable keys.
    var keys = allKeys(obj);
    if (_getLength(keys)) return false;
    for (var i = 0; i < length; i++) {
      if (!modules_isFunction(obj[methods[i]])) return false;
    }
    // If we are testing against `WeakMap`, we need to ensure that
    // `obj` doesn't have a `forEach` method in order to distinguish
    // it from a regular `Map`.
    return methods !== weakMapMethods || !modules_isFunction(obj[forEachName]);
  };
}

// In the interest of compact minification, we write
// each string in the fingerprints only once.
var forEachName = 'forEach',
    hasName = 'has',
    commonInit = ['clear', 'delete'],
    mapTail = ['get', hasName, 'set'];

// `Map`, `WeakMap` and `Set` each have slightly different
// combinations of the above sublists.
var mapMethods = commonInit.concat(forEachName, mapTail),
    weakMapMethods = commonInit.concat(mapTail),
    setMethods = ['add'].concat(commonInit, forEachName, hasName);

// CONCATENATED MODULE: ./node_modules/underscore/modules/isMap.js




/* harmony default export */ var isMap = (isIE11 ? ie11fingerprint(mapMethods) : tagTester('Map'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isWeakMap.js




/* harmony default export */ var isWeakMap = (isIE11 ? ie11fingerprint(weakMapMethods) : tagTester('WeakMap'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isSet.js




/* harmony default export */ var isSet = (isIE11 ? ie11fingerprint(setMethods) : tagTester('Set'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/isWeakSet.js


/* harmony default export */ var isWeakSet = (tagTester('WeakSet'));

// CONCATENATED MODULE: ./node_modules/underscore/modules/values.js


// Retrieve the values of an object's properties.
function values_values(obj) {
  var _keys = keys_keys(obj);
  var length = _keys.length;
  var values = Array(length);
  for (var i = 0; i < length; i++) {
    values[i] = obj[_keys[i]];
  }
  return values;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/pairs.js


// Convert an object into a list of `[key, value]` pairs.
// The opposite of `_.object` with one argument.
function pairs_pairs(obj) {
  var _keys = keys_keys(obj);
  var length = _keys.length;
  var pairs = Array(length);
  for (var i = 0; i < length; i++) {
    pairs[i] = [_keys[i], obj[_keys[i]]];
  }
  return pairs;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/invert.js


// Invert the keys and values of an object. The values must be serializable.
function invert(obj) {
  var result = {};
  var _keys = keys_keys(obj);
  for (var i = 0, length = _keys.length; i < length; i++) {
    result[obj[_keys[i]]] = _keys[i];
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/functions.js


// Return a sorted list of the function names available on the object.
function functions(obj) {
  var names = [];
  for (var key in obj) {
    if (modules_isFunction(obj[key])) names.push(key);
  }
  return names.sort();
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createAssigner.js
// An internal function for creating assigner functions.
function createAssigner(keysFunc, defaults) {
  return function(obj) {
    var length = arguments.length;
    if (defaults) obj = Object(obj);
    if (length < 2 || obj == null) return obj;
    for (var index = 1; index < length; index++) {
      var source = arguments[index],
          keys = keysFunc(source),
          l = keys.length;
      for (var i = 0; i < l; i++) {
        var key = keys[i];
        if (!defaults || obj[key] === void 0) obj[key] = source[key];
      }
    }
    return obj;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/extend.js



// Extend a given object with all the properties in passed-in object(s).
/* harmony default export */ var extend = (createAssigner(allKeys));

// CONCATENATED MODULE: ./node_modules/underscore/modules/extendOwn.js



// Assigns a given object with all the own properties in the passed-in
// object(s).
// (https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
/* harmony default export */ var extendOwn = (createAssigner(keys_keys));

// CONCATENATED MODULE: ./node_modules/underscore/modules/defaults.js



// Fill in a given object with default properties.
/* harmony default export */ var defaults = (createAssigner(allKeys, true));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_baseCreate.js



// Create a naked function reference for surrogate-prototype-swapping.
function ctor() {
  return function(){};
}

// An internal function for creating a new object that inherits from another.
function baseCreate(prototype) {
  if (!isObject(prototype)) return {};
  if (_setup["j" /* nativeCreate */]) return Object(_setup["j" /* nativeCreate */])(prototype);
  var Ctor = ctor();
  Ctor.prototype = prototype;
  var result = new Ctor;
  Ctor.prototype = null;
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/create.js



// Creates an object that inherits from the given prototype object.
// If additional properties are provided then they will be added to the
// created object.
function create(prototype, props) {
  var result = baseCreate(prototype);
  if (props) extendOwn(result, props);
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/clone.js




// Create a (shallow-cloned) duplicate of an object.
function clone(obj) {
  if (!isObject(obj)) return obj;
  return isArray(obj) ? obj.slice() : extend({}, obj);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/tap.js
// Invokes `interceptor` with the `obj` and then returns `obj`.
// The primary purpose of this method is to "tap into" a method chain, in
// order to perform operations on intermediate results within the chain.
function tap(obj, interceptor) {
  interceptor(obj);
  return obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/toPath.js



// Normalize a (deep) property `path` to array.
// Like `_.iteratee`, this function can be customized.
function toPath(path) {
  return isArray(path) ? path : [path];
}
_.toPath = toPath;

// CONCATENATED MODULE: ./node_modules/underscore/modules/_toPath.js



// Internal wrapper for `_.toPath` to enable minification.
// Similar to `cb` for `_.iteratee`.
function _toPath_toPath(path) {
  return _.toPath(path);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_deepGet.js
// Internal function to obtain a nested property in `obj` along `path`.
function deepGet(obj, path) {
  var length = path.length;
  for (var i = 0; i < length; i++) {
    if (obj == null) return void 0;
    obj = obj[path[i]];
  }
  return length ? obj : void 0;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/get.js




// Get the value of the (deep) property on `path` from `object`.
// If any property in `path` does not exist or if the value is
// `undefined`, return `defaultValue` instead.
// The `path` is normalized through `_.toPath`.
function get(object, path, defaultValue) {
  var value = deepGet(object, _toPath_toPath(path));
  return isUndefined(value) ? defaultValue : value;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/has.js



// Shortcut function for checking if an object has a given property directly on
// itself (in other words, not on a prototype). Unlike the internal `has`
// function, this public version can also traverse nested properties.
function has_has(obj, path) {
  path = _toPath_toPath(path);
  var length = path.length;
  for (var i = 0; i < length; i++) {
    var key = path[i];
    if (!has(obj, key)) return false;
    obj = obj[key];
  }
  return !!length;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/identity.js
// Keep the identity function around for default iteratees.
function identity(value) {
  return value;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/matcher.js



// Returns a predicate for checking whether an object has a given set of
// `key:value` pairs.
function matcher_matcher(attrs) {
  attrs = extendOwn({}, attrs);
  return function(obj) {
    return isMatch(obj, attrs);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/property.js



// Creates a function that, when passed an object, will traverse that object’s
// properties down the given `path`, specified as an array of keys or indices.
function property(path) {
  path = _toPath_toPath(path);
  return function(obj) {
    return deepGet(obj, path);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_optimizeCb.js
// Internal function that returns an efficient (for current engines) version
// of the passed-in callback, to be repeatedly applied in other Underscore
// functions.
function optimizeCb(func, context, argCount) {
  if (context === void 0) return func;
  switch (argCount == null ? 3 : argCount) {
    case 1: return function(value) {
      return func.call(context, value);
    };
    // The 2-argument case is omitted because we’re not using it.
    case 3: return function(value, index, collection) {
      return func.call(context, value, index, collection);
    };
    case 4: return function(accumulator, value, index, collection) {
      return func.call(context, accumulator, value, index, collection);
    };
  }
  return function() {
    return func.apply(context, arguments);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_baseIteratee.js








// An internal function to generate callbacks that can be applied to each
// element in a collection, returning the desired result — either `_.identity`,
// an arbitrary callback, a property matcher, or a property accessor.
function baseIteratee(value, context, argCount) {
  if (value == null) return identity;
  if (modules_isFunction(value)) return optimizeCb(value, context, argCount);
  if (isObject(value) && !isArray(value)) return matcher_matcher(value);
  return property(value);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/iteratee.js



// External wrapper for our callback generator. Users may customize
// `_.iteratee` if they want additional predicate/iteratee shorthand styles.
// This abstraction hides the internal-only `argCount` argument.
function iteratee_iteratee(value, context) {
  return baseIteratee(value, context, Infinity);
}
_.iteratee = iteratee_iteratee;

// CONCATENATED MODULE: ./node_modules/underscore/modules/_cb.js




// The function we call internally to generate a callback. It invokes
// `_.iteratee` if overridden, otherwise `baseIteratee`.
function cb(value, context, argCount) {
  if (_.iteratee !== iteratee_iteratee) return _.iteratee(value, context);
  return baseIteratee(value, context, argCount);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/mapObject.js



// Returns the results of applying the `iteratee` to each element of `obj`.
// In contrast to `_.map` it returns an object.
function mapObject(obj, iteratee, context) {
  iteratee = cb(iteratee, context);
  var _keys = keys_keys(obj),
      length = _keys.length,
      results = {};
  for (var index = 0; index < length; index++) {
    var currentKey = _keys[index];
    results[currentKey] = iteratee(obj[currentKey], currentKey, obj);
  }
  return results;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/noop.js
// Predicate-generating function. Often useful outside of Underscore.
function noop(){}

// CONCATENATED MODULE: ./node_modules/underscore/modules/propertyOf.js



// Generates a function for a given object that returns a given property.
function propertyOf(obj) {
  if (obj == null) return noop;
  return function(path) {
    return get(obj, path);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/times.js


// Run a function **n** times.
function times(n, iteratee, context) {
  var accum = Array(Math.max(0, n));
  iteratee = optimizeCb(iteratee, context, 1);
  for (var i = 0; i < n; i++) accum[i] = iteratee(i);
  return accum;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/random.js
// Return a random integer between `min` and `max` (inclusive).
function random(min, max) {
  if (max == null) {
    max = min;
    min = 0;
  }
  return min + Math.floor(Math.random() * (max - min + 1));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/now.js
// A (possibly faster) way to get the current timestamp as an integer.
/* harmony default export */ var now = (Date.now || function() {
  return new Date().getTime();
});

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createEscaper.js


// Internal helper to generate functions for escaping and unescaping strings
// to/from HTML interpolation.
function createEscaper(map) {
  var escaper = function(match) {
    return map[match];
  };
  // Regexes for identifying a key that needs to be escaped.
  var source = '(?:' + keys_keys(map).join('|') + ')';
  var testRegexp = RegExp(source);
  var replaceRegexp = RegExp(source, 'g');
  return function(string) {
    string = string == null ? '' : '' + string;
    return testRegexp.test(string) ? string.replace(replaceRegexp, escaper) : string;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_escapeMap.js
// Internal list of HTML entities for escaping.
/* harmony default export */ var _escapeMap = ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#x27;',
  '`': '&#x60;'
});

// CONCATENATED MODULE: ./node_modules/underscore/modules/escape.js



// Function for escaping strings to HTML interpolation.
/* harmony default export */ var modules_escape = (createEscaper(_escapeMap));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_unescapeMap.js



// Internal list of HTML entities for unescaping.
/* harmony default export */ var _unescapeMap = (invert(_escapeMap));

// CONCATENATED MODULE: ./node_modules/underscore/modules/unescape.js



// Function for unescaping strings from HTML interpolation.
/* harmony default export */ var modules_unescape = (createEscaper(_unescapeMap));

// CONCATENATED MODULE: ./node_modules/underscore/modules/templateSettings.js


// By default, Underscore uses ERB-style template delimiters. Change the
// following template settings to use alternative delimiters.
/* harmony default export */ var templateSettings = (_.templateSettings = {
  evaluate: /<%([\s\S]+?)%>/g,
  interpolate: /<%=([\s\S]+?)%>/g,
  escape: /<%-([\s\S]+?)%>/g
});

// CONCATENATED MODULE: ./node_modules/underscore/modules/template.js




// When customizing `_.templateSettings`, if you don't want to define an
// interpolation, evaluation or escaping regex, we need one that is
// guaranteed not to match.
var noMatch = /(.)^/;

// Certain characters need to be escaped so that they can be put into a
// string literal.
var escapes = {
  "'": "'",
  '\\': '\\',
  '\r': 'r',
  '\n': 'n',
  '\u2028': 'u2028',
  '\u2029': 'u2029'
};

var escapeRegExp = /\\|'|\r|\n|\u2028|\u2029/g;

function escapeChar(match) {
  return '\\' + escapes[match];
}

var bareIdentifier = /^\s*(\w|\$)+\s*$/;

// JavaScript micro-templating, similar to John Resig's implementation.
// Underscore templating handles arbitrary delimiters, preserves whitespace,
// and correctly escapes quotes within interpolated code.
// NB: `oldSettings` only exists for backwards compatibility.
function template_template(text, settings, oldSettings) {
  if (!settings && oldSettings) settings = oldSettings;
  settings = defaults({}, settings, _.templateSettings);

  // Combine delimiters into one regular expression via alternation.
  var matcher = RegExp([
    (settings.escape || noMatch).source,
    (settings.interpolate || noMatch).source,
    (settings.evaluate || noMatch).source
  ].join('|') + '|$', 'g');

  // Compile the template source, escaping string literals appropriately.
  var index = 0;
  var source = "__p+='";
  text.replace(matcher, function(match, escape, interpolate, evaluate, offset) {
    source += text.slice(index, offset).replace(escapeRegExp, escapeChar);
    index = offset + match.length;

    if (escape) {
      source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'";
    } else if (interpolate) {
      source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'";
    } else if (evaluate) {
      source += "';\n" + evaluate + "\n__p+='";
    }

    // Adobe VMs need the match returned to produce the correct offset.
    return match;
  });
  source += "';\n";

  var argument = settings.variable;
  if (argument) {
    if (!bareIdentifier.test(argument)) throw new Error(argument);
  } else {
    // If a variable is not specified, place data values in local scope.
    source = 'with(obj||{}){\n' + source + '}\n';
    argument = 'obj';
  }

  source = "var __t,__p='',__j=Array.prototype.join," +
    "print=function(){__p+=__j.call(arguments,'');};\n" +
    source + 'return __p;\n';

  var render;
  try {
    render = new Function(argument, '_', source);
  } catch (e) {
    e.source = source;
    throw e;
  }

  var template = function(data) {
    return render.call(this, data, _);
  };

  // Provide the compiled source as a convenience for precompilation.
  template.source = 'function(' + argument + '){\n' + source + '}';

  return template;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/result.js



// Traverses the children of `obj` along `path`. If a child is a function, it
// is invoked with its parent as context. Returns the value of the final
// child, or `fallback` if any child is undefined.
function result_result(obj, path, fallback) {
  path = _toPath_toPath(path);
  var length = path.length;
  if (!length) {
    return modules_isFunction(fallback) ? fallback.call(obj) : fallback;
  }
  for (var i = 0; i < length; i++) {
    var prop = obj == null ? void 0 : obj[path[i]];
    if (prop === void 0) {
      prop = fallback;
      i = length; // Ensure we don't continue iterating.
    }
    obj = modules_isFunction(prop) ? prop.call(obj) : prop;
  }
  return obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/uniqueId.js
// Generate a unique integer id (unique within the entire client session).
// Useful for temporary DOM ids.
var idCounter = 0;
function uniqueId(prefix) {
  var id = ++idCounter + '';
  return prefix ? prefix + id : id;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/chain.js


// Start chaining a wrapped Underscore object.
function chain(obj) {
  var instance = _(obj);
  instance._chain = true;
  return instance;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_executeBound.js



// Internal function to execute `sourceFunc` bound to `context` with optional
// `args`. Determines whether to execute a function as a constructor or as a
// normal function.
function executeBound(sourceFunc, boundFunc, context, callingContext, args) {
  if (!(callingContext instanceof boundFunc)) return sourceFunc.apply(context, args);
  var self = baseCreate(sourceFunc.prototype);
  var result = sourceFunc.apply(self, args);
  if (isObject(result)) return result;
  return self;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/partial.js




// Partially apply a function by creating a version that has had some of its
// arguments pre-filled, without changing its dynamic `this` context. `_` acts
// as a placeholder by default, allowing any combination of arguments to be
// pre-filled. Set `_.partial.placeholder` for a custom placeholder argument.
var partial = restArguments(function(func, boundArgs) {
  var placeholder = partial.placeholder;
  var bound = function() {
    var position = 0, length = boundArgs.length;
    var args = Array(length);
    for (var i = 0; i < length; i++) {
      args[i] = boundArgs[i] === placeholder ? arguments[position++] : boundArgs[i];
    }
    while (position < arguments.length) args.push(arguments[position++]);
    return executeBound(func, bound, this, this, args);
  };
  return bound;
});

partial.placeholder = _;
/* harmony default export */ var modules_partial = (partial);

// CONCATENATED MODULE: ./node_modules/underscore/modules/bind.js




// Create a function bound to a given object (assigning `this`, and arguments,
// optionally).
/* harmony default export */ var bind = (restArguments(function(func, context, args) {
  if (!modules_isFunction(func)) throw new TypeError('Bind must be called on a function');
  var bound = restArguments(function(callArgs) {
    return executeBound(func, bound, context, this, args.concat(callArgs));
  });
  return bound;
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_isArrayLike.js



// Internal helper for collection methods to determine whether a collection
// should be iterated as an array or as an object.
// Related: https://people.mozilla.org/~jorendorff/es6-draft.html#sec-tolength
// Avoids a very nasty iOS 8 JIT bug on ARM-64. #2094
/* harmony default export */ var _isArrayLike = (createSizePropertyCheck(_getLength));

// CONCATENATED MODULE: ./node_modules/underscore/modules/_flatten.js





// Internal implementation of a recursive `flatten` function.
function flatten(input, depth, strict, output) {
  output = output || [];
  if (!depth && depth !== 0) {
    depth = Infinity;
  } else if (depth <= 0) {
    return output.concat(input);
  }
  var idx = output.length;
  for (var i = 0, length = _getLength(input); i < length; i++) {
    var value = input[i];
    if (_isArrayLike(value) && (isArray(value) || modules_isArguments(value))) {
      // Flatten current level of array or arguments object.
      if (depth > 1) {
        flatten(value, depth - 1, strict, output);
        idx = output.length;
      } else {
        var j = 0, len = value.length;
        while (j < len) output[idx++] = value[j++];
      }
    } else if (!strict) {
      output[idx++] = value;
    }
  }
  return output;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/bindAll.js




// Bind a number of an object's methods to that object. Remaining arguments
// are the method names to be bound. Useful for ensuring that all callbacks
// defined on an object belong to it.
/* harmony default export */ var bindAll = (restArguments(function(obj, keys) {
  keys = flatten(keys, false, false);
  var index = keys.length;
  if (index < 1) throw new Error('bindAll must be passed function names');
  while (index--) {
    var key = keys[index];
    obj[key] = bind(obj[key], obj);
  }
  return obj;
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/memoize.js


// Memoize an expensive function by storing its results.
function memoize_memoize(func, hasher) {
  var memoize = function(key) {
    var cache = memoize.cache;
    var address = '' + (hasher ? hasher.apply(this, arguments) : key);
    if (!has(cache, address)) cache[address] = func.apply(this, arguments);
    return cache[address];
  };
  memoize.cache = {};
  return memoize;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/delay.js


// Delays a function for the given number of milliseconds, and then calls
// it with the arguments supplied.
/* harmony default export */ var delay = (restArguments(function(func, wait, args) {
  return setTimeout(function() {
    return func.apply(null, args);
  }, wait);
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/defer.js




// Defers a function, scheduling it to run after the current call stack has
// cleared.
/* harmony default export */ var defer = (modules_partial(delay, _, 1));

// CONCATENATED MODULE: ./node_modules/underscore/modules/throttle.js


// Returns a function, that, when invoked, will only be triggered at most once
// during a given window of time. Normally, the throttled function will run
// as much as it can, without ever going more than once per `wait` duration;
// but if you'd like to disable the execution on the leading edge, pass
// `{leading: false}`. To disable execution on the trailing edge, ditto.
function throttle(func, wait, options) {
  var timeout, context, args, result;
  var previous = 0;
  if (!options) options = {};

  var later = function() {
    previous = options.leading === false ? 0 : now();
    timeout = null;
    result = func.apply(context, args);
    if (!timeout) context = args = null;
  };

  var throttled = function() {
    var _now = now();
    if (!previous && options.leading === false) previous = _now;
    var remaining = wait - (_now - previous);
    context = this;
    args = arguments;
    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = _now;
      result = func.apply(context, args);
      if (!timeout) context = args = null;
    } else if (!timeout && options.trailing !== false) {
      timeout = setTimeout(later, remaining);
    }
    return result;
  };

  throttled.cancel = function() {
    clearTimeout(timeout);
    previous = 0;
    timeout = context = args = null;
  };

  return throttled;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/debounce.js



// When a sequence of calls of the returned function ends, the argument
// function is triggered. The end of a sequence is defined by the `wait`
// parameter. If `immediate` is passed, the argument function will be
// triggered at the beginning of the sequence instead of at the end.
function debounce(func, wait, immediate) {
  var timeout, previous, args, result, context;

  var later = function() {
    var passed = now() - previous;
    if (wait > passed) {
      timeout = setTimeout(later, wait - passed);
    } else {
      timeout = null;
      if (!immediate) result = func.apply(context, args);
      // This check is needed because `func` can recursively invoke `debounced`.
      if (!timeout) args = context = null;
    }
  };

  var debounced = restArguments(function(_args) {
    context = this;
    args = _args;
    previous = now();
    if (!timeout) {
      timeout = setTimeout(later, wait);
      if (immediate) result = func.apply(context, args);
    }
    return result;
  });

  debounced.cancel = function() {
    clearTimeout(timeout);
    timeout = args = context = null;
  };

  return debounced;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/wrap.js


// Returns the first function passed as an argument to the second,
// allowing you to adjust arguments, run code before and after, and
// conditionally execute the original function.
function wrap(func, wrapper) {
  return modules_partial(wrapper, func);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/negate.js
// Returns a negated version of the passed-in predicate.
function negate(predicate) {
  return function() {
    return !predicate.apply(this, arguments);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/compose.js
// Returns a function that is the composition of a list of functions, each
// consuming the return value of the function that follows.
function compose() {
  var args = arguments;
  var start = args.length - 1;
  return function() {
    var i = start;
    var result = args[start].apply(this, arguments);
    while (i--) result = args[i].call(this, result);
    return result;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/after.js
// Returns a function that will only be executed on and after the Nth call.
function after(times, func) {
  return function() {
    if (--times < 1) {
      return func.apply(this, arguments);
    }
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/before.js
// Returns a function that will only be executed up to (but not including) the
// Nth call.
function before(times, func) {
  var memo;
  return function() {
    if (--times > 0) {
      memo = func.apply(this, arguments);
    }
    if (times <= 1) func = null;
    return memo;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/once.js



// Returns a function that will be executed at most one time, no matter how
// often you call it. Useful for lazy initialization.
/* harmony default export */ var once = (modules_partial(before, 2));

// CONCATENATED MODULE: ./node_modules/underscore/modules/findKey.js



// Returns the first key on an object that passes a truth test.
function findKey(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = keys_keys(obj), key;
  for (var i = 0, length = _keys.length; i < length; i++) {
    key = _keys[i];
    if (predicate(obj[key], key, obj)) return key;
  }
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createPredicateIndexFinder.js



// Internal function to generate `_.findIndex` and `_.findLastIndex`.
function createPredicateIndexFinder(dir) {
  return function(array, predicate, context) {
    predicate = cb(predicate, context);
    var length = _getLength(array);
    var index = dir > 0 ? 0 : length - 1;
    for (; index >= 0 && index < length; index += dir) {
      if (predicate(array[index], index, array)) return index;
    }
    return -1;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/findIndex.js


// Returns the first index on an array-like that passes a truth test.
/* harmony default export */ var findIndex = (createPredicateIndexFinder(1));

// CONCATENATED MODULE: ./node_modules/underscore/modules/findLastIndex.js


// Returns the last index on an array-like that passes a truth test.
/* harmony default export */ var findLastIndex = (createPredicateIndexFinder(-1));

// CONCATENATED MODULE: ./node_modules/underscore/modules/sortedIndex.js



// Use a comparator function to figure out the smallest index at which
// an object should be inserted so as to maintain order. Uses binary search.
function sortedIndex_sortedIndex(array, obj, iteratee, context) {
  iteratee = cb(iteratee, context, 1);
  var value = iteratee(obj);
  var low = 0, high = _getLength(array);
  while (low < high) {
    var mid = Math.floor((low + high) / 2);
    if (iteratee(array[mid]) < value) low = mid + 1; else high = mid;
  }
  return low;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createIndexFinder.js




// Internal function to generate the `_.indexOf` and `_.lastIndexOf` functions.
function createIndexFinder(dir, predicateFind, sortedIndex) {
  return function(array, item, idx) {
    var i = 0, length = _getLength(array);
    if (typeof idx == 'number') {
      if (dir > 0) {
        i = idx >= 0 ? idx : Math.max(idx + length, i);
      } else {
        length = idx >= 0 ? Math.min(idx + 1, length) : idx + length + 1;
      }
    } else if (sortedIndex && idx && length) {
      idx = sortedIndex(array, item);
      return array[idx] === item ? idx : -1;
    }
    if (item !== item) {
      idx = predicateFind(_setup["q" /* slice */].call(array, i, length), isNaN_isNaN);
      return idx >= 0 ? idx + i : -1;
    }
    for (idx = dir > 0 ? i : length - 1; idx >= 0 && idx < length; idx += dir) {
      if (array[idx] === item) return idx;
    }
    return -1;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/indexOf.js




// Return the position of the first occurrence of an item in an array,
// or -1 if the item is not included in the array.
// If the array is large and already in sort order, pass `true`
// for **isSorted** to use binary search.
/* harmony default export */ var indexOf = (createIndexFinder(1, findIndex, sortedIndex_sortedIndex));

// CONCATENATED MODULE: ./node_modules/underscore/modules/lastIndexOf.js



// Return the position of the last occurrence of an item in an array,
// or -1 if the item is not included in the array.
/* harmony default export */ var lastIndexOf = (createIndexFinder(-1, findLastIndex));

// CONCATENATED MODULE: ./node_modules/underscore/modules/find.js




// Return the first value which passes a truth test.
function find(obj, predicate, context) {
  var keyFinder = _isArrayLike(obj) ? findIndex : findKey;
  var key = keyFinder(obj, predicate, context);
  if (key !== void 0 && key !== -1) return obj[key];
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/findWhere.js



// Convenience version of a common use case of `_.find`: getting the first
// object containing specific `key:value` pairs.
function findWhere(obj, attrs) {
  return find(obj, matcher_matcher(attrs));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/each.js




// The cornerstone for collection functions, an `each`
// implementation, aka `forEach`.
// Handles raw objects in addition to array-likes. Treats all
// sparse array-likes as if they were dense.
function each(obj, iteratee, context) {
  iteratee = optimizeCb(iteratee, context);
  var i, length;
  if (_isArrayLike(obj)) {
    for (i = 0, length = obj.length; i < length; i++) {
      iteratee(obj[i], i, obj);
    }
  } else {
    var _keys = keys_keys(obj);
    for (i = 0, length = _keys.length; i < length; i++) {
      iteratee(obj[_keys[i]], _keys[i], obj);
    }
  }
  return obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/map.js




// Return the results of applying the iteratee to each element.
function map_map(obj, iteratee, context) {
  iteratee = cb(iteratee, context);
  var _keys = !_isArrayLike(obj) && keys_keys(obj),
      length = (_keys || obj).length,
      results = Array(length);
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    results[index] = iteratee(obj[currentKey], currentKey, obj);
  }
  return results;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_createReduce.js




// Internal helper to create a reducing function, iterating left or right.
function createReduce(dir) {
  // Wrap code that reassigns argument variables in a separate function than
  // the one that accesses `arguments.length` to avoid a perf hit. (#1991)
  var reducer = function(obj, iteratee, memo, initial) {
    var _keys = !_isArrayLike(obj) && keys_keys(obj),
        length = (_keys || obj).length,
        index = dir > 0 ? 0 : length - 1;
    if (!initial) {
      memo = obj[_keys ? _keys[index] : index];
      index += dir;
    }
    for (; index >= 0 && index < length; index += dir) {
      var currentKey = _keys ? _keys[index] : index;
      memo = iteratee(memo, obj[currentKey], currentKey, obj);
    }
    return memo;
  };

  return function(obj, iteratee, memo, context) {
    var initial = arguments.length >= 3;
    return reducer(obj, optimizeCb(iteratee, context, 4), memo, initial);
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/reduce.js


// **Reduce** builds up a single result from a list of values, aka `inject`,
// or `foldl`.
/* harmony default export */ var reduce = (createReduce(1));

// CONCATENATED MODULE: ./node_modules/underscore/modules/reduceRight.js


// The right-associative version of reduce, also known as `foldr`.
/* harmony default export */ var reduceRight = (createReduce(-1));

// CONCATENATED MODULE: ./node_modules/underscore/modules/filter.js



// Return all the elements that pass a truth test.
function filter(obj, predicate, context) {
  var results = [];
  predicate = cb(predicate, context);
  each(obj, function(value, index, list) {
    if (predicate(value, index, list)) results.push(value);
  });
  return results;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/reject.js




// Return all the elements for which a truth test fails.
function reject(obj, predicate, context) {
  return filter(obj, negate(cb(predicate)), context);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/every.js




// Determine whether all of the elements pass a truth test.
function every(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = !_isArrayLike(obj) && keys_keys(obj),
      length = (_keys || obj).length;
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    if (!predicate(obj[currentKey], currentKey, obj)) return false;
  }
  return true;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/some.js




// Determine if at least one element in the object passes a truth test.
function some(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = !_isArrayLike(obj) && keys_keys(obj),
      length = (_keys || obj).length;
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    if (predicate(obj[currentKey], currentKey, obj)) return true;
  }
  return false;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/contains.js




// Determine if the array or object contains a given item (using `===`).
function contains(obj, item, fromIndex, guard) {
  if (!_isArrayLike(obj)) obj = values_values(obj);
  if (typeof fromIndex != 'number' || guard) fromIndex = 0;
  return indexOf(obj, item, fromIndex) >= 0;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/invoke.js






// Invoke a method (with arguments) on every item in a collection.
/* harmony default export */ var invoke = (restArguments(function(obj, path, args) {
  var contextPath, func;
  if (modules_isFunction(path)) {
    func = path;
  } else {
    path = _toPath_toPath(path);
    contextPath = path.slice(0, -1);
    path = path[path.length - 1];
  }
  return map_map(obj, function(context) {
    var method = func;
    if (!method) {
      if (contextPath && contextPath.length) {
        context = deepGet(context, contextPath);
      }
      if (context == null) return void 0;
      method = context[path];
    }
    return method == null ? method : method.apply(context, args);
  });
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/pluck.js



// Convenience version of a common use case of `_.map`: fetching a property.
function pluck(obj, key) {
  return map_map(obj, property(key));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/where.js



// Convenience version of a common use case of `_.filter`: selecting only
// objects containing specific `key:value` pairs.
function where(obj, attrs) {
  return filter(obj, matcher_matcher(attrs));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/max.js





// Return the maximum element (or element-based computation).
function max(obj, iteratee, context) {
  var result = -Infinity, lastComputed = -Infinity,
      value, computed;
  if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
    obj = _isArrayLike(obj) ? obj : values_values(obj);
    for (var i = 0, length = obj.length; i < length; i++) {
      value = obj[i];
      if (value != null && value > result) {
        result = value;
      }
    }
  } else {
    iteratee = cb(iteratee, context);
    each(obj, function(v, index, list) {
      computed = iteratee(v, index, list);
      if (computed > lastComputed || computed === -Infinity && result === -Infinity) {
        result = v;
        lastComputed = computed;
      }
    });
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/min.js





// Return the minimum element (or element-based computation).
function min(obj, iteratee, context) {
  var result = Infinity, lastComputed = Infinity,
      value, computed;
  if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
    obj = _isArrayLike(obj) ? obj : values_values(obj);
    for (var i = 0, length = obj.length; i < length; i++) {
      value = obj[i];
      if (value != null && value < result) {
        result = value;
      }
    }
  } else {
    iteratee = cb(iteratee, context);
    each(obj, function(v, index, list) {
      computed = iteratee(v, index, list);
      if (computed < lastComputed || computed === Infinity && result === Infinity) {
        result = v;
        lastComputed = computed;
      }
    });
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/sample.js






// Sample **n** random values from a collection using the modern version of the
// [Fisher-Yates shuffle](https://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
// If **n** is not specified, returns a single random element.
// The internal `guard` argument allows it to work with `_.map`.
function sample_sample(obj, n, guard) {
  if (n == null || guard) {
    if (!_isArrayLike(obj)) obj = values_values(obj);
    return obj[random(obj.length - 1)];
  }
  var sample = _isArrayLike(obj) ? clone(obj) : values_values(obj);
  var length = _getLength(sample);
  n = Math.max(Math.min(n, length), 0);
  var last = length - 1;
  for (var index = 0; index < n; index++) {
    var rand = random(index, last);
    var temp = sample[index];
    sample[index] = sample[rand];
    sample[rand] = temp;
  }
  return sample.slice(0, n);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/shuffle.js


// Shuffle a collection.
function shuffle(obj) {
  return sample_sample(obj, Infinity);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/sortBy.js




// Sort the object's values by a criterion produced by an iteratee.
function sortBy(obj, iteratee, context) {
  var index = 0;
  iteratee = cb(iteratee, context);
  return pluck(map_map(obj, function(value, key, list) {
    return {
      value: value,
      index: index++,
      criteria: iteratee(value, key, list)
    };
  }).sort(function(left, right) {
    var a = left.criteria;
    var b = right.criteria;
    if (a !== b) {
      if (a > b || a === void 0) return 1;
      if (a < b || b === void 0) return -1;
    }
    return left.index - right.index;
  }), 'value');
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_group.js



// An internal function used for aggregate "group by" operations.
function group(behavior, partition) {
  return function(obj, iteratee, context) {
    var result = partition ? [[], []] : {};
    iteratee = cb(iteratee, context);
    each(obj, function(value, index) {
      var key = iteratee(value, index, obj);
      behavior(result, value, key);
    });
    return result;
  };
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/groupBy.js



// Groups the object's values by a criterion. Pass either a string attribute
// to group by, or a function that returns the criterion.
/* harmony default export */ var groupBy = (group(function(result, value, key) {
  if (has(result, key)) result[key].push(value); else result[key] = [value];
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/indexBy.js


// Indexes the object's values by a criterion, similar to `_.groupBy`, but for
// when you know that your index values will be unique.
/* harmony default export */ var indexBy = (group(function(result, value, key) {
  result[key] = value;
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/countBy.js



// Counts instances of an object that group by a certain criterion. Pass
// either a string attribute to count by, or a function that returns the
// criterion.
/* harmony default export */ var countBy = (group(function(result, value, key) {
  if (has(result, key)) result[key]++; else result[key] = 1;
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/partition.js


// Split a collection into two arrays: one whose elements all pass the given
// truth test, and one whose elements all do not pass the truth test.
/* harmony default export */ var modules_partition = (group(function(result, value, pass) {
  result[pass ? 0 : 1].push(value);
}, true));

// CONCATENATED MODULE: ./node_modules/underscore/modules/toArray.js








// Safely create a real, live array from anything iterable.
var reStrSymbol = /[^\ud800-\udfff]|[\ud800-\udbff][\udc00-\udfff]|[\ud800-\udfff]/g;
function toArray(obj) {
  if (!obj) return [];
  if (isArray(obj)) return _setup["q" /* slice */].call(obj);
  if (isString(obj)) {
    // Keep surrogate pair characters together.
    return obj.match(reStrSymbol);
  }
  if (_isArrayLike(obj)) return map_map(obj, identity);
  return values_values(obj);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/size.js



// Return the number of elements in a collection.
function size(obj) {
  if (obj == null) return 0;
  return _isArrayLike(obj) ? obj.length : keys_keys(obj).length;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_keyInObj.js
// Internal `_.pick` helper function to determine whether `key` is an enumerable
// property name of `obj`.
function keyInObj(value, key, obj) {
  return key in obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/pick.js







// Return a copy of the object only containing the allowed properties.
/* harmony default export */ var pick = (restArguments(function(obj, keys) {
  var result = {}, iteratee = keys[0];
  if (obj == null) return result;
  if (modules_isFunction(iteratee)) {
    if (keys.length > 1) iteratee = optimizeCb(iteratee, keys[1]);
    keys = allKeys(obj);
  } else {
    iteratee = keyInObj;
    keys = flatten(keys, false, false);
    obj = Object(obj);
  }
  for (var i = 0, length = keys.length; i < length; i++) {
    var key = keys[i];
    var value = obj[key];
    if (iteratee(value, key, obj)) result[key] = value;
  }
  return result;
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/omit.js








// Return a copy of the object without the disallowed properties.
/* harmony default export */ var omit = (restArguments(function(obj, keys) {
  var iteratee = keys[0], context;
  if (modules_isFunction(iteratee)) {
    iteratee = negate(iteratee);
    if (keys.length > 1) context = keys[1];
  } else {
    keys = map_map(flatten(keys, false, false), String);
    iteratee = function(value, key) {
      return !contains(keys, key);
    };
  }
  return pick(obj, iteratee, context);
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/initial.js


// Returns everything but the last entry of the array. Especially useful on
// the arguments object. Passing **n** will return all the values in
// the array, excluding the last N.
function initial_initial(array, n, guard) {
  return _setup["q" /* slice */].call(array, 0, Math.max(0, array.length - (n == null || guard ? 1 : n)));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/first.js


// Get the first element of an array. Passing **n** will return the first N
// values in the array. The **guard** check allows it to work with `_.map`.
function first(array, n, guard) {
  if (array == null || array.length < 1) return n == null || guard ? void 0 : [];
  if (n == null || guard) return array[0];
  return initial_initial(array, array.length - n);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/rest.js


// Returns everything but the first entry of the `array`. Especially useful on
// the `arguments` object. Passing an **n** will return the rest N values in the
// `array`.
function rest_rest(array, n, guard) {
  return _setup["q" /* slice */].call(array, n == null || guard ? 1 : n);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/last.js


// Get the last element of an array. Passing **n** will return the last N
// values in the array.
function last_last(array, n, guard) {
  if (array == null || array.length < 1) return n == null || guard ? void 0 : [];
  if (n == null || guard) return array[array.length - 1];
  return rest_rest(array, Math.max(0, array.length - n));
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/compact.js


// Trim out all falsy values from an array.
function compact(array) {
  return filter(array, Boolean);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/flatten.js


// Flatten out an array, either recursively (by default), or up to `depth`.
// Passing `true` or `false` as `depth` means `1` or `Infinity`, respectively.
function flatten_flatten(array, depth) {
  return flatten(array, depth, false);
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/difference.js





// Take the difference between one array and a number of other arrays.
// Only the elements present in just the first array will remain.
/* harmony default export */ var difference = (restArguments(function(array, rest) {
  rest = flatten(rest, true, true);
  return filter(array, function(value){
    return !contains(rest, value);
  });
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/without.js



// Return a version of the array that does not contain the specified value(s).
/* harmony default export */ var without = (restArguments(function(array, otherArrays) {
  return difference(array, otherArrays);
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/uniq.js





// Produce a duplicate-free version of the array. If the array has already
// been sorted, you have the option of using a faster algorithm.
// The faster algorithm will not work with an iteratee if the iteratee
// is not a one-to-one function, so providing an iteratee will disable
// the faster algorithm.
function uniq(array, isSorted, iteratee, context) {
  if (!isBoolean(isSorted)) {
    context = iteratee;
    iteratee = isSorted;
    isSorted = false;
  }
  if (iteratee != null) iteratee = cb(iteratee, context);
  var result = [];
  var seen = [];
  for (var i = 0, length = _getLength(array); i < length; i++) {
    var value = array[i],
        computed = iteratee ? iteratee(value, i, array) : value;
    if (isSorted && !iteratee) {
      if (!i || seen !== computed) result.push(value);
      seen = computed;
    } else if (iteratee) {
      if (!contains(seen, computed)) {
        seen.push(computed);
        result.push(value);
      }
    } else if (!contains(result, value)) {
      result.push(value);
    }
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/union.js




// Produce an array that contains the union: each distinct element from all of
// the passed-in arrays.
/* harmony default export */ var union = (restArguments(function(arrays) {
  return uniq(flatten(arrays, true, true));
}));

// CONCATENATED MODULE: ./node_modules/underscore/modules/intersection.js



// Produce an array that contains every item shared between all the
// passed-in arrays.
function intersection(array) {
  var result = [];
  var argsLength = arguments.length;
  for (var i = 0, length = _getLength(array); i < length; i++) {
    var item = array[i];
    if (contains(result, item)) continue;
    var j;
    for (j = 1; j < argsLength; j++) {
      if (!contains(arguments[j], item)) break;
    }
    if (j === argsLength) result.push(item);
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/unzip.js




// Complement of zip. Unzip accepts an array of arrays and groups
// each array's elements on shared indices.
function unzip(array) {
  var length = array && max(array, _getLength).length || 0;
  var result = Array(length);

  for (var index = 0; index < length; index++) {
    result[index] = pluck(array, index);
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/zip.js



// Zip together multiple lists into a single array -- elements that share
// an index go together.
/* harmony default export */ var zip = (restArguments(unzip));

// CONCATENATED MODULE: ./node_modules/underscore/modules/object.js


// Converts lists into objects. Pass either a single array of `[key, value]`
// pairs, or two parallel arrays of the same length -- one of keys, and one of
// the corresponding values. Passing by pairs is the reverse of `_.pairs`.
function object_object(list, values) {
  var result = {};
  for (var i = 0, length = _getLength(list); i < length; i++) {
    if (values) {
      result[list[i]] = values[i];
    } else {
      result[list[i][0]] = list[i][1];
    }
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/range.js
// Generate an integer Array containing an arithmetic progression. A port of
// the native Python `range()` function. See
// [the Python documentation](https://docs.python.org/library/functions.html#range).
function range(start, stop, step) {
  if (stop == null) {
    stop = start || 0;
    start = 0;
  }
  if (!step) {
    step = stop < start ? -1 : 1;
  }

  var length = Math.max(Math.ceil((stop - start) / step), 0);
  var range = Array(length);

  for (var idx = 0; idx < length; idx++, start += step) {
    range[idx] = start;
  }

  return range;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/chunk.js


// Chunk a single array into multiple arrays, each containing `count` or fewer
// items.
function chunk(array, count) {
  if (count == null || count < 1) return [];
  var result = [];
  var i = 0, length = array.length;
  while (i < length) {
    result.push(_setup["q" /* slice */].call(array, i, i += count));
  }
  return result;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/_chainResult.js


// Helper function to continue chaining intermediate results.
function chainResult(instance, obj) {
  return instance._chain ? _(obj).chain() : obj;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/mixin.js






// Add your own custom functions to the Underscore object.
function mixin(obj) {
  each(functions(obj), function(name) {
    var func = _[name] = obj[name];
    _.prototype[name] = function() {
      var args = [this._wrapped];
      _setup["o" /* push */].apply(args, arguments);
      return chainResult(this, func.apply(_, args));
    };
  });
  return _;
}

// CONCATENATED MODULE: ./node_modules/underscore/modules/underscore-array-methods.js





// Add all mutator `Array` functions to the wrapper.
each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
  var method = _setup["a" /* ArrayProto */][name];
  _.prototype[name] = function() {
    var obj = this._wrapped;
    if (obj != null) {
      method.apply(obj, arguments);
      if ((name === 'shift' || name === 'splice') && obj.length === 0) {
        delete obj[0];
      }
    }
    return chainResult(this, obj);
  };
});

// Add all accessor `Array` functions to the wrapper.
each(['concat', 'join', 'slice'], function(name) {
  var method = _setup["a" /* ArrayProto */][name];
  _.prototype[name] = function() {
    var obj = this._wrapped;
    if (obj != null) obj = method.apply(obj, arguments);
    return chainResult(this, obj);
  };
});

/* harmony default export */ var underscore_array_methods = (_);

// CONCATENATED MODULE: ./node_modules/underscore/modules/index.js
// Named Exports
// =============

//     Underscore.js 1.12.1
//     https://underscorejs.org
//     (c) 2009-2020 Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
//     Underscore may be freely distributed under the MIT license.

// Baseline setup.



// Object Functions
// ----------------
// Our most fundamental functions operate on any JavaScript object.
// Most functions in Underscore depend on at least one function in this section.

// A group of functions that check the types of core JavaScript values.
// These are often informally referred to as the "isType" functions.



























// Functions that treat an object as a dictionary of key-value pairs.
















// Utility Functions
// -----------------
// A bit of a grab bag: Predicate-generating functions for use with filters and
// loops, string escaping and templating, create random numbers and unique ids,
// and functions that facilitate Underscore's chaining and iteration conventions.



















// Function (ahem) Functions
// -------------------------
// These functions take a function as an argument and return a new function
// as the result. Also known as higher-order functions.















// Finders
// -------
// Functions that extract (the position of) a single element from an object
// or array based on some criterion.









// Collection Functions
// --------------------
// Functions that work on any collection of elements: either an array, or
// an object of key-value pairs.
























// `_.pick` and `_.omit` are actually object functions, but we put
// them here in order to create a more natural reading order in the
// monolithic build as they depend on `_.contains`.



// Array Functions
// ---------------
// Functions that operate on arrays (and array-likes) only, because they’re
// expressed in terms of operations on an ordered list of values.

















// OOP
// ---
// These modules support the "object-oriented" calling style. See also
// `underscore.js` and `index-default.js`.



// CONCATENATED MODULE: ./node_modules/underscore/modules/index-default.js
// Default Export
// ==============
// In this module, we mix our bundled exports into the `_` object and export
// the result. This is analogous to setting `module.exports = _` in CommonJS.
// Hence, this module is also the entry point of our UMD bundle and the package
// entry point for CommonJS and AMD users. In other words, this is (the source
// of) the module you are interfacing with when you do any of the following:
//
// ```js
// // CommonJS
// var _ = require('underscore');
//
// // AMD
// define(['underscore'], function(_) {...});
//
// // UMD in the browser
// // _ is available as a global variable
// ```



// Add all of the Underscore functions to the wrapper object.
var index_default_ = mixin(modules_namespaceObject);
// Legacy Node.js API.
index_default_._ = index_default_;
// Export the Underscore API.
/* harmony default export */ var index_default = (index_default_);

// CONCATENATED MODULE: ./node_modules/underscore/modules/index-all.js
// ESM Exports
// ===========
// This module is the package entry point for ES module users. In other words,
// it is the module they are interfacing with when they import from the whole
// package instead of from a submodule, like this:
//
// ```js
// import { map } from 'underscore';
// ```
//
// The difference with `./index-default`, which is the package entry point for
// CommonJS, AMD and UMD users, is purely technical. In ES modules, named and
// default exports are considered to be siblings, so when you have a default
// export, its properties are not automatically available as named exports. For
// this reason, we re-export the named exports in addition to providing the same
// default export as in `./index-default`.




/***/ }),

/***/ 74:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export parser */
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(19);
/* harmony import */ var regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _core_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(5);
/* harmony import */ var _core_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(4);
/* harmony import */ var _core_logging__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(6);
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

 // needed for ``await`` support



 // Lazy loading modules.

var Moment;
var log = _core_logging__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].getLogger("pat-display-time");
var parser = new _core_parser__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"]("display-time"); // input datetime options

parser.add_argument("format", "");
parser.add_argument("locale", null);
parser.add_argument("strict", false); // output options

parser.add_argument("from-now", false);
parser.add_argument("no-suffix", false);
parser.add_argument("output-format", null);
/* harmony default export */ __webpack_exports__["a"] = (_core_base__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].extend({
  name: "display-time",
  trigger: ".pat-display-time",
  init: function init() {
    var _this = this;

    return _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var lang;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              _context.next = 2;
              return __webpack_require__.e(/* import() */ 0).then(__webpack_require__.t.bind(null, 179, 7));

            case 2:
              Moment = _context.sent.default;
              _this.options = parser.parse(_this.el, _this.options);
              lang = _this.options.locale || document.querySelector("html").lang || "en"; // we don't support any country-specific language variants, always use first 2 letters

              lang = lang.substr(0, 2).toLowerCase();
              _context.prev = 6;
              _context.next = 9;
              return __webpack_require__(105)("./".concat(lang, ".js"));

            case 9:
              Moment.locale(lang);
              _context.next = 15;
              break;

            case 12:
              _context.prev = 12;
              _context.t0 = _context["catch"](6);
              Moment.locale("en");

            case 15:
              log.info("Moment.js language used: " + lang);

              _this.format();

            case 17:
            case "end":
              return _context.stop();
          }
        }
      }, _callee, null, [[6, 12]]);
    }))();
  },
  format: function format() {
    var out = this.el.getAttribute("datetime");

    if (out && this.options.outputFormat) {
      var date = Moment(out, this.options.format, this.options.strict);

      if (this.options.fromNow === true) {
        out = date.fromNow(this.options.noSuffix);
      } else {
        out = date.format(this.options.outputFormat || undefined);
      }
    }

    this.el.textContent = out;
  }
}));

/***/ }),

/***/ 9:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(0);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(11);
/* harmony import */ var _logging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(6);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(2);
function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

/**
 * Patterns registry - Central registry and scan logic for patterns
 *
 * Copyright 2012-2013 Simplon B.V.
 * Copyright 2012-2013 Florian Friesdorf
 * Copyright 2013 Marko Durkovic
 * Copyright 2013 Rok Garbas
 * Copyright 2014-2015 Syslab.com GmBH, JC Brand
 */

/*
 * changes to previous patterns.register/scan mechanism
 * - if you want initialised class, do it in init
 * - init returns set of elements actually initialised
 * - handle once within init
 * - no turnstile anymore
 * - set pattern.jquery_plugin if you want it
 */




var log = _logging__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].getLogger("registry");
var disable_re = /patterns-disable=([^&]+)/g;
var dont_catch_re = /patterns-dont-catch/g;
var disabled = {};
var dont_catch = false;
var match;

while ((match = disable_re.exec(window.location.search)) !== null) {
  disabled[match[1]] = true;
  log.info("Pattern disabled via url config:", match[1]);
}

while ((match = dont_catch_re.exec(window.location.search)) !== null) {
  dont_catch = true;
  log.info("I will not catch init exceptions");
}

var registry = {
  patterns: {},
  // as long as the registry is not initialized, pattern
  // registration just registers a pattern. Once init is called,
  // the DOM is scanned. After that registering a new pattern
  // results in rescanning the DOM only for this pattern.
  initialized: false,
  init: function init() {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(document).ready(function () {
      log.info("loaded: " + Object.keys(registry.patterns).sort().join(", "));
      registry.scan(document.body);
      registry.initialized = true;
      log.info("finished initial scan.");
    });
  },
  clear: function clear() {
    // Removes all patterns from the registry. Currently only being
    // used in tests.
    this.patterns = {};
  },
  transformPattern: function transformPattern(name, content) {
    var _pattern$prototype;

    /* Call the transform method on the pattern with the given name, if
     * it exists.
     */
    if (disabled[name]) {
      log.debug("Skipping disabled pattern:", name);
      return;
    }

    var pattern = registry.patterns[name];
    var transform = pattern.transform || ((_pattern$prototype = pattern.prototype) === null || _pattern$prototype === void 0 ? void 0 : _pattern$prototype.transform);

    if (transform) {
      try {
        transform(jquery__WEBPACK_IMPORTED_MODULE_0___default()(content));
      } catch (e) {
        if (dont_catch) {
          throw e;
        }

        log.error("Transform error for pattern" + name, e);
      }
    }
  },
  initPattern: function initPattern(name, el, trigger) {
    /* Initialize the pattern with the provided name and in the context
     * of the passed in DOM element.
     */
    var $el = jquery__WEBPACK_IMPORTED_MODULE_0___default()(el);
    var pattern = registry.patterns[name];

    if (pattern.init) {
      var plog = _logging__WEBPACK_IMPORTED_MODULE_2__[/* default */ "a"].getLogger("pat." + name);

      if ($el.is(pattern.trigger)) {
        plog.debug("Initialising:", $el);

        try {
          pattern.init($el, null, trigger);
          plog.debug("done.");
        } catch (e) {
          if (dont_catch) {
            throw e;
          }

          plog.error("Caught error:", e);
        }
      }
    }
  },
  orderPatterns: function orderPatterns(patterns) {
    // XXX: Bit of a hack. We need the validation pattern to be
    // parsed and initiated before the inject pattern. So we make
    // sure here, that it appears first. Not sure what would be
    // the best solution. Perhaps some kind of way to register
    // patterns "before" or "after" other patterns.
    if (patterns.includes("validation") && patterns.includes("inject")) {
      patterns.splice(patterns.indexOf("validation"), 1);
      patterns.unshift("validation");
    }

    return patterns;
  },
  scan: function scan(content, patterns, trigger) {
    if (typeof content === "string") {
      content = document.querySelector(content);
    } else if (content.jquery) {
      content = content[0];
    }

    var selectors = [];
    patterns = this.orderPatterns(patterns || Object.keys(registry.patterns));

    var _iterator = _createForOfIteratorHelper(patterns),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var name = _step.value;
        this.transformPattern(name, content);
        var pattern = registry.patterns[name];

        if (pattern.trigger) {
          selectors.unshift(pattern.trigger);
        }
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }

    var matches = _dom__WEBPACK_IMPORTED_MODULE_1__[/* default */ "a"].querySelectorAllAndMe(content, selectors.map(function (it) {
      return it.trim().replace(/,$/, "");
    }).join(","));
    matches = matches.filter(function (el) {
      var _el$parentNode, _el$parentNode$closes, _el$parentNode2, _el$parentNode2$close, _el$parentNode3, _el$parentNode3$close;

      // Filter out patterns:
      // - with class ``.cant-touch-this``
      // - wrapped in ``.cant-touch-this`` elements
      // - wrapped in ``<pre>`` elements
      // - wrapped in ``<template>`` elements
      return !el.matches(".cant-touch-this") && !(el !== null && el !== void 0 && (_el$parentNode = el.parentNode) !== null && _el$parentNode !== void 0 && (_el$parentNode$closes = _el$parentNode.closest) !== null && _el$parentNode$closes !== void 0 && _el$parentNode$closes.call(_el$parentNode, ".cant-touch-this")) && !(el !== null && el !== void 0 && (_el$parentNode2 = el.parentNode) !== null && _el$parentNode2 !== void 0 && (_el$parentNode2$close = _el$parentNode2.closest) !== null && _el$parentNode2$close !== void 0 && _el$parentNode2$close.call(_el$parentNode2, "pre")) && !(el !== null && el !== void 0 && (_el$parentNode3 = el.parentNode) !== null && _el$parentNode3 !== void 0 && (_el$parentNode3$close = _el$parentNode3.closest) !== null && _el$parentNode3$close !== void 0 && _el$parentNode3$close.call(_el$parentNode3, "template")) // NOTE: not strictly necessary. Template is a DocumentFragment and not reachable except for IE.
      ;
    }); // walk list backwards and initialize patterns inside-out.

    var _iterator2 = _createForOfIteratorHelper(matches.reverse()),
        _step2;

    try {
      for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
        var el = _step2.value;

        var _iterator3 = _createForOfIteratorHelper(patterns),
            _step3;

        try {
          for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
            var _name = _step3.value;
            this.initPattern(_name, el, trigger);
          }
        } catch (err) {
          _iterator3.e(err);
        } finally {
          _iterator3.f();
        }
      }
    } catch (err) {
      _iterator2.e(err);
    } finally {
      _iterator2.f();
    }

    document.body.classList.add("patterns-loaded");
  },
  register: function register(pattern, name) {
    name = name || pattern.name;

    if (!name) {
      log.error("Pattern lacks a name:", pattern);
      return false;
    }

    if (registry.patterns[name]) {
      log.error("Already have a pattern called: " + name);
      return false;
    } // register pattern to be used for scanning new content


    registry.patterns[name] = pattern; // register pattern as jquery plugin

    if (pattern.jquery_plugin) {
      var plugin_name = ("pat-" + name).replace(/-([a-zA-Z])/g, function (match, p1) {
        return p1.toUpperCase();
      });
      jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn[plugin_name] = _utils__WEBPACK_IMPORTED_MODULE_3__[/* default */ "a"].jqueryPlugin(pattern); // BBB 2012-12-10 and also for Mockup patterns.

      jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn[plugin_name.replace(/^pat/, "pattern")] = jquery__WEBPACK_IMPORTED_MODULE_0___default.a.fn[plugin_name];
    }

    log.debug("Registered pattern:", name, pattern);

    if (registry.initialized) {
      registry.scan(document.body, [name]);
    }

    return true;
  }
};
/* harmony default export */ __webpack_exports__["a"] = (registry);

/***/ }),

/***/ 96:
/***/ (function(module, exports) {

module.exports = function(module) {
	if (!module.webpackPolyfill) {
		module.deprecate = function() {};
		module.paths = [];
		// module.parent = undefined by default
		if (!module.children) module.children = [];
		Object.defineProperty(module, "loaded", {
			enumerable: true,
			get: function() {
				return module.l;
			}
		});
		Object.defineProperty(module, "id", {
			enumerable: true,
			get: function() {
				return module.i;
			}
		});
		module.webpackPolyfill = 1;
	}
	return module;
};


/***/ }),

/***/ 98:
/***/ (function(module, exports, __webpack_require__) {

// NOTE: Import this file before any other files
// Overwrite path to load resources or use default one.
__webpack_require__.p = window.__patternslib_public_path__ || "/assets/oira/script/"; // eslint-disable-line no-undef

/***/ }),

/***/ 99:
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(module) {function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

;

(function (window) {
  var hadGlobal = ('Modernizr' in window);
  var oldGlobal = window.Modernizr;
  /*!
  * modernizr v3.11.7
  * Build https://modernizr.com/download?-adownload-appearance-applicationcache-backdropfilter-backgroundblendmode-backgroundcliptext-backgroundsize-bgpositionshorthand-bgpositionxy-bgrepeatspace_bgrepeatround-bgsizecover-blobconstructor-bloburls-borderimage-borderradius-boxshadow-boxsizing-canvas-canvasblending-canvastext-canvaswinding-capture-checked-classlist-contenteditable-contextmenu-cookies-cors-createelementattrs_createelement_attrs-cssall-cssanimations-csscalc-csschunit-csscolumns-cssescape-cssexunit-cssfilters-cssgradients-cssgrid_cssgridlegacy-cssinvalid-cssmask-csspointerevents-csspositionsticky-csspseudoanimations-csspseudotransitions-cssreflections-cssremunit-cssresize-cssscrollbar-csstransforms-csstransforms3d-csstransformslevel2-csstransitions-cssvalid-cssvhunit-cssvmaxunit-cssvminunit-cssvwunit-cubicbezierrange-customelements-dataset-datauri-devicemotion_deviceorientation-directory-display_runin-displaytable-documentfragment-ellipsis-eventlistener-exiforientation-fileinput-flexbox-flexboxlegacy-flexboxtweener-flexwrap-fontface-formattribute-formvalidation-fullscreen-generatedcontent-hairline-hashchange-hidden-hiddenscroll-history-hovermq-hsla-htmlimports-inputtypes-json-lastchild-localstorage-mediaqueries-microdata-multiplebgs-mutationobserver-notification-nthchild-objectfit-oninput-opacity-overflowscrolling-pagevisibility-passiveeventlisteners-performance-placeholder-pointermq-postmessage-preserve3d-proximity-queryselector-regions-requestanimationframe-requestautocomplete-rgba-sandbox-scrollsnappoints-seamless-sessionstorage-shapes-siblinggeneral-srcdoc-subpixelfont-supports-target-textalignlast-textshadow-todataurljpeg_todataurlpng_todataurlwebp-touchevents-unicode-unicoderange-urlparser-urlsearchparams-userdata-userselect-vibrate-video-videoautoplay-videocrossorigin-videoloop-videopreload-websqldatabase-willchange-wrapflow-xdomainrequest-addtest-atrule-domprefixes-hasevent-load-mq-prefixed-prefixedcss-prefixes-printshiv-setclasses-testallprops-testprop-teststyles-dontmin
  *
  * Copyright (c)
  *  Faruk Ates
  *  Paul Irish
  *  Alex Sexton
  *  Ryan Seddon
  *  Patrick Kettner
  *  Stu Cox
  *  Richard Herrera
  *  Veeck
  * MIT License
  */

  /*
   * Modernizr tests which native CSS3 and HTML5 features are available in the
   * current UA and makes the results available to you in two ways: as properties on
   * a global `Modernizr` object, and as classes on the `<html>` element. This
   * information allows you to progressively enhance your pages with a granular level
   * of control over the experience.
  */

  ;

  (function (scriptGlobalObject, window, document, undefined) {
    var tests = [];
    /**
     * ModernizrProto is the constructor for Modernizr
     *
     * @class
     * @access public
     */

    var ModernizrProto = {
      _version: '3.11.7',
      // Any settings that don't work as separate modules
      // can go in here as configuration.
      _config: {
        'classPrefix': '',
        'enableClasses': true,
        'enableJSClass': true,
        'usePrefixes': true
      },
      // Queue of tests
      _q: [],
      // Stub these for people who are listening
      on: function on(test, cb) {
        // I don't really think people should do this, but we can
        // safe guard it a bit.
        // -- NOTE:: this gets WAY overridden in src/addTest for actual async tests.
        // This is in case people listen to synchronous tests. I would leave it out,
        // but the code to *disallow* sync tests in the real version of this
        // function is actually larger than this.
        var self = this;
        setTimeout(function () {
          cb(self[test]);
        }, 0);
      },
      addTest: function addTest(name, fn, options) {
        tests.push({
          name: name,
          fn: fn,
          options: options
        });
      },
      addAsyncTest: function addAsyncTest(fn) {
        tests.push({
          name: null,
          fn: fn
        });
      }
    }; // Fake some of Object.create so we can force non test results to be non "own" properties.

    var Modernizr = function Modernizr() {};

    Modernizr.prototype = ModernizrProto; // Leak modernizr globally when you `require` it rather than force it here.
    // Overwrite name so constructor name is nicer :D

    Modernizr = new Modernizr();
    var classes = [];
    /**
     * is returns a boolean if the typeof an obj is exactly type.
     *
     * @access private
     * @function is
     * @param {*} obj - A thing we want to check the type of
     * @param {string} type - A string to compare the typeof against
     * @returns {boolean} true if the typeof the first parameter is exactly the specified type, false otherwise
     */

    function is(obj, type) {
      return _typeof(obj) === type;
    }

    ;
    /**
     * Run through all tests and detect their support in the current UA.
     *
     * @access private
     * @returns {void}
     */

    function testRunner() {
      var featureNames;
      var feature;
      var aliasIdx;
      var result;
      var nameIdx;
      var featureName;
      var featureNameSplit;

      for (var featureIdx in tests) {
        if (tests.hasOwnProperty(featureIdx)) {
          featureNames = [];
          feature = tests[featureIdx]; // run the test, throw the return value into the Modernizr,
          // then based on that boolean, define an appropriate className
          // and push it into an array of classes we'll join later.
          //
          // If there is no name, it's an 'async' test that is run,
          // but not directly added to the object. That should
          // be done with a post-run addTest call.

          if (feature.name) {
            featureNames.push(feature.name.toLowerCase());

            if (feature.options && feature.options.aliases && feature.options.aliases.length) {
              // Add all the aliases into the names list
              for (aliasIdx = 0; aliasIdx < feature.options.aliases.length; aliasIdx++) {
                featureNames.push(feature.options.aliases[aliasIdx].toLowerCase());
              }
            }
          } // Run the test, or use the raw value if it's not a function


          result = is(feature.fn, 'function') ? feature.fn() : feature.fn; // Set each of the names on the Modernizr object

          for (nameIdx = 0; nameIdx < featureNames.length; nameIdx++) {
            featureName = featureNames[nameIdx]; // Support dot properties as sub tests. We don't do checking to make sure
            // that the implied parent tests have been added. You must call them in
            // order (either in the test, or make the parent test a dependency).
            //
            // Cap it to TWO to make the logic simple and because who needs that kind of subtesting
            // hashtag famous last words

            featureNameSplit = featureName.split('.');

            if (featureNameSplit.length === 1) {
              Modernizr[featureNameSplit[0]] = result;
            } else {
              // cast to a Boolean, if not one already or if it doesnt exist yet (like inputtypes)
              if (!Modernizr[featureNameSplit[0]] || Modernizr[featureNameSplit[0]] && !(Modernizr[featureNameSplit[0]] instanceof Boolean)) {
                Modernizr[featureNameSplit[0]] = new Boolean(Modernizr[featureNameSplit[0]]);
              }

              Modernizr[featureNameSplit[0]][featureNameSplit[1]] = result;
            }

            classes.push((result ? '' : 'no-') + featureNameSplit.join('-'));
          }
        }
      }
    }

    ;
    /**
     * docElement is a convenience wrapper to grab the root element of the document
     *
     * @access private
     * @returns {HTMLElement|SVGElement} The root element of the document
     */

    var docElement = document.documentElement;
    /**
     * A convenience helper to check if the document we are running in is an SVG document
     *
     * @access private
     * @returns {boolean}
     */

    var isSVG = docElement.nodeName.toLowerCase() === 'svg';
    /**
     * setClasses takes an array of class names and adds them to the root element
     *
     * @access private
     * @function setClasses
     * @param {string[]} classes - Array of class names
     */
    // Pass in an and array of class names, e.g.:
    //  ['no-webp', 'borderradius', ...]

    function setClasses(classes) {
      var className = docElement.className;
      var classPrefix = Modernizr._config.classPrefix || '';

      if (isSVG) {
        className = className.baseVal;
      } // Change `no-js` to `js` (independently of the `enableClasses` option)
      // Handle classPrefix on this too


      if (Modernizr._config.enableJSClass) {
        var reJS = new RegExp('(^|\\s)' + classPrefix + 'no-js(\\s|$)');
        className = className.replace(reJS, '$1' + classPrefix + 'js$2');
      }

      if (Modernizr._config.enableClasses) {
        // Add the new classes
        if (classes.length > 0) {
          className += ' ' + classPrefix + classes.join(' ' + classPrefix);
        }

        if (isSVG) {
          docElement.className.baseVal = className;
        } else {
          docElement.className = className;
        }
      }
    }

    ;
    /**
     * hasOwnProp is a shim for hasOwnProperty that is needed for Safari 2.0 support
     *
     * @author kangax
     * @access private
     * @function hasOwnProp
     * @param {object} object - The object to check for a property
     * @param {string} property - The property to check for
     * @returns {boolean}
     */
    // hasOwnProperty shim by kangax needed for Safari 2.0 support

    var hasOwnProp;

    (function () {
      var _hasOwnProperty = {}.hasOwnProperty;
      /* istanbul ignore else */

      /* we have no way of testing IE 5.5 or safari 2,
       * so just assume the else gets hit */

      if (!is(_hasOwnProperty, 'undefined') && !is(_hasOwnProperty.call, 'undefined')) {
        hasOwnProp = function hasOwnProp(object, property) {
          return _hasOwnProperty.call(object, property);
        };
      } else {
        hasOwnProp = function hasOwnProp(object, property) {
          /* yes, this can give false positives/negatives, but most of the time we don't care about those */
          return property in object && is(object.constructor.prototype[property], 'undefined');
        };
      }
    })(); // _l tracks listeners for async tests, as well as tests that execute after the initial run


    ModernizrProto._l = {};
    /**
     * Modernizr.on is a way to listen for the completion of async tests. Being
     * asynchronous, they may not finish before your scripts run. As a result you
     * will get a possibly false negative `undefined` value.
     *
     * @memberOf Modernizr
     * @name Modernizr.on
     * @access public
     * @function on
     * @param {string} feature - String name of the feature detect
     * @param {Function} cb - Callback function returning a Boolean - true if feature is supported, false if not
     * @returns {void}
     * @example
     *
     * ```js
     * Modernizr.on('flash', function( result ) {
     *   if (result) {
     *    // the browser has flash
     *   } else {
     *     // the browser does not have flash
     *   }
     * });
     * ```
     */

    ModernizrProto.on = function (feature, cb) {
      // Create the list of listeners if it doesn't exist
      if (!this._l[feature]) {
        this._l[feature] = [];
      } // Push this test on to the listener list


      this._l[feature].push(cb); // If it's already been resolved, trigger it on next tick


      if (Modernizr.hasOwnProperty(feature)) {
        // Next Tick
        setTimeout(function () {
          Modernizr._trigger(feature, Modernizr[feature]);
        }, 0);
      }
    };
    /**
     * _trigger is the private function used to signal test completion and run any
     * callbacks registered through [Modernizr.on](#modernizr-on)
     *
     * @memberOf Modernizr
     * @name Modernizr._trigger
     * @access private
     * @function _trigger
     * @param {string} feature - string name of the feature detect
     * @param {Function|boolean} [res] - A feature detection function, or the boolean =
     * result of a feature detection function
     * @returns {void}
     */


    ModernizrProto._trigger = function (feature, res) {
      if (!this._l[feature]) {
        return;
      }

      var cbs = this._l[feature]; // Force async

      setTimeout(function () {
        var i, cb;

        for (i = 0; i < cbs.length; i++) {
          cb = cbs[i];
          cb(res);
        }
      }, 0); // Don't trigger these again

      delete this._l[feature];
    };
    /**
     * addTest allows you to define your own feature detects that are not currently
     * included in Modernizr (under the covers it's the exact same code Modernizr
     * uses for its own [feature detections](https://github.com/Modernizr/Modernizr/tree/master/feature-detects)).
     * Just like the official detects, the result
     * will be added onto the Modernizr object, as well as an appropriate className set on
     * the html element when configured to do so
     *
     * @memberOf Modernizr
     * @name Modernizr.addTest
     * @optionName Modernizr.addTest()
     * @optionProp addTest
     * @access public
     * @function addTest
     * @param {string|object} feature - The string name of the feature detect, or an
     * object of feature detect names and test
     * @param {Function|boolean} test - Function returning true if feature is supported,
     * false if not. Otherwise a boolean representing the results of a feature detection
     * @returns {object} the Modernizr object to allow chaining
     * @example
     *
     * The most common way of creating your own feature detects is by calling
     * `Modernizr.addTest` with a string (preferably just lowercase, without any
     * punctuation), and a function you want executed that will return a boolean result
     *
     * ```js
     * Modernizr.addTest('itsTuesday', function() {
     *  var d = new Date();
     *  return d.getDay() === 2;
     * });
     * ```
     *
     * When the above is run, it will set Modernizr.itstuesday to `true` when it is tuesday,
     * and to `false` every other day of the week. One thing to notice is that the names of
     * feature detect functions are always lowercased when added to the Modernizr object. That
     * means that `Modernizr.itsTuesday` will not exist, but `Modernizr.itstuesday` will.
     *
     *
     *  Since we only look at the returned value from any feature detection function,
     *  you do not need to actually use a function. For simple detections, just passing
     *  in a statement that will return a boolean value works just fine.
     *
     * ```js
     * Modernizr.addTest('hasjquery', 'jQuery' in window);
     * ```
     *
     * Just like before, when the above runs `Modernizr.hasjquery` will be true if
     * jQuery has been included on the page. Not using a function saves a small amount
     * of overhead for the browser, as well as making your code much more readable.
     *
     * Finally, you also have the ability to pass in an object of feature names and
     * their tests. This is handy if you want to add multiple detections in one go.
     * The keys should always be a string, and the value can be either a boolean or
     * function that returns a boolean.
     *
     * ```js
     * var detects = {
     *  'hasjquery': 'jQuery' in window,
     *  'itstuesday': function() {
     *    var d = new Date();
     *    return d.getDay() === 2;
     *  }
     * }
     *
     * Modernizr.addTest(detects);
     * ```
     *
     * There is really no difference between the first methods and this one, it is
     * just a convenience to let you write more readable code.
     */


    function addTest(feature, test) {
      if (_typeof(feature) === 'object') {
        for (var key in feature) {
          if (hasOwnProp(feature, key)) {
            addTest(key, feature[key]);
          }
        }
      } else {
        feature = feature.toLowerCase();
        var featureNameSplit = feature.split('.');
        var last = Modernizr[featureNameSplit[0]]; // Again, we don't check for parent test existence. Get that right, though.

        if (featureNameSplit.length === 2) {
          last = last[featureNameSplit[1]];
        }

        if (typeof last !== 'undefined') {
          // we're going to quit if you're trying to overwrite an existing test
          // if we were to allow it, we'd do this:
          //   var re = new RegExp("\\b(no-)?" + feature + "\\b");
          //   docElement.className = docElement.className.replace( re, '' );
          // but, no rly, stuff 'em.
          return Modernizr;
        }

        test = typeof test === 'function' ? test() : test; // Set the value (this is the magic, right here).

        if (featureNameSplit.length === 1) {
          Modernizr[featureNameSplit[0]] = test;
        } else {
          // cast to a Boolean, if not one already
          if (Modernizr[featureNameSplit[0]] && !(Modernizr[featureNameSplit[0]] instanceof Boolean)) {
            Modernizr[featureNameSplit[0]] = new Boolean(Modernizr[featureNameSplit[0]]);
          }

          Modernizr[featureNameSplit[0]][featureNameSplit[1]] = test;
        } // Set a single class (either `feature` or `no-feature`)


        setClasses([(!!test && test !== false ? '' : 'no-') + featureNameSplit.join('-')]); // Trigger the event

        Modernizr._trigger(feature, test);
      }

      return Modernizr; // allow chaining.
    } // After all the tests are run, add self to the Modernizr prototype


    Modernizr._q.push(function () {
      ModernizrProto.addTest = addTest;
    });
    /**
     * If the browsers follow the spec, then they would expose vendor-specific styles as:
     *   elem.style.WebkitBorderRadius
     * instead of something like the following (which is technically incorrect):
     *   elem.style.webkitBorderRadius
     *
     * WebKit ghosts their properties in lowercase but Opera & Moz do not.
     * Microsoft uses a lowercase `ms` instead of the correct `Ms` in IE8+
     *   erik.eae.net/archives/2008/03/10/21.48.10/
     *
     * More here: github.com/Modernizr/Modernizr/issues/issue/21
     *
     * @access private
     * @returns {string} The string representing the vendor-specific style properties
     */


    var omPrefixes = 'Moz O ms Webkit';
    var cssomPrefixes = ModernizrProto._config.usePrefixes ? omPrefixes.split(' ') : [];
    ModernizrProto._cssomPrefixes = cssomPrefixes;
    /**
     * atRule returns a given CSS property at-rule (eg @keyframes), possibly in
     * some prefixed form, or false, in the case of an unsupported rule
     *
     * @memberOf Modernizr
     * @name Modernizr.atRule
     * @optionName Modernizr.atRule()
     * @optionProp atRule
     * @access public
     * @function atRule
     * @param {string} prop - String name of the @-rule to test for
     * @returns {string|boolean} The string representing the (possibly prefixed)
     * valid version of the @-rule, or `false` when it is unsupported.
     * @example
     * ```js
     *  var keyframes = Modernizr.atRule('@keyframes');
     *
     *  if (keyframes) {
     *    // keyframes are supported
     *    // could be `@-webkit-keyframes` or `@keyframes`
     *  } else {
     *    // keyframes === `false`
     *  }
     * ```
     */

    var atRule = function atRule(prop) {
      var length = prefixes.length;
      var cssrule = window.CSSRule;
      var rule;

      if (typeof cssrule === 'undefined') {
        return undefined;
      }

      if (!prop) {
        return false;
      } // remove literal @ from beginning of provided property


      prop = prop.replace(/^@/, ''); // CSSRules use underscores instead of dashes

      rule = prop.replace(/-/g, '_').toUpperCase() + '_RULE';

      if (rule in cssrule) {
        return '@' + prop;
      }

      for (var i = 0; i < length; i++) {
        // prefixes gives us something like -o-, and we want O_
        var prefix = prefixes[i];
        var thisRule = prefix.toUpperCase() + '_' + rule;

        if (thisRule in cssrule) {
          return '@-' + prefix.toLowerCase() + '-' + prop;
        }
      }

      return false;
    };

    ModernizrProto.atRule = atRule;
    /**
     * List of JavaScript DOM values used for tests
     *
     * @memberOf Modernizr
     * @name Modernizr._domPrefixes
     * @optionName Modernizr._domPrefixes
     * @optionProp domPrefixes
     * @access public
     * @example
     *
     * Modernizr._domPrefixes is exactly the same as [_prefixes](#modernizr-_prefixes), but rather
     * than hyphen-case properties, all properties are their Capitalized variant
     *
     * ```js
     * Modernizr._domPrefixes === [ "Moz", "O", "ms", "Webkit" ];
     * ```
     */

    var domPrefixes = ModernizrProto._config.usePrefixes ? omPrefixes.toLowerCase().split(' ') : [];
    ModernizrProto._domPrefixes = domPrefixes;
    /**
     * createElement is a convenience wrapper around document.createElement. Since we
     * use createElement all over the place, this allows for (slightly) smaller code
     * as well as abstracting away issues with creating elements in contexts other than
     * HTML documents (e.g. SVG documents).
     *
     * @access private
     * @function createElement
     * @returns {HTMLElement|SVGElement} An HTML or SVG element
     */

    function createElement() {
      if (typeof document.createElement !== 'function') {
        // This is the case in IE7, where the type of createElement is "object".
        // For this reason, we cannot call apply() as Object is not a Function.
        return document.createElement(arguments[0]);
      } else if (isSVG) {
        return document.createElementNS.call(document, 'http://www.w3.org/2000/svg', arguments[0]);
      } else {
        return document.createElement.apply(document, arguments);
      }
    }

    ;
    /**
     * Modernizr.hasEvent() detects support for a given event
     *
     * @memberOf Modernizr
     * @name Modernizr.hasEvent
     * @optionName Modernizr.hasEvent()
     * @optionProp hasEvent
     * @access public
     * @function hasEvent
     * @param {string|*} eventName - the name of an event to test for (e.g. "resize")
     * @param {Element|string} [element=HTMLDivElement] - is the element|document|window|tagName to test on
     * @returns {boolean}
     * @example
     *  `Modernizr.hasEvent` lets you determine if the browser supports a supplied event.
     *  By default, it does this detection on a div element
     *
     * ```js
     *  hasEvent('blur') // true;
     * ```
     *
     * However, you are able to give an object as a second argument to hasEvent to
     * detect an event on something other than a div.
     *
     * ```js
     *  hasEvent('devicelight', window) // true;
     * ```
     */

    var hasEvent = function () {
      // Detect whether event support can be detected via `in`. Test on a DOM element
      // using the "blur" event b/c it should always exist. bit.ly/event-detection
      var needsFallback = !('onblur' in docElement);

      function inner(eventName, element) {
        var isSupported;

        if (!eventName) {
          return false;
        }

        if (!element || typeof element === 'string') {
          element = createElement(element || 'div');
        } // Testing via the `in` operator is sufficient for modern browsers and IE.
        // When using `setAttribute`, IE skips "unload", WebKit skips "unload" and
        // "resize", whereas `in` "catches" those.


        eventName = 'on' + eventName;
        isSupported = eventName in element; // Fallback technique for old Firefox - bit.ly/event-detection

        if (!isSupported && needsFallback) {
          if (!element.setAttribute) {
            // Switch to generic element if it lacks `setAttribute`.
            // It could be the `document`, `window`, or something else.
            element = createElement('div');
          }

          element.setAttribute(eventName, '');
          isSupported = typeof element[eventName] === 'function';

          if (element[eventName] !== undefined) {
            // If property was created, "remove it" by setting value to `undefined`.
            element[eventName] = undefined;
          }

          element.removeAttribute(eventName);
        }

        return isSupported;
      }

      return inner;
    }();

    ModernizrProto.hasEvent = hasEvent;
    /**
     * @optionName html5printshiv
     * @optionProp html5printshiv
     */
    // Take the html5 variable out of the html5shiv scope so we can return it.

    var html5;

    if (!isSVG) {
      /**
       * @preserve HTML5 Shiv 3.7.3 | @afarkas @jdalton @jon_neal @rem | MIT/GPL2 Licensed
       */
      ;

      (function (window, document) {
        /*jshint evil:true */

        /** version */
        var version = '3.7.3';
        /** Preset options */

        var options = window.html5 || {};
        /** Used to skip problem elements */

        var reSkip = /^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i;
        /** Not all elements can be cloned in IE **/

        var saveClones = /^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i;
        /** Detect whether the browser supports default html5 styles */

        var supportsHtml5Styles;
        /** Name of the expando, to work with multiple documents or to re-shiv one document */

        var expando = '_html5shiv';
        /** The id for the the documents expando */

        var expanID = 0;
        /** Cached data for each document */

        var expandoData = {};
        /** Detect whether the browser supports unknown elements */

        var supportsUnknownElements;

        (function () {
          try {
            var a = document.createElement('a');
            a.innerHTML = '<xyz></xyz>'; //if the hidden property is implemented we can assume, that the browser supports basic HTML5 Styles

            supportsHtml5Styles = 'hidden' in a;

            supportsUnknownElements = a.childNodes.length == 1 || function () {
              // assign a false positive if unable to shiv
              document.createElement('a');
              var frag = document.createDocumentFragment();
              return typeof frag.cloneNode == 'undefined' || typeof frag.createDocumentFragment == 'undefined' || typeof frag.createElement == 'undefined';
            }();
          } catch (e) {
            // assign a false positive if detection fails => unable to shiv
            supportsHtml5Styles = true;
            supportsUnknownElements = true;
          }
        })();
        /*--------------------------------------------------------------------------*/

        /**
         * Creates a style sheet with the given CSS text and adds it to the document.
         * @private
         * @param {Document} ownerDocument The document.
         * @param {String} cssText The CSS text.
         * @returns {StyleSheet} The style element.
         */


        function addStyleSheet(ownerDocument, cssText) {
          var p = ownerDocument.createElement('p'),
              parent = ownerDocument.getElementsByTagName('head')[0] || ownerDocument.documentElement;
          p.innerHTML = 'x<style>' + cssText + '</style>';
          return parent.insertBefore(p.lastChild, parent.firstChild);
        }
        /**
         * Returns the value of `html5.elements` as an array.
         * @private
         * @returns {Array} An array of shived element node names.
         */


        function getElements() {
          var elements = html5.elements;
          return typeof elements == 'string' ? elements.split(' ') : elements;
        }
        /**
         * Extends the built-in list of html5 elements
         * @memberOf html5
         * @param {String|Array} newElements whitespace separated list or array of new element names to shiv
         * @param {Document} ownerDocument The context document.
         */


        function addElements(newElements, ownerDocument) {
          var elements = html5.elements;

          if (typeof elements != 'string') {
            elements = elements.join(' ');
          }

          if (typeof newElements != 'string') {
            newElements = newElements.join(' ');
          }

          html5.elements = elements + ' ' + newElements;
          shivDocument(ownerDocument);
        }
        /**
         * Returns the data associated to the given document
         * @private
         * @param {Document} ownerDocument The document.
         * @returns {Object} An object of data.
         */


        function getExpandoData(ownerDocument) {
          var data = expandoData[ownerDocument[expando]];

          if (!data) {
            data = {};
            expanID++;
            ownerDocument[expando] = expanID;
            expandoData[expanID] = data;
          }

          return data;
        }
        /**
         * returns a shived element for the given nodeName and document
         * @memberOf html5
         * @param {String} nodeName name of the element
         * @param {Document} ownerDocument The context document.
         * @returns {Object} The shived element.
         */


        function createElement(nodeName, ownerDocument, data) {
          if (!ownerDocument) {
            ownerDocument = document;
          }

          if (supportsUnknownElements) {
            return ownerDocument.createElement(nodeName);
          }

          if (!data) {
            data = getExpandoData(ownerDocument);
          }

          var node;

          if (data.cache[nodeName]) {
            node = data.cache[nodeName].cloneNode();
          } else if (saveClones.test(nodeName)) {
            node = (data.cache[nodeName] = data.createElem(nodeName)).cloneNode();
          } else {
            node = data.createElem(nodeName);
          } // Avoid adding some elements to fragments in IE < 9 because
          // * Attributes like `name` or `type` cannot be set/changed once an element
          //   is inserted into a document/fragment
          // * Link elements with `src` attributes that are inaccessible, as with
          //   a 403 response, will cause the tab/window to crash
          // * Script elements appended to fragments will execute when their `src`
          //   or `text` property is set


          return node.canHaveChildren && !reSkip.test(nodeName) && !node.tagUrn ? data.frag.appendChild(node) : node;
        }
        /**
         * returns a shived DocumentFragment for the given document
         * @memberOf html5
         * @param {Document} ownerDocument The context document.
         * @returns {Object} The shived DocumentFragment.
         */


        function createDocumentFragment(ownerDocument, data) {
          if (!ownerDocument) {
            ownerDocument = document;
          }

          if (supportsUnknownElements) {
            return ownerDocument.createDocumentFragment();
          }

          data = data || getExpandoData(ownerDocument);
          var clone = data.frag.cloneNode(),
              i = 0,
              elems = getElements(),
              l = elems.length;

          for (; i < l; i++) {
            clone.createElement(elems[i]);
          }

          return clone;
        }
        /**
         * Shivs the `createElement` and `createDocumentFragment` methods of the document.
         * @private
         * @param {Document|DocumentFragment} ownerDocument The document.
         * @param {Object} data of the document.
         */


        function shivMethods(ownerDocument, data) {
          if (!data.cache) {
            data.cache = {};
            data.createElem = ownerDocument.createElement;
            data.createFrag = ownerDocument.createDocumentFragment;
            data.frag = data.createFrag();
          }

          ownerDocument.createElement = function (nodeName) {
            //abort shiv
            if (!html5.shivMethods) {
              return data.createElem(nodeName);
            }

            return createElement(nodeName, ownerDocument, data);
          };

          ownerDocument.createDocumentFragment = Function('h,f', 'return function(){' + 'var n=f.cloneNode(),c=n.createElement;' + 'h.shivMethods&&(' + // unroll the `createElement` calls
          getElements().join().replace(/[\w\-:]+/g, function (nodeName) {
            data.createElem(nodeName);
            data.frag.createElement(nodeName);
            return 'c("' + nodeName + '")';
          }) + ');return n}')(html5, data.frag);
        }
        /*--------------------------------------------------------------------------*/

        /**
         * Shivs the given document.
         * @memberOf html5
         * @param {Document} ownerDocument The document to shiv.
         * @returns {Document} The shived document.
         */


        function shivDocument(ownerDocument) {
          if (!ownerDocument) {
            ownerDocument = document;
          }

          var data = getExpandoData(ownerDocument);

          if (html5.shivCSS && !supportsHtml5Styles && !data.hasCSS) {
            data.hasCSS = !!addStyleSheet(ownerDocument, // corrects block display not defined in IE6/7/8/9
            'article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}' + // adds styling not present in IE6/7/8/9
            'mark{background:#FF0;color:#000}' + // hides non-rendered elements
            'template{display:none}');
          }

          if (!supportsUnknownElements) {
            shivMethods(ownerDocument, data);
          }

          return ownerDocument;
        }
        /*--------------------------------------------------------------------------*/

        /**
         * The `html5` object is exposed so that more elements can be shived and
         * existing shiving can be detected on iframes.
         * @type Object
         * @example
         *
         * // options can be changed before the script is included
         * html5 = { 'elements': 'mark section', 'shivCSS': false, 'shivMethods': false };
         */


        var html5 = {
          /**
           * An array or space separated string of node names of the elements to shiv.
           * @memberOf html5
           * @type Array|String
           */
          'elements': options.elements || 'abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output picture progress section summary template time video',

          /**
           * current version of html5shiv
           */
          'version': version,

          /**
           * A flag to indicate that the HTML5 style sheet should be inserted.
           * @memberOf html5
           * @type Boolean
           */
          'shivCSS': options.shivCSS !== false,

          /**
           * Is equal to true if a browser supports creating unknown/HTML5 elements
           * @memberOf html5
           * @type boolean
           */
          'supportsUnknownElements': supportsUnknownElements,

          /**
           * A flag to indicate that the document's `createElement` and `createDocumentFragment`
           * methods should be overwritten.
           * @memberOf html5
           * @type Boolean
           */
          'shivMethods': options.shivMethods !== false,

          /**
           * A string to describe the type of `html5` object ("default" or "default print").
           * @memberOf html5
           * @type String
           */
          'type': 'default',
          // shivs the document according to the specified `html5` object options
          'shivDocument': shivDocument,
          //creates a shived element
          createElement: createElement,
          //creates a shived documentFragment
          createDocumentFragment: createDocumentFragment,
          //extends list of elements
          addElements: addElements
        };
        /*--------------------------------------------------------------------------*/
        // expose html5

        window.html5 = html5; // shiv the document

        shivDocument(document);
        /*------------------------------- Print Shiv -------------------------------*/

        /** Used to filter media types */

        var reMedia = /^$|\b(?:all|print)\b/;
        /** Used to namespace printable elements */

        var shivNamespace = 'html5shiv';
        /** Detect whether the browser supports shivable style sheets */

        var supportsShivableSheets = !supportsUnknownElements && function () {
          // assign a false negative if unable to shiv
          var docEl = document.documentElement;
          return !(typeof document.namespaces == 'undefined' || typeof document.parentWindow == 'undefined' || typeof docEl.applyElement == 'undefined' || typeof docEl.removeNode == 'undefined' || typeof window.attachEvent == 'undefined');
        }();
        /*--------------------------------------------------------------------------*/

        /**
         * Wraps all HTML5 elements in the given document with printable elements.
         * (eg. the "header" element is wrapped with the "html5shiv:header" element)
         * @private
         * @param {Document} ownerDocument The document.
         * @returns {Array} An array wrappers added.
         */


        function addWrappers(ownerDocument) {
          var node,
              nodes = ownerDocument.getElementsByTagName('*'),
              index = nodes.length,
              reElements = RegExp('^(?:' + getElements().join('|') + ')$', 'i'),
              result = [];

          while (index--) {
            node = nodes[index];

            if (reElements.test(node.nodeName)) {
              result.push(node.applyElement(createWrapper(node)));
            }
          }

          return result;
        }
        /**
         * Creates a printable wrapper for the given element.
         * @private
         * @param {Element} element The element.
         * @returns {Element} The wrapper.
         */


        function createWrapper(element) {
          var node,
              nodes = element.attributes,
              index = nodes.length,
              wrapper = element.ownerDocument.createElement(shivNamespace + ':' + element.nodeName); // copy element attributes to the wrapper

          while (index--) {
            node = nodes[index];
            node.specified && wrapper.setAttribute(node.nodeName, node.nodeValue);
          } // copy element styles to the wrapper


          wrapper.style.cssText = element.style.cssText;
          return wrapper;
        }
        /**
         * Shivs the given CSS text.
         * (eg. header{} becomes html5shiv\:header{})
         * @private
         * @param {String} cssText The CSS text to shiv.
         * @returns {String} The shived CSS text.
         */


        function shivCssText(cssText) {
          var pair,
              parts = cssText.split('{'),
              index = parts.length,
              reElements = RegExp('(^|[\\s,>+~])(' + getElements().join('|') + ')(?=[[\\s,>+~#.:]|$)', 'gi'),
              replacement = '$1' + shivNamespace + '\\:$2';

          while (index--) {
            pair = parts[index] = parts[index].split('}');
            pair[pair.length - 1] = pair[pair.length - 1].replace(reElements, replacement);
            parts[index] = pair.join('}');
          }

          return parts.join('{');
        }
        /**
         * Removes the given wrappers, leaving the original elements.
         * @private
         * @params {Array} wrappers An array of printable wrappers.
         */


        function removeWrappers(wrappers) {
          var index = wrappers.length;

          while (index--) {
            wrappers[index].removeNode();
          }
        }
        /*--------------------------------------------------------------------------*/

        /**
         * Shivs the given document for print.
         * @memberOf html5
         * @param {Document} ownerDocument The document to shiv.
         * @returns {Document} The shived document.
         */


        function shivPrint(ownerDocument) {
          var shivedSheet,
              wrappers,
              data = getExpandoData(ownerDocument),
              namespaces = ownerDocument.namespaces,
              ownerWindow = ownerDocument.parentWindow;

          if (!supportsShivableSheets || ownerDocument.printShived) {
            return ownerDocument;
          }

          if (typeof namespaces[shivNamespace] == 'undefined') {
            namespaces.add(shivNamespace);
          }

          function removeSheet() {
            clearTimeout(data._removeSheetTimer);

            if (shivedSheet) {
              shivedSheet.removeNode(true);
            }

            shivedSheet = null;
          }

          ownerWindow.attachEvent('onbeforeprint', function () {
            removeSheet();
            var imports,
                length,
                sheet,
                collection = ownerDocument.styleSheets,
                cssText = [],
                index = collection.length,
                sheets = Array(index); // convert styleSheets collection to an array

            while (index--) {
              sheets[index] = collection[index];
            } // concat all style sheet CSS text


            while (sheet = sheets.pop()) {
              // IE does not enforce a same origin policy for external style sheets...
              // but has trouble with some dynamically created stylesheets
              if (!sheet.disabled && reMedia.test(sheet.media)) {
                try {
                  imports = sheet.imports;
                  length = imports.length;
                } catch (er) {
                  length = 0;
                }

                for (index = 0; index < length; index++) {
                  sheets.push(imports[index]);
                }

                try {
                  cssText.push(sheet.cssText);
                } catch (er) {}
              }
            } // wrap all HTML5 elements with printable elements and add the shived style sheet


            cssText = shivCssText(cssText.reverse().join(''));
            wrappers = addWrappers(ownerDocument);
            shivedSheet = addStyleSheet(ownerDocument, cssText);
          });
          ownerWindow.attachEvent('onafterprint', function () {
            // remove wrappers, leaving the original elements, and remove the shived style sheet
            removeWrappers(wrappers);
            clearTimeout(data._removeSheetTimer);
            data._removeSheetTimer = setTimeout(removeSheet, 500);
          });
          ownerDocument.printShived = true;
          return ownerDocument;
        }
        /*--------------------------------------------------------------------------*/
        // expose API


        html5.type += ' print';
        html5.shivPrint = shivPrint; // shiv for print

        shivPrint(document);

        if (( false ? undefined : _typeof(module)) == 'object' && module.exports) {
          module.exports = html5;
        }
      })(typeof window !== "undefined" ? window : this, document);
    }

    ;

    var err = function err() {};

    var warn = function warn() {};

    if (window.console) {
      err = function err() {
        var method = console.error ? 'error' : 'log';
        window.console[method].apply(window.console, Array.prototype.slice.call(arguments));
      };

      warn = function warn() {
        var method = console.warn ? 'warn' : 'log';
        window.console[method].apply(window.console, Array.prototype.slice.call(arguments));
      };
    }
    /**
     * Previously, Modernizr.load was an alias for yepnope. Since yepnope was
     * deprecated, we removed it as well. It is not available on the website builder,
     * this is only included as an improved warning to those who build a custom
     * version locally.
     *
     * @memberOf Modernizr
     * @name Modernizr.load
     * @function load
     * @returns {void}
     */


    ModernizrProto.load = function () {
      if ('yepnope' in window) {
        warn('yepnope.js (aka Modernizr.load) is no longer included as part of Modernizr. yepnope appears to be available on the page, so we’ll use it to handle this call to Modernizr.load, but please update your code to use yepnope directly.\n See http://github.com/Modernizr/Modernizr/issues/1182 for more information.');
        window.yepnope.apply(window, [].slice.call(arguments, 0));
      } else {
        err('yepnope.js (aka Modernizr.load) is no longer included as part of Modernizr. Get it from http://yepnopejs.com. See http://github.com/Modernizr/Modernizr/issues/1182 for more information.');
      }
    };
    /**
     * getBody returns the body of a document, or an element that can stand in for
     * the body if a real body does not exist
     *
     * @access private
     * @function getBody
     * @returns {HTMLElement|SVGElement} Returns the real body of a document, or an
     * artificially created element that stands in for the body
     */


    function getBody() {
      // After page load injecting a fake body doesn't work so check if body exists
      var body = document.body;

      if (!body) {
        // Can't use the real body create a fake one.
        body = createElement(isSVG ? 'svg' : 'body');
        body.fake = true;
      }

      return body;
    }

    ;
    /**
     * injectElementWithStyles injects an element with style element and some CSS rules
     *
     * @access private
     * @function injectElementWithStyles
     * @param {string} rule - String representing a css rule
     * @param {Function} callback - A function that is used to test the injected element
     * @param {number} [nodes] - An integer representing the number of additional nodes you want injected
     * @param {string[]} [testnames] - An array of strings that are used as ids for the additional nodes
     * @returns {boolean} the result of the specified callback test
     */

    function injectElementWithStyles(rule, callback, nodes, testnames) {
      var mod = 'modernizr';
      var style;
      var ret;
      var node;
      var docOverflow;
      var div = createElement('div');
      var body = getBody();

      if (parseInt(nodes, 10)) {
        // In order not to give false positives we create a node for each test
        // This also allows the method to scale for unspecified uses
        while (nodes--) {
          node = createElement('div');
          node.id = testnames ? testnames[nodes] : mod + (nodes + 1);
          div.appendChild(node);
        }
      }

      style = createElement('style');
      style.type = 'text/css';
      style.id = 's' + mod; // IE6 will false positive on some tests due to the style element inside the test div somehow interfering offsetHeight, so insert it into body or fakebody.
      // Opera will act all quirky when injecting elements in documentElement when page is served as xml, needs fakebody too. #270

      (!body.fake ? div : body).appendChild(style);
      body.appendChild(div);

      if (style.styleSheet) {
        style.styleSheet.cssText = rule;
      } else {
        style.appendChild(document.createTextNode(rule));
      }

      div.id = mod;

      if (body.fake) {
        //avoid crashing IE8, if background image is used
        body.style.background = ''; //Safari 5.13/5.1.4 OSX stops loading if ::-webkit-scrollbar is used and scrollbars are visible

        body.style.overflow = 'hidden';
        docOverflow = docElement.style.overflow;
        docElement.style.overflow = 'hidden';
        docElement.appendChild(body);
      }

      ret = callback(div, rule); // If this is done after page load we don't want to remove the body so check if body exists

      if (body.fake && body.parentNode) {
        body.parentNode.removeChild(body);
        docElement.style.overflow = docOverflow; // Trigger layout so kinetic scrolling isn't disabled in iOS6+
        // eslint-disable-next-line

        docElement.offsetHeight;
      } else {
        div.parentNode.removeChild(div);
      }

      return !!ret;
    }

    ;
    /**
     * wrapper around getComputedStyle, to fix issues with Firefox returning null when
     * called inside of a hidden iframe
     *
     * @access private
     * @function computedStyle
     * @param {HTMLElement|SVGElement} elem - The element we want to find the computed styles of
     * @param {string|null} [pseudo] - An optional pseudo element selector (e.g. :before), of null if none
     * @param {string} prop - A CSS property
     * @returns {CSSStyleDeclaration} the value of the specified CSS property
     */

    function computedStyle(elem, pseudo, prop) {
      var result;

      if ('getComputedStyle' in window) {
        result = getComputedStyle.call(window, elem, pseudo);
        var console = window.console;

        if (result !== null) {
          if (prop) {
            result = result.getPropertyValue(prop);
          }
        } else {
          if (console) {
            var method = console.error ? 'error' : 'log';
            console[method].call(console, 'getComputedStyle returning null, its possible modernizr test results are inaccurate');
          }
        }
      } else {
        result = !pseudo && elem.currentStyle && elem.currentStyle[prop];
      }

      return result;
    }

    ;
    /**
     * Modernizr.mq tests a given media query, live against the current state of the window
     * adapted from matchMedia polyfill by Scott Jehl and Paul Irish
     * gist.github.com/786768
     *
     * @memberOf Modernizr
     * @name Modernizr.mq
     * @optionName Modernizr.mq()
     * @optionProp mq
     * @access public
     * @function mq
     * @param {string} mq - String of the media query we want to test
     * @returns {boolean}
     * @example
     * Modernizr.mq allows for you to programmatically check if the current browser
     * window state matches a media query.
     *
     * ```js
     *  var query = Modernizr.mq('(min-width: 900px)');
     *
     *  if (query) {
     *    // the browser window is larger than 900px
     *  }
     * ```
     *
     * Only valid media queries are supported, therefore you must always include values
     * with your media query
     *
     * ```js
     * // good
     *  Modernizr.mq('(min-width: 900px)');
     *
     * // bad
     *  Modernizr.mq('min-width');
     * ```
     *
     * If you would just like to test that media queries are supported in general, use
     *
     * ```js
     *  Modernizr.mq('only all'); // true if MQ are supported, false if not
     * ```
     *
     * Note that if the browser does not support media queries (e.g. old IE) mq will
     * always return false.
     */

    var mq = function () {
      var matchMedia = window.matchMedia || window.msMatchMedia;

      if (matchMedia) {
        return function (mq) {
          var mql = matchMedia(mq);
          return mql && mql.matches || false;
        };
      }

      return function (mq) {
        var bool = false;
        injectElementWithStyles('@media ' + mq + ' { #modernizr { position: absolute; } }', function (node) {
          bool = computedStyle(node, null, 'position') === 'absolute';
        });
        return bool;
      };
    }();

    ModernizrProto.mq = mq;
    /**
     * contains checks to see if a string contains another string
     *
     * @access private
     * @function contains
     * @param {string} str - The string we want to check for substrings
     * @param {string} substr - The substring we want to search the first string for
     * @returns {boolean} true if and only if the first string 'str' contains the second string 'substr'
     */

    function contains(str, substr) {
      return !!~('' + str).indexOf(substr);
    }

    ;
    /**
     * Create our "modernizr" element that we do most feature tests on.
     *
     * @access private
     */

    var modElem = {
      elem: createElement('modernizr')
    }; // Clean up this element

    Modernizr._q.push(function () {
      delete modElem.elem;
    });

    var mStyle = {
      style: modElem.elem.style
    }; // kill ref for gc, must happen before mod.elem is removed, so we unshift on to
    // the front of the queue.

    Modernizr._q.unshift(function () {
      delete mStyle.style;
    });
    /**
     * domToCSS takes a camelCase string and converts it to hyphen-case
     * e.g. boxSizing -> box-sizing
     *
     * @access private
     * @function domToCSS
     * @param {string} name - String name of camelCase prop we want to convert
     * @returns {string} The hyphen-case version of the supplied name
     */


    function domToCSS(name) {
      return name.replace(/([A-Z])/g, function (str, m1) {
        return '-' + m1.toLowerCase();
      }).replace(/^ms-/, '-ms-');
    }

    ;
    /**
     * nativeTestProps allows for us to use native feature detection functionality if available.
     * some prefixed form, or false, in the case of an unsupported rule
     *
     * @access private
     * @function nativeTestProps
     * @param {Array} props - An array of property names
     * @param {string} value - A string representing the value we want to check via @supports
     * @returns {boolean|undefined} A boolean when @supports exists, undefined otherwise
     */
    // Accepts a list of property names and a single value
    // Returns `undefined` if native detection not available

    function nativeTestProps(props, value) {
      var i = props.length; // Start with the JS API: https://www.w3.org/TR/css3-conditional/#the-css-interface

      if ('CSS' in window && 'supports' in window.CSS) {
        // Try every prefixed variant of the property
        while (i--) {
          if (window.CSS.supports(domToCSS(props[i]), value)) {
            return true;
          }
        }

        return false;
      } // Otherwise fall back to at-rule (for Opera 12.x)
      else if ('CSSSupportsRule' in window) {
          // Build a condition string for every prefixed variant
          var conditionText = [];

          while (i--) {
            conditionText.push('(' + domToCSS(props[i]) + ':' + value + ')');
          }

          conditionText = conditionText.join(' or ');
          return injectElementWithStyles('@supports (' + conditionText + ') { #modernizr { position: absolute; } }', function (node) {
            return computedStyle(node, null, 'position') === 'absolute';
          });
        }

      return undefined;
    }

    ;
    /**
     * cssToDOM takes a hyphen-case string and converts it to camelCase
     * e.g. box-sizing -> boxSizing
     *
     * @access private
     * @function cssToDOM
     * @param {string} name - String name of hyphen-case prop we want to convert
     * @returns {string} The camelCase version of the supplied name
     */

    function cssToDOM(name) {
      return name.replace(/([a-z])-([a-z])/g, function (str, m1, m2) {
        return m1 + m2.toUpperCase();
      }).replace(/^-/, '');
    }

    ; // testProps is a generic CSS / DOM property test.
    // In testing support for a given CSS property, it's legit to test:
    //    `elem.style[styleName] !== undefined`
    // If the property is supported it will return an empty string,
    // if unsupported it will return undefined.
    // We'll take advantage of this quick test and skip setting a style
    // on our modernizr element, but instead just testing undefined vs
    // empty string.
    // Property names can be provided in either camelCase or hyphen-case.

    function testProps(props, prefixed, value, skipValueTest) {
      skipValueTest = is(skipValueTest, 'undefined') ? false : skipValueTest; // Try native detect first

      if (!is(value, 'undefined')) {
        var result = nativeTestProps(props, value);

        if (!is(result, 'undefined')) {
          return result;
        }
      } // Otherwise do it properly


      var afterInit, i, propsLength, prop, before; // If we don't have a style element, that means we're running async or after
      // the core tests, so we'll need to create our own elements to use.
      // Inside of an SVG element, in certain browsers, the `style` element is only
      // defined for valid tags. Therefore, if `modernizr` does not have one, we
      // fall back to a less used element and hope for the best.
      // For strict XHTML browsers the hardly used samp element is used.

      var elems = ['modernizr', 'tspan', 'samp'];

      while (!mStyle.style && elems.length) {
        afterInit = true;
        mStyle.modElem = createElement(elems.shift());
        mStyle.style = mStyle.modElem.style;
      } // Delete the objects if we created them.


      function cleanElems() {
        if (afterInit) {
          delete mStyle.style;
          delete mStyle.modElem;
        }
      }

      propsLength = props.length;

      for (i = 0; i < propsLength; i++) {
        prop = props[i];
        before = mStyle.style[prop];

        if (contains(prop, '-')) {
          prop = cssToDOM(prop);
        }

        if (mStyle.style[prop] !== undefined) {
          // If value to test has been passed in, do a set-and-check test.
          // 0 (integer) is a valid property value, so check that `value` isn't
          // undefined, rather than just checking it's truthy.
          if (!skipValueTest && !is(value, 'undefined')) {
            // Needs a try catch block because of old IE. This is slow, but will
            // be avoided in most cases because `skipValueTest` will be used.
            try {
              mStyle.style[prop] = value;
            } catch (e) {} // If the property value has changed, we assume the value used is
            // supported. If `value` is empty string, it'll fail here (because
            // it hasn't changed), which matches how browsers have implemented
            // CSS.supports()


            if (mStyle.style[prop] !== before) {
              cleanElems();
              return prefixed === 'pfx' ? prop : true;
            }
          } // Otherwise just return true, or the property name if this is a
          // `prefixed()` call
          else {
              cleanElems();
              return prefixed === 'pfx' ? prop : true;
            }
        }
      }

      cleanElems();
      return false;
    }

    ;
    /**
     * fnBind is a super small [bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind) polyfill.
     *
     * @access private
     * @function fnBind
     * @param {Function} fn - a function you want to change `this` reference to
     * @param {object} that - the `this` you want to call the function with
     * @returns {Function} The wrapped version of the supplied function
     */

    function fnBind(fn, that) {
      return function () {
        return fn.apply(that, arguments);
      };
    }

    ;
    /**
     * testDOMProps is a generic DOM property test; if a browser supports
     *   a certain property, it won't return undefined for it.
     *
     * @access private
     * @function testDOMProps
     * @param {Array<string>} props - An array of properties to test for
     * @param {object} obj - An object or Element you want to use to test the parameters again
     * @param {boolean|object} elem - An Element to bind the property lookup again. Use `false` to prevent the check
     * @returns {boolean|*} returns `false` if the prop is unsupported, otherwise the value that is supported
     */

    function testDOMProps(props, obj, elem) {
      var item;

      for (var i in props) {
        if (props[i] in obj) {
          // return the property name as a string
          if (elem === false) {
            return props[i];
          }

          item = obj[props[i]]; // let's bind a function

          if (is(item, 'function')) {
            // bind to obj unless overridden
            return fnBind(item, elem || obj);
          } // return the unbound function or obj or value


          return item;
        }
      }

      return false;
    }

    ;
    /**
     * testPropsAll tests a list of DOM properties we want to check against.
     * We specify literally ALL possible (known and/or likely) properties on
     * the element including the non-vendor prefixed one, for forward-
     * compatibility.
     *
     * @access private
     * @function testPropsAll
     * @param {string} prop - A string of the property to test for
     * @param {string|object} [prefixed] - An object to check the prefixed properties on. Use a string to skip
     * @param {HTMLElement|SVGElement} [elem] - An element used to test the property and value against
     * @param {string} [value] - A string of a css value
     * @param {boolean} [skipValueTest] - An boolean representing if you want to test if value sticks when set
     * @returns {string|boolean} returns the string version of the property, or `false` if it is unsupported
     */

    function testPropsAll(prop, prefixed, elem, value, skipValueTest) {
      var ucProp = prop.charAt(0).toUpperCase() + prop.slice(1),
          props = (prop + ' ' + cssomPrefixes.join(ucProp + ' ') + ucProp).split(' '); // did they call .prefixed('boxSizing') or are we just testing a prop?

      if (is(prefixed, 'string') || is(prefixed, 'undefined')) {
        return testProps(props, prefixed, value, skipValueTest); // otherwise, they called .prefixed('requestAnimationFrame', window[, elem])
      } else {
        props = (prop + ' ' + domPrefixes.join(ucProp + ' ') + ucProp).split(' ');
        return testDOMProps(props, prefixed, elem);
      }
    } // Modernizr.testAllProps() investigates whether a given style property,
    // or any of its vendor-prefixed variants, is recognized
    //
    // Note that the property names must be provided in the camelCase variant.
    // Modernizr.testAllProps('boxSizing')


    ModernizrProto.testAllProps = testPropsAll;
    /**
     * prefixed returns the prefixed or nonprefixed property name variant of your input
     *
     * @memberOf Modernizr
     * @name Modernizr.prefixed
     * @optionName Modernizr.prefixed()
     * @optionProp prefixed
     * @access public
     * @function prefixed
     * @param {string} prop - String name of the property to test for
     * @param {object} [obj] - An object to test for the prefixed properties on
     * @param {HTMLElement} [elem] - An element used to test specific properties against
     * @returns {string|boolean} The string representing the (possibly prefixed) valid
     * version of the property, or `false` when it is unsupported.
     * @example
     *
     * Modernizr.prefixed takes a string css value in the DOM style camelCase (as
     * opposed to the css style hyphen-case) form and returns the (possibly prefixed)
     * version of that property that the browser actually supports.
     *
     * For example, in older Firefox...
     * ```js
     * prefixed('boxSizing')
     * ```
     * returns 'MozBoxSizing'
     *
     * In newer Firefox, as well as any other browser that support the unprefixed
     * version would simply return `boxSizing`. Any browser that does not support
     * the property at all, it will return `false`.
     *
     * By default, prefixed is checked against a DOM element. If you want to check
     * for a property on another object, just pass it as a second argument
     *
     * ```js
     * var rAF = prefixed('requestAnimationFrame', window);
     *
     * raf(function() {
     *  renderFunction();
     * })
     * ```
     *
     * Note that this will return _the actual function_ - not the name of the function.
     * If you need the actual name of the property, pass in `false` as a third argument
     *
     * ```js
     * var rAFProp = prefixed('requestAnimationFrame', window, false);
     *
     * rafProp === 'WebkitRequestAnimationFrame' // in older webkit
     * ```
     *
     * One common use case for prefixed is if you're trying to determine which transition
     * end event to bind to, you might do something like...
     * ```js
     * var transEndEventNames = {
     *     'WebkitTransition' : 'webkitTransitionEnd', * Saf 6, Android Browser
     *     'MozTransition'    : 'transitionend',       * only for FF < 15
     *     'transition'       : 'transitionend'        * IE10, Opera, Chrome, FF 15+, Saf 7+
     * };
     *
     * var transEndEventName = transEndEventNames[ Modernizr.prefixed('transition') ];
     * ```
     *
     * If you want a similar lookup, but in hyphen-case, you can use [prefixedCSS](#modernizr-prefixedcss).
     */

    var prefixed = ModernizrProto.prefixed = function (prop, obj, elem) {
      if (prop.indexOf('@') === 0) {
        return atRule(prop);
      }

      if (prop.indexOf('-') !== -1) {
        // Convert hyphen-case to camelCase
        prop = cssToDOM(prop);
      }

      if (!obj) {
        return testPropsAll(prop, 'pfx');
      } else {
        // Testing DOM property e.g. Modernizr.prefixed('requestAnimationFrame', window) // 'mozRequestAnimationFrame'
        return testPropsAll(prop, obj, elem);
      }
    };
    /**
     * List of property values to set for css tests. See ticket #21
     * https://github.com/modernizr/modernizr/issues/21
     *
     * @memberOf Modernizr
     * @name Modernizr._prefixes
     * @optionName Modernizr._prefixes
     * @optionProp prefixes
     * @access public
     * @example
     *
     * Modernizr._prefixes is the internal list of prefixes that we test against
     * inside of things like [prefixed](#modernizr-prefixed) and [prefixedCSS](#-code-modernizr-prefixedcss). It is simply
     * an array of hyphen-case vendor prefixes you can use within your code.
     *
     * Some common use cases include
     *
     * Generating all possible prefixed version of a CSS property
     * ```js
     * var rule = Modernizr._prefixes.join('transform: rotate(20deg); ');
     *
     * rule === 'transform: rotate(20deg); webkit-transform: rotate(20deg); moz-transform: rotate(20deg); o-transform: rotate(20deg); ms-transform: rotate(20deg);'
     * ```
     *
     * Generating all possible prefixed version of a CSS value
     * ```js
     * rule = 'display:' +  Modernizr._prefixes.join('flex; display:') + 'flex';
     *
     * rule === 'display:flex; display:-webkit-flex; display:-moz-flex; display:-o-flex; display:-ms-flex; display:flex'
     * ```
     */
    // we use ['',''] rather than an empty array in order to allow a pattern of .`join()`ing prefixes to test
    // values in feature detects to continue to work


    var prefixes = ModernizrProto._config.usePrefixes ? ' -webkit- -moz- -o- -ms- '.split(' ') : ['', '']; // expose these for the plugin API. Look in the source for how to join() them against your input

    ModernizrProto._prefixes = prefixes;
    /**
     * prefixedCSS is just like [prefixed](#modernizr-prefixed), but the returned values are in
     * hyphen-case (e.g. `box-sizing`) rather than camelCase (boxSizing).
     *
     * @memberOf Modernizr
     * @name Modernizr.prefixedCSS
     * @optionName Modernizr.prefixedCSS()
     * @optionProp prefixedCSS
     * @access public
     * @function prefixedCSS
     * @param {string} prop - String name of the property to test for
     * @returns {string|boolean} The string representing the (possibly prefixed)
     * valid version of the property, or `false` when it is unsupported.
     * @example
     *
     * `Modernizr.prefixedCSS` is like `Modernizr.prefixed`, but returns the result
     * in hyphenated form
     *
     * ```js
     * Modernizr.prefixedCSS('transition') // '-moz-transition' in old Firefox
     * ```
     *
     * Since it is only useful for CSS style properties, it can only be tested against
     * an HTMLElement.
     *
     * Properties can be passed as both the DOM style camelCase or CSS style hyphen-case.
     */

    var prefixedCSS = ModernizrProto.prefixedCSS = function (prop) {
      var prefixedProp = prefixed(prop);
      return prefixedProp && domToCSS(prefixedProp);
    };
    /**
     * testAllProps determines whether a given CSS property is supported in the browser
     *
     * @memberOf Modernizr
     * @name Modernizr.testAllProps
     * @optionName Modernizr.testAllProps()
     * @optionProp testAllProps
     * @access public
     * @function testAllProps
     * @param {string} prop - String naming the property to test (either camelCase or hyphen-case)
     * @param {string} [value] - String of the value to test
     * @param {boolean} [skipValueTest=false] - Whether to skip testing that the value is supported when using non-native detection
     * @returns {string|boolean} returns the string version of the property, or `false` if it is unsupported
     * @example
     *
     * testAllProps determines whether a given CSS property, in some prefixed form,
     * is supported by the browser.
     *
     * ```js
     * testAllProps('boxSizing')  // true
     * ```
     *
     * It can optionally be given a CSS value in string form to test if a property
     * value is valid
     *
     * ```js
     * testAllProps('display', 'block') // true
     * testAllProps('display', 'penguin') // false
     * ```
     *
     * A boolean can be passed as a third parameter to skip the value check when
     * native detection (@supports) isn't available.
     *
     * ```js
     * testAllProps('shapeOutside', 'content-box', true);
     * ```
     */


    function testAllProps(prop, value, skipValueTest) {
      return testPropsAll(prop, undefined, undefined, value, skipValueTest);
    }

    ModernizrProto.testAllProps = testAllProps;
    /**
     * testProp() investigates whether a given style property is recognized
     * Property names can be provided in either camelCase or hyphen-case.
     *
     * @memberOf Modernizr
     * @name Modernizr.testProp
     * @access public
     * @optionName Modernizr.testProp()
     * @optionProp testProp
     * @function testProp
     * @param {string} prop - Name of the CSS property to check
     * @param {string} [value] - Name of the CSS value to check
     * @param {boolean} [useValue] - Whether or not to check the value if @supports isn't supported
     * @returns {boolean} an empty string if the property is supported, undefined if its unsupported
     * @example
     *
     * Just like [testAllProps](#modernizr-testallprops), only it does not check any vendor prefixed
     * version of the string.
     *
     * Note that the property name must be provided in camelCase (e.g. boxSizing not box-sizing)
     *
     * ```js
     * Modernizr.testProp('pointerEvents')  // true
     * ```
     *
     * You can also provide a value as an optional second argument to check if a
     * specific value is supported
     *
     * ```js
     * Modernizr.testProp('pointerEvents', 'none') // true
     * Modernizr.testProp('pointerEvents', 'penguin') // false
     * ```
     */

    var testProp = ModernizrProto.testProp = function (prop, value, useValue) {
      return testProps([prop], undefined, value, useValue);
    };
    /**
     * testStyles injects an element with style element and some CSS rules
     *
     * @memberOf Modernizr
     * @name Modernizr.testStyles
     * @optionName Modernizr.testStyles()
     * @optionProp testStyles
     * @access public
     * @function testStyles
     * @param {string} rule - String representing a css rule
     * @param {Function} callback - A function that is used to test the injected element
     * @param {number} [nodes] - An integer representing the number of additional nodes you want injected
     * @param {string[]} [testnames] - An array of strings that are used as ids for the additional nodes
     * @returns {boolean}
     * @example
     *
     * `Modernizr.testStyles` takes a CSS rule and injects it onto the current page
     * along with (possibly multiple) DOM elements. This lets you check for features
     * that can not be detected by simply checking the [IDL](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Interface_development_guide/IDL_interface_rules).
     *
     * ```js
     * Modernizr.testStyles('#modernizr { width: 9px; color: papayawhip; }', function(elem, rule) {
     *   // elem is the first DOM node in the page (by default #modernizr)
     *   // rule is the first argument you supplied - the CSS rule in string form
     *
     *   addTest('widthworks', elem.style.width === '9px')
     * });
     * ```
     *
     * If your test requires multiple nodes, you can include a third argument
     * indicating how many additional div elements to include on the page. The
     * additional nodes are injected as children of the `elem` that is returned as
     * the first argument to the callback.
     *
     * ```js
     * Modernizr.testStyles('#modernizr {width: 1px}; #modernizr2 {width: 2px}', function(elem) {
     *   document.getElementById('modernizr').style.width === '1px'; // true
     *   document.getElementById('modernizr2').style.width === '2px'; // true
     *   elem.firstChild === document.getElementById('modernizr2'); // true
     * }, 1);
     * ```
     *
     * By default, all of the additional elements have an ID of `modernizr[n]`, where
     * `n` is its index (e.g. the first additional, second overall is `#modernizr2`,
     * the second additional is `#modernizr3`, etc.).
     * If you want to have more meaningful IDs for your function, you can provide
     * them as the fourth argument, as an array of strings
     *
     * ```js
     * Modernizr.testStyles('#foo {width: 10px}; #bar {height: 20px}', function(elem) {
     *   elem.firstChild === document.getElementById('foo'); // true
     *   elem.lastChild === document.getElementById('bar'); // true
     * }, 2, ['foo', 'bar']);
     * ```
     */


    var testStyles = ModernizrProto.testStyles = injectElementWithStyles;
    /*!
    {
      "name": "a[download] Attribute",
      "property": "adownload",
      "caniuse": "download",
      "tags": ["media", "attribute"],
      "builderAliases": ["a_download"],
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://developers.whatwg.org/links.html#downloading-resources"
      }]
    }
    !*/

    /* DOC
    When used on an `<a>`, this attribute signifies that the resource it points to should be downloaded by the browser rather than navigating to it.
    */

    Modernizr.addTest('adownload', !window.externalHost && 'download' in createElement('a'));
    /*!
    {
      "name": "Application Cache",
      "property": "applicationcache",
      "caniuse": "offline-apps",
      "tags": ["storage", "offline"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/docs/HTML/Using_the_application_cache"
      }],
      "polyfills": ["html5gears"]
    }
    !*/

    /* DOC
    Detects support for the Application Cache, for storing data to enable web-based applications run offline.
    
    The API has been [heavily criticized](https://alistapart.com/article/application-cache-is-a-douchebag) and discussions are underway to address this.
    */

    Modernizr.addTest('applicationcache', 'applicationCache' in window);
    /*!
    {
      "name": "Blob constructor",
      "property": "blobconstructor",
      "aliases": ["blob-constructor"],
      "builderAliases": ["blob_constructor"],
      "caniuse": "blobbuilder",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://w3c.github.io/FileAPI/#constructorBlob"
      }],
      "polyfills": ["blobjs"]
    }
    !*/

    /* DOC
    Detects support for the Blob constructor, for creating file-like objects of immutable, raw data.
    */

    Modernizr.addTest('blobconstructor', function () {
      try {
        return !!new Blob();
      } catch (e) {
        return false;
      }
    }, {
      aliases: ['blob-constructor']
    });
    /*!
    {
      "name": "Canvas",
      "property": "canvas",
      "caniuse": "canvas",
      "tags": ["canvas", "graphics"],
      "polyfills": ["flashcanvas", "excanvas", "slcanvas", "fxcanvas"]
    }
    !*/

    /* DOC
    Detects support for the `<canvas>` element for 2D drawing.
    */
    // On the S60 and BB Storm, getContext exists, but always returns undefined
    // so we actually have to call getContext() to verify
    // github.com/Modernizr/Modernizr/issues/issue/97/

    Modernizr.addTest('canvas', function () {
      var elem = createElement('canvas');
      return !!(elem.getContext && elem.getContext('2d'));
    });
    /*!
    {
      "name": "canvas blending support",
      "property": "canvasblending",
      "caniuse": "canvas-blending",
      "tags": ["canvas"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://drafts.fxtf.org/compositing-1/"
      }, {
        "name": "Article",
        "href": "https://web.archive.org/web/20171003232921/http://blogs.adobe.com/webplatform/2013/01/28/blending-features-in-canvas/"
      }]
    }
    !*/

    /* DOC
    Detects if Photoshop style blending modes are available in canvas.
    */

    Modernizr.addTest('canvasblending', function () {
      if (Modernizr.canvas === false) {
        return false;
      }

      var ctx = createElement('canvas').getContext('2d'); // firefox 3 throws an error when setting an invalid `globalCompositeOperation`

      try {
        ctx.globalCompositeOperation = 'screen';
      } catch (e) {}

      return ctx.globalCompositeOperation === 'screen';
    });
    /*!
    {
      "name": "canvas.toDataURL type support",
      "property": ["todataurljpeg", "todataurlpng", "todataurlwebp"],
      "tags": ["canvas"],
      "builderAliases": ["canvas_todataurl_type"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement.toDataURL"
      }]
    }
    !*/

    var canvas = createElement('canvas');
    Modernizr.addTest('todataurljpeg', function () {
      var supports = false; // AVG secure browser with 'Anti-Fingerprinting' turned on throws an exception when using an "invalid" toDataUrl

      try {
        supports = !!Modernizr.canvas && canvas.toDataURL('image/jpeg').indexOf('data:image/jpeg') === 0;
      } catch (e) {}

      return supports;
    });
    Modernizr.addTest('todataurlpng', function () {
      var supports = false; // AVG secure browser with 'Anti-Fingerprinting' turned on throws an exception when using an "invalid" toDataUrl

      try {
        supports = !!Modernizr.canvas && canvas.toDataURL('image/png').indexOf('data:image/png') === 0;
      } catch (e) {}

      return supports;
    });
    Modernizr.addTest('todataurlwebp', function () {
      var supports = false; // firefox 3 throws an error when you use an "invalid" toDataUrl

      try {
        supports = !!Modernizr.canvas && canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
      } catch (e) {}

      return supports;
    });
    /*!
    {
      "name": "canvas winding support",
      "property": "canvaswinding",
      "tags": ["canvas"],
      "notes": [{
        "name": "Article",
        "href": "https://web.archive.org/web/20170825024655/http://blogs.adobe.com/webplatform/2013/01/30/winding-rules-in-canvas/"
      }]
    }
    !*/

    /* DOC
    Determines if winding rules, which controls if a path can go clockwise or counterclockwise
    */

    Modernizr.addTest('canvaswinding', function () {
      if (Modernizr.canvas === false) {
        return false;
      }

      var ctx = createElement('canvas').getContext('2d');
      ctx.rect(0, 0, 10, 10);
      ctx.rect(2, 2, 6, 6);
      return ctx.isPointInPath(5, 5, 'evenodd') === false;
    });
    /*!
    {
      "name": "Canvas text",
      "property": "canvastext",
      "caniuse": "canvas-text",
      "tags": ["canvas", "graphics"],
      "polyfills": ["canvastext"]
    }
    !*/

    /* DOC
    Detects support for the text APIs for `<canvas>` elements.
    */

    Modernizr.addTest('canvastext', function () {
      if (Modernizr.canvas === false) {
        return false;
      }

      return typeof createElement('canvas').getContext('2d').fillText === 'function';
    });
    /*!
    {
      "name": "Content Editable",
      "property": "contenteditable",
      "caniuse": "contenteditable",
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/multipage/interaction.html#contenteditable"
      }]
    }
    !*/

    /* DOC
    Detects support for the `contenteditable` attribute of elements, allowing their DOM text contents to be edited directly by the user.
    */

    Modernizr.addTest('contenteditable', function () {
      // early bail out
      if (!('contentEditable' in docElement)) {
        return;
      } // some mobile browsers (android < 3.0, iOS < 5) claim to support
      // contentEditable, but but don't really. This test checks to see
      // confirms whether or not it actually supports it.


      var div = createElement('div');
      div.contentEditable = true;
      return div.contentEditable === 'true';
    });
    /*!
    {
      "name": "Context menus",
      "property": "contextmenu",
      "caniuse": "menu",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/html5/interactive-elements.html#context-menus"
      }, {
        "name": "thewebrocks.com Demo",
        "href": "http://thewebrocks.com/demos/context-menu/"
      }],
      "polyfills": ["jquery-contextmenu"]
    }
    !*/

    /* DOC
    Detects support for custom context menus.
    */

    Modernizr.addTest('contextmenu', 'contextMenu' in docElement && 'HTMLMenuItemElement' in window);
    /*!
    {
      "name": "Cookies",
      "property": "cookies",
      "tags": ["storage"],
      "authors": ["tauren"]
    }
    !*/

    /* DOC
    Detects whether cookie support is enabled.
    */
    // https://github.com/Modernizr/Modernizr/issues/191

    Modernizr.addTest('cookies', function () {
      // navigator.cookieEnabled cannot detect custom or nuanced cookie blocking
      // configurations. For example, when blocking cookies via the Advanced
      // Privacy Settings in IE9, it always returns true. And there have been
      // issues in the past with site-specific exceptions.
      // Don't rely on it.
      // try..catch because some in situations `document.cookie` is exposed but throws a
      // SecurityError if you try to access it; e.g. documents created from data URIs
      // or in sandboxed iframes (depending on flags/context)
      try {
        // Create cookie
        document.cookie = 'cookietest=1';
        var ret = document.cookie.indexOf('cookietest=') !== -1; // Delete cookie

        document.cookie = 'cookietest=1; expires=Thu, 01-Jan-1970 00:00:01 GMT';
        return ret;
      } catch (e) {
        return false;
      }
    });
    /*!
    {
      "name": "Cross-Origin Resource Sharing",
      "property": "cors",
      "caniuse": "cors",
      "authors": ["Theodoor van Donge"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS"
      }],
      "polyfills": ["pmxdr", "ppx", "flxhr"]
    }
    !*/

    /* DOC
    Detects support for Cross-Origin Resource Sharing: method of performing XMLHttpRequests across domains.
    */

    Modernizr.addTest('cors', 'XMLHttpRequest' in window && 'withCredentials' in new XMLHttpRequest());
    /*!
    {
      "name": "Custom Elements API",
      "property": "customelements",
      "caniuse": "custom-elementsv1",
      "tags": ["customelements"],
      "polyfills": ["customelements"],
      "notes": [{
        "name": "Specs for Custom Elements",
        "href": "https://www.w3.org/TR/custom-elements/"
      }]
    }
    !*/

    /* DOC
    Detects support for the Custom Elements API, to create custom html elements via js
    */

    Modernizr.addTest('customelements', 'customElements' in window);
    /*!
    {
      "name": "cssall",
      "property": "cssall",
      "notes": [{
        "name": "Spec",
        "href": "https://drafts.csswg.org/css-cascade/#all-shorthand"
      }]
    }
    !*/

    /* DOC
    Detects support for the `all` css property, which is a shorthand to reset all css properties (except direction and unicode-bidi) to their original value
    */

    Modernizr.addTest('cssall', 'all' in docElement.style);
    /*!
    {
      "name": "CSS Animations",
      "property": "cssanimations",
      "caniuse": "css-animation",
      "polyfills": ["transformie", "csssandpaper"],
      "tags": ["css"],
      "warnings": ["Android < 4 will pass this test, but can only animate a single property at a time"],
      "notes": [{
        "name": "Article: 'Dispelling the Android CSS animation myths'",
        "href": "https://web.archive.org/web/20180602074607/https://daneden.me/2011/12/14/putting-up-with-androids-bullshit/"
      }]
    }
    !*/

    /* DOC
    Detects whether or not elements can be animated using CSS
    */

    Modernizr.addTest('cssanimations', testAllProps('animationName', 'a', true));
    /*!
    {
      "name": "Appearance",
      "property": "appearance",
      "caniuse": "css-appearance",
      "tags": ["css"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/-moz-appearance"
      }, {
        "name": "CSS-Tricks CSS Almanac: appearance",
        "href": "https://css-tricks.com/almanac/properties/a/appearance/"
      }]
    }
    !*/

    /* DOC
    Detects support for the `appearance` css property, which is used to make an
    element inherit the style of a standard user interface element. It can also be
    used to remove the default styles of an element, such as input and buttons.
    */

    Modernizr.addTest('appearance', testAllProps('appearance'));
    /*!
    {
      "name": "Backdrop Filter",
      "property": "backdropfilter",
      "authors": ["Brian Seward"],
      "tags": ["css"],
      "caniuse": "css-backdrop-filter",
      "notes": [{
        "name": "W3C Editor’s Draft Spec",
        "href": "https://drafts.fxtf.org/filters-2/#BackdropFilterProperty"
      }, {
        "name": "WebKit Blog introduction + Demo",
        "href": "https://www.webkit.org/blog/3632/introducing-backdrop-filters/"
      }]
    }
    !*/

    /* DOC
    Detects support for CSS Backdrop Filters, allowing for background blur effects like those introduced in iOS 7. Support for this was added to iOS Safari/WebKit in iOS 9.
    */

    Modernizr.addTest('backdropfilter', testAllProps('backdropFilter'));
    /*!
    {
      "name": "CSS Background Blend Mode",
      "property": "backgroundblendmode",
      "caniuse": "css-backgroundblendmode",
      "tags": ["css"],
      "notes": [{
        "name": "CSS Blend Modes could be the next big thing in Web Design",
        "href": "https://medium.com/@bennettfeely/css-blend-modes-could-be-the-next-big-thing-in-web-design-6b51bf53743a"
      }, {
        "name": "Demo",
        "href": "https://bennettfeely.com/gradients/"
      }]
    }
    !*/

    /* DOC
    Detects the ability for the browser to composite backgrounds using blending modes similar to ones found in Photoshop or Illustrator.
    */

    Modernizr.addTest('backgroundblendmode', prefixed('backgroundBlendMode', 'text'));
    /*!
    {
      "name": "CSS Background Clip Text",
      "property": "backgroundcliptext",
      "authors": ["ausi"],
      "tags": ["css"],
      "notes": [{
        "name": "CSS Tricks Article",
        "href": "https://css-tricks.com/image-under-text/"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/199"
      }]
    }
    !*/

    /* DOC
    Detects the ability to control specifies whether or not an element's background
    extends beyond its border in CSS
    */

    Modernizr.addTest('backgroundcliptext', function () {
      return testAllProps('backgroundClip', 'text');
    });
    /*!
    {
      "name": "Background Position Shorthand",
      "property": "bgpositionshorthand",
      "caniuse": "css-background-offsets",
      "tags": ["css"],
      "builderAliases": ["css_backgroundposition_shorthand"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/CSS/background-position"
      }, {
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-background/#background-position"
      }, {
        "name": "Demo",
        "href": "https://jsfiddle.net/Blink/bBXvt/"
      }]
    }
    !*/

    /* DOC
    Detects if you can use the shorthand method to define multiple parts of an
    element's background-position simultaneously.
    
    eg `background-position: right 10px bottom 10px`
    */

    Modernizr.addTest('bgpositionshorthand', function () {
      var elem = createElement('a');
      var eStyle = elem.style;
      var val = 'right 10px bottom 10px';
      eStyle.cssText = 'background-position: ' + val + ';';
      return eStyle.backgroundPosition === val;
    });
    /*!
    {
      "name": "Background Position XY",
      "property": "bgpositionxy",
      "tags": ["css"],
      "builderAliases": ["css_backgroundposition_xy"],
      "authors": ["Allan Lei", "Brandom Aaron"],
      "notes": [{
        "name": "Demo",
        "href": "https://jsfiddle.net/allanlei/R8AYS/"
      }, {
        "name": "Adapted From",
        "href": "https://github.com/brandonaaron/jquery-cssHooks/blob/master/bgpos.js"
      }]
    }
    !*/

    /* DOC
    Detects the ability to control an element's background position using css
    */

    Modernizr.addTest('bgpositionxy', function () {
      return testAllProps('backgroundPositionX', '3px', true) && testAllProps('backgroundPositionY', '5px', true);
    });
    /*!
    {
      "name": "Background Repeat",
      "property": ["bgrepeatspace", "bgrepeatround"],
      "tags": ["css"],
      "builderAliases": ["css_backgroundrepeat"],
      "authors": ["Ryan Seddon"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/background-repeat"
      }, {
        "name": "Test Page",
        "href": "https://jsbin.com/uzesun/"
      }, {
        "name": "Demo",
        "href": "https://jsfiddle.net/ryanseddon/yMLTQ/6/"
      }]
    }
    !*/

    /* DOC
    Detects the ability to use round and space as properties for background-repeat
    */
    // Must value-test these

    Modernizr.addTest('bgrepeatround', testAllProps('backgroundRepeat', 'round'));
    Modernizr.addTest('bgrepeatspace', testAllProps('backgroundRepeat', 'space'));
    /*!
    {
      "name": "Background Size",
      "property": "backgroundsize",
      "tags": ["css"],
      "knownBugs": ["This will false positive in Opera Mini - https://github.com/Modernizr/Modernizr/issues/396"],
      "notes": [{
        "name": "Related Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/396"
      }]
    }
    !*/

    Modernizr.addTest('backgroundsize', testAllProps('backgroundSize', '100%', true));
    /*!
    {
      "name": "Background Size Cover",
      "property": "bgsizecover",
      "tags": ["css"],
      "builderAliases": ["css_backgroundsizecover"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/CSS/background-size"
      }]
    }
    !*/
    // Must test value, as this specifically tests the `cover` value

    Modernizr.addTest('bgsizecover', testAllProps('backgroundSize', 'cover'));
    /*!
    {
      "name": "Border Image",
      "property": "borderimage",
      "caniuse": "border-image",
      "polyfills": ["css3pie"],
      "knownBugs": ["Android < 2.0 is true, but has a broken implementation"],
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('borderimage', testAllProps('borderImage', 'url() 1', true));
    /*!
    {
      "name": "Border Radius",
      "property": "borderradius",
      "caniuse": "border-radius",
      "polyfills": ["css3pie"],
      "tags": ["css"],
      "notes": [{
        "name": "Comprehensive Compat Chart",
        "href": "https://muddledramblings.com/table-of-css3-border-radius-compliance"
      }]
    }
    !*/

    Modernizr.addTest('borderradius', testAllProps('borderRadius', '0px', true));
    /*!
    {
      "name": "Box Shadow",
      "property": "boxshadow",
      "caniuse": "css-boxshadow",
      "tags": ["css"],
      "knownBugs": [
        "WebOS false positives on this test.",
        "The Kindle Silk browser false positives"
      ]
    }
    !*/

    Modernizr.addTest('boxshadow', testAllProps('boxShadow', '1px 1px', true));
    /*!
    {
      "name": "Box Sizing",
      "property": "boxsizing",
      "caniuse": "css3-boxsizing",
      "polyfills": ["borderboxmodel", "boxsizingpolyfill", "borderbox"],
      "tags": ["css"],
      "builderAliases": ["css_boxsizing"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/248"
      }]
    }
    !*/

    Modernizr.addTest('boxsizing', testAllProps('boxSizing', 'border-box', true) && (document.documentMode === undefined || document.documentMode > 7));
    /*!
    {
      "name": "CSS Calc",
      "property": "csscalc",
      "caniuse": "calc",
      "tags": ["css"],
      "builderAliases": ["css_calc"],
      "authors": ["@calvein"]
    }
    !*/

    /* DOC
    Method of allowing calculated values for length units. For example:
    
    ```css
    //lem {
      width: calc(100% - 3em);
    }
    ```
    */

    Modernizr.addTest('csscalc', function () {
      var prop = 'width:';
      var value = 'calc(10px);';
      var el = createElement('a');
      el.style.cssText = prop + prefixes.join(value + prop);
      return !!el.style.length;
    });
    /*!
    {
      "name": "CSS :checked pseudo-selector",
      "caniuse": "css-sel3",
      "property": "checked",
      "tags": ["css"],
      "notes": [{
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/pull/879"
      }]
    }
    !*/

    Modernizr.addTest('checked', function () {
      return testStyles('#modernizr {position:absolute} #modernizr input {margin-left:10px} #modernizr :checked {margin-left:20px;display:block}', function (elem) {
        var cb = createElement('input');
        cb.setAttribute('type', 'checkbox');
        cb.setAttribute('checked', 'checked');
        elem.appendChild(cb);
        return cb.offsetLeft === 20;
      });
    });
    /*!
    {
      "name": "CSS Font ch Units",
      "authors": ["Ron Waldon (@jokeyrhyme)"],
      "property": "csschunit",
      "caniuse": "ch-unit",
      "tags": ["css"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-values/#font-relative-lengths"
      }]
    }
    !*/

    Modernizr.addTest('csschunit', function () {
      var elemStyle = modElem.elem.style;
      var supports;

      try {
        elemStyle.fontSize = '3ch';
        supports = elemStyle.fontSize.indexOf('ch') !== -1;
      } catch (e) {
        supports = false;
      }

      return supports;
    });
    /*!
    {
      "name": "CSS Columns",
      "property": "csscolumns",
      "caniuse": "multicolumn",
      "polyfills": ["css3multicolumnjs"],
      "tags": ["css"]
    }
    !*/

    (function () {
      Modernizr.addTest('csscolumns', function () {
        var bool = false;
        var test = testAllProps('columnCount');

        try {
          bool = !!test;

          if (bool) {
            bool = new Boolean(bool);
          }
        } catch (e) {}

        return bool;
      });
      var props = ['Width', 'Span', 'Fill', 'Gap', 'Rule', 'RuleColor', 'RuleStyle', 'RuleWidth', 'BreakBefore', 'BreakAfter', 'BreakInside'];
      var name, test;

      for (var i = 0; i < props.length; i++) {
        name = props[i].toLowerCase();
        test = testAllProps('column' + props[i]); // break-before, break-after & break-inside are not "column"-prefixed in spec

        if (name === 'breakbefore' || name === 'breakafter' || name === 'breakinside') {
          test = test || testAllProps(props[i]);
        }

        Modernizr.addTest('csscolumns.' + name, test);
      }
    })();
    /*!
    {
      "name": "CSS Grid (old & new)",
      "property": ["cssgrid", "cssgridlegacy"],
      "authors": ["Faruk Ates"],
      "tags": ["css"],
      "notes": [{
        "name": "The new, standardized CSS Grid",
        "href": "https://www.w3.org/TR/css3-grid-layout/"
      }, {
        "name": "The _old_ CSS Grid (legacy)",
        "href": "https://www.w3.org/TR/2011/WD-css3-grid-layout-20110407/"
      }]
    }
    !*/
    // `grid-columns` is only in the old syntax, `grid-column` exists in both and so `grid-template-rows` is used for the new syntax.


    Modernizr.addTest('cssgridlegacy', testAllProps('grid-columns', '10px', true));
    Modernizr.addTest('cssgrid', testAllProps('grid-template-rows', 'none', true));
    /*!
    {
      "name": "CSS Cubic Bezier Range",
      "property": "cubicbezierrange",
      "tags": ["css"],
      "builderAliases": ["css_cubicbezierrange"],
      "authors": ["@calvein"],
      "warnings": ["cubic-bezier values can't be > 1 for Webkit until [bug #45761](https://bugs.webkit.org/show_bug.cgi?id=45761) is fixed"],
      "notes": [{
        "name": "Comprehensive Compat Chart",
        "href": "https://muddledramblings.com/table-of-css3-border-radius-compliance/"
      }]
    }
    !*/

    Modernizr.addTest('cubicbezierrange', function () {
      var el = createElement('a');
      el.style.cssText = prefixes.join('transition-timing-function:cubic-bezier(1,0,0,1.1); ');
      return !!el.style.length;
    });
    /*!
    {
      "name": "CSS Display run-in",
      "property": "display-runin",
      "authors": ["alanhogan"],
      "tags": ["css"],
      "builderAliases": ["css_displayrunin"],
      "notes": [{
        "name": "CSS Tricks Article",
        "href": "https://web.archive.org/web/20111204150927/http://css-tricks.com:80/596-run-in/"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/198"
      }]
    }
    !*/

    Modernizr.addTest('displayrunin', testAllProps('display', 'run-in'), {
      aliases: ['display-runin']
    });
    /*!
    {
      "name": "CSS Display table",
      "property": "displaytable",
      "caniuse": "css-table",
      "authors": ["scottjehl"],
      "tags": ["css"],
      "builderAliases": ["css_displaytable"],
      "notes": [{
        "name": "Detects for all additional table display values",
        "href": "https://pastebin.com/Gk9PeVaQ"
      }]
    }
    !*/

    /* DOC
    `display: table` and `table-cell` test. (both are tested under one name `table-cell` )
    */
    // If a document is in rtl mode this test will fail so we force ltr mode on the injected
    // element https://github.com/Modernizr/Modernizr/issues/716

    testStyles('#modernizr{display: table; direction: ltr}#modernizr div{display: table-cell; padding: 10px}', function (elem) {
      var ret;
      var child = elem.childNodes;
      ret = child[0].offsetLeft < child[1].offsetLeft;
      Modernizr.addTest('displaytable', ret, {
        aliases: ['display-table']
      });
    }, 2);
    /*!
    {
      "name": "CSS text-overflow ellipsis",
      "property": "ellipsis",
      "caniuse": "text-overflow",
      "polyfills": ["text-overflow"],
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('ellipsis', testAllProps('textOverflow', 'ellipsis'));
    /*!
    {
      "name": "CSS.escape()",
      "property": "cssescape",
      "polyfills": ["css-escape"],
      "tags": ["css", "cssom"]
    }
    !*/

    /* DOC
    Tests for `CSS.escape()` support.
    */

    var CSS = window.CSS;
    Modernizr.addTest('cssescape', CSS ? typeof CSS.escape === 'function' : false);
    /*!
    {
      "name": "CSS Font ex Units",
      "authors": ["Ron Waldon (@jokeyrhyme)"],
      "property": "cssexunit",
      "caniuse": "mdn-css_types_length_ex",
      "tags": ["css"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-values/#font-relative-lengths"
      }]
    }
    !*/

    Modernizr.addTest('cssexunit', function () {
      var elemStyle = modElem.elem.style;
      var supports;

      try {
        elemStyle.fontSize = '3ex';
        supports = elemStyle.fontSize.indexOf('ex') !== -1;
      } catch (e) {
        supports = false;
      }

      return supports;
    });
    /*!
    {
      "name": "CSS Supports",
      "property": "supports",
      "caniuse": "css-featurequeries",
      "tags": ["css"],
      "builderAliases": ["css_supports"],
      "notes": [{
        "name": "W3C Spec (The @supports rule)",
        "href": "https://dev.w3.org/csswg/css3-conditional/#at-supports"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/648"
      }, {
        "name": "W3C Spec (The CSSSupportsRule interface)",
        "href": "https://dev.w3.org/csswg/css3-conditional/#the-csssupportsrule-interface"
      }]
    }
    !*/

    var newSyntax = 'CSS' in window && 'supports' in window.CSS;
    var oldSyntax = ('supportsCSS' in window);
    Modernizr.addTest('supports', newSyntax || oldSyntax);
    /*!
    {
      "name": "CSS Filters",
      "property": "cssfilters",
      "caniuse": "css-filters",
      "polyfills": ["polyfilter"],
      "tags": ["css"],
      "builderAliases": ["css_filters"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/filter"
      }]
    }
    !*/

    Modernizr.addTest('cssfilters', function () {
      if (Modernizr.supports) {
        return testAllProps('filter', 'blur(2px)');
      } else {
        var el = createElement('a');
        el.style.cssText = prefixes.join('filter:blur(2px); '); // https://github.com/Modernizr/Modernizr/issues/615
        // documentMode is needed for false positives in oldIE, please see issue above

        return !!el.style.length && (document.documentMode === undefined || document.documentMode > 9);
      }
    });
    /*!
    {
      "name": "Flexbox",
      "property": "flexbox",
      "caniuse": "flexbox",
      "tags": ["css"],
      "notes": [{
        "name": "The _new_ flexbox",
        "href": "https://www.w3.org/TR/css-flexbox-1/"
      }],
      "warnings": [
        "A `true` result for this detect does not imply that the `flex-wrap` property is supported; see the `flexwrap` detect."
      ]
    }
    !*/

    /* DOC
    Detects support for the Flexible Box Layout model, a.k.a. Flexbox, which allows easy manipulation of layout order and sizing within a container.
    */

    Modernizr.addTest('flexbox', testAllProps('flexBasis', '1px', true));
    /*!
    {
      "name": "Flexbox (legacy)",
      "property": "flexboxlegacy",
      "tags": ["css"],
      "polyfills": ["flexie"],
      "notes": [{
        "name": "The _old_ flexbox",
        "href": "https://www.w3.org/TR/2009/WD-css3-flexbox-20090723/"
      }]
    }
    !*/

    Modernizr.addTest('flexboxlegacy', testAllProps('boxDirection', 'reverse', true));
    /*!
    {
      "name": "Flexbox (tweener)",
      "property": "flexboxtweener",
      "tags": ["css"],
      "polyfills": ["flexie"],
      "notes": [{
        "name": "The _inbetween_ flexbox",
        "href": "https://www.w3.org/TR/2011/WD-css3-flexbox-20111129/"
      }],
      "warnings": ["This represents an old syntax, not the latest standard syntax."]
    }
    !*/

    Modernizr.addTest('flexboxtweener', testAllProps('flexAlign', 'end', true));
    /*!
    {
      "name": "Flex Line Wrapping",
      "property": "flexwrap",
      "tags": ["css", "flexbox"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css-flexbox-1/"
      }],
      "warnings": [
        "Does not imply a modern implementation – see documentation."
      ]
    }
    !*/

    /* DOC
    Detects support for the `flex-wrap` CSS property, part of Flexbox, which isn’t present in all Flexbox implementations (notably Firefox).
    
    This featured in both the 'tweener' syntax (implemented by IE10) and the 'modern' syntax (implemented by others). This detect will return `true` for either of these implementations, as long as the `flex-wrap` property is supported. So to ensure the modern syntax is supported, use together with `Modernizr.flexbox`:
    
    ```javascript
    if (Modernizr.flexbox && Modernizr.flexwrap) {
      // Modern Flexbox with `flex-wrap` supported
    }
    else {
      // Either old Flexbox syntax, or `flex-wrap` not supported
    }
    ```
    */

    Modernizr.addTest('flexwrap', testAllProps('flexWrap', 'wrap', true));
    /*!
    {
      "name": "@font-face",
      "property": "fontface",
      "authors": ["Diego Perini", "Mat Marquis"],
      "tags": ["css"],
      "knownBugs": [
        "False Positive: WebOS https://github.com/Modernizr/Modernizr/issues/342",
        "False Positive: WP7 https://github.com/Modernizr/Modernizr/issues/538"
      ],
      "notes": [{
        "name": "@font-face detection routine by Diego Perini",
        "href": "http://javascript.nwbox.com/CSSSupport/"
      }, {
        "name": "Filament Group @font-face compatibility research",
        "href": "https://docs.google.com/presentation/d/1n4NyG4uPRjAA8zn_pSQ_Ket0RhcWC6QlZ6LMjKeECo0/edit#slide=id.p"
      }, {
        "name": "Filament Grunticon/@font-face device testing results",
        "href": "https://docs.google.com/spreadsheet/ccc?key=0Ag5_yGvxpINRdHFYeUJPNnZMWUZKR2ItMEpRTXZPdUE#gid=0"
      }, {
        "name": "CSS fonts on Android",
        "href": "https://stackoverflow.com/questions/3200069/css-fonts-on-android"
      }, {
        "name": "@font-face and Android",
        "href": "http://archivist.incutio.com/viewlist/css-discuss/115960"
      }]
    }
    !*/

    var unsupportedUserAgent = function () {
      var ua = navigator.userAgent;
      var webos = ua.match(/w(eb)?osbrowser/gi);
      var wppre8 = ua.match(/windows phone/gi) && ua.match(/iemobile\/([0-9])+/gi) && parseFloat(RegExp.$1) >= 9;
      return webos || wppre8;
    }();

    if (unsupportedUserAgent) {
      Modernizr.addTest('fontface', false);
    } else {
      testStyles('@font-face {font-family:"font";src:url("https://")}', function (node, rule) {
        var style = document.getElementById('smodernizr');
        var sheet = style.sheet || style.styleSheet;
        var cssText = sheet ? sheet.cssRules && sheet.cssRules[0] ? sheet.cssRules[0].cssText : sheet.cssText || '' : '';
        var bool = /src/i.test(cssText) && cssText.indexOf(rule.split(' ')[0]) === 0;
        Modernizr.addTest('fontface', bool);
      });
    }

    ;
    /*!
    {
      "name": "CSS Generated Content",
      "property": "generatedcontent",
      "tags": ["css"],
      "warnings": ["Android won't return correct height for anything below 7px #738"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-selectors/#gen-content"
      }, {
        "name": "MDN Docs on :before",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/::before"
      }, {
        "name": "MDN Docs on :after",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/::after"
      }]
    }
    !*/

    testStyles('#modernizr{font:0/0 a}#modernizr:after{content:":)";visibility:hidden;font:7px/1 a}', function (node) {
      // See bug report on why this value is 6 crbug.com/608142
      Modernizr.addTest('generatedcontent', node.offsetHeight >= 6);
    });
    /*!
    {
      "name": "CSS Gradients",
      "caniuse": "css-gradients",
      "property": "cssgradients",
      "tags": ["css"],
      "knownBugs": ["False-positives on webOS (https://github.com/Modernizr/Modernizr/issues/202)"],
      "notes": [{
        "name": "Webkit Gradient Syntax",
        "href": "https://webkit.org/blog/175/introducing-css-gradients/"
      }, {
        "name": "Linear Gradient Syntax",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient"
      }, {
        "name": "W3C Spec",
        "href": "https://drafts.csswg.org/css-images-3/#gradients"
      }]
    }
    !*/

    Modernizr.addTest('cssgradients', function () {
      var str1 = 'background-image:';
      var str2 = 'gradient(linear,left top,right bottom,from(#9f9),to(white));';
      var css = '';
      var angle;

      for (var i = 0, len = prefixes.length - 1; i < len; i++) {
        angle = i === 0 ? 'to ' : '';
        css += str1 + prefixes[i] + 'linear-gradient(' + angle + 'left top, #9f9, white);';
      }

      if (Modernizr._config.usePrefixes) {
        // legacy webkit syntax (TODO:: remove when syntax not in use anymore)
        css += str1 + '-webkit-' + str2;
      }

      var elem = createElement('a');
      var style = elem.style;
      style.cssText = css; // IE6 returns undefined so cast to string

      return ('' + style.backgroundImage).indexOf('gradient') > -1;
    });
    /*! {
      "name": "CSS Hairline",
      "property": "hairline",
      "tags": ["css"],
      "authors": ["strarsis"],
      "notes": [{
        "name": "Blog post about CSS retina hairlines",
        "href": "http://dieulot.net/css-retina-hairline"
      }, {
        "name": "Derived from",
        "href": "https://gist.github.com/dieulot/520a49463f6058fbc8d1"
      }]
    }
    !*/

    /* DOC
    Detects support for hidpi/retina hairlines, which are CSS borders with less than 1px in width, for being physically 1px on hidpi screens.
    */

    Modernizr.addTest('hairline', function () {
      return testStyles('#modernizr {border:.5px solid transparent}', function (elem) {
        return elem.offsetHeight === 1;
      });
    });
    /*!
    {
      "name": "CSS HSLA Colors",
      "caniuse": "css3-colors",
      "property": "hsla",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('hsla', function () {
      var style = createElement('a').style;
      style.cssText = 'background-color:hsla(120,40%,100%,.5)';
      return contains(style.backgroundColor, 'rgba') || contains(style.backgroundColor, 'hsla');
    });
    /*!
    {
      "name": "CSS :invalid pseudo-class",
      "property": "cssinvalid",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/:invalid"
      }]
    }
    !*/

    /* DOC
      Detects support for the ':invalid' CSS pseudo-class.
    */

    Modernizr.addTest('cssinvalid', function () {
      return testStyles('#modernizr input{height:0;border:0;padding:0;margin:0;width:10px} #modernizr input:invalid{width:50px}', function (elem) {
        var input = createElement('input');
        input.required = true;
        elem.appendChild(input);
        return input.clientWidth > 10;
      });
    });
    /*!
    {
      "name": "CSS :last-child pseudo-selector",
      "caniuse": "css-sel3",
      "property": "lastchild",
      "tags": ["css"],
      "builderAliases": ["css_lastchild"],
      "notes": [{
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/pull/304"
      }]
    }
    !*/

    testStyles('#modernizr div {width:100px} #modernizr :last-child{width:200px;display:block}', function (elem) {
      Modernizr.addTest('lastchild', elem.lastChild.offsetWidth > elem.firstChild.offsetWidth);
    }, 2);
    /*!
    {
      "name": "CSS Mask",
      "caniuse": "css-masks",
      "property": "cssmask",
      "tags": ["css"],
      "builderAliases": ["css_mask"],
      "notes": [{
        "name": "Webkit blog on CSS Masks",
        "href": "https://webkit.org/blog/181/css-masks/"
      }, {
        "name": "Safari Docs",
        "href": "https://developer.apple.com/library/archive/documentation/InternetWeb/Conceptual/SafariVisualEffectsProgGuide/Masks/Masks.html"
      }, {
        "name": "CSS SVG mask",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/mask"
      }, {
        "name": "Combine with clippaths for awesomeness",
        "href": "https://web.archive.org/web/20150508193041/http://generic.cx:80/for/webkit/test.html"
      }]
    }
    !*/

    Modernizr.addTest('cssmask', testAllProps('maskRepeat', 'repeat-x', true));
    /*!
    {
      "name": "CSS Media Queries",
      "caniuse": "css-mediaqueries",
      "property": "mediaqueries",
      "tags": ["css"],
      "builderAliases": ["css_mediaqueries"]
    }
    !*/

    Modernizr.addTest('mediaqueries', mq('only all'));
    /*!
    {
      "name": "CSS Multiple Backgrounds",
      "caniuse": "multibackgrounds",
      "property": "multiplebgs",
      "tags": ["css"]
    }
    !*/
    // Setting multiple images AND a color on the background shorthand property
    // and then querying the style.background property value for the number of
    // occurrences of "url(" is a reliable method for detecting ACTUAL support for this!

    Modernizr.addTest('multiplebgs', function () {
      var style = createElement('a').style;
      style.cssText = 'background:url(https://),url(https://),red url(https://)'; // If the UA supports multiple backgrounds, there should be three occurrences
      // of the string "url(" in the return value for elemStyle.background

      return /(url\s*\(.*?){3}/.test(style.background);
    });
    /*!
    {
      "name": "CSS :nth-child pseudo-selector",
      "caniuse": "css-sel3",
      "property": "nthchild",
      "tags": ["css"],
      "notes": [{
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/pull/685"
      }, {
        "name": "Sitepoint :nth-child documentation",
        "href": "https://www.sitepoint.com/atoz-css-screencast-nth-child/"
      }],
      "authors": ["@emilchristensen"],
      "warnings": ["Known false negative in Safari 3.1 and Safari 3.2.2"]
    }
    !*/

    /* DOC
    Detects support for the ':nth-child()' CSS pseudo-selector.
    */
    // 4 `<div>` elements with `1px` width are created. Then every other element has its `width` set to `2px`.
    // Then we check if the width of the even elements is different then the width of the odd elements
    // while the two even elements have the same width (and the two odd elements too).
    // Earlier versions of the tests tried to check for the actual width which didnt work on chrome when the
    // browser was zoomed in our out in specific ways.

    testStyles('#modernizr div {width:1px} #modernizr div:nth-child(2n) {width:2px;}', function (elem) {
      var elems = elem.getElementsByTagName('div');
      var correctWidths = elems[0].offsetWidth === elems[2].offsetWidth && elems[1].offsetWidth === elems[3].offsetWidth && elems[0].offsetWidth !== elems[1].offsetWidth;
      Modernizr.addTest('nthchild', correctWidths);
    }, 4);
    /*!
    {
      "name": "CSS Object Fit",
      "caniuse": "object-fit",
      "property": "objectfit",
      "tags": ["css"],
      "builderAliases": ["css_objectfit"],
      "notes": [{
        "name": "Opera Article on Object Fit",
        "href": "https://dev.opera.com/articles/css3-object-fit-object-position/"
      }]
    }
    !*/

    Modernizr.addTest('objectfit', !!prefixed('objectFit'), {
      aliases: ['object-fit']
    });
    /*!
    {
      "name": "CSS Opacity",
      "caniuse": "css-opacity",
      "property": "opacity",
      "tags": ["css"]
    }
    !*/
    // Browsers that actually have CSS Opacity implemented have done so
    // according to spec, which means their return values are within the
    // range of [0.0,1.0] - including the leading zero.

    Modernizr.addTest('opacity', function () {
      var style = createElement('a').style;
      style.cssText = prefixes.join('opacity:.55;'); // The non-literal . in this regex is intentional:
      // German Chrome returns this value as 0,55
      // github.com/Modernizr/Modernizr/issues/#issue/59/comment/516632

      return /^0.55$/.test(style.opacity);
    });
    /*!
    {
      "name": "CSS Overflow Scrolling",
      "property": "overflowscrolling",
      "tags": ["css"],
      "builderAliases": ["css_overflow_scrolling"],
      "warnings": ["Introduced in iOS5b2. API is subject to change."],
      "notes": [{
        "name": "Article on iOS overflow scrolling",
        "href": "https://css-tricks.com/snippets/css/momentum-scrolling-on-ios-overflow-elements/"
      }]
    }
    !*/

    Modernizr.addTest('overflowscrolling', testAllProps('overflowScrolling', 'touch', true));
    /*!
    {
      "name": "CSS Pointer Events",
      "caniuse": "pointer-events",
      "property": "csspointerevents",
      "authors": ["ausi"],
      "tags": ["css"],
      "builderAliases": ["css_pointerevents"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events"
      }, {
        "name": "Test Project Page",
        "href": "https://ausi.github.com/Feature-detection-technique-for-pointer-events/"
      }, {
        "name": "Test Project Wiki",
        "href": "https://github.com/ausi/Feature-detection-technique-for-pointer-events/wiki"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/80"
      }]
    }
    !*/

    Modernizr.addTest('csspointerevents', function () {
      var style = createElement('a').style;
      style.cssText = 'pointer-events:auto';
      return style.pointerEvents === 'auto';
    });
    /*!
    {
      "name": "CSS position: sticky",
      "property": "csspositionsticky",
      "tags": ["css"],
      "builderAliases": ["css_positionsticky"],
      "notes": [{
        "name": "Chrome bug report",
        "href":"https://bugs.chromium.org/p/chromium/issues/detail?id=322972"
      }],
      "warnings": ["using position:sticky on anything but top aligned elements is buggy in Chrome < 37 and iOS <=7+"]
    }
    !*/
    // Sticky positioning - constrains an element to be positioned inside the
    // intersection of its container box, and the viewport.

    Modernizr.addTest('csspositionsticky', function () {
      var prop = 'position:';
      var value = 'sticky';
      var el = createElement('a');
      var mStyle = el.style;
      mStyle.cssText = prop + prefixes.join(value + ';' + prop).slice(0, -prop.length);
      return mStyle.position.indexOf(value) !== -1;
    });
    /*!
    {
      "name": "CSS Generated Content Animations",
      "property": "csspseudoanimations",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('csspseudoanimations', function () {
      var result = false;

      if (!Modernizr.cssanimations) {
        return result;
      }

      var styles = ['@', prefixes.join('keyframes csspseudoanimations { from { font-size: 10px; } }@').replace(/\@$/, ''), '#modernizr:before { content:" "; font-size:5px;', prefixes.join('animation:csspseudoanimations 1ms infinite;'), '}'].join('');
      testStyles(styles, function (elem) {
        result = computedStyle(elem, ':before', 'font-size') === '10px';
      });
      return result;
    });
    /*!
    {
      "name": "CSS Transitions",
      "property": "csstransitions",
      "caniuse": "css-transitions",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('csstransitions', testAllProps('transition', 'all', true));
    /*!
    {
      "name": "CSS Generated Content Transitions",
      "property": "csspseudotransitions",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('csspseudotransitions', function () {
      var result = false;

      if (!Modernizr.csstransitions) {
        return result;
      }

      var styles = '#modernizr:before { content:" "; font-size:5px;' + prefixes.join('transition:0s 100s;') + '}' + '#modernizr.trigger:before { font-size:10px; }';
      testStyles(styles, function (elem) {
        // Force rendering of the element's styles so that the transition will trigger
        computedStyle(elem, ':before', 'font-size');
        elem.className += 'trigger';
        result = computedStyle(elem, ':before', 'font-size') === '5px';
      });
      return result;
    });
    /*!
    {
      "name": "CSS Reflections",
      "caniuse": "css-reflections",
      "property": "cssreflections",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('cssreflections', testAllProps('boxReflect', 'above', true));
    /*!
    {
      "name": "CSS Regions",
      "caniuse": "css-regions",
      "authors": ["Mihai Balan"],
      "property": "regions",
      "tags": ["css"],
      "builderAliases": ["css_regions"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-regions/"
      }]
    }
    !*/
    // We start with a CSS parser test then we check page geometry to see if it's affected by regions
    // Later we might be able to retire the second part, as WebKit builds with the false positives die out

    Modernizr.addTest('regions', function () {
      if (isSVG) {
        // css regions don't work inside of SVG elements. Rather than update the
        // below test to work in an SVG context, just exit early to save bytes
        return false;
      }
      /* Get the 'flowFrom' property name available in the browser. Either default or vendor prefixed.
         If the property name can't be found we'll get Boolean 'false' and fail quickly */


      var flowFromProperty = prefixed('flowFrom');
      var flowIntoProperty = prefixed('flowInto');
      var result = false;

      if (!flowFromProperty || !flowIntoProperty) {
        return result;
      }
      /* If CSS parsing is there, try to determine if regions actually work. */


      var iframeContainer = createElement('iframe');
      var container = createElement('div');
      var content = createElement('div');
      var region = createElement('div');
      /* we create a random, unlikely to be generated flow number to make sure we don't
         clash with anything more vanilla, like 'flow', or 'article', or 'f1' */

      var flowName = 'modernizr_flow_for_regions_check';
      /* First create a div with two adjacent divs inside it. The first will be the
         content, the second will be the region. To be able to distinguish between the two,
         we'll give the region a particular padding */

      content.innerText = 'M';
      container.style.cssText = 'top: 150px; left: 150px; padding: 0px;';
      region.style.cssText = 'width: 50px; height: 50px; padding: 42px;';
      region.style[flowFromProperty] = flowName;
      container.appendChild(content);
      container.appendChild(region);
      docElement.appendChild(container);
      /* Now compute the bounding client rect, before and after attempting to flow the
         content div in the region div. If regions are enabled, the after bounding rect
         should reflect the padding of the region div.*/

      var flowedRect, delta;
      var plainRect = content.getBoundingClientRect();
      content.style[flowIntoProperty] = flowName;
      flowedRect = content.getBoundingClientRect();
      delta = parseInt(flowedRect.left - plainRect.left, 10);
      docElement.removeChild(container);

      if (delta === 42) {
        result = true;
      } else {
        /* IE only allows for the content to come from iframes. This has the
         * side effect of automatic collapsing of iframes once they get the flow-into
         * property set. checking for a change on the height allows us to detect this
         * in a sync way, without having to wait for a frame to load */
        docElement.appendChild(iframeContainer);
        plainRect = iframeContainer.getBoundingClientRect();
        iframeContainer.style[flowIntoProperty] = flowName;
        flowedRect = iframeContainer.getBoundingClientRect();

        if (plainRect.height > 0 && plainRect.height !== flowedRect.height && flowedRect.height === 0) {
          result = true;
        }
      }

      content = region = container = iframeContainer = undefined;
      return result;
    });
    /*!
    {
      "name": "CSS Font rem Units",
      "caniuse": "rem",
      "authors": ["nsfmc"],
      "property": "cssremunit",
      "tags": ["css"],
      "builderAliases": ["css_remunit"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-values/#relative0"
      }, {
        "name": "Font Size with rem by Jonathan Snook",
        "href": "https://snook.ca/archives/html_and_css/font-size-with-rem"
      }]
    }
    !*/
    // "The 'rem' unit ('root em') is relative to the computed
    // value of the 'font-size' value of the root element."
    // you can test by checking if the prop was ditched

    Modernizr.addTest('cssremunit', function () {
      var style = createElement('a').style;

      try {
        style.fontSize = '3rem';
      } catch (e) {}

      return /rem/.test(style.fontSize);
    });
    /*!
    {
      "name": "CSS UI Resize",
      "property": "cssresize",
      "caniuse": "css-resize",
      "tags": ["css"],
      "builderAliases": ["css_resize"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-ui/#resize"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/CSS/resize"
      }]
    }
    !*/

    /* DOC
    Test for CSS 3 UI "resize" property
    */

    Modernizr.addTest('cssresize', testAllProps('resize', 'both', true));
    /*!
    {
      "name": "CSS rgba",
      "caniuse": "css3-colors",
      "property": "rgba",
      "tags": ["css"],
      "notes": [{
        "name": "CSSTricks Tutorial",
        "href": "https://css-tricks.com/rgba-browser-support/"
      }]
    }
    !*/

    Modernizr.addTest('rgba', function () {
      var style = createElement('a').style;
      style.cssText = 'background-color:rgba(150,255,150,.5)';
      return ('' + style.backgroundColor).indexOf('rgba') > -1;
    });
    /*!
    {
      "name": "CSS Stylable Scrollbars",
      "property": "cssscrollbar",
      "tags": ["css"],
      "builderAliases": ["css_scrollbars"]
    }
    !*/

    testStyles('#modernizr{overflow: scroll; width: 40px; height: 40px; }#' + prefixes.join('scrollbar{width:10px}' + ' #modernizr::').split('#').slice(1).join('#') + 'scrollbar{width:10px}', function (node) {
      Modernizr.addTest('cssscrollbar', 'scrollWidth' in node && node.scrollWidth === 30);
    });
    /*!
    {
      "name": "Scroll Snap Points",
      "property": "scrollsnappoints",
      "caniuse": "css-snappoints",
      "notes": [{
        "name": "Setting native-like scrolling offsets in CSS with Scrolling Snap Points",
        "href": "http://generatedcontent.org/post/66817675443/setting-native-like-scrolling-offsets-in-css-with"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap_Points"
      }],
      "polyfills": ["scrollsnap"]
    }
    !*/

    /* DOC
    Detects support for CSS Snap Points
    */

    Modernizr.addTest('scrollsnappoints', testAllProps('scrollSnapType'));
    /*!
    {
      "name": "CSS Shapes",
      "property": "shapes",
      "tags": ["css"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css-shapes"
      }, {
        "name": "Examples from Adobe",
        "href": "https://web.archive.org/web/20171230010236/http://webplatform.adobe.com:80/shapes"
      }, {
        "name": "Examples from CSS-Tricks",
        "href": "https://css-tricks.com/examples/ShapesOfCSS/"
      }]
    }
    !*/

    Modernizr.addTest('shapes', testAllProps('shapeOutside', 'content-box', true));
    /*!
    {
      "name": "CSS general sibling selector",
      "caniuse": "css-sel3",
      "property": "siblinggeneral",
      "tags": ["css"],
      "notes": [{
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/pull/889"
      }]
    }
    !*/

    Modernizr.addTest('siblinggeneral', function () {
      return testStyles('#modernizr div {width:100px} #modernizr div ~ div {width:200px;display:block}', function (elem) {
        return elem.lastChild.offsetWidth === 200;
      }, 2);
    });
    /*!
    {
      "name": "CSS Subpixel Fonts",
      "property": "subpixelfont",
      "tags": ["css"],
      "builderAliases": ["css_subpixelfont"],
      "authors": ["@derSchepp", "@gerritvanaaken", "@rodneyrehm", "@yatil", "@ryanseddon"],
      "notes": [{
        "name": "Origin Test",
        "href": "https://github.com/gerritvanaaken/subpixeldetect"
      }]
    }
    !*/

    /*
     * (to infer if GDI or DirectWrite is used on Windows)
     */

    testStyles('#modernizr{position: absolute; top: -10em; visibility:hidden; font: normal 10px arial;}#subpixel{float: left; font-size: 33.3333%;}', function (elem) {
      var subpixel = elem.firstChild;
      subpixel.innerHTML = 'This is a text written in Arial';
      Modernizr.addTest('subpixelfont', computedStyle(subpixel, null, 'width') !== '44px');
    }, 1, ['subpixel']);
    /*!
    {
      "name": "CSS :target pseudo-class",
      "caniuse": "css-sel3",
      "property": "target",
      "tags": ["css"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/:target"
      }],
      "authors": ["@zachleat"],
      "warnings": ["Opera Mini supports :target but doesn't update the hash for anchor links."]
    }
    !*/

    /* DOC
    Detects support for the ':target' CSS pseudo-class.
    */
    // querySelector

    Modernizr.addTest('target', function () {
      var doc = window.document;

      if (!('querySelectorAll' in doc)) {
        return false;
      }

      try {
        doc.querySelectorAll(':target');
        return true;
      } catch (e) {
        return false;
      }
    });
    /*!
    {
      "name": "CSS text-align-last",
      "property": "textalignlast",
      "caniuse": "css-text-align-last",
      "tags": ["css"],
      "knownBugs": ["IE does not support the 'start' or 'end' values."],
      "notes": [{
        "name": "Quirksmode",
        "href": "https://www.quirksmode.org/css/text/textalignlast.html"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/text-align-last"
      }]
    }
    !*/

    Modernizr.addTest('textalignlast', testAllProps('textAlignLast'));
    /*!
    {
      "name": "CSS textshadow",
      "property": "textshadow",
      "caniuse": "css-textshadow",
      "tags": ["css"],
      "knownBugs": ["FF3.0 will false positive on this test"]
    }
    !*/

    Modernizr.addTest('textshadow', testProp('textShadow', '1px 1px'));
    /*!
    {
      "name": "CSS Transforms",
      "property": "csstransforms",
      "caniuse": "transforms2d",
      "tags": ["css"]
    }
    !*/

    Modernizr.addTest('csstransforms', function () {
      // Android < 3.0 is buggy, so we sniff and reject it
      // https://github.com/Modernizr/Modernizr/issues/903
      return navigator.userAgent.indexOf('Android 2.') === -1 && testAllProps('transform', 'scale(1)', true);
    });
    /*!
    {
      "name": "CSS Transforms Level 2",
      "property": "csstransformslevel2",
      "authors": ["rupl"],
      "tags": ["css"],
      "notes": [{
        "name": "CSSWG Draft Spec",
        "href": "https://drafts.csswg.org/css-transforms-2/"
      }]
    }
    !*/

    Modernizr.addTest('csstransformslevel2', function () {
      return testAllProps('translate', '45px', true);
    });
    /*!
    {
      "name": "CSS Transforms 3D",
      "property": "csstransforms3d",
      "caniuse": "transforms3d",
      "tags": ["css"],
      "warnings": [
        "Chrome may occasionally fail this test on some systems; more info: https://bugs.chromium.org/p/chromium/issues/detail?id=129004"
      ]
    }
    !*/

    Modernizr.addTest('csstransforms3d', function () {
      return !!testAllProps('perspective', '1px', true);
    });
    /*!
    {
      "name": "CSS Transform Style preserve-3d",
      "property": "preserve3d",
      "authors": ["denyskoch", "aFarkas"],
      "tags": ["css"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/transform-style"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/1748"
      }]
    }
    !*/

    /* DOC
    Detects support for `transform-style: preserve-3d`, for getting a proper 3D perspective on elements.
    */

    Modernizr.addTest('preserve3d', function () {
      var outerAnchor, innerAnchor;
      var CSS = window.CSS;
      var result = false;

      if (CSS && CSS.supports && CSS.supports('(transform-style: preserve-3d)')) {
        return true;
      }

      outerAnchor = createElement('a');
      innerAnchor = createElement('a');
      outerAnchor.style.cssText = 'display: block; transform-style: preserve-3d; transform-origin: right; transform: rotateY(40deg);';
      innerAnchor.style.cssText = 'display: block; width: 9px; height: 1px; background: #000; transform-origin: right; transform: rotateY(40deg);';
      outerAnchor.appendChild(innerAnchor);
      docElement.appendChild(outerAnchor);
      result = innerAnchor.getBoundingClientRect();
      docElement.removeChild(outerAnchor);
      result = result.width && result.width < 4;
      return result;
    });
    /*!
    {
      "name": "CSS user-select",
      "property": "userselect",
      "caniuse": "user-select-none",
      "authors": ["ryan seddon"],
      "tags": ["css"],
      "builderAliases": ["css_userselect"],
      "notes": [{
        "name": "Related Modernizr Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/250"
      }]
    }
    !*/
    //https://github.com/Modernizr/Modernizr/issues/250

    Modernizr.addTest('userselect', testAllProps('userSelect', 'none', true));
    /*!
    {
      "name": "CSS :valid pseudo-class",
      "property": "cssvalid",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/CSS/:valid"
      }]
    }
    !*/

    /* DOC
      Detects support for the ':valid' CSS pseudo-class.
    */

    Modernizr.addTest('cssvalid', function () {
      return testStyles('#modernizr input{height:0;border:0;padding:0;margin:0;width:10px} #modernizr input:valid{width:50px}', function (elem) {
        var input = createElement('input');
        elem.appendChild(input);
        return input.clientWidth > 10;
      });
    });
    /*!
    {
      "name": "CSS vh unit",
      "property": "cssvhunit",
      "caniuse": "viewport-units",
      "tags": ["css"],
      "builderAliases": ["css_vhunit"],
      "notes": [{
        "name": "Related Modernizr Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/572"
      }, {
        "name": "Similar JSFiddle",
        "href": "https://jsfiddle.net/FWeinb/etnYC/"
      }]
    }
    !*/

    testStyles('#modernizr { height: 50vh; max-height: 10px; }', function (elem) {
      var compStyle = parseInt(computedStyle(elem, null, 'height'), 10);
      Modernizr.addTest('cssvhunit', compStyle === 10);
    });
    /**
     * roundedEquals takes two integers and checks if the first is within 1 of the second
     *
     * @access private
     * @function roundedEquals
     * @param {number} a - first integer
     * @param {number} b - second integer
     * @returns {boolean} true if the first integer is within 1 of the second, false otherwise
     */

    function roundedEquals(a, b) {
      return a - 1 === b || a === b || a + 1 === b;
    }

    ;
    /*!
    {
      "name": "CSS vmax unit",
      "property": "cssvmaxunit",
      "caniuse": "viewport-units",
      "tags": ["css"],
      "builderAliases": ["css_vmaxunit"],
      "notes": [{
        "name": "Related Modernizr Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/572"
      }, {
        "name": "JSFiddle Example",
        "href": "https://jsfiddle.net/glsee/JDsWQ/4/"
      }]
    }
    !*/

    testStyles('#modernizr1{width: 50vmax}#modernizr2{width:50px;height:50px;overflow:scroll}#modernizr3{position:fixed;top:0;left:0;bottom:0;right:0}', function (node) {
      var elem = node.childNodes[2];
      var scroller = node.childNodes[1];
      var fullSizeElem = node.childNodes[0];
      var scrollbarWidth = parseInt((scroller.offsetWidth - scroller.clientWidth) / 2, 10);
      var one_vw = fullSizeElem.clientWidth / 100;
      var one_vh = fullSizeElem.clientHeight / 100;
      var expectedWidth = parseInt(Math.max(one_vw, one_vh) * 50, 10);
      var compWidth = parseInt(computedStyle(elem, null, 'width'), 10);
      Modernizr.addTest('cssvmaxunit', roundedEquals(expectedWidth, compWidth) || roundedEquals(expectedWidth, compWidth - scrollbarWidth));
    }, 3);
    /*!
    {
      "name": "CSS vmin unit",
      "property": "cssvminunit",
      "caniuse": "viewport-units",
      "tags": ["css"],
      "builderAliases": ["css_vminunit"],
      "notes": [{
        "name": "Related Modernizr Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/572"
      }, {
        "name": "JSFiddle Example",
        "href": "https://jsfiddle.net/glsee/JRmdq/8/"
      }]
    }
    !*/

    testStyles('#modernizr1{width: 50vm;width:50vmin}#modernizr2{width:50px;height:50px;overflow:scroll}#modernizr3{position:fixed;top:0;left:0;bottom:0;right:0}', function (node) {
      var elem = node.childNodes[2];
      var scroller = node.childNodes[1];
      var fullSizeElem = node.childNodes[0];
      var scrollbarWidth = parseInt((scroller.offsetWidth - scroller.clientWidth) / 2, 10);
      var one_vw = fullSizeElem.clientWidth / 100;
      var one_vh = fullSizeElem.clientHeight / 100;
      var expectedWidth = parseInt(Math.min(one_vw, one_vh) * 50, 10);
      var compWidth = parseInt(computedStyle(elem, null, 'width'), 10);
      Modernizr.addTest('cssvminunit', roundedEquals(expectedWidth, compWidth) || roundedEquals(expectedWidth, compWidth - scrollbarWidth));
    }, 3);
    /*!
    {
      "name": "CSS vw unit",
      "property": "cssvwunit",
      "caniuse": "viewport-units",
      "tags": ["css"],
      "builderAliases": ["css_vwunit"],
      "notes": [{
        "name": "Related Modernizr Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/572"
      }, {
        "name": "JSFiddle Example",
        "href": "https://jsfiddle.net/FWeinb/etnYC/"
      }]
    }
    !*/

    testStyles('#modernizr { width: 50vw; }', function (elem) {
      var width = parseInt(window.innerWidth / 2, 10);
      var compStyle = parseInt(computedStyle(elem, null, 'width'), 10);
      Modernizr.addTest('cssvwunit', roundedEquals(compStyle, width));
    });
    /*!
    {
      "name": "will-change",
      "property": "willchange",
      "caniuse": "will-change",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://drafts.csswg.org/css-will-change/"
      }]
    }
    !*/

    /* DOC
    Detects support for the `will-change` css property, which formally signals to the
    browser that an element will be animating.
    */

    Modernizr.addTest('willchange', 'willChange' in docElement.style);
    /*!
    {
      "name": "CSS wrap-flow",
      "property": "wrapflow",
      "tags": ["css"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/css3-exclusions"
      }, {
        "name": "Example by Louie Rootfield",
        "href": "https://webdesign.tutsplus.com/tutorials/css-exclusions--cms-28087"
      }]
    }
    !*/

    Modernizr.addTest('wrapflow', function () {
      var prefixedProperty = prefixed('wrapFlow');

      if (!prefixedProperty || isSVG) {
        return false;
      }

      var wrapFlowProperty = prefixedProperty.replace(/([A-Z])/g, function (str, m1) {
        return '-' + m1.toLowerCase();
      }).replace(/^ms-/, '-ms-');
      /* If the CSS parsing is there we need to determine if wrap-flow actually works to avoid false positive cases, e.g. the browser parses
         the property, but it hasn't got the implementation for the functionality yet. */

      var container = createElement('div');
      var exclusion = createElement('div');
      var content = createElement('span');
      /* First we create a div with two adjacent divs inside it. The first div will be the content, the second div will be the exclusion area.
         We use the "wrap-flow: end" property to test the actual behavior. (https://drafts.csswg.org/css-exclusions-1/#wrap-flow-property)
         The wrap-flow property is applied to the exclusion area what has a 50px left offset and a 100px width.
         If the wrap-flow property is working correctly then the content should start after the exclusion area, so the content's left offset should be 150px. */

      exclusion.style.cssText = 'position: absolute; left: 50px; width: 100px; height: 20px;' + wrapFlowProperty + ':end;';
      content.innerText = 'X';
      container.appendChild(exclusion);
      container.appendChild(content);
      docElement.appendChild(container);
      var leftOffset = content.offsetLeft;
      docElement.removeChild(container);
      exclusion = content = container = undefined;
      return leftOffset === 150;
    });
    /*!
    {
      "name": "classList",
      "caniuse": "classlist",
      "property": "classlist",
      "tags": ["dom"],
      "builderAliases": ["dataview_api"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/DOM/element.classList"
      }]
    }
    !*/

    Modernizr.addTest('classlist', 'classList' in docElement);
    /*!
    {
      "name": "createElement with Attributes",
      "property": ["createelementattrs", "createelement-attrs"],
      "tags": ["dom"],
      "builderAliases": ["dom_createElement_attrs"],
      "authors": ["James A. Rosen"],
      "notes": [{
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/258"
      }]
    }
    !*/

    Modernizr.addTest('createelementattrs', function () {
      try {
        return createElement('<input name="test" />').getAttribute('name') === 'test';
      } catch (e) {
        return false;
      }
    }, {
      aliases: ['createelement-attrs']
    });
    /*!
    {
      "name": "dataset API",
      "caniuse": "dataset",
      "property": "dataset",
      "tags": ["dom"],
      "builderAliases": ["dom_dataset"],
      "authors": ["@phiggins42"]
    }
    !*/
    // dataset API for data-* attributes

    Modernizr.addTest('dataset', function () {
      var n = createElement('div');
      n.setAttribute('data-a-b', 'c');
      return !!(n.dataset && n.dataset.aB === 'c');
    });
    /*!
    {
      "name": "Document Fragment",
      "property": "documentfragment",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/REC-DOM-Level-1/level-one-core.html#ID-B63ED1A3"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment"
      }, {
        "name": "QuirksMode Compatibility Tables",
        "href": "https://www.quirksmode.org/m/w3c_core.html#t112"
      }],
      "authors": ["Ron Waldon (@jokeyrhyme)"],
      "knownBugs": ["false-positive on Blackberry 9500, see QuirksMode note"],
      "tags": ["dom"]
    }
    !*/

    /* DOC
    Append multiple elements to the DOM within a single insertion.
    */

    Modernizr.addTest('documentfragment', function () {
      return 'createDocumentFragment' in document && 'appendChild' in docElement;
    });
    /*!
    {
      "name": "[hidden] Attribute",
      "property": "hidden",
      "tags": ["dom"],
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/dev/interaction.html#the-hidden-attribute"
      }, {
        "name": "original implementation of detect code",
        "href": "https://github.com/aFarkas/html5shiv/blob/bf4fcc4/src/html5shiv.js#L38"
      }],
      "polyfills": ["html5shiv"],
      "authors": ["Ron Waldon (@jokeyrhyme)"]
    }
    !*/

    /* DOC
    Does the browser support the HTML5 [hidden] attribute?
    */

    Modernizr.addTest('hidden', 'hidden' in createElement('a'));
    /*!
    {
      "name": "microdata",
      "property": "microdata",
      "tags": ["dom"],
      "builderAliases": ["dom_microdata"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/microdata/"
      }]
    }
    !*/

    Modernizr.addTest('microdata', 'getItems' in document);
    /*!
    {
      "name": "DOM4 MutationObserver",
      "property": "mutationobserver",
      "caniuse": "mutationobserver",
      "tags": ["dom"],
      "authors": ["Karel Sedláček (@ksdlck)"],
      "polyfills": ["mutationobservers"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver"
      }]
    }
    !*/

    /* DOC
    Determines if DOM4 MutationObserver support is available.
    */

    Modernizr.addTest('mutationobserver', !!window.MutationObserver || !!window.WebKitMutationObserver);
    /*!
    {
      "property": "passiveeventlisteners",
      "caniuse": "passive-event-listener",
      "tags": ["dom"],
      "authors": ["Rick Byers"],
      "name": "Passive event listeners",
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://dom.spec.whatwg.org/#dom-addeventlisteneroptions-passive"
      }, {
        "name": "WICG explainer",
        "href": "https://github.com/WICG/EventListenerOptions/blob/gh-pages/explainer.md"
      }]
    }
    !*/

    /* DOC
    Detects support for the passive option to addEventListener.
    */

    Modernizr.addTest('passiveeventlisteners', function () {
      var supportsPassiveOption = false;

      try {
        var opts = Object.defineProperty({}, 'passive', {
          get: function get() {
            supportsPassiveOption = true;
            return;
          }
        });

        var noop = function noop() {};

        window.addEventListener('testPassiveEventSupport', noop, opts);
        window.removeEventListener('testPassiveEventSupport', noop, opts);
      } catch (e) {}

      return supportsPassiveOption;
    });
    /*!
    {
      "name": "Orientation and Motion Events",
      "property": ["devicemotion", "deviceorientation"],
      "caniuse": "deviceorientation",
      "notes": [{
        "name": "W3C Editor's Draft Spec",
        "href": "https://w3c.github.io/deviceorientation/"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/Detecting_device_orientation"
      }],
      "authors": ["Shi Chuan"],
      "tags": ["event"],
      "builderAliases": ["event_deviceorientation_motion"]
    }
    !*/

    /* DOC
    Part of Device Access aspect of HTML5, same category as geolocation.
    
    `devicemotion` tests for Device Motion Event support, returns boolean value true/false.
    
    `deviceorientation` tests for Device Orientation Event support, returns boolean value true/false
    */

    Modernizr.addTest('devicemotion', 'DeviceMotionEvent' in window);
    Modernizr.addTest('deviceorientation', 'DeviceOrientationEvent' in window);
    /*!
    {
      "name": "onInput Event",
      "property": "oninput",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers.oninput"
      }, {
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/multipage/input.html#common-input-element-attributes"
      }, {
        "name": "Related Github Issue",
        "href": "https://github.com/Modernizr/Modernizr/issues/210"
      }],
      "authors": ["Patrick Kettner"],
      "tags": ["event"]
    }
    !*/

    /* DOC
    `oninput` tests if the browser is able to detect the input event
    */

    Modernizr.addTest('oninput', function () {
      var input = createElement('input');
      var supportsOnInput;
      input.setAttribute('oninput', 'return');
      input.style.cssText = 'position:fixed;top:0;';

      if (hasEvent('oninput', docElement) || typeof input.oninput === 'function') {
        return true;
      } // IE doesn't support onInput, so we wrap up the non IE APIs
      // (createEvent, addEventListener) in a try catch, rather than test for
      // their trident equivalent.


      try {
        // Older Firefox didn't map oninput attribute to oninput property
        var testEvent = document.createEvent('KeyboardEvent');
        supportsOnInput = false;

        var handler = function handler(e) {
          supportsOnInput = true;
          e.preventDefault();
          e.stopPropagation();
        };

        testEvent.initKeyEvent('keypress', true, true, window, false, false, false, false, 0, 'e'.charCodeAt(0));
        docElement.appendChild(input);
        input.addEventListener('input', handler, false);
        input.focus();
        input.dispatchEvent(testEvent);
        input.removeEventListener('input', handler, false);
        docElement.removeChild(input);
      } catch (e) {
        supportsOnInput = false;
      }

      return supportsOnInput;
    });
    /*!
    {
      "name": "Event Listener",
      "property": "eventlistener",
      "caniuse": "addeventlistener",
      "authors": ["Andrew Betts (@triblondon)"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/DOM-Level-2-Events/events.html#Events-Registration-interfaces"
      }],
      "polyfills": ["eventlistener"]
    }
    !*/

    /* DOC
    Detects native support for addEventListener
    */

    Modernizr.addTest('eventlistener', 'addEventListener' in window);
    /*!
    {
      "name": "EXIF Orientation",
      "property": "exiforientation",
      "tags": ["image"],
      "builderAliases": ["exif_orientation"],
      "async": true,
      "authors": ["Paul Sayre"],
      "notes": [{
        "name": "Article by Dave Perrett",
        "href": "https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/"
      }, {
        "name": "Article by Calvin Hass",
        "href": "https://www.impulseadventure.com/photo/exif-orientation.html"
      }]
    }
    !*/

    /* DOC
    Detects support for EXIF Orientation in JPEG images.
    
    iOS looks at the EXIF Orientation flag in JPEGs and rotates the image accordingly. Most desktop browsers just ignore this data.
    */
    // Bug trackers:
    //    bugzil.la/298619 (unimplemented)
    //    crbug.com/56845 (looks incomplete)
    //    webk.it/19688 (available upstream but its up all ports to turn on individually)

    Modernizr.addAsyncTest(function () {
      var img = new Image();

      img.onerror = function () {
        addTest('exiforientation', false, {
          aliases: ['exif-orientation']
        });
      };

      img.onload = function () {
        addTest('exiforientation', img.width !== 2, {
          aliases: ['exif-orientation']
        });
      }; // There may be a way to shrink this more, it's a 1x2 white jpg with the orientation flag set to 6


      img.src = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAASUkqAAgAAAABABIBAwABAAAABgASAAAAAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+/iiiigD/2Q==';
    });
    /*!
    {
      "name": "input[capture] Attribute",
      "property": "capture",
      "tags": ["video", "image", "audio", "media", "attribute"],
      "notes": [{
        "name": "W3C Draft Spec",
        "href": "https://www.w3.org/TR/html-media-capture/"
      }]
    }
    !*/

    /* DOC
    When used on an `<input>`, this attribute signifies that the resource it takes should be generated via device's camera, camcorder, sound recorder.
    */
    // testing for capture attribute in inputs

    Modernizr.addTest('capture', 'capture' in createElement('input'));
    /*!
    {
      "name": "input[file] Attribute",
      "property": "fileinput",
      "caniuse": "forms",
      "tags": ["file", "forms", "input"],
      "builderAliases": ["forms_fileinput"]
    }
    !*/

    /* DOC
    Detects whether input type="file" is available on the platform
    
    E.g. iOS < 6, some android versions and embedded Chrome WebViews don't support this
    */

    Modernizr.addTest('fileinput', function () {
      var ua = navigator.userAgent;

      if (ua.match(/(Android (1.0|1.1|1.5|1.6|2.0|2.1))|(Windows Phone (OS 7|8.0))|(XBLWP)|(ZuneWP)|(w(eb)?OSBrowser)|(webOS)|(Kindle\/(1.0|2.0|2.5|3.0))/) || ua.match(/\swv\).+(chrome)\/([\w\.]+)/i)) {
        return false;
      }

      var elem = createElement('input');
      elem.type = 'file';
      return !elem.disabled;
    });
    /**
     * List of JavaScript DOM values used for tests including a NON-prefix
     *
     * @memberOf Modernizr
     * @name Modernizr._domPrefixesAll
     * @optionName Modernizr._domPrefixesAll
     * @optionProp domPrefixesAll
     * @access public
     * @example
     *
     * Modernizr._domPrefixesAll is exactly the same as [_domPrefixes](#modernizr-_domPrefixes), but also
     * adds an empty string in the array to test for a non-prefixed value
     *
     * ```js
     * Modernizr._domPrefixesAll === [ "", "Moz", "O", "ms", "Webkit" ];
     * ```
     */

    var domPrefixesAll = [''].concat(domPrefixes);
    ModernizrProto._domPrefixesAll = domPrefixesAll;
    /*!
    {
      "name": "input[directory] Attribute",
      "property": "directory",
      "authors": ["silverwind"],
      "tags": ["file", "input", "attribute"]
    }
    !*/

    /* DOC
    When used on an `<input type="file">`, the `directory` attribute instructs
    the user agent to present a directory selection dialog instead of the usual
    file selection dialog.
    */

    Modernizr.addTest('fileinputdirectory', function () {
      var elem = createElement('input'),
          dir = 'directory';
      elem.type = 'file';

      for (var i = 0, len = domPrefixesAll.length; i < len; i++) {
        if (domPrefixesAll[i] + dir in elem) {
          return true;
        }
      }

      return false;
    });
    /*!
    {
      "name": "input[form] Attribute",
      "property": "formattribute",
      "tags": ["attribute", "forms", "input"],
      "builderAliases": ["forms_formattribute"]
    }
    !*/

    /* DOC
    Detects whether input form="form_id" is available on the platform
    E.g. IE 10 (and below), don't support this
    */

    Modernizr.addTest('formattribute', function () {
      var form = createElement('form');
      var input = createElement('input');
      var div = createElement('div');
      var id = 'formtest' + new Date().getTime();
      var attr;
      var bool = false;
      form.id = id; //IE6/7 confuses the form idl attribute and the form content attribute, so we use document.createAttribute

      try {
        input.setAttribute('form', id);
      } catch (e) {
        if (document.createAttribute) {
          attr = document.createAttribute('form');
          attr.nodeValue = id;
          input.setAttributeNode(attr);
        }
      }

      div.appendChild(form);
      div.appendChild(input);
      docElement.appendChild(div);
      bool = form.elements && form.elements.length === 1 && input.form === form;
      div.parentNode.removeChild(div);
      return bool;
    });
    /*!
    {
      "name": "placeholder attribute",
      "property": "placeholder",
      "tags": ["forms", "attribute"],
      "builderAliases": ["forms_placeholder"]
    }
    !*/

    /* DOC
    Tests for placeholder attribute in inputs and textareas
    */

    Modernizr.addTest('placeholder', 'placeholder' in createElement('input') && 'placeholder' in createElement('textarea'));
    /*!
    {
      "name": "form#requestAutocomplete()",
      "property": "requestautocomplete",
      "tags": ["form", "forms", "requestAutocomplete", "payments"],
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://wiki.whatwg.org/wiki/RequestAutocomplete"
      }]
    }
    !*/

    /* DOC
    When used with input[autocomplete] to annotate a form, form.requestAutocomplete() shows a dialog in Chrome that speeds up
    checkout flows (payments specific for now).
    */

    Modernizr.addTest('requestautocomplete', !!prefixed('requestAutocomplete', createElement('form')));
    /*!
    {
      "name": "Form Validation",
      "property": "formvalidation",
      "tags": ["forms", "validation", "attribute"],
      "builderAliases": ["forms_validation"]
    }
    !*/

    /* DOC
    This implementation only tests support for interactive form validation.
    To check validation for a specific type or a specific other constraint,
    the test can be combined:
    
    - `Modernizr.inputtypes.number && Modernizr.formvalidation` (browser supports rangeOverflow, typeMismatch etc. for type=number)
    - `Modernizr.input.required && Modernizr.formvalidation` (browser supports valueMissing)
    */

    Modernizr.addTest('formvalidation', function () {
      var form = createElement('form');

      if (!('checkValidity' in form) || !('addEventListener' in form)) {
        return false;
      }

      if ('reportValidity' in form) {
        return true;
      }

      var invalidFired = false;
      var input;
      Modernizr.formvalidationapi = true; // Prevent form from being submitted

      form.addEventListener('submit', function (e) {
        // Old Presto based Opera does not validate form, if submit is prevented
        // although Opera Mini servers use newer Presto.
        if (!window.opera || window.operamini) {
          e.preventDefault();
        }

        e.stopPropagation();
      }, false); // Calling form.submit() doesn't trigger interactive validation,
      // use a submit button instead
      //older opera browsers need a name attribute

      form.innerHTML = '<input name="modTest" required="required" /><button></button>';
      testStyles('#modernizr form{position:absolute;top:-99999em}', function (node) {
        node.appendChild(form);
        input = form.getElementsByTagName('input')[0]; // Record whether "invalid" event is fired

        input.addEventListener('invalid', function (e) {
          invalidFired = true;
          e.preventDefault();
          e.stopPropagation();
        }, false); //Opera does not fully support the validationMessage property

        Modernizr.formvalidationmessage = !!input.validationMessage; // Submit form by clicking submit button

        form.getElementsByTagName('button')[0].click();
      });
      return invalidFired;
    });
    /**
     * since we have a fairly large number of input tests that don't mutate the input
     * we create a single element that can be shared with all of those tests for a
     * minor perf boost
     *
     * @access private
     * @returns {HTMLInputElement}
     */

    var inputElem = createElement('input');
    /*!
    {
      "name": "Form input types",
      "property": "inputtypes",
      "caniuse": "forms",
      "tags": ["forms"],
      "authors": ["Mike Taylor"],
      "polyfills": [
        "jquerytools",
        "webshims",
        "h5f",
        "webforms2",
        "nwxforms",
        "fdslider",
        "html5slider",
        "galleryhtml5forms",
        "jscolor",
        "html5formshim",
        "selectedoptionsjs",
        "formvalidationjs"
      ]
    }
    !*/

    /* DOC
    Detects support for HTML5 form input types and exposes Boolean subproperties with the results:
    
    ```javascript
    Modernizr.inputtypes.color
    Modernizr.inputtypes.date
    Modernizr.inputtypes.datetime
    Modernizr.inputtypes['datetime-local']
    Modernizr.inputtypes.email
    Modernizr.inputtypes.month
    Modernizr.inputtypes.number
    Modernizr.inputtypes.range
    Modernizr.inputtypes.search
    Modernizr.inputtypes.tel
    Modernizr.inputtypes.time
    Modernizr.inputtypes.url
    Modernizr.inputtypes.week
    ```
    */
    // Run through HTML5's new input types to see if the UA understands any.
    //   This is put behind the tests runloop because it doesn't return a
    //   true/false like all the other tests; instead, it returns an object
    //   containing each input type with its corresponding true/false value
    // Big thanks to @miketaylr for the html5 forms expertise. miketaylr.com/

    (function () {
      var props = ['search', 'tel', 'url', 'email', 'datetime', 'date', 'month', 'week', 'time', 'datetime-local', 'number', 'range', 'color'];
      var smile = '1)';
      var inputElemType;
      var defaultView;
      var bool;

      for (var i = 0; i < props.length; i++) {
        inputElem.setAttribute('type', inputElemType = props[i]);
        bool = inputElem.type !== 'text' && 'style' in inputElem; // We first check to see if the type we give it sticks..
        // If the type does, we feed it a textual value, which shouldn't be valid.
        // If the value doesn't stick, we know there's input sanitization which infers a custom UI

        if (bool) {
          inputElem.value = smile;
          inputElem.style.cssText = 'position:absolute;visibility:hidden;';

          if (/^range$/.test(inputElemType) && inputElem.style.WebkitAppearance !== undefined) {
            docElement.appendChild(inputElem);
            defaultView = document.defaultView; // Safari 2-4 allows the smiley as a value, despite making a slider

            bool = defaultView.getComputedStyle && defaultView.getComputedStyle(inputElem, null).WebkitAppearance !== 'textfield' && // Mobile android web browser has false positive, so must
            // check the height to see if the widget is actually there.
            inputElem.offsetHeight !== 0;
            docElement.removeChild(inputElem);
          } else if (/^(search|tel)$/.test(inputElemType)) {// Spec doesn't define any special parsing or detectable UI
            //   behaviors so we pass these through as true
            // Interestingly, opera fails the earlier test, so it doesn't
            //  even make it here.
          } else if (/^(url|email)$/.test(inputElemType)) {
            // Real url and email support comes with prebaked validation.
            bool = inputElem.checkValidity && inputElem.checkValidity() === false;
          } else {
            // If the upgraded input component rejects the :) text, we got a winner
            bool = inputElem.value !== smile;
          }
        }

        Modernizr.addTest('inputtypes.' + inputElemType, !!bool);
      }
    })();
    /*!
    {
      "name": "Fullscreen API",
      "property": "fullscreen",
      "caniuse": "fullscreen",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/API/Fullscreen"
      }],
      "polyfills": ["screenfulljs"],
      "builderAliases": ["fullscreen_api"]
    }
    !*/

    /* DOC
    Detects support for the ability to make the current website take over the user's entire screen
    */
    // github.com/Modernizr/Modernizr/issues/739


    Modernizr.addTest('fullscreen', !!(prefixed('exitFullscreen', document, false) || prefixed('cancelFullScreen', document, false)));
    /*!
    {
      "name": "Hashchange event",
      "property": "hashchange",
      "caniuse": "hashchange",
      "tags": ["history"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onhashchange"
      }],
      "polyfills": [
        "jquery-hashchange",
        "moo-historymanager",
        "jquery-ajaxy",
        "hasher",
        "shistory"
      ]
    }
    !*/

    /* DOC
    Detects support for the `hashchange` event, fired when the current location fragment changes.
    */

    Modernizr.addTest('hashchange', function () {
      if (hasEvent('hashchange', window) === false) {
        return false;
      } // documentMode logic from YUI to filter out IE8 Compat Mode
      //   which false positives.


      return document.documentMode === undefined || document.documentMode > 7;
    });
    /*!
    {
      "name": "Hidden Scrollbar",
      "property": "hiddenscroll",
      "authors": ["Oleg Korsunsky"],
      "tags": ["overlay"],
      "notes": [{
        "name": "Overlay Scrollbar description",
        "href": "https://developer.apple.com/library/mac/releasenotes/MacOSX/WhatsNewInOSX/Articles/MacOSX10_7.html#//apple_ref/doc/uid/TP40010355-SW39"
      }, {
        "name": "Video example of overlay scrollbars",
        "href": "https://gfycat.com/FoolishMeaslyAtlanticsharpnosepuffer"
      }]
    }
    !*/

    /* DOC
    Detects overlay scrollbars (when scrollbars on overflowed blocks are visible). This is found most commonly on mobile and OS X.
    */

    Modernizr.addTest('hiddenscroll', function () {
      return testStyles('#modernizr {width:100px;height:100px;overflow:scroll}', function (elem) {
        return elem.offsetWidth === elem.clientWidth;
      });
    });
    /*!
    {
      "name": "History API",
      "property": "history",
      "caniuse": "history",
      "tags": ["history"],
      "authors": ["Hay Kranen", "Alexander Farkas"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/html51/browsers.html#the-history-interface"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/window.history"
      }],
      "polyfills": ["historyjs", "html5historyapi"]
    }
    !*/

    /* DOC
    Detects support for the History API for manipulating the browser session history.
    */

    Modernizr.addTest('history', function () {
      // Issue #733
      // The stock browser on Android 2.2 & 2.3, and 4.0.x returns positive on history support
      // Unfortunately support is really buggy and there is no clean way to detect
      // these bugs, so we fall back to a user agent sniff :(
      var ua = navigator.userAgent; // Some browsers allow to have empty userAgent.
      // Therefore, we need to check ua before using "indexOf" on it.

      if (!ua) {
        return false;
      } // We only want Android 2 and 4.0, stock browser, and not Chrome which identifies
      // itself as 'Mobile Safari' as well, nor Windows Phone (issue #1471).


      if ((ua.indexOf('Android 2.') !== -1 || ua.indexOf('Android 4.0') !== -1) && ua.indexOf('Mobile Safari') !== -1 && ua.indexOf('Chrome') === -1 && ua.indexOf('Windows Phone') === -1 && // Since all documents on file:// share an origin, the History apis are
      // blocked there as well
      location.protocol !== 'file:') {
        return false;
      } // Return the regular check


      return window.history && 'pushState' in window.history;
    });
    /*!
    {
      "name": "HTML Imports",
      "property": "htmlimports",
      "tags": ["html", "import"],
      "polyfills": ["polymer-htmlimports"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://w3c.github.io/webcomponents/spec/imports/"
      }, {
        "name": "HTML Imports - #include for the web",
        "href": "https://www.html5rocks.com/en/tutorials/webcomponents/imports/"
      }]
    }
    !*/

    /* DOC
    Detects support for HTML import, a feature that is used for loading in Web Components.
     */

    Modernizr.addTest('htmlimports', 'import' in createElement('link'));
    /*!
    {
      "name": "iframe[sandbox] Attribute",
      "property": "sandbox",
      "caniuse": "iframe-sandbox",
      "tags": ["iframe"],
      "builderAliases": ["iframe_sandbox"],
      "notes": [
      {
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/multipage/embedded-content.html#attr-iframe-sandbox"
      }],
      "knownBugs": ["False-positive on Firefox < 29"]
    }
    !*/

    /* DOC
    Test for `sandbox` attribute in iframes.
    */

    Modernizr.addTest('sandbox', 'sandbox' in createElement('iframe'));
    /*!
    {
      "name": "iframe[seamless] Attribute",
      "property": "seamless",
      "tags": ["iframe"],
      "builderAliases": ["iframe_seamless"],
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/multipage/embedded-content.html#attr-iframe-seamless"
      }]
    }
    !*/

    /* DOC
    Test for `seamless` attribute in iframes.
    */

    Modernizr.addTest('seamless', 'seamless' in createElement('iframe'));
    /*!
    {
      "name": "iframe[srcdoc] Attribute",
      "property": "srcdoc",
      "caniuse": "iframe-srcdoc",
      "tags": ["iframe"],
      "builderAliases": ["iframe_srcdoc"],
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://html.spec.whatwg.org/multipage/embedded-content.html#attr-iframe-srcdoc"
      }]
    }
    !*/

    /* DOC
    Test for `srcdoc` attribute in iframes.
    */

    Modernizr.addTest('srcdoc', 'srcdoc' in createElement('iframe'));
    /*!
    {
      "name": "JSON",
      "property": "json",
      "caniuse": "json",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Glossary/JSON"
      }],
      "polyfills": ["json2"]
    }
    !*/

    /* DOC
    Detects native support for JSON handling functions.
    */
    // this will also succeed if you've loaded the JSON2.js polyfill ahead of time
    //   ... but that should be obvious. :)

    Modernizr.addTest('json', 'JSON' in window && 'parse' in JSON && 'stringify' in JSON);
    /*!
    {
      "name": "Hover Media Query",
      "property": "hovermq"
    }
    !*/

    /* DOC
    Detect support for Hover based media queries
    */

    Modernizr.addTest('hovermq', mq('(hover)'));
    /*!
    {
      "name": "Pointer Media Query",
      "property": "pointermq"
    }
    !*/

    /* DOC
    Detect support for Pointer based media queries
    */

    Modernizr.addTest('pointermq', mq('(pointer:coarse),(pointer:fine),(pointer:none)'));
    /*!
    {
      "name": "Notification",
      "property": "notification",
      "caniuse": "notifications",
      "authors": ["Theodoor van Donge", "Hendrik Beskow"],
      "notes": [{
        "name": "HTML5 Rocks Tutorial",
        "href": "https://www.html5rocks.com/en/tutorials/notifications/quick/"
      }, {
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/notifications/"
      }, {
        "name": "Changes in Chrome to Notifications API due to Service Worker Push Notifications",
        "href": "https://developers.google.com/web/updates/2015/05/Notifying-you-of-notificiation-changes"
      }],
      "knownBugs": ["Possibility of false-positive on Chrome for Android if permissions we're granted for a website prior to Chrome 44."],
      "polyfills": ["desktop-notify", "html5-notifications"]
    }
    !*/

    /* DOC
    Detects support for the Notifications API
    */

    Modernizr.addTest('notification', function () {
      if (!window.Notification || !window.Notification.requestPermission) {
        return false;
      } // if permission is already granted, assume support


      if (window.Notification.permission === 'granted') {
        return true;
      }

      try {
        new window.Notification('');
      } catch (e) {
        if (e.name === 'TypeError') {
          return false;
        }
      }

      return true;
    });
    /*!
    {
      "name": "Page Visibility API",
      "property": "pagevisibility",
      "caniuse": "pagevisibility",
      "tags": ["performance"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/DOM/Using_the_Page_Visibility_API"
      }, {
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/2011/WD-page-visibility-20110602/"
      }, {
        "name": "HTML5 Rocks Tutorial",
        "href": "https://www.html5rocks.com/en/tutorials/pagevisibility/intro/"
      }],
      "polyfills": ["visibilityjs", "visiblyjs", "jquery-visibility"]
    }
    !*/

    /* DOC
    Detects support for the Page Visibility API, which can be used to disable unnecessary actions and otherwise improve user experience.
    */

    Modernizr.addTest('pagevisibility', !!prefixed('hidden', document, false));
    /*!
    {
      "name": "Navigation Timing API",
      "property": "performance",
      "caniuse": "nav-timing",
      "tags": ["performance"],
      "authors": ["Scott Murphy (@uxder)"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/navigation-timing/"
      }, {
        "name": "HTML5 Rocks Tutorial",
        "href": "https://www.html5rocks.com/en/tutorials/webperformance/basics/"
      }],
      "polyfills": ["perfnow"]
    }
    !*/

    /* DOC
    Detects support for the Navigation Timing API, for measuring browser and connection performance.
    */

    Modernizr.addTest('performance', !!prefixed('performance', window));
    /*!
    {
      "name": "postMessage",
      "property": "postmessage",
      "caniuse": "x-doc-messaging",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/webmessaging/#crossDocumentMessages"
      }],
      "polyfills": ["easyxdm", "postmessage-jquery"],
      "knownBugs": ["structuredclones - Android 2&3 can not send a structured clone of dates, filelists or regexps"],
      "warnings": ["Some old WebKit versions have bugs. Stick with object, array, number and pixeldata to be safe."]
    }
    !*/

    /* DOC
    Detects support for the `window.postMessage` protocol for cross-document messaging.
    `Modernizr.postmessage.structuredclones` reports if `postMessage` can send objects.
    */

    var bool = true;

    try {
      window.postMessage({
        toString: function toString() {
          bool = false;
        }
      }, '*');
    } catch (e) {}

    Modernizr.addTest('postmessage', new Boolean('postMessage' in window));
    Modernizr.addTest('postmessage.structuredclones', bool);
    /*!
    {
      "name": "Proximity API",
      "property": "proximity",
      "authors": ["Cătălin Mariș"],
      "tags": ["events", "proximity"],
      "caniuse": "proximity",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/Proximity_Events"
      }, {
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/proximity/"
      }]
    }
    !*/

    /* DOC
    Detects support for an API that allows users to get proximity related information from the device's proximity sensor.
    */

    Modernizr.addAsyncTest(function () {
      var timeout;
      var timeoutTime = 300;

      function advertiseSupport() {
        // Clean up after ourselves
        clearTimeout(timeout);
        window.removeEventListener('deviceproximity', advertiseSupport); // Advertise support as the browser supports
        // the API and the device has a proximity sensor

        addTest('proximity', true);
      } // Check if the browser has support for the API


      if ('ondeviceproximity' in window && 'onuserproximity' in window) {
        // Check if the device has a proximity sensor
        // ( devices without such a sensor support the events but
        //   will never fire them resulting in a false positive )
        window.addEventListener('deviceproximity', advertiseSupport); // If the event doesn't fire in a reasonable amount of time,
        // it means that the device doesn't have a proximity sensor,
        // thus, we can advertise the "lack" of support

        timeout = setTimeout(function () {
          window.removeEventListener('deviceproximity', advertiseSupport);
          addTest('proximity', false);
        }, timeoutTime);
      } else {
        addTest('proximity', false);
      }
    });
    /*!
    {
      "name": "QuerySelector",
      "property": "queryselector",
      "caniuse": "queryselector",
      "tags": ["queryselector"],
      "authors": ["Andrew Betts (@triblondon)"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/selectors-api/#queryselectorall"
      }],
      "polyfills": ["css-selector-engine"]
    }
    !*/

    /* DOC
    Detects support for querySelector.
    */

    Modernizr.addTest('queryselector', 'querySelector' in document && 'querySelectorAll' in document);
    /*!
    {
      "name": "requestAnimationFrame",
      "property": "requestanimationframe",
      "aliases": ["raf"],
      "caniuse": "requestanimationframe",
      "tags": ["animation"],
      "authors": ["Addy Osmani"],
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/animation-timing/"
      }],
      "polyfills": ["raf"]
    }
    !*/

    /* DOC
    Detects support for the `window.requestAnimationFrame` API, for offloading animation repainting to the browser for optimized performance.
    */

    Modernizr.addTest('requestanimationframe', !!prefixed('requestAnimationFrame', window), {
      aliases: ['raf']
    });
    /*!
    {
      "name": "Local Storage",
      "property": "localstorage",
      "caniuse": "namevalue-storage",
      "tags": ["storage"],
      "polyfills": [
        "joshuabell-polyfill",
        "cupcake",
        "storagepolyfill",
        "amplifyjs",
        "yui-cacheoffline"
      ]
    }
    !*/
    // In FF4, if disabled, window.localStorage should === null.
    // Normally, we could not test that directly and need to do a
    //   `('localStorage' in window)` test first because otherwise Firefox will
    //   throw bugzil.la/365772 if cookies are disabled
    // Similarly, in Chrome with "Block third-party cookies and site data" enabled,
    // attempting to access `window.sessionStorage` will throw an exception. crbug.com/357625
    // Also in iOS5 Private Browsing mode, attempting to use localStorage.setItem
    // will throw the exception:
    //   QUOTA_EXCEEDED_ERROR DOM Exception 22.
    // Peculiarly, getItem and removeItem calls do not throw.
    // Because we are forced to try/catch this, we'll go aggressive.
    // Just FWIW: IE8 Compat mode supports these features completely:
    //   www.quirksmode.org/dom/html5.html
    // But IE8 doesn't support either with local files

    Modernizr.addTest('localstorage', function () {
      var mod = 'modernizr';

      try {
        localStorage.setItem(mod, mod);
        localStorage.removeItem(mod);
        return true;
      } catch (e) {
        return false;
      }
    });
    /*!
    {
      "name": "Session Storage",
      "property": "sessionstorage",
      "tags": ["storage"],
      "polyfills": ["joshuabell-polyfill", "cupcake", "sessionstorage"]
    }
    !*/
    // Because we are forced to try/catch this, we'll go aggressive.
    // Just FWIW: IE8 Compat mode supports these features completely:
    //   www.quirksmode.org/dom/html5.html
    // But IE8 doesn't support either with local files

    Modernizr.addTest('sessionstorage', function () {
      var mod = 'modernizr';

      try {
        sessionStorage.setItem(mod, mod);
        sessionStorage.removeItem(mod);
        return true;
      } catch (e) {
        return false;
      }
    });
    /*!
    {
      "name": "Web SQL Database",
      "property": "websqldatabase",
      "caniuse": "sql-storage",
      "tags": ["storage"]
    }
    !*/
    // Chrome incognito mode used to throw an exception when using openDatabase
    // It doesn't anymore.

    Modernizr.addTest('websqldatabase', 'openDatabase' in window);
    /*!
    {
      "name": "Touch Events",
      "property": "touchevents",
      "caniuse": "touch",
      "tags": ["media", "attribute"],
      "notes": [{
        "name": "Touch Events spec",
        "href": "https://www.w3.org/TR/2013/WD-touch-events-20130124/"
      }],
      "warnings": [
        "** DEPRECATED see https://github.com/Modernizr/Modernizr/pull/2432 **",
        "Indicates if the browser supports the Touch Events spec, and does not necessarily reflect a touchscreen device"
      ],
      "knownBugs": [
        "False-positive on some configurations of Nokia N900",
        "False-positive on some BlackBerry 6.0 builds – https://github.com/Modernizr/Modernizr/issues/372#issuecomment-3112695"
      ]
    }
    !*/

    /* DOC
    Indicates if the browser supports the W3C Touch Events API.
    
    This *does not* necessarily reflect a touchscreen device:
    
    * Older touchscreen devices only emulate mouse events
    * Modern IE touch devices implement the Pointer Events API instead: use `Modernizr.pointerevents` to detect support for that
    * Some browsers & OS setups may enable touch APIs when no touchscreen is connected
    * Future browsers may implement other event models for touch interactions
    
    See this article: [You Can't Detect A Touchscreen](http://www.stucox.com/blog/you-cant-detect-a-touchscreen/).
    
    It's recommended to bind both mouse and touch/pointer events simultaneously – see [this HTML5 Rocks tutorial](https://www.html5rocks.com/en/mobile/touchandmouse/).
    
    This test will also return `true` for Firefox 4 Multitouch support.
    */
    // Chrome (desktop) used to lie about its support on this, but that has since been rectified: https://bugs.chromium.org/p/chromium/issues/detail?id=36415
    // Chrome also changed its behaviour since v70 and recommends the TouchEvent object for detection: https://www.chromestatus.com/feature/4764225348042752

    Modernizr.addTest('touchevents', function () {
      if ('ontouchstart' in window || window.TouchEvent || window.DocumentTouch && document instanceof DocumentTouch) {
        return true;
      } // include the 'heartz' as a way to have a non matching MQ to help terminate the join
      // https://github.com/Modernizr/Modernizr/issues/1814


      var query = ['(', prefixes.join('touch-enabled),('), 'heartz', ')'].join('');
      return mq(query);
    });
    /*!
    {
      "name": "Unicode characters",
      "property": "unicode",
      "tags": ["encoding"],
      "warnings": [
        "** DEPRECATED see https://github.com/Modernizr/Modernizr/issues/2468 **",
        "positive Unicode support doesn't mean you can use it inside <title>, this seems more related to OS & Language packs"
      ]
    }
    !*/

    /* DOC
    Detects if unicode characters are supported in the current document.
    */

    /**
     * Unicode special character support
     *
     * Detection is made by testing missing glyph box rendering against star character
     * If widths are the same, this "probably" means the browser didn't support the star character and rendered a glyph box instead
     * Just need to ensure the font characters have different widths
     */

    Modernizr.addTest('unicode', function () {
      var bool;
      var missingGlyph = createElement('span');
      var star = createElement('span');
      testStyles('#modernizr{font-family:Arial,sans;font-size:300em;}', function (node) {
        missingGlyph.innerHTML = isSVG ? "\u5987" : '&#5987;';
        star.innerHTML = isSVG ? "\u2606" : '&#9734;';
        node.appendChild(missingGlyph);
        node.appendChild(star);
        bool = 'offsetWidth' in missingGlyph && missingGlyph.offsetWidth !== star.offsetWidth;
      });
      return bool;
    });
    /*!
    {
      "name": "Unicode Range",
      "property": "unicoderange",
      "notes": [{
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/2013/CR-css-fonts-3-20131003/#descdef-unicode-range"
      }, {
        "name": "24 Way article",
        "href": "https://24ways.org/2011/creating-custom-font-stacks-with-unicode-range"
      }]
    }
    !*/

    Modernizr.addTest('unicoderange', function () {
      return testStyles('@font-face{font-family:"unicodeRange";src:local("Arial");unicode-range:U+0020,U+002E}#modernizr span{font-size:20px;display:inline-block;font-family:"unicodeRange",monospace}#modernizr .mono{font-family:monospace}', function (elem) {
        // we use specify a unicode-range of 002E (the `.` glyph,
        // and a monospace font as the fallback. If the first of
        // these test glyphs is a different width than the other
        // the other three (which are all monospace), then we
        // have a winner.
        var testGlyphs = ['.', '.', 'm', 'm'];

        for (var i = 0; i < testGlyphs.length; i++) {
          var elm = createElement('span');
          elm.innerHTML = testGlyphs[i];
          elm.className = i % 2 ? 'mono' : '';
          elem.appendChild(elm);
          testGlyphs[i] = elm.clientWidth;
        }

        return testGlyphs[0] !== testGlyphs[1] && testGlyphs[2] === testGlyphs[3];
      });
    });
    /*!
    {
      "name": "Blob URLs",
      "property": "bloburls",
      "caniuse": "bloburls",
      "notes": [{
        "name": "W3C Working Draft Spec",
        "href": "https://www.w3.org/TR/FileAPI/#creating-revoking"
      }],
      "tags": ["file", "url"],
      "authors": ["Ron Waldon (@jokeyrhyme)"]
    }
    !*/

    /* DOC
    Detects support for creating Blob URLs
    */

    var url = prefixed('URL', window, false);
    url = url && window[url];
    Modernizr.addTest('bloburls', url && 'revokeObjectURL' in url && 'createObjectURL' in url);
    /*!
    {
      "name": "Data URI",
      "property": "datauri",
      "caniuse": "datauri",
      "tags": ["url"],
      "builderAliases": ["url_data_uri"],
      "async": true,
      "notes": [{
        "name": "Wikipedia article",
        "href": "https://en.wikipedia.org/wiki/Data_URI_scheme"
      }],
      "warnings": ["Support in Internet Explorer 8 is limited to images and linked resources like CSS files, not HTML files"]
    }
    !*/

    /* DOC
    Detects support for data URIs. Provides a subproperty to report support for data URIs over 32kb in size:
    
    ```javascript
    Modernizr.datauri           // true
    Modernizr.datauri.over32kb  // false in IE8
    ```
    */
    // https://github.com/Modernizr/Modernizr/issues/14

    Modernizr.addAsyncTest(function () {
      // IE7 throw a mixed content warning on HTTPS for this test, so we'll
      // just reject it (we know it doesn't support data URIs anyway)
      // https://github.com/Modernizr/Modernizr/issues/362
      if (navigator.userAgent.indexOf('MSIE 7.') !== -1) {
        // Keep the test async
        setTimeout(function () {
          Modernizr.addTest('datauri', new Boolean(false));
        }, 10);
      }

      var datauri = new Image();

      datauri.onerror = function () {
        Modernizr.addTest('datauri', new Boolean(false));
      };

      datauri.onload = function () {
        if (datauri.width === 1 && datauri.height === 1) {
          testOver32kb();
        } else {
          Modernizr.addTest('datauri', new Boolean(false));
        }
      };

      datauri.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='; // Once we have datauri, let's check to see if we can use data URIs over
      // 32kb (IE8 can't). https://github.com/Modernizr/Modernizr/issues/321

      function testOver32kb() {
        var datauriBig = new Image();

        datauriBig.onerror = function () {
          Modernizr.addTest('datauri', new Boolean(true));
          Modernizr.addTest('datauri.over32kb', false);
        };

        datauriBig.onload = function () {
          Modernizr.addTest('datauri', new Boolean(true));
          Modernizr.addTest('datauri.over32kb', datauriBig.width === 1 && datauriBig.height === 1);
        };

        var base64str = 'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';

        while (base64str.length < 33000) {
          base64str = '\r\n' + base64str;
        }

        datauriBig.src = 'data:image/gif;base64,' + base64str;
      }
    });
    /*!
    {
      "name": "URL parser",
      "property": "urlparser",
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://url.spec.whatwg.org/"
      }],
      "polyfills": ["urlparser"],
      "authors": ["Ron Waldon (@jokeyrhyme)"],
      "tags": ["url"]
    }
    !*/

    /* DOC
    Check if browser implements the URL constructor for parsing URLs.
    */

    Modernizr.addTest('urlparser', function () {
      var url;

      try {
        // have to actually try use it, because Safari defines a dud constructor
        url = new URL('http://modernizr.com/');
        return url.href === 'http://modernizr.com/';
      } catch (e) {
        return false;
      }
    });
    /*!
    {
      "property": "urlsearchparams",
      "caniuse": "urlsearchparams",
      "tags": ["querystring", "url"],
      "authors": ["Cătălin Mariș"],
      "name": "URLSearchParams API",
      "notes": [{
        "name": "WHATWG Spec",
        "href": "https://url.spec.whatwg.org/#interface-urlsearchparams"
      }, {
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams"
      }]
    }
    !*/

    /* DOC
    Detects support for an API that provides utility methods for working with the query string of a URL.
    */

    Modernizr.addTest('urlsearchparams', 'URLSearchParams' in window);
    /*!
    {
      "name": "IE User Data API",
      "property": "userdata",
      "tags": ["storage"],
      "authors": ["@stereobooster"],
      "notes": [{
        "name": "MSDN Documentation",
        "href": "https://msdn.microsoft.com/en-us/library/ms531424.aspx"
      }]
    }
    !*/

    /* DOC
    Detects support for IE userData for persisting data, an API similar to localStorage but supported since IE5.
    */

    Modernizr.addTest('userdata', !!createElement('div').addBehavior);
    /*!
    {
      "name": "Vibration API",
      "property": "vibrate",
      "caniuse": "vibration",
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en/DOM/window.navigator.mozVibrate"
      }, {
        "name": "W3C Spec",
        "href": "https://www.w3.org/TR/vibration/"
      }]
    }
    !*/

    /* DOC
    Detects support for the API that provides access to the vibration mechanism of the hosting device, to provide tactile feedback.
    */

    Modernizr.addTest('vibrate', !!prefixed('vibrate', navigator));
    /*!
    {
      "name": "HTML5 Video",
      "property": "video",
      "caniuse": "video",
      "tags": ["html5", "video", "media"],
      "knownBugs": ["Without QuickTime, `Modernizr.video.h264` will be `undefined`; https://github.com/Modernizr/Modernizr/issues/546"],
      "polyfills": [
        "html5media",
        "mediaelementjs",
        "sublimevideo",
        "videojs",
        "leanbackplayer",
        "videoforeverybody"
      ]
    }
    !*/

    /* DOC
    Detects support for the video element, as well as testing what types of content it supports.
    
    Subproperties are provided to describe support for `ogg`, `h264`, `h265`, `webm`, `vp9`, `hls` and `av1` formats, e.g.:
    
    ```javascript
    Modernizr.video         // true
    Modernizr.video.ogg     // 'probably'
    ```
    */
    // Codec values from : github.com/NielsLeenheer/html5test/blob/9106a8/index.html#L845
    //                     thx to NielsLeenheer and zcorpan
    // Note: in some older browsers, "no" was a return value instead of empty string.
    //   It was live in FF3.5.0 and 3.5.1, but fixed in 3.5.2
    //   It was also live in Safari 4.0.0 - 4.0.4, but fixed in 4.0.5

    (function () {
      var elem = createElement('video');
      Modernizr.addTest('video', function () {
        var bool = false;

        try {
          bool = !!elem.canPlayType;

          if (bool) {
            bool = new Boolean(bool);
          }
        } catch (e) {}

        return bool;
      }); // IE9 Running on Windows Server SKU can cause an exception to be thrown, bug #224

      try {
        if (!!elem.canPlayType) {
          Modernizr.addTest('video.ogg', elem.canPlayType('video/ogg; codecs="theora"').replace(/^no$/, '')); // Without QuickTime, this value will be `undefined`. github.com/Modernizr/Modernizr/issues/546

          Modernizr.addTest('video.h264', elem.canPlayType('video/mp4; codecs="avc1.42E01E"').replace(/^no$/, ''));
          Modernizr.addTest('video.h265', elem.canPlayType('video/mp4; codecs="hev1"').replace(/^no$/, ''));
          Modernizr.addTest('video.webm', elem.canPlayType('video/webm; codecs="vp8, vorbis"').replace(/^no$/, ''));
          Modernizr.addTest('video.vp9', elem.canPlayType('video/webm; codecs="vp9"').replace(/^no$/, ''));
          Modernizr.addTest('video.hls', elem.canPlayType('application/x-mpegURL; codecs="avc1.42E01E"').replace(/^no$/, ''));
          Modernizr.addTest('video.av1', elem.canPlayType('video/mp4; codecs="av01"').replace(/^no$/, ''));
        }
      } catch (e) {}
    })();
    /*!
    {
      "name": "Video Autoplay",
      "property": "videoautoplay",
      "tags": ["video"],
      "async": true,
      "warnings": ["This test is very large – only include it if you absolutely need it"],
      "knownBugs": ["crashes with an alert on iOS7 when added to homescreen"]
    }
    !*/

    /* DOC
    Checks for support of the autoplay attribute of the video element.
    */


    Modernizr.addAsyncTest(function () {
      var timeout;
      var waitTime = 200;
      var retries = 5;
      var currentTry = 0;
      var elem = createElement('video');
      var elemStyle = elem.style;

      function testAutoplay(arg) {
        currentTry++;
        clearTimeout(timeout);
        var result = arg && arg.type === 'playing' || elem.currentTime !== 0;

        if (!result && currentTry < retries) {
          //Detection can be flaky if the browser is slow, so lets retry in a little bit
          timeout = setTimeout(testAutoplay, waitTime);
          return;
        }

        elem.removeEventListener('playing', testAutoplay, false);
        addTest('videoautoplay', result); // Cleanup, but don't assume elem is still in the page -
        // an extension (eg Flashblock) may already have removed it.

        if (elem.parentNode) {
          elem.parentNode.removeChild(elem);
        }
      } //skip the test if video itself, or the autoplay
      //element on it isn't supported


      if (!Modernizr.video || !('autoplay' in elem)) {
        addTest('videoautoplay', false);
        return;
      }

      elemStyle.position = 'absolute';
      elemStyle.height = 0;
      elemStyle.width = 0;

      try {
        if (Modernizr.video.ogg) {
          elem.src = 'data:video/ogg;base64,T2dnUwACAAAAAAAAAABmnCATAAAAAHDEixYBKoB0aGVvcmEDAgEAAQABAAAQAAAQAAAAAAAFAAAAAQAAAAAAAAAAAGIAYE9nZ1MAAAAAAAAAAAAAZpwgEwEAAAACrA7TDlj///////////////+QgXRoZW9yYSsAAABYaXBoLk9yZyBsaWJ0aGVvcmEgMS4xIDIwMDkwODIyIChUaHVzbmVsZGEpAQAAABoAAABFTkNPREVSPWZmbXBlZzJ0aGVvcmEtMC4yOYJ0aGVvcmG+zSj3uc1rGLWpSUoQc5zmMYxSlKQhCDGMYhCEIQhAAAAAAAAAAAAAEW2uU2eSyPxWEvx4OVts5ir1aKtUKBMpJFoQ/nk5m41mUwl4slUpk4kkghkIfDwdjgajQYC8VioUCQRiIQh8PBwMhgLBQIg4FRba5TZ5LI/FYS/Hg5W2zmKvVoq1QoEykkWhD+eTmbjWZTCXiyVSmTiSSCGQh8PB2OBqNBgLxWKhQJBGIhCHw8HAyGAsFAiDgUCw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDAwPEhQUFQ0NDhESFRUUDg4PEhQVFRUOEBETFBUVFRARFBUVFRUVEhMUFRUVFRUUFRUVFRUVFRUVFRUVFRUVEAwLEBQZGxwNDQ4SFRwcGw4NEBQZHBwcDhATFhsdHRwRExkcHB4eHRQYGxwdHh4dGxwdHR4eHh4dHR0dHh4eHRALChAYKDM9DAwOExo6PDcODRAYKDlFOA4RFh0zV1A+EhYlOkRtZ00YIzdAUWhxXDFATldneXhlSFxfYnBkZ2MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEhIVGRoaGhoSFBYaGhoaGhUWGRoaGhoaGRoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhESFh8kJCQkEhQYIiQkJCQWGCEkJCQkJB8iJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQREhgvY2NjYxIVGkJjY2NjGBo4Y2NjY2MvQmNjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjY2NjFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRISEhUXGBkbEhIVFxgZGxwSFRcYGRscHRUXGBkbHB0dFxgZGxwdHR0YGRscHR0dHhkbHB0dHR4eGxwdHR0eHh4REREUFxocIBERFBcaHCAiERQXGhwgIiUUFxocICIlJRcaHCAiJSUlGhwgIiUlJSkcICIlJSUpKiAiJSUlKSoqEBAQFBgcICgQEBQYHCAoMBAUGBwgKDBAFBgcICgwQEAYHCAoMEBAQBwgKDBAQEBgICgwQEBAYIAoMEBAQGCAgAfF5cdH1e3Ow/L66wGmYnfIUbwdUTe3LMRbqON8B+5RJEvcGxkvrVUjTMrsXYhAnIwe0dTJfOYbWrDYyqUrz7dw/JO4hpmV2LsQQvkUeGq1BsZLx+cu5iV0e0eScJ91VIQYrmqfdVSK7GgjOU0oPaPOu5IcDK1mNvnD+K8LwS87f8Jx2mHtHnUkTGAurWZlNQa74ZLSFH9oF6FPGxzLsjQO5Qe0edcpttd7BXBSqMCL4k/4tFrHIPuEQ7m1/uIWkbDMWVoDdOSuRQ9286kvVUlQjzOE6VrNguN4oRXYGkgcnih7t13/9kxvLYKQezwLTrO44sVmMPgMqORo1E0sm1/9SludkcWHwfJwTSybR4LeAz6ugWVgRaY8mV/9SluQmtHrzsBtRF/wPY+X0JuYTs+ltgrXAmlk10xQHmTu9VSIAk1+vcvU4ml2oNzrNhEtQ3CysNP8UeR35wqpKUBdGdZMSjX4WVi8nJpdpHnbhzEIdx7mwf6W1FKAiucMXrWUWVjyRf23chNtR9mIzDoT/6ZLYailAjhFlZuvPtSeZ+2oREubDoWmT3TguY+JHPdRVSLKxfKH3vgNqJ/9emeEYikGXDFNzaLjvTeGAL61mogOoeG3y6oU4rW55ydoj0lUTSR/mmRhPmF86uwIfzp3FtiufQCmppaHDlGE0r2iTzXIw3zBq5hvaTldjG4CPb9wdxAme0SyedVKczJ9AtYbgPOzYKJvZZImsN7ecrxWZg5dR6ZLj/j4qpWsIA+vYwE+Tca9ounMIsrXMB4Stiib2SPQtZv+FVIpfEbzv8ncZoLBXc3YBqTG1HsskTTotZOYTG+oVUjLk6zhP8bg4RhMUNtfZdO7FdpBuXzhJ5Fh8IKlJG7wtD9ik8rWOJxy6iQ3NwzBpQ219mlyv+FLicYs2iJGSE0u2txzed++D61ZWCiHD/cZdQVCqkO2gJpdpNaObhnDfAPrT89RxdWFZ5hO3MseBSIlANppdZNIV/Rwe5eLTDvkfWKzFnH+QJ7m9QWV1KdwnuIwTNtZdJMoXBf74OhRnh2t+OTGL+AVUnIkyYY+QG7g9itHXyF3OIygG2s2kud679ZWKqSFa9n3IHD6MeLv1lZ0XyduRhiDRtrNnKoyiFVLcBm0ba5Yy3fQkDh4XsFE34isVpOzpa9nR8iCpS4HoxG2rJpnRhf3YboVa1PcRouh5LIJv/uQcPNd095ickTaiGBnWLKVWRc0OnYTSyex/n2FofEPnDG8y3PztHrzOLK1xo6RAml2k9owKajOC0Wr4D5x+3nA0UEhK2m198wuBHF3zlWWVKWLN1CHzLClUfuoYBcx4b1llpeBKmbayaR58njtE9onD66lUcsg0Spm2snsb+8HaJRn4dYcLbCuBuYwziB8/5U1C1DOOz2gZjSZtrLJk6vrLF3hwY4Io9xuT/ruUFRSBkNtUzTOWhjh26irLEPx4jPZL3Fo3QrReoGTTM21xYTT9oFdhTUIvjqTkfkvt0bzgVUjq/hOYY8j60IaO/0AzRBtqkTS6R5ellZd5uKdzzhb8BFlDdAcrwkE0rbXTOPB+7Y0FlZO96qFL4Ykg21StJs8qIW7h16H5hGiv8V2Cflau7QVDepTAHa6Lgt6feiEvJDM21StJsmOH/hynURrKxvUpQ8BH0JF7BiyG2qZpnL/7AOU66gt+reLEXY8pVOCQvSsBtqZTNM8bk9ohRcwD18o/WVkbvrceVKRb9I59IEKysjBeTMmmbA21xu/6iHadLRxuIzkLpi8wZYmmbbWi32RVAUjruxWlJ//iFxE38FI9hNKOoCdhwf5fDe4xZ81lgREhK2m1j78vW1CqkuMu/AjBNK210kzRUX/B+69cMMUG5bYrIeZxVSEZISmkzbXOi9yxwIfPgdsov7R71xuJ7rFcACjG/9PzApqFq7wEgzNJm2suWESPuwrQvejj7cbnQxMkxpm21lUYJL0fKmogPPqywn7e3FvB/FCNxPJ85iVUkCE9/tLKx31G4CgNtWTTPFhMvlu8G4/TrgaZttTChljfNJGgOT2X6EqpETy2tYd9cCBI4lIXJ1/3uVUllZEJz4baqGF64yxaZ+zPLYwde8Uqn1oKANtUrSaTOPHkhvuQP3bBlEJ/LFe4pqQOHUI8T8q7AXx3fLVBgSCVpMba55YxN3rv8U1Dv51bAPSOLlZWebkL8vSMGI21lJmmeVxPRwFlZF1CpqCN8uLwymaZyjbXHCRytogPN3o/n74CNykfT+qqRv5AQlHcRxYrC5KvGmbbUwmZY/29BvF6C1/93x4WVglXDLFpmbapmF89HKTogRwqqSlGbu+oiAkcWFbklC6Zhf+NtTLFpn8oWz+HsNRVSgIxZWON+yVyJlE5tq/+GWLTMutYX9ekTySEQPLVNQQ3OfycwJBM0zNtZcse7CvcKI0V/zh16Dr9OSA21MpmmcrHC+6pTAPHPwoit3LHHqs7jhFNRD6W8+EBGoSEoaZttTCZljfduH/fFisn+dRBGAZYtMzbVMwvul/T/crK1NQh8gN0SRRa9cOux6clC0/mDLFpmbarmF8/e6CopeOLCNW6S/IUUg3jJIYiAcDoMcGeRbOvuTPjXR/tyo79LK3kqqkbxkkMRAOB0GODPItnX3Jnxro/25Ud+llbyVVSN4ySGIgHA6DHBnkWzr7kz410f7cqO/Syt5KqpFVJwn6gBEvBM0zNtZcpGOEPiysW8vvRd2R0f7gtjhqUvXL+gWVwHm4XJDBiMpmmZtrLfPwd/IugP5+fKVSysH1EXreFAcEhelGmbbUmZY4Xdo1vQWVnK19P4RuEnbf0gQnR+lDCZlivNM22t1ESmopPIgfT0duOfQrsjgG4tPxli0zJmF5trdL1JDUIUT1ZXSqQDeR4B8mX3TrRro/2McGeUvLtwo6jIEKMkCUXWsLyZROd9P/rFYNtXPBli0z398iVUlVKAjFlY437JXImUTm2r/4ZYtMy61hf16RPJIU9nZ1MABAwAAAAAAAAAZpwgEwIAAABhp658BScAAAAAAADnUFBQXIDGXLhwtttNHDhw5OcpQRMETBEwRPduylKVB0HRdF0A';
        } else if (Modernizr.video.h264) {
          elem.src = 'data:video/mp4;base64,AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAAAs1tZGF0AAACrgYF//+q3EXpvebZSLeWLNgg2SPu73gyNjQgLSBjb3JlIDE0OCByMjYwMSBhMGNkN2QzIC0gSC4yNjQvTVBFRy00IEFWQyBjb2RlYyAtIENvcHlsZWZ0IDIwMDMtMjAxNSAtIGh0dHA6Ly93d3cudmlkZW9sYW4ub3JnL3gyNjQuaHRtbCAtIG9wdGlvbnM6IGNhYmFjPTEgcmVmPTMgZGVibG9jaz0xOjA6MCBhbmFseXNlPTB4MzoweDExMyBtZT1oZXggc3VibWU9NyBwc3k9MSBwc3lfcmQ9MS4wMDowLjAwIG1peGVkX3JlZj0xIG1lX3JhbmdlPTE2IGNocm9tYV9tZT0xIHRyZWxsaXM9MSA4eDhkY3Q9MSBjcW09MCBkZWFkem9uZT0yMSwxMSBmYXN0X3Bza2lwPTEgY2hyb21hX3FwX29mZnNldD0tMiB0aHJlYWRzPTEgbG9va2FoZWFkX3RocmVhZHM9MSBzbGljZWRfdGhyZWFkcz0wIG5yPTAgZGVjaW1hdGU9MSBpbnRlcmxhY2VkPTAgYmx1cmF5X2NvbXBhdD0wIGNvbnN0cmFpbmVkX2ludHJhPTAgYmZyYW1lcz0zIGJfcHlyYW1pZD0yIGJfYWRhcHQ9MSBiX2JpYXM9MCBkaXJlY3Q9MSB3ZWlnaHRiPTEgb3Blbl9nb3A9MCB3ZWlnaHRwPTIga2V5aW50PTI1MCBrZXlpbnRfbWluPTEwIHNjZW5lY3V0PTQwIGludHJhX3JlZnJlc2g9MCByY19sb29rYWhlYWQ9NDAgcmM9Y3JmIG1idHJlZT0xIGNyZj0yMy4wIHFjb21wPTAuNjAgcXBtaW49MCBxcG1heD02OSBxcHN0ZXA9NCBpcF9yYXRpbz0xLjQwIGFxPTE6MS4wMACAAAAAD2WIhAA3//728P4FNjuZQQAAAu5tb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAAAAZAABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACGHRyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAAZAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAgAAAAIAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAAGQAAAAAAAEAAAAAAZBtZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAACgAAAAEAFXEAAAAAAAtaGRscgAAAAAAAAAAdmlkZQAAAAAAAAAAAAAAAFZpZGVvSGFuZGxlcgAAAAE7bWluZgAAABR2bWhkAAAAAQAAAAAAAAAAAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAAA+3N0YmwAAACXc3RzZAAAAAAAAAABAAAAh2F2YzEAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAgACAEgAAABIAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY//8AAAAxYXZjQwFkAAr/4QAYZ2QACqzZX4iIhAAAAwAEAAADAFA8SJZYAQAGaOvjyyLAAAAAGHN0dHMAAAAAAAAAAQAAAAEAAAQAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAABAAAAAQAAABRzdHN6AAAAAAAAAsUAAAABAAAAFHN0Y28AAAAAAAAAAQAAADAAAABidWR0YQAAAFptZXRhAAAAAAAAACFoZGxyAAAAAAAAAABtZGlyYXBwbAAAAAAAAAAAAAAAAC1pbHN0AAAAJal0b28AAAAdZGF0YQAAAAEAAAAATGF2ZjU2LjQwLjEwMQ==';
        } else {
          addTest('videoautoplay', false);
          return;
        }
      } catch (e) {
        addTest('videoautoplay', false);
        return;
      }

      elem.setAttribute('autoplay', '');
      elemStyle.cssText = 'display:none';
      docElement.appendChild(elem); // wait for the next tick to add the listener, otherwise the element may
      // not have time to play in high load situations (e.g. the test suite)

      setTimeout(function () {
        elem.addEventListener('playing', testAutoplay, false);
        timeout = setTimeout(testAutoplay, waitTime);
      }, 0);
    });
    /*!
    {
      "name": "Video crossOrigin",
      "property": "videocrossorigin",
      "caniuse": "cors",
      "authors": ["Florian Mailliet"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/HTML/CORS_settings_attributes"
      }]
    }
    !*/

    /* DOC
    Detects support for the crossOrigin attribute on video tag
    */

    Modernizr.addTest('videocrossorigin', 'crossOrigin' in createElement('video'));
    /*!
    {
      "name": "Video Loop Attribute",
      "property": "videoloop",
      "tags": ["video", "media"]
    }
    !*/

    Modernizr.addTest('videoloop', 'loop' in createElement('video'));
    /*!
    {
      "name": "Video Preload Attribute",
      "property": "videopreload",
      "tags": ["video", "media"]
    }
    !*/

    Modernizr.addTest('videopreload', 'preload' in createElement('video'));
    /*!
    {
      "name": "XDomainRequest",
      "property": "xdomainrequest",
      "tags": ["cors", "xdomainrequest", "ie9", "ie8"],
      "authors": ["Ivan Pan (@hypotenuse)"],
      "notes": [{
        "name": "MDN Docs",
        "href": "https://developer.mozilla.org/en-US/docs/Web/API/XDomainRequest"
      }]
    }
    !*/

    /* DOC
    Detects support for XDomainRequest in IE9 & IE8
    */

    Modernizr.addTest('xdomainrequest', 'XDomainRequest' in window); // Run each test

    testRunner(); // Remove the "no-js" class if it exists

    setClasses(classes);
    delete ModernizrProto.addTest;
    delete ModernizrProto.addAsyncTest; // Run the things that are supposed to run after the tests

    for (var i = 0; i < Modernizr._q.length; i++) {
      Modernizr._q[i]();
    } // Leak Modernizr namespace


    scriptGlobalObject.Modernizr = Modernizr;
    ;
  })(window, window, document);

  module.exports = window.Modernizr;

  if (hadGlobal) {
    window.Modernizr = oldGlobal;
  } else {
    delete window.Modernizr;
  }
})(window);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(96)(module)))

/***/ })

/******/ });