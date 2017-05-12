$ ->
    $.ajaxSetup
        cache: false
        beforeSend: (xhr, settings) =>
            xhr.setRequestHeader "X-CSRFToken", getCookie('csrftoken')

    # alert
#    showAlert = (message, buttons, showCloseBtn) ->
#        if message != ''
#            if showCloseBtn? and showCloseBtn is true
#                $('#alert-wrapper .clear-alert-btn').show()
#            else
#                $('#alert-wrapper .clear-alert-btn').hide()
#
#            if $('#alert-wrapper .alert-text').length == 0
#                $('#alert-wrapper .alert').append('<div class="alert-text"></div>')
#
#            $('#alert-wrapper .alert-text').html(message)
#
#            if $('#alert-wrapper .alert-buttons').length > 0 and not $('#alert-wrapper').hasClass('keep-alert')
#                $('#alert-wrapper .alert-buttons').remove()
#            $('#alert-wrapper .alert').append(buttons)
#
#        if $('#alert-wrapper .alert-text').length > 0 and $.trim($('#alert-wrapper .alert-text').html()) != ''
#            $('#alert-wrapper').removeClass('keep-alert').show()
#
#    hideAlert = ->
#        $('#alert-wrapper').hide()
#        $('#alert-wrapper .alert-text').html('')
#        $('#alert-wrapper .alert-buttons').remove()
#    /end alert


#    showAlert()


    # search filter
    $('#search-input').on 'keyup', (e) ->
        q = $.trim($(e.target).val()).toUpperCase()

        visibleVideos = []
        $('.video').each (idx, video) ->
            pos = $(video).data('div-position')
            visibleVideos.push pos
            if $(video).data('title').toUpperCase().indexOf(q) > -1
                index = visibleVideos.indexOf(pos)
                if (index == -1)
                    visibleVideos.push(index)

                visibleVideos.sort(numSort)
                insertAfter = visibleVideos[visibleVideos.indexOf(pos) - 1]

                if insertAfter
                    $('*[data-div-position="' + insertAfter + '"]').after($(video))
                else
                    $('.videos').prepend($(video))

            else
                index = visibleVideos.indexOf(pos)
                if (index > -1)
                    visibleVideos.splice(index, 1)

                $videoClone = $(video).clone()
                $(video).remove()
                $('.hidden-videos').append($videoClone)
    # /search filter


#    $('.clear-alert-btn').on 'click', ->
#        hideAlert()


    # tooltip
    $('[rel="tooltip"]').on 'mouseenter', (e) ->
        $el = $(e.target)
        text = $el.attr('title')
    # /end tooltip


    # sync videos
#    $('.sync-btn').on 'click', (e) =>
#        $(e.target).removeClass('active').attr('disabled', 'disabled').text('Syncing')
#        $(e.target).addClass('busy')
#        showAlert('<i class="spinner icon-contrast"></i>Retrieving YouTube videos from your Facebook timeline...')
#        $.get URLS.sync_videos, (response) ->
#            $('.date.faded').text('Synced just now')
#            $(e.target).removeClass('busy').prop('disabled', '').text('Sync Videos')
#
#            if response > 0
#                $('#video-list').load window.location.pathname + " #video-list-content"
#                showAlert(response + ' new videos found and synced', '', true)
#            else
#                showAlert('No new videos were found', '', true)
    # /end sync videos


    # delete videos
#    $('body').on 'click', '.delete-all-btn', (e) ->
#        $('.content-header-btn').not('.secondary').removeClass('active')
#        $(e.currentTarget).addClass('active')
#        showAlert('Delete all your synced videos?',
#        '
#            <div class="alert-buttons">
#                <button class="btn confirm-delete">Yes</button><button class="btn cancel-delete">No</button>
#            </div>
#        ')
#    $('body').on 'click', '.confirm-delete', ->
#        $.get URLS.delete_videos, (response) ->
#            $('.sync-btn').addClass('active')
#            $('.date.faded').text('')
#            window.location.href = URLS.video_list
#    $('body').on 'click', '.cancel-delete', ->
#        $('.delete-all-btn').removeClass('active')
#        hideAlert()
#    $('body').on 'click', '.delete-all-btn.active', (e) ->
#        $(e.currentTarget).removeClass('active')
#        hideAlert()
    # /end delete videos


    # archive video
    $('body').on 'click', '.archive-video-btn', (e) ->
        if $(e.currentTarget).hasClass('active')
            $(e.currentTarget).removeClass('active')
            hideAlert()
            return false

        $('.content-header-btn').not('.secondary').removeClass('active')
        $(e.currentTarget).addClass('active')
        showAlert('Archive video?',
        '
            <div class="alert-buttons">
                <button class="btn confirm-archive">Yes</button><button class="btn cancel-archive">No</button>
            </div>
        ')
    $('body').on 'click', '.confirm-archive', ->
        url = '/video/' + $('#video-detail').data('video-id') + '/archive-video/'
        $.get url, (response) ->
            showAlert('This video has been archived. It will not show up in your video list.',
            '
                <div class="alert-buttons">
                    <button class="btn restore-video-btn">Restore</button>
                </div>
            ')
            $('.archive-video-btn').remove()
    $('body').on 'click', '.cancel-archive', ->
        $('.archive-video-btn').removeClass('active')
        hideAlert()
    # /end archive video


    # restore video
    $('body').on 'click', '.restore-video-btn', (e) ->
        url = '/video/' + $('#video-detail').data('video-id') + '/restore-video/'
        $.get url, (response) ->
            showAlert('This video has been restored', '', true)
            $('#share-date').before('
                <a class="archive-video-btn content-header-btn" href="javascript:">
                    <i class="icon-archive"></i>
                </a>
            ')
    # /end restore video


    # sorting
    $('body').on 'mouseenter', '.sort-videos-btn', (e) ->
        if $(e.currentTarget).hasClass('active')
            return false
        $(e.currentTarget).addClass('active')
    $('body').on 'mouseleave', '.sort-videos-btn', (e) ->
        $(e.currentTarget).removeClass('active')
    $('body').on 'click', '.sort-videos-link', (e) ->
        window.location.href = URLS.sort_url + '&sort=' + $(e.target).data('sort')
    # /end sorting


    # inline player
    $('body').on 'click', '.thumbnail', (e) ->
        $('#video-container').remove()
        $('.player-open.arrow').remove()
        $video = $($(e.target).parents('.video'))
        $title = $video.find('.title').text()
        $embedUrl = $video.data('embed-url') + '?autoplay=1'
        top = $video.offset().top
        $video.append('<i class="player-open arrow icon-caret-up"></i>')
        while $video.next().hasClass('video') and top == $video.next().offset().top
            $video = $video.next()
            top = $video.offset().top

        $player = $('
            <div id="video-container">
                <i class="icon-times close-btn"></i>
                <div class="player-title ellipsize">' + $title + '</div>
                <div class="auto-resizable-iframe">
                    <div><iframe type="text/html" class="video-player" src="' + $embedUrl + '" frameborder="0" allowfullscreen></iframe></div>
                </div>
                <div class="clear"></div>
            </div>
        ')
        $video.after($player)
#        window.addEventListener('scroll', repositionPlayer($player), false)

    $('body').on 'click', '.close-btn', (e) ->
        $(e.target).parent().remove()
        $('.mask').remove()
        $('.player-open.arrow').remove()
#        window.removeEventListener('scroll', repositionPlayer())
    # /end inline player


    # infinite scroll
#    @listBottom = $('#video-list').offset().top + $('#video-list').height()
#    @wh = $(window).height()
#    if @listBottom < @wh
#        @stopScroll = false
    $(window).on 'scroll', ->
        if @stopScroll
            return false

        @dh = $(document).height() - 10
        @nextUrl = $('#next-page').data('next-url')
        @wscroll = $(window).scrollTop() + $(window).height()
        if @wscroll > @dh
            if @nextUrl
                @stopScroll = true
                $('.video-loader').html('<i class="icon-contrast spinner"></i>')
                $.get @nextUrl, (response) =>
                    $(response).find('.video').each (idx, el) =>
                        $('.videos-content').append($(el))

                    $('#pagination').html $(response).find('#pagination').html()
                    @stopScroll = false
                    $('.video-loader').html('')
            else
                @stopScroll = true
    # /end infinite scroll


    # rating
    $('.video-rating').on 'click', (e) ->
        if not $(e.target).hasClass('label-icon')
            return false

        $div = $(e.currentTarget)
        $icon = $(e.target)
        $btn = $icon.parents('.video-rating-btn')
        $label = $icon.next()
        url = $div.data('rate-url')

        if $btn.hasClass('disabled')
            return false

        $sibling = $btn.siblings('.video-rating-btn')
        $siblingLabel = $sibling.find('label')

        if $btn.hasClass('selected')
            $label.text(parseInt($label.text()) - 1)
            $btn.removeClass('selected')
        else
            $label.text(parseInt($label.text()) + 1)
            $btn.addClass('selected')
            if $sibling.hasClass('selected')
                $siblingLabel.text(parseInt($siblingLabel.text()) - 1)
            $sibling.removeClass('selected')


        $.get url, {'rating': $btn.data('rating')}
    # /end rating


    # delete account
    $('body').on 'click', '.delete-account-btn', (e) ->
        $('.content-header-btn').removeClass('active')
        $(e.currentTarget).addClass('active')
        showAlert('So... this is how it all ends?&nbsp;&nbsp;<i class="icon-heart-broken"></i><br/>
            <label class="delete-account-radio radio">
                <input type="radio" name="deleteAccount" value="disable" checked="checked">disable account and keep the synced data
            </label>
            <label class="radio">
                <input type="radio" name="deleteAccount" value="delete">delete account and all the data
            </label>
        ',
        '
            <div class="alert-buttons">
                <button class="btn confirm-account-delete">Yes, Proceed</button>
                <button class="btn cancel-account-delete">No</button>
            </div>
        ')
    $('body').on 'click', '.confirm-account-delete', ->
        $.post URLS.delete_account + '?action=' + $('input[name="deleteAccount"]:checked').attr('value'), ->
            window.location = URLS.login
    $('body').on 'click', '.cancel-account-delete', ->
        $('.delete-account-btn').removeClass('active')
        showAlert('A-ha! We knew you were just fooling around&nbsp;&nbsp;<i class="icon-heart"></i>', '', true)
    $('body').on 'click', '.delete-account-btn.active', (e) ->
        $(e.currentTarget).removeClass('active')
        hideAlert()
    # /end delete account

    # show/hide forms
    $('body').on 'click', '.show-form:not(".open")', (e) ->
        $(e.currentTarget).addClass('open')
        $(e.currentTarget).find('i').removeClass().addClass('icon-caret-up')
        $(e.currentTarget).next('form').removeClass('hidden').show()

    $('body').on 'click', '.show-form.open', (e) ->
        $form = $(e.currentTarget).next('form')
        hideForm($form)
    # /end show/hide forms


    # password forms
    $('body').on 'keyup keypress', ('.password-form'), (e) ->
        keyCode = e.keyCode or e.which
        if keyCode == 13
            e.preventDefault()
            return false

    $('body').on 'click', ('.submit-password-form-btn'), (e) ->
        e.preventDefault()
        $form = $(e.target).parents('form')
        hideFormErrors($form)
        $form.submit(
            $.ajax
                url: $form.attr('action')
                type: 'POST'
                data: $form.serializeArray()
                success: (response) ->
                    if response.errors
                        showFormErrors(response.errors, $form)
                    if response.success
                        showAlert(response.success, '', true)
                        hideForm($form)
        )
    # /end password forms


    # util functions
    showFormErrors = (errors, form) ->
        for errorField, errorText of errors
            $(form).find('input[name="'+ errorField + '"]').addClass('error-field').select()
            $(form).find('[data-for-field="'+ errorField + '"]').text(errorText)


    hideFormErrors = (form) ->
        $(form).find('.form-error').text('')
        $(form).find('input').removeClass('error-field')


    hideForm = (form) ->
        if $(form).hasClass('set-password-form')
            $(form).parents('.settings-section-content').remove()
            return false
        $(form).addClass('hidden').hide()
        $(form).prev().removeClass('open')
        $(form).prev().find('i').removeClass().addClass('icon-caret-down')
        $(form).find('.form-error').text('')
        $(form).find('input').removeClass('error-field')
        $(form)[0].reset()


    repositionPlayer = (player) ->
        $(window).on 'scroll', =>
            playerTop = $(player).offset().top
            playerHeight = $(player).height()
            playerPosition = playerTop - $(window).scrollTop() + playerHeight/3
            if playerPosition < 0 and $('.content-wrapper').find('.video-player.preview').length == 0
                console.log 'adding clong'
                $clone = $(player).find('.video-player').clone()
                $(player).find('.video-player').hide()
                $clone.addClass('preview')


    numSort = (a, b) ->
        return a - b

    getCookie = (name) ->
        cookieValue = null
        if document.cookie and document.cookie isnt ""
            cookies = document.cookie.split(";")
            i = 0
            while i < cookies.length
                cookie = jQuery.trim(cookies[i])
                if cookie.substring(0, name.length + 1) is (name + "=")
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
                i++
        cookieValue
    # /end util functions