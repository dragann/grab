class VideoListView extends Backbone.View
    events:
        'click .delete-all-btn': 'alertDeleteVideos'
        'click .delete-all-btn.active': 'cancel'
        'click .cancel-delete': 'cancel'
        'click .sync-btn': 'syncVideos'

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


new VideoListView(el: $('.content'))