
(function ($) {

    var start_navigation = function () {
        var $navigation = $('ul.nav-level-1');
        var $opened = $([]);
        var queue = $.Deferred();
        queue.resolve();

        var open = function($openning) {
            if ($opened.length) {
                if ($openning !== undefined && $openning.is($opened)) {
                    return;
                };
                queue = queue.pipe((function($closing) {
                    return function() {
                        $opened = $([]);
                        return $closing.fadeOut('fast').promise();
                    };
                })($opened));
            };
            if ($openning !== undefined) {
                queue = queue.pipe(function() {
                    $openning.show();
                    $opened = $openning;
                    return {};
                });
            };
        };

        $navigation.delegate(
            'li.nav-entry-1 > a span', 'mouseenter',
            function() {
                open($(this).parent().next('.nav-level-2'));
            });
        $navigation.delegate(
            '.nav-level-2', 'mouseleave',
            function() {
                open();
            });
    };

    $(document).ready(function() {
      start_navigation();
    });
})(jQuery);
