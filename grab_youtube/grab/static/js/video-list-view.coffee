class VideoListView extends Backbone.View
    events:
        'click .delete-all-btn': 'alertDeleteVideos'
        'click .delete-all-btn.active': 'cancel'
        'click .cancel-delete': 'cancel'
        'click .sync-btn': 'syncVideos'
        'click .thumbnail': 'showInlinePlayer'
        'click .close-btn': 'closeInlinePlayer'

    initialize: ->
        alertView.showAlert()
        $('.sync-btn').on 'click', (e) =>
            @syncVideos($(e.target))

    alertDeleteVideos: (e) ->
        @$('.content-header-btn').not('.secondary').removeClass('active')
        $(e.currentTarget).addClass('active')
        alertView.showAlert(
            buttons: '<a href="' + URLS.delete_videos + '" class="btn confirm-delete">Yes</a><button class="btn cancel-delete">No</button>',
            message: 'Delete all your synced videos?'
        )

    cancel: ->
        @$('.delete-all-btn').removeClass('active')
        alertView.hideAlert()

    syncVideos: (btn) ->
        $btn = $(btn)
        $btn.removeClass('active').addClass('busy').attr('disabled', 'disabled').text('Syncing')
#        $(e.target).addClass('busy')
        alertView.showAlert(message: '<i class="spinner icon-contrast"></i>Retrieving YouTube videos from your Facebook timeline...')
        $.get URLS.sync_videos, (response) =>
            @$('.date.faded').text('Synced just now')
            $btn.removeClass('busy').prop('disabled', '').text('Sync Videos')

            if response > 0
                @$('#video-list').load window.location.pathname + " #video-list-content"
                alertView.showAlert(
                    message: response + ' new videos found and synced',
                    showCloseBtn: true
                )
            else
                alertView.showAlert(message: 'No new videos were found', showCloseBtn: true)

    showInlinePlayer: (e) ->
        @$('#video-container').remove()
        @$('.player-open.arrow').remove()
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

    closeInlinePlayer: (e) ->
        $(e.target).parent().remove()
#        $('.mask').remove()
        @$('.player-open.arrow').remove()


new VideoListView(el: $('.content'))