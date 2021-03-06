!function (n) {
    var o = {};

    function a(e) {
        if (o[e]) return o[e].exports;
        var t = o[e] = {i: e, l: !1, exports: {}};
        return n[e].call(t.exports, t, t.exports, a), t.l = !0, t.exports
    }

    a.m = n, a.c = o, a.d = function (e, t, n) {
        a.o(e, t) || Object.defineProperty(e, t, {enumerable: !0, get: n})
    }, a.r = function (e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {value: "Module"}), Object.defineProperty(e, "__esModule", {value: !0})
    }, a.t = function (t, e) {
        if (1 & e && (t = a(t)), 8 & e) return t;
        if (4 & e && "object" == typeof t && t && t.__esModule) return t;
        var n = Object.create(null);
        if (a.r(n), Object.defineProperty(n, "default", {
            enumerable: !0,
            value: t
        }), 2 & e && "string" != typeof t) for (var o in t) a.d(n, o, function (e) {
            return t[e]
        }.bind(null, o));
        return n
    }, a.n = function (e) {
        var t = e && e.__esModule ? function () {
            return e.default
        } : function () {
            return e
        };
        return a.d(t, "a", t), t
    }, a.o = function (e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, a.p = "/dist", a(a.s = 2)
}([function (e, t) {
    e.exports = jQuery
}, function (e, t, n) {
}, function (e, t, n) {
    "use strict";
    n.r(t);
    var o = n(0), r = n.n(o), i = "simple-tree";

    function a(e, t) {
        for (var n = 0; n < t.length; n++) {
            var o = t[n];
            o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
        }
    }

    var s = function () {
        function n(e) {
            var t = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
            !function (e, t) {
                if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
            }(this, n), this.tree = e, this.key = t.storeKey, this.storage = n.storage(t.storeType)
        }

        var e, t, o;
        return e = n, o = [{
            key: "storage", value: function (e) {
                return "local" == e ? window.localStorage : window.sessionStorage
            }
        }, {
            key: "saveData", value: function (e, t, n) {
                var o = JSON.stringify(n);
                e.setItem(t, o)
            }
        }, {
            key: "loadData", value: function (e, t) {
                var n = e.getItem(t);
                return n ? JSON.parse(n) : null
            }
        }], (t = [{
            key: "save", value: function () {
                var e = this.tree.nodes().filter(".tree-opened").map(function (e, t) {
                    return r()(t).data("node-id")
                }).get();
                n.saveData(this.storage, this.key, e)
            }
        }, {
            key: "load", value: function () {
                var o = this, a = n.loadData(this.storage, this.key);
                a && this.tree.nodes().each(function (e, t) {
                    var n = r()(t);
                    -1 != a.indexOf(n.data("node-id")) ? o.tree.show(n) : o.tree.hide(n)
                })
            }
        }]) && a(e.prototype, t), o && a(e, o), n
    }();

    function l(e, t) {
        for (var n = 0; n < t.length; n++) {
            var o = t[n];
            o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, o.key, o)
        }
    }

    var u = {
        expander: null,
        collapser: null,
        opened: "all",
        storeState: !1,
        storeKey: i,
        storeType: "session",
        iconTemplate: "<span />"
    }, c = function () {
        function n(e) {
            var t = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
            !function (e, t) {
                if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function")
            }(this, n), this.options = r.a.extend({}, u, t), this.$root = r()(e), this.$expander = r()(this.options.expander), this.$collapser = r()(this.options.collapser), this.options.storeState && (this.store = new s(this, this.options)), this.init()
        }

        var e, t, o;
        return e = n, o = [{
            key: "getDefaults", value: function () {
                return u
            }
        }, {
            key: "setDefaults", value: function (e) {
                r.a.extend(u, e)
            }
        }], (t = [{
            key: "init", value: function () {
                this.$root.addClass(i), this.build(), this.bind(), this.loadState()
            }
        }, {
            key: "build", value: function () {
                var i = this;
                this.nodes().each(function (e, t) {
                    var n = r()(t);
                    if (0 == n.children(".tree-icon").length) {
                        var o = r()(i.options.iconTemplate).addClass("tree-icon");
                        n.prepend(o)
                    }
                    var a = n.attr("class");
                    a && a.split(" ").some(function (e) {
                        return e.match(/^(tree-empty|tree-opened|tree-closed)$/)
                    }) || (n.data("node-lazy") ? n.addClass("tree-closed") : 0 == n.children("ul").length ? n.addClass("tree-empty") : i.opensDefault(n) ? n.addClass("tree-opened") : n.addClass("tree-closed")), n.hasClass("tree-opened") ? n.children("ul").show() : n.hasClass("tree-closed") && n.children("ul").hide()
                })
            }
        }, {
            key: "opensDefault", value: function (e) {
                var t = this.options.opened;
                return t && ("all" == t || -1 != t.indexOf(e.data("node-id")))
            }
        }, {
            key: "bind", value: function () {
                var n = this;
                this.$expander.on("click.".concat(i), function (e) {
                    n.expand()
                }), this.$collapser.on("click.".concat(i), function (e) {
                    n.collapse()
                }), this.$root.on("click.".concat(i), ".tree-icon", function (e) {
                    var t = r()(e.currentTarget).parent();
                    t.hasClass("tree-opened") ? n.close(t) : n.open(t)
                })
            }
        }, {
            key: "unbind", value: function () {
                this.$expander.off(".".concat(i)), this.$collapser.off(".".concat(i)), this.$root.off(".".concat(i))
            }
        }, {
            key: "expand", value: function () {
                var n = this;
                this.nodes().each(function (e, t) {
                    n.show(r()(t))
                }), this.saveState()
            }
        }, {
            key: "collapse", value: function () {
                var n = this;
                this.nodes().each(function (e, t) {
                    n.hide(r()(t))
                }), this.saveState()
            }
        }, {
            key: "nodes", value: function () {
                return this.$root.find("li")
            }
        }, {
            key: "open", value: function (e) {
                this.show(e), this.saveState(), e.trigger("node:open", [e])
            }
        }, {
            key: "show", value: function (e) {
                e.hasClass("tree-empty") || (e.removeClass("tree-closed").addClass("tree-opened"), e.children("ul").show())
            }
        }, {
            key: "close", value: function (e) {
                this.hide(e), this.saveState(), e.trigger("node:close", [e])
            }
        }, {
            key: "hide", value: function (e) {
                e.hasClass("tree-empty") || (e.removeClass("tree-opened").addClass("tree-closed"), e.children("ul").hide())
            }
        }, {
            key: "findByID", value: function (e) {
                return this.$root.find('li[data-node-id="'.concat(e, '"]:first'))
            }
        }, {
            key: "openByID", value: function (e) {
                this.open(this.findByID(e))
            }
        }, {
            key: "closeByID", value: function (e) {
                this.close(this.findByID(e))
            }
        }, {
            key: "saveState", value: function () {
                this.store && this.store.save()
            }
        }, {
            key: "loadState", value: function () {
                this.store && this.store.load()
            }
        }]) && l(e.prototype, t), o && l(e, o), n
    }();
    n(1);
    r.a.fn.simpleTree = function (a) {
        return this.each(function (e, t) {
            var n = r()(t);
            if (!n.data(i)) {
                var o = new c(n, a);
                n.data(i, o)
            }
        })
    }, r.a.SimpleTree = c
}]);