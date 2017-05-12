class AlertView extends Backbone.View
    events:
        'click .clear-alert-btn': 'hideAlert'


    showAlert: (alertData) ->
        if alertData
            message = alertData.message or ''
            buttons = alertData.buttons or ''
            showCloseBtn = alertData.showCloseBtn or false
            if showCloseBtn? and showCloseBtn is true
                @$('.clear-alert-btn').show()
            else
                @$('.clear-alert-btn').hide()

            if @$('.alert-buttons').length > 0 and not @$el.hasClass('keep-alert')
                @$('.alert-buttons').remove()

            if @$('.alert-text').length == 0
                @$('.alert').append('<div class="alert-text"></div>')
            if @$('.alert-buttons').length == 0 and buttons != ''
                @$('.alert').append('<div class="alert-buttons"></div>')

            @$('.alert-text').html(message)
            @$('.alert-buttons').append(buttons)

        if @$('.alert-text').length > 0
            @$el.removeClass('keep-alert').show()

    hideAlert: ->
        @$el.hide()
        @$('.alert-text').html('')
        @$('.alert-buttons').html('')

window.alertView = new AlertView(el: $('#alert-wrapper'))