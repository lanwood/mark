var n = {}

function f(t, e) {
var n = (65535 & t) + (65535 & e);
return (t >> 16) + (e >> 16) + (n >> 16) << 16 | 65535 & n
}
function s(t, e, n, o, i, r) {
return f((a = f(f(e, t), f(o, r))) << (s = i) | a >>> 32 - s, n);
var a, s
}
function d(t, e, n, o, i, r, a) {
return s(e & n | ~e & o, t, e, i, r, a)
}
function p(t, e, n, o, i, r, a) {
return s(e & o | n & ~o, t, e, i, r, a)
}
function h(t, e, n, o, i, r, a) {
return s(e ^ n ^ o, t, e, i, r, a)
}
function m(t, e, n, o, i, r, a) {
return s(n ^ (e | ~o), t, e, i, r, a)
}
function c(t, e) {
t[e >> 5] |= 128 << e % 32,
t[14 + (e + 64 >>> 9 << 4)] = e;
var n, o, i, r, a, s = 1732584193,
c = -271733879,
u = -1732584194,
l = 271733878;
for (n = 0; n < t.length; n += 16) s = d(o = s, i = c, r = u, a = l, t[n], 7, -680876936),
l = d(l, s, c, u, t[n + 1], 12, -389564586),
u = d(u, l, s, c, t[n + 2], 17, 606105819),
c = d(c, u, l, s, t[n + 3], 22, -1044525330),
s = d(s, c, u, l, t[n + 4], 7, -176418897),
l = d(l, s, c, u, t[n + 5], 12, 1200080426),
u = d(u, l, s, c, t[n + 6], 17, -1473231341),
c = d(c, u, l, s, t[n + 7], 22, -45705983),
s = d(s, c, u, l, t[n + 8], 7, 1770035416),
l = d(l, s, c, u, t[n + 9], 12, -1958414417),
u = d(u, l, s, c, t[n + 10], 17, -42063),
c = d(c, u, l, s, t[n + 11], 22, -1990404162),
s = d(s, c, u, l, t[n + 12], 7, 1804603682),
l = d(l, s, c, u, t[n + 13], 12, -40341101),
u = d(u, l, s, c, t[n + 14], 17, -1502002290),
s = p(s, c = d(c, u, l, s, t[n + 15], 22, 1236535329), u, l, t[n + 1], 5, -165796510),
l = p(l, s, c, u, t[n + 6], 9, -1069501632),
u = p(u, l, s, c, t[n + 11], 14, 643717713),
c = p(c, u, l, s, t[n], 20, -373897302),
s = p(s, c, u, l, t[n + 5], 5, -701558691),
l = p(l, s, c, u, t[n + 10], 9, 38016083),
u = p(u, l, s, c, t[n + 15], 14, -660478335),
c = p(c, u, l, s, t[n + 4], 20, -405537848),
s = p(s, c, u, l, t[n + 9], 5, 568446438),
l = p(l, s, c, u, t[n + 14], 9, -1019803690),
u = p(u, l, s, c, t[n + 3], 14, -187363961),
c = p(c, u, l, s, t[n + 8], 20, 1163531501),
s = p(s, c, u, l, t[n + 13], 5, -1444681467),
l = p(l, s, c, u, t[n + 2], 9, -51403784),
u = p(u, l, s, c, t[n + 7], 14, 1735328473),
s = h(s, c = p(c, u, l, s, t[n + 12], 20, -1926607734), u, l, t[n + 5], 4, -378558),
l = h(l, s, c, u, t[n + 8], 11, -2022574463),
u = h(u, l, s, c, t[n + 11], 16, 1839030562),
c = h(c, u, l, s, t[n + 14], 23, -35309556),
s = h(s, c, u, l, t[n + 1], 4, -1530992060),
l = h(l, s, c, u, t[n + 4], 11, 1272893353),
u = h(u, l, s, c, t[n + 7], 16, -155497632),
c = h(c, u, l, s, t[n + 10], 23, -1094730640),
s = h(s, c, u, l, t[n + 13], 4, 681279174),
l = h(l, s, c, u, t[n], 11, -358537222),
u = h(u, l, s, c, t[n + 3], 16, -722521979),
c = h(c, u, l, s, t[n + 6], 23, 76029189),
s = h(s, c, u, l, t[n + 9], 4, -640364487),
l = h(l, s, c, u, t[n + 12], 11, -421815835),
u = h(u, l, s, c, t[n + 15], 16, 530742520),
s = m(s, c = h(c, u, l, s, t[n + 2], 23, -995338651), u, l, t[n], 6, -198630844),
l = m(l, s, c, u, t[n + 7], 10, 1126891415),
u = m(u, l, s, c, t[n + 14], 15, -1416354905),
c = m(c, u, l, s, t[n + 5], 21, -57434055),
s = m(s, c, u, l, t[n + 12], 6, 1700485571),
l = m(l, s, c, u, t[n + 3], 10, -1894986606),
u = m(u, l, s, c, t[n + 10], 15, -1051523),
c = m(c, u, l, s, t[n + 1], 21, -2054922799),
s = m(s, c, u, l, t[n + 8], 6, 1873313359),
l = m(l, s, c, u, t[n + 15], 10, -30611744),
u = m(u, l, s, c, t[n + 6], 15, -1560198380),
c = m(c, u, l, s, t[n + 13], 21, 1309151649),
s = m(s, c, u, l, t[n + 4], 6, -145523070),
l = m(l, s, c, u, t[n + 11], 10, -1120210379),
u = m(u, l, s, c, t[n + 2], 15, 718787259),
c = m(c, u, l, s, t[n + 9], 21, -343485551),
s = f(s, o),
c = f(c, i),
u = f(u, r),
l = f(l, a);
return [s, c, u, l]
}
function u(t) {
var e, n = "";
for (e = 0; e < 32 * t.length; e += 8) n += String.fromCharCode(t[e >> 5] >>> e % 32 & 255);
return n
}
function l(t) {
var e, n = [];
for (n[(t.length >> 2) - 1] = void 0, e = 0; e < n.length; e += 1) n[e] = 0;
for (e = 0; e < 8 * t.length; e += 8) n[e >> 5] |= (255 & t.charCodeAt(e / 8)) << e % 32;
return n
}
function o(t) {
var e, n, o = "0123456789abcdef",
i = "";
for (n = 0; n < t.length; n += 1) e = t.charCodeAt(n),
i += o.charAt(e >>> 4 & 15) + o.charAt(15 & e);
return i
}
function i(t) {
return unescape(encodeURIComponent(t))
}
function r(t) {
return u(c(l(e = i(t)), 8 * e.length));
var e
}
function a(t, e) {
return function(t, e) {
    var n, o, i = l(t),
    r = [],
    a = [];
    for (r[15] = a[15] = void 0, 16 < i.length && (i = c(i, 8 * t.length)), n = 0; n < 16; n += 1) r[n] = 909522486 ^ i[n],
    a[n] = 1549556828 ^ i[n];
    return o = c(r.concat(l(e)), 512 + 8 * e.length),
    u(c(a.concat(o), 640))
} (i(t), i(e))
}
function getPwd(t, e, n) {
return e ? n ? a(e, t) : o(a(e, t)) : n ? r(t) : o(r(t))
}