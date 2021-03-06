var casper = casper || {};
var phantom = phantom || {};
var document_list_url = casper.cli.options['url'];
var slug = casper.cli.options['slug'];
var b1_id = casper.cli.options['b1_id'];
var b2_id = casper.cli.options['b2_id'];

function inject_cookies() {
    var m = casper.cli.options['url-base'].match(/https?:\/\/([^:]+)(:\d+)?\//);
    var domain = m ? m[1] : 'localhost';

    for (var key in casper.cli.options) {
        if (key.indexOf('cookie-') === 0) {
            var cn = key.substring('cookie-'.length);
            var c = phantom.addCookie({
                name: cn,
                value: casper.cli.options[key],
                domain: domain
            });
        }
    }
}
inject_cookies();


casper.test.begin('Bookmarks are loaded upon page load', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        var select = casper.getHTML('select#id_bookmark');
        test.assertMatch(select, /search_terms=hazop/);
        test.assertMatch(select, /sort_by=current_revision/);
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Search is updated when a bookmark is selected', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.viewport(1024, 768);
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        casper.evaluate(function(b1_id) {
            $('#id_bookmark option#bookmark_' + b1_id).prop('selected', true);
            $('#id_bookmark').change();
        }, b1_id);
        casper.wait(50);
    });

    casper.then(function() {
        test.assertUrlMatch(/search_terms=hazop/);
    });

    casper.then(function() {
        casper.evaluate(function(b2_id) {
            $('#id_bookmark option#bookmark_' + b2_id).prop('selected', true);
            $('#id_bookmark').change();
        }, b2_id);
        casper.wait(50);
    });

    casper.then(function() {
        test.assertUrlMatch(/sort_by=current_revision/);

        // previous url parameters are reset
        var url = casper.getCurrentUrl();
        test.assert(!url.match(/search_terms=hazop/));
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('The bookmark is unselected when the search is refined', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.click('button#toggle-filters-button');
        casper.evaluate(function(b1_id) {
            $('#id_bookmark option#bookmark_' + b1_id).prop('selected', true);
            $('#id_bookmark').change();
        }, b1_id);
        casper.wait(50);
    });

    casper.then(function() {
        test.assertField('bookmark', slug + '?search_terms=hazop');
    });

    casper.then(function() {
        casper.fill('#table-filters', {
            'search_terms': 'receiving'
        });
        casper.sendKeys('#id_search_terms', casper.page.event.key.Enter, {keepFocus: true});
        casper.wait(300);
    });

    casper.then(function() {
        test.assertField('bookmark', '');
    });

    casper.run(function() {
        test.done();
    });
});

casper.test.begin('Bookmarking a search', 0, function suite(test) {
    casper.start(document_list_url, function() {
        casper.viewport(1024, 768);
        test.assertNotVisible('#bookmark-form');
        casper.click('button#toggle-filters-button');
    });

    casper.then(function() {
        casper.click('button#bookmark-button');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertVisible('#bookmark-modal');
        casper.fill('#bookmark-form', {
            'name': 'Test bookmark'
        }, true);
        casper.wait(500);
    });

    casper.then(function() {
        test.assertNotVisible('#bookmark-form');
        casper.click('button#bookmark-button');
        casper.wait(500);
    });

    casper.then(function() {
        test.assertField('name', '');
    });

    casper.run(function() {
        test.done();
    });
});
