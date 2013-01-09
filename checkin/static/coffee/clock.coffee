createClock = (cv, timestamp = null, showDigital = false) =>
    if timestamp != null
        cv.timeDiff = timestamp - new Date().getTime()
    window.setInterval (->
        updateClock cv, showDigital),1

window.createAnalogClock = createClock

updateClock = (cv, showDigital = false) =>
    calculateAngle = (amount, max=12) ->
        amount/max * 2 * Math.PI - Math.PI/2

    angleToCoords =  (angle, radius, centre) ->
        coords =
            x: radius * Math.cos(angle) + centre.x
            y: radius * Math.sin(angle) + centre.y


    if cv.timeDiff?
        now = new Date new Date().getTime() + cv.timeDiff
    else
        now = new Date

    ctx = cv.getContext "2d"

    #clean canvas
    ctx.save()
    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.clearRect(0, 0, cv.width, cv.height)
    ctx.restore()

    centre =
        x: cv.width / 2
        y: cv.height / 2
    radius = Math.min centre.x, centre.y

    drawRadius = (angle, length, lineWidth=2, strokeStyle="black", shadowOffset=2) ->
        coords = angleToCoords angle, length, centre
        ctx.lineWidth = lineWidth

        # Shadow
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)'
        ctx.beginPath()
        ctx.moveTo centre.x + shadowOffset, centre.y + shadowOffset
        ctx.lineTo coords.x + shadowOffset, coords.y + shadowOffset
        ctx.stroke()

        # Hand
        ctx.strokeStyle = strokeStyle
        ctx.beginPath()
        ctx.moveTo centre.x, centre.y
        ctx.lineTo coords.x, coords.y
        ctx.stroke()


    drawPartialRadius = (angle, innerLength, outerLength, lineWidth=2, strokeStyle="black") ->
        innerCoords = angleToCoords angle, innerLength, centre
        outerCoords = angleToCoords angle, outerLength, centre
        ctx.lineWidth = lineWidth
        ctx.strokeStyle = strokeStyle
        ctx.beginPath()
        ctx.moveTo innerCoords.x, innerCoords.y
        ctx.lineTo outerCoords.x, outerCoords.y
        ctx.stroke()


    #Face
    ctx.lineWidth = 10
    ctx.strokeStyle = "#A7C520"
    ctx.fillStyle = "black"
    ctx.beginPath()
    ctx.arc centre.x, centre.y, 0.90*radius, 0, 2*Math.PI
    ctx.fill()
    ctx.stroke()
    
    #Center circle shadow
    ctx.beginPath()
    ctx.arc centre.x, centre.y, 20, 0, 2*Math.PI
    ctx.fillStyle = "rgba(255, 255, 255, 0.4)"
    ctx.fill()

    ctx.beginPath()
    ctx.arc centre.x + 2, centre.y + 2, 5, 0, 2*Math.PI
    ctx.fillStyle = "rgba(0, 0, 0, 0.4)"
    ctx.fill()

    for i in [10..0]
        ctx.beginPath()
        ctx.arc centre.x, centre.y, (0.70 + ( i * 0.01)) * radius, 0, 2*Math.PI
        ctx.fillStyle = "rgba(25, 25, 25, 0.1)"
        ctx.fill()
    
    for i in [0..12]
        drawPartialRadius i * 2 * Math.PI / 12, 0.7 * radius, 0.8 * radius, 3, "#ccc"

    if showDigital
        #Digital time
        ctx.fillStyle = "#666"
        ctx.textAlign = "center"
        ctx.font = "15pt Sans"
        if now.getMinutes() < 10
            ctx.fillText "#{now.getHours()}:0#{now.getMinutes()}", centre.x, 1.6 * centre.y
        else
            ctx.fillText "#{now.getHours()}:#{now.getMinutes()}", centre.x, 1.6 * centre.y
    
    hourAngle = calculateAngle now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds(), 12 * 60 * 60
    minAngle = calculateAngle now.getMinutes() * 60 + now.getSeconds(), 60 * 60
    secAngle = calculateAngle now.getSeconds(), 60

    drawRadius hourAngle, radius * 0.55, 9, "white"
    drawRadius minAngle, radius * 0.75, 7, "white"
    drawRadius secAngle, radius * 0.80, 2, "#cc0000"

    # Center circle
    ctx.beginPath()
    ctx.arc centre.x, centre.y, 5, 0, 2*Math.PI
    ctx.fillStyle = "white"
    ctx.fill()

