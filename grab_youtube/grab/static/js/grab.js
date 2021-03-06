// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var getCookie, hideForm, hideFormErrors, numSort, repositionPlayer, showFormErrors;
    $.ajaxSetup({
      cache: false,
      beforeSend: (function(_this) {
        return function(xhr, settings) {
          return xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        };
      })(this)
    });
    $('#search-input').on('keyup', function(e) {
      var q, visibleVideos;
      q = $.trim($(e.target).val()).toUpperCase();
      visibleVideos = [];
      return $('.video').each(function(idx, video) {
        var $videoClone, index, insertAfter, pos;
        pos = $(video).data('div-position');
        visibleVideos.push(pos);
        if ($(video).data('title').toUpperCase().indexOf(q) > -1) {
          index = visibleVideos.indexOf(pos);
          if (index === -1) {
            visibleVideos.push(index);
          }
          visibleVideos.sort(numSort);
          insertAfter = visibleVideos[visibleVideos.indexOf(pos) - 1];
          if (insertAfter) {
            return $('*[data-div-position="' + insertAfter + '"]').after($(video));
          } else {
            return $('.videos').prepend($(video));
          }
        } else {
          index = visibleVideos.indexOf(pos);
          if (index > -1) {
            visibleVideos.splice(index, 1);
          }
          $videoClone = $(video).clone();
          $(video).remove();
          return $('.hidden-videos').append($videoClone);
        }
      });
    });
    $('[rel="tooltip"]').on('mouseenter', function(e) {
      var $el, text;
      $el = $(e.target);
      return text = $el.attr('title');
    });
    $('body').on('click', '.archive-video-btn', function(e) {
      if ($(e.currentTarget).hasClass('active')) {
        $(e.currentTarget).removeClass('active');
        hideAlert();
        return false;
      }
      $('.content-header-btn').not('.secondary').removeClass('active');
      $(e.currentTarget).addClass('active');
      return showAlert('Archive video?', '<div class="alert-buttons"> <button class="btn confirm-archive">Yes</button><button class="btn cancel-archive">No</button> </div>');
    });
    $('body').on('click', '.confirm-archive', function() {
      var url;
      url = '/video/' + $('#video-detail').data('video-id') + '/archive-video/';
      return $.get(url, function(response) {
        showAlert('This video has been archived. It will not show up in your video list.', '<div class="alert-buttons"> <button class="btn restore-video-btn">Restore</button> </div>');
        return $('.archive-video-btn').remove();
      });
    });
    $('body').on('click', '.cancel-archive', function() {
      $('.archive-video-btn').removeClass('active');
      return hideAlert();
    });
    $('body').on('click', '.restore-video-btn', function(e) {
      var url;
      url = '/video/' + $('#video-detail').data('video-id') + '/restore-video/';
      return $.get(url, function(response) {
        showAlert('This video has been restored', '', true);
        return $('#share-date').before('<a class="archive-video-btn content-header-btn" href="javascript:"> <i class="icon-archive"></i> </a>');
      });
    });
    $('body').on('mouseenter', '.sort-videos-btn', function(e) {
      if ($(e.currentTarget).hasClass('active')) {
        return false;
      }
      return $(e.currentTarget).addClass('active');
    });
    $('body').on('mouseleave', '.sort-videos-btn', function(e) {
      return $(e.currentTarget).removeClass('active');
    });
    $('body').on('click', '.sort-videos-link', function(e) {
      return window.location.href = URLS.sort_url + '&sort=' + $(e.target).data('sort');
    });
    $('.video-rating').on('click', function(e) {
      var $btn, $div, $icon, $label, $sibling, $siblingLabel, url;
      if (!$(e.target).hasClass('label-icon')) {
        return false;
      }
      $div = $(e.currentTarget);
      $icon = $(e.target);
      $btn = $icon.parents('.video-rating-btn');
      $label = $icon.next();
      url = $div.data('rate-url');
      if ($btn.hasClass('disabled')) {
        return false;
      }
      $sibling = $btn.siblings('.video-rating-btn');
      $siblingLabel = $sibling.find('label');
      if ($btn.hasClass('selected')) {
        $label.text(parseInt($label.text()) - 1);
        $btn.removeClass('selected');
      } else {
        $label.text(parseInt($label.text()) + 1);
        $btn.addClass('selected');
        if ($sibling.hasClass('selected')) {
          $siblingLabel.text(parseInt($siblingLabel.text()) - 1);
        }
        $sibling.removeClass('selected');
      }
      return $.get(url, {
        'rating': $btn.data('rating')
      });
    });
    $('body').on('click', '.delete-account-btn', function(e) {
      $('.content-header-btn').removeClass('active');
      $(e.currentTarget).addClass('active');
      return showAlert('So... this is how it all ends?&nbsp;&nbsp;<i class="icon-heart-broken"></i><br/> <label class="delete-account-radio radio"> <input type="radio" name="deleteAccount" value="disable" checked="checked">disable account and keep the synced data </label> <label class="radio"> <input type="radio" name="deleteAccount" value="delete">delete account and all the data </label>', '<div class="alert-buttons"> <button class="btn confirm-account-delete">Yes, Proceed</button> <button class="btn cancel-account-delete">No</button> </div>');
    });
    $('body').on('click', '.confirm-account-delete', function() {
      return $.post(URLS.delete_account + '?action=' + $('input[name="deleteAccount"]:checked').attr('value'), function() {
        return window.location = URLS.login;
      });
    });
    $('body').on('click', '.cancel-account-delete', function() {
      $('.delete-account-btn').removeClass('active');
      return showAlert('A-ha! We knew you were just fooling around&nbsp;&nbsp;<i class="icon-heart"></i>', '', true);
    });
    $('body').on('click', '.delete-account-btn.active', function(e) {
      $(e.currentTarget).removeClass('active');
      return hideAlert();
    });
    $('body').on('click', '.show-form:not(".open")', function(e) {
      $(e.currentTarget).addClass('open');
      $(e.currentTarget).find('i').removeClass().addClass('icon-caret-up');
      return $(e.currentTarget).next('form').removeClass('hidden').show();
    });
    $('body').on('click', '.show-form.open', function(e) {
      var $form;
      $form = $(e.currentTarget).next('form');
      return hideForm($form);
    });
    $('body').on('keyup keypress', '.password-form', function(e) {
      var keyCode;
      keyCode = e.keyCode || e.which;
      if (keyCode === 13) {
        e.preventDefault();
        return false;
      }
    });
    $('body').on('click', '.submit-password-form-btn', function(e) {
      var $form;
      e.preventDefault();
      $form = $(e.target).parents('form');
      hideFormErrors($form);
      return $form.submit($.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: $form.serializeArray(),
        success: function(response) {
          if (response.errors) {
            showFormErrors(response.errors, $form);
          }
          if (response.success) {
            showAlert(response.success, '', true);
            return hideForm($form);
          }
        }
      }));
    });
    showFormErrors = function(errors, form) {
      var errorField, errorText, results;
      results = [];
      for (errorField in errors) {
        errorText = errors[errorField];
        $(form).find('input[name="' + errorField + '"]').addClass('error-field').select();
        results.push($(form).find('[data-for-field="' + errorField + '"]').text(errorText));
      }
      return results;
    };
    hideFormErrors = function(form) {
      $(form).find('.form-error').text('');
      return $(form).find('input').removeClass('error-field');
    };
    hideForm = function(form) {
      if ($(form).hasClass('set-password-form')) {
        $(form).parents('.settings-section-content').remove();
        return false;
      }
      $(form).addClass('hidden').hide();
      $(form).prev().removeClass('open');
      $(form).prev().find('i').removeClass().addClass('icon-caret-down');
      $(form).find('.form-error').text('');
      $(form).find('input').removeClass('error-field');
      return $(form)[0].reset();
    };
    repositionPlayer = function(player) {
      return $(window).on('scroll', (function(_this) {
        return function() {
          var $clone, playerHeight, playerPosition, playerTop;
          playerTop = $(player).offset().top;
          playerHeight = $(player).height();
          playerPosition = playerTop - $(window).scrollTop() + playerHeight / 3;
          if (playerPosition < 0 && $('.content-wrapper').find('.video-player.preview').length === 0) {
            console.log('adding clong');
            $clone = $(player).find('.video-player').clone();
            $(player).find('.video-player').hide();
            return $clone.addClass('preview');
          }
        };
      })(this));
    };
    numSort = function(a, b) {
      return a - b;
    };
    return getCookie = function(name) {
      var cookie, cookieValue, cookies, i;
      cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        cookies = document.cookie.split(";");
        i = 0;
        while (i < cookies.length) {
          cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
          i++;
        }
      }
      return cookieValue;
    };
  });

}).call(this);

//# sourceMappingURL=grab.js.map
