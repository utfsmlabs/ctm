(function() {
  var createClock, updateClock;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  createClock = __bind(function(cv, timestamp, showDigital) {
    if (timestamp == null) {
      timestamp = null;
    }
    if (showDigital == null) {
      showDigital = false;
    }
    if (timestamp !== null) {
      cv.timeDiff = timestamp - new Date().getTime();
    }
    return window.setInterval((function() {
      return updateClock(cv, showDigital);
    }), 1);
  }, this);
  window.createAnalogClock = createClock;
  updateClock = __bind(function(cv, showDigital) {
    var angleToCoords, calculateAngle, centre, ctx, drawPartialRadius, drawRadius, hourAngle, i, minAngle, now, radius, secAngle;
    if (showDigital == null) {
      showDigital = false;
    }
    calculateAngle = function(amount, max) {
      if (max == null) {
        max = 12;
      }
      return amount / max * 2 * Math.PI - Math.PI / 2;
    };
    angleToCoords = function(angle, radius, centre) {
      var coords;
      return coords = {
        x: radius * Math.cos(angle) + centre.x,
        y: radius * Math.sin(angle) + centre.y
      };
    };
    if (cv.timeDiff != null) {
      now = new Date(new Date().getTime() + cv.timeDiff);
    } else {
      now = new Date;
    }
    ctx = cv.getContext("2d");
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.restore();
    centre = {
      x: cv.width / 2,
      y: cv.height / 2
    };
    radius = Math.min(centre.x, centre.y);
    drawRadius = function(angle, length, lineWidth, strokeStyle, shadowOffset) {
      var coords;
      if (lineWidth == null) {
        lineWidth = 2;
      }
      if (strokeStyle == null) {
        strokeStyle = "black";
      }
      if (shadowOffset == null) {
        shadowOffset = 2;
      }
      coords = angleToCoords(angle, length, centre);
      ctx.lineWidth = lineWidth;
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
      ctx.beginPath();
      ctx.moveTo(centre.x + shadowOffset, centre.y + shadowOffset);
      ctx.lineTo(coords.x + shadowOffset, coords.y + shadowOffset);
      ctx.stroke();
      ctx.strokeStyle = strokeStyle;
      ctx.beginPath();
      ctx.moveTo(centre.x, centre.y);
      ctx.lineTo(coords.x, coords.y);
      return ctx.stroke();
    };
    drawPartialRadius = function(angle, innerLength, outerLength, lineWidth, strokeStyle) {
      var innerCoords, outerCoords;
      if (lineWidth == null) {
        lineWidth = 2;
      }
      if (strokeStyle == null) {
        strokeStyle = "black";
      }
      innerCoords = angleToCoords(angle, innerLength, centre);
      outerCoords = angleToCoords(angle, outerLength, centre);
      ctx.lineWidth = lineWidth;
      ctx.strokeStyle = strokeStyle;
      ctx.beginPath();
      ctx.moveTo(innerCoords.x, innerCoords.y);
      ctx.lineTo(outerCoords.x, outerCoords.y);
      return ctx.stroke();
    };
    ctx.lineWidth = 10;
    ctx.strokeStyle = "#A7C520";
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.arc(centre.x, centre.y, 0.90 * radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(centre.x, centre.y, 20, 0, 2 * Math.PI);
    ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
    ctx.fill();
    ctx.beginPath();
    ctx.arc(centre.x + 2, centre.y + 2, 5, 0, 2 * Math.PI);
    ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
    ctx.fill();
    for (i = 10; i >= 0; i--) {
      ctx.beginPath();
      ctx.arc(centre.x, centre.y, (0.70 + (i * 0.01)) * radius, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(25, 25, 25, 0.1)";
      ctx.fill();
    }
    for (i = 0; i <= 12; i++) {
      drawPartialRadius(i * 2 * Math.PI / 12, 0.7 * radius, 0.8 * radius, 3, "#ccc");
    }
    if (showDigital) {
      ctx.fillStyle = "#666";
      ctx.textAlign = "center";
      ctx.font = "15pt Sans";
      if (now.getMinutes() < 10) {
        ctx.fillText("" + (now.getHours()) + ":0" + (now.getMinutes()), centre.x, 1.6 * centre.y);
      } else {
        ctx.fillText("" + (now.getHours()) + ":" + (now.getMinutes()), centre.x, 1.6 * centre.y);
      }
    }
    hourAngle = calculateAngle(now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds(), 12 * 60 * 60);
    minAngle = calculateAngle(now.getMinutes() * 60 + now.getSeconds(), 60 * 60);
    secAngle = calculateAngle(now.getSeconds(), 60);
    drawRadius(hourAngle, radius * 0.55, 9, "white");
    drawRadius(minAngle, radius * 0.75, 7, "white");
    drawRadius(secAngle, radius * 0.80, 2, "#cc0000");
    ctx.beginPath();
    ctx.arc(centre.x, centre.y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = "white";
    return ctx.fill();
  }, this);
}).call(this);
