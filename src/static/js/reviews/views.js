var Phase = Phase || {};

(function(exports, Phase, Backbone, _) {
    "use strict";

    var dispatcher = Phase.Events.dispatcher;

    Phase.Views = Phase.Views || {};

    /**
     * The table containing the list of waiting reviews.
     */
    Phase.Views.TableView = Backbone.View.extend({
        el: '#documents',
        events: {
            'click input[type=checkbox]': 'selectReview'
        },
        selectReview: function(event) {
            var target = $(event.currentTarget);
            var reviewId = target.data('review-id');
            var checked = target.is(':checked');

            if (checked) {
                this.collection.add({id: reviewId});
            } else {
                this.collection.remove(reviewId);
            }
        }
    });

    /**
     * The form with reviews batch actions.
     *
     * When a review is selected and thus added to / removed from the
     * collection, we add / delete the related hidden inputs in the form.
     */
    Phase.Views.ActionForm = Backbone.View.extend({
        el: '#review-batch-action-form',
        events: {
            'submit': 'batchCloseReviews'
        },
        initialize: function(options) {
            _.bindAll(this, 'batchSuccess', 'batchPoll', 'batchPollSuccess');

            this.progress = options.progress;
            this.button = this.$el.find('button');

            this.listenTo(this.collection, 'add', this.addReview);
            this.listenTo(this.collection, 'remove', this.removeReview);
            this.listenTo(this.collection, 'update', this.showButton);
        },
        addReview: function(model, collection, options) {
            var input = $('<input type="hidden" name="review_ids"></input>');
            input.attr('id', 'review-id-' + model.get('id'));
            input.val(model.get('id'));
            this.$el.append(input);
        },
        removeReview: function(model, collection, options) {
            var id ='#review-id-' + model.get('id');
            var input = this.$el.find(id);
            input.remove();
        },
        showButton: function(collection, options) {
            if (collection.length === 0) {
                this.button.addClass('disabled');
            } else {
                this.button.removeClass('disabled');
            }
        },
        /**
         * Submit the "close review" form as ajax.
         */
        batchCloseReviews: function(event) {
            event.preventDefault();

            var data = this.$el.serialize();
            var url = this.$el.attr('action');
            $.post(url, data, this.batchSuccess);
        },
        batchSuccess: function(data) {
            var pollUrl = data.poll_url;
            this.pollId = setInterval(this.batchPoll, 1000, pollUrl);
        },
        batchPoll: function(pollUrl) {
            $.get(pollUrl, this.batchPollSuccess);
        },
        batchPollSuccess: function(data) {
            this.progress.set('progress', data.progress);
            if (data.done) {
                clearInterval(this.pollId);
                location.reload();
            }
        }
    });

    /**
     * Handle the "pick a distribution list" widget.
     */
    Phase.Views.PickDistribListWidgetView = Backbone.View.extend({
        el: '#pick-distrib-list-field',
        initialize: function() {
            _.bindAll(this, 'selectList');

            this.collection = new Phase.Collections.DistributionListCollection(
                null, {
                apiUrl: this.apiUrl});

            this.apiUrl = this.$el.data('api-url');
            this.select = this.$el.find('select');

            var that = this;
            this.select.selectize({
                plugins: {
                    'no_results': {message: 'No corresponding list was found.'}
                },
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                mode: 'single',
                create: false,
                preload: true,
                onOptionAdd: function(value, data) {
                    that.collection.add(data);
                },
                load: function(query, callback) {
                    $.ajax({
                        url: that.apiUrl,
                        type: 'GET',
                        dataType: 'json',
                        data: {
                            q: query,
                            page_limit: 10,
                        },
                        error: function() {
                            callback();
                        },
                        success: function(res) {
                            callback(res.results);
                        }
                    });
                }
            });
            this.selectize = this.select[0].selectize;
            this.selectize.on('item_add', this.selectList);
        },
        selectList: function(value) {
            if (value >= 0) {
                var list = this.collection.get(value);
                dispatcher.trigger('onLeaderSelected', list.get('leader'));
                dispatcher.trigger('onApproverSelected', list.get('approver'));
                dispatcher.trigger('onReviewersSelected', list.get('reviewers'));
            } else {
                this.selectize.clear();
            }
        }
    });

    Phase.Views.LeaderWidgetView = Backbone.View.extend({
        el: '#id_leader',
        initialize: function() {
            this.listenTo(dispatcher, 'onLeaderSelected', this.setValue);
            this.selectize = this.$el[0].selectize;
        },
        setValue: function(leader) {
            this.selectize.addOption(leader);
            this.selectize.addItem(leader.id);
        }
    });

    Phase.Views.ApproverWidgetView = Backbone.View.extend({
        el: '#id_approver',
        initialize: function() {
            this.listenTo(dispatcher, 'onApproverSelected', this.setValue);
            this.selectize = this.$el[0].selectize;
        },
        setValue: function(approver) {
            if (approver !== null) {
                this.selectize.addOption(approver);
                this.selectize.addItem(approver.id);
            } else {
                this.selectize.clear();
            }
        }
    });

    Phase.Views.ReviewersWidgetView = Backbone.View.extend({
        el: '#id_reviewers',
        initialize: function() {
            this.listenTo(dispatcher, 'onReviewersSelected', this.setValue);
            this.selectize = this.$el[0].selectize;
        },
        setValue: function(reviewers) {
            this.selectize.clear();
            if (reviewers !== null ) {
                var selectize = this.selectize;
                _.each(reviewers, function(reviewer) {
                    selectize.addOption(reviewer);
                    selectize.addItem(reviewer.id);
                });
            }
        }
    });

    Phase.Views.InternalReviewView = Backbone.View.extend({
        /* On document creation and edit, we have to disable or enable purpose
        of issue widget according to internal review widget state.
        Poi is disabled if document is for internal review only. */
        el: '#fieldset-outgoing-transmittal',
            events: {
            "change #id_internal_review": "handleChange"
        },
        initialize: function() {
            // When editing a form, initialize the proper widget state
            this.poiField= $('#id_purpose_of_issue');
            this.togglePoi($('#id_internal_review').val());
        },
        togglePoi: function(disable) {
            if (disable === 'True') {
                this.poiField.prop('disabled', true);
            }else{
                this.poiField.prop('disabled', false);
            }
        },
        handleChange: function(el){
            this.togglePoi(el.target.value);
            // We set the poi select value to empty, only on internal
            // review change event.
            this.poiField.val('');
        }
    });

})(this, Phase, Backbone, _);
