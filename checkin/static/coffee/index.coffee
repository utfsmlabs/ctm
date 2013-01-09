$(document).ready -> 
    ($.get "private/time", (data) ->
        serverTime = Date.parse data
        createAnalogClock canvas, serverTime, true for canvas in $ 'canvas#clock_canvas'
    ).error ->
        $('<div class="alert-message error data-alert">
           Error obteniendo la hora del servidor
           </div>').insertAfter('canvas#clock_canvas')

