class VideoListView extends Backbone.View
    events:
        'click .delete-all-btn': 'deleteVideos'
    initialize: ->
        console.log 'init video list', @$el

    deleteVideos: (e) ->



new VideoListView(el: $('#video-list'))