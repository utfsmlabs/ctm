(function() {
  $(document).ready(function() {
    return ($.get("private/time", function(data) {
      var canvas, serverTime, _i, _len, _ref, _results;
      serverTime = Date.parse(data);
      _ref = $('canvas#clock_canvas');
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        canvas = _ref[_i];
        _results.push(createAnalogClock(canvas, serverTime, true));
      }
      return _results;
    })).error(function() {
      return $('<div class="alert-message error data-alert">\
           Error obteniendo la hora del servidor\
           </div>').insertAfter('canvas#clock_canvas');
    });
  });
}).call(this);
