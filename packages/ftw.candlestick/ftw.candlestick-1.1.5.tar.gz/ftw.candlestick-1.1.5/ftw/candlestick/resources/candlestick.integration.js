(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery', 'ftw.candlestick'], factory);
    } else {
        // Browser globals
        factory(root.jQuery, root.ftw.candlestick);
    }
}(typeof self !== 'undefined' ? self : this, function ($, candlestick) {
  $(function() {
    candlestick();
  });
}));
