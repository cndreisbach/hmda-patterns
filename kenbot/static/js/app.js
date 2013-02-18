(function ($, window, undefined) {
    'use strict';

    var $doc = $(document),
        Modernizr = window.Modernizr;

    $(document).ready(function () {
        $.fn.foundationAlerts ? $doc.foundationAlerts() : null;
        $.fn.foundationButtons ? $doc.foundationButtons() : null;
        $.fn.foundationAccordion ? $doc.foundationAccordion() : null;
        $.fn.foundationNavigation ? $doc.foundationNavigation() : null;
        $.fn.foundationTopBar ? $doc.foundationTopBar() : null;
        $.fn.foundationCustomForms ? $doc.foundationCustomForms() : null;
        $.fn.foundationMediaQueryViewer ? $doc.foundationMediaQueryViewer() : null;
        $.fn.foundationTabs ? $doc.foundationTabs({
            callback: $.foundation.customForms.appendCustomMarkup
        }) : null;
        $.fn.foundationTooltips ? $doc.foundationTooltips() : null;
        $.fn.foundationMagellan ? $doc.foundationMagellan() : null;
        $.fn.foundationClearing ? $doc.foundationClearing() : null;

        $.fn.placeholder ? $('input, textarea').placeholder() : null;
    });

    // UNCOMMENT THE LINE YOU WANT BELOW IF YOU WANT IE8 SUPPORT AND ARE USING .block-grids
    // $('.block-grid.two-up>li:nth-child(2n+1)').css({clear: 'both'});
    // $('.block-grid.three-up>li:nth-child(3n+1)').css({clear: 'both'});
    // $('.block-grid.four-up>li:nth-child(4n+1)').css({clear: 'both'});
    // $('.block-grid.five-up>li:nth-child(5n+1)').css({clear: 'both'});

    // Hide address bar on mobile devices (except if #hash present, so we don't mess up deep linking).
    if (Modernizr.touch && !window.location.hash) {
        $(window).load(function () {
            setTimeout(function () {
                window.scrollTo(0, 1);
            }, 0);
        });
    }
})(jQuery, this);

(function ($) {
    var tt = document.createElement('div'),
        leftOffset = -(~~$('html').css('padding-left').replace('px', '') + ~~$('body').css('margin-left').replace('px', '')),
        topOffset = -32;

    tt.className = 'ex-tooltip';
    document.body.appendChild(tt);

    var raceLabels = function (race) {
        var raceMap = {
            'Black or African American': 'Black',
            'Native Hawaiian or Other Pacific Islander': 'Pacific Islander',
            'American Indian or Alaska Native': 'Native American'
        };
        return raceMap[race] || race;
    };

    var updateDenialRates = function (msa_md) {
        $.get('/denial_rates_data/' + msa_md, function (data) {
            data = data.result.map(function (datum) {
                return {
                    "x": raceLabels(datum.race),
                    "y": datum.denial_rate,
                    "loan_purpose": datum.loan_purpose
                };
            }).groupBy(function (datum) {
                return datum.loan_purpose;
            });

            var chartData = {
                "xScale": "ordinal",
                "yScale": "linear",
                "main": [{
                    "className": ".msa",
                    "data": data['Home purchase'],
                    "legend": "Purchase"
                }, {
                    "className": ".msa2",
                    "data": data['Refinancing'],
                    "legend": "Refinancing"
                }]
            };

            var options = {
                "mouseover": function (d, i) {
                    var pos = $(this).offset();
                    $(tt).text(d.loan_purpose + " - " + d.y.round(2) + "%")
                        .css({
                        top: topOffset + pos.top,
                        left: pos.left + leftOffset
                    })
                        .show();
                },
                "mouseout": function (x) {
                    $(tt).hide();
                }
            };

            var raceChart = new xChart('bar',
            chartData,
                '#race-chart',
            options);
            draw_legend(chartData.main, $('#race-legend'));
        });
    };

    var updateDenialRatesByIncome = function (msa_md, container) {
        container = container || "#income-chart";

        $.get('/denial_by_income/' + msa_md, function (data) {
            data = data.result.map(function (datum) {
                return {
                    "x": datum.income_group * 1000,
                    "y": (datum.denial_percent / 100.0).round(4),
                    "income_group": datum.income_group,
                    "race": datum.race,
                    "total_denied": datum.total_denied
                };
            }).filter(function (datum) {
                return datum.income_group !== 999999;
            }).groupBy(function (datum) {
                return datum.race;
            });

            var chartData = [{
                "key": "White",
                "values": data['White']
            }, {
                "key": "Asian",
                "values": data['Asian']
            }, {
                "key": "Black",
                "values": data['Black or African American']
            }, {
                "key": "Pacific Islander",
                "values": data['Native Hawaiian or Other Pacific Islander']
            }, {
                "key": "Native American",
                "values": data['American Indian or Alaska Native']
            }];

            nv.addGraph(function () {
                var chart = nv.models.lineChart()
                    .color(d3.scale.category10().range());

                chart.xAxis.axisLabel('Income')
                    .tickFormat(d3.format(',r'));

                chart.yAxis.axisLabel('Denial Rate')
                    .tickFormat(d3.format('4.2p'));

                d3.select(container)
                    .datum(chartData)
                    .transition().duration(500)
                    .call(chart);

                nv.utils.windowResize(function () {
                    d3.select(container).call(chart);
                });
                return chart;
            });
        });
    };

    var nvDenialRatesByIncome = function () {
        $.get('/denial_by_income/' + msa_md, function (data) {
            data = data.result.map(function (datum) {
                return {
                    "x": datum.income_group,
                    "y": datum.denial_percent,
                    "income_group": datum.income_group,
                    "race": raceLabels(datum.race),
                    "total_denied": datum.total_denied
                };
            }).filter(function (datum) {
                return datum.income_group !== 999999;
            }).groupBy(function (datum) {
                return datum.race;
            });


        });
    };

    var updateHalGovBackedByIncome = function (msa_md) {
        $.get('/hal_gov_backed_by_income/' + msa_md, function (data) {
            var hal = [];
            var gov = [];
            data = data.result.each(function (datum) {
                var obj = {
                    x: datum.income_group,
                    y: datum.is_hal_percent
                };
                hal.push(obj);
                var obj2 = {
                    x: datum.income_group,
                    y: datum.is_gov_backed_percent
                };
                gov.push(obj2);
            });
            var chart_data = {
                "xScale": "ordinal",
                "yScale": "linear",
                "main": [{
                    "className": ".main.l1",
                    "data": hal,
                    legend: 'hal'
                }, {
                    "className": ".main.l2",
                    "data": gov,
                    legend: 'gov'
                }]
            };
            var options = {
                "tickFormatY": function (y) {
                    return y + '%';

                },
                "tickFormatX": function (x) {
                    return x == '999999' ? '$250,000+' : '$' + x + ',000';

                }
            };

            var myChart = new xChart('bar', chart_data, '#hal_income_chart', options);
            draw_legend(chart_data.main, $('#hal_income_legend'));
        });
    };

    var updateHalGovBackedByRace = function (msa_md) {
        $.get('/hal_gov_backed_by_race/' + msa_md, function (data) {
            var hal = [];
            var gov = [];
            data = data.result.each(function (datum) {
                var obj = {
                    x: raceLabels(datum.race),
                    y: datum.is_hal_percent
                };
                hal.push(obj);
                var obj2 = {
                    x: raceLabels(datum.race),
                    y: datum.is_gov_backed_percent
                };
                gov.push(obj2);
            });
            var chart_data = {
                "xScale": "ordinal",
                "yScale": "linear",
                "main": [{
                    "className": ".main.l1",
                    "data": hal,
                    legend: 'hal'
                }, {
                    "className": ".main.l2",
                    "data": gov,
                    legend: 'gov'
                }]
            };


            var options = {
                "tickFormatY": function (y) {
                    return y + '%';

                },
                "tickFormatX": function (d) {
                    return d.truncate(15, false);
                }
            };

            var myChart = new xChart('bar', chart_data, '#hal_race_chart', options);
            draw_legend(chart_data.main, $('#hal_race_legend'));
        });
    };

    var updateGovBackedByRacePurpose = function (msa_md) {
        $.get('/gov_backed_by_race_purpose/' + msa_md, function (_data) {
            var data = _data.result.map(

            function (datum) {
                return ({
                    x: raceLabels(datum.race),
                    y: datum.is_gov_backed_percent,
                    loan_purpose_name: datum.loan_purpose_name
                });
            }).groupBy(function (d) {
                return d.loan_purpose_name;
            });

            var chart_data = {
                "xScale": "ordinal",
                "yScale": "linear",
                "main": [{
                    "className": ".main.l1",
                    "data": data['refinance'],
                    legend: 'Refinance'
                }, {
                    "className": ".main.l2",
                    "data": data['purchase'],
                    legend: 'Purchase'
                }]
            };

            var options = {
                "tickFormatY": function (y) {
                    return y + '%';

                },
                "tickFormatX": function (d) {
                    return d.truncate(15, false);
                }
            };

            var myChart = new xChart('bar', chart_data, '#purpose_race_chart', options);
            draw_legend(chart_data.main, $('#purpose_race_legend'));
        });
    };

    var updateGovBackedByIncomePurpose = function (msa_md) {
        $.get('/gov_backed_by_income_purpose/' + msa_md, function (_data) {
            var data = _data.result.map(

            function (datum) {
                return ({
                    x: datum.income_group,
                    y: datum.is_gov_backed_percent,
                    loan_purpose_name: datum.loan_purpose_name
                });
            }).groupBy(function (d) {
                return d.loan_purpose_name;
            });
            var chart_data = {
                "xScale": "ordinal",
                "yScale": "linear",
                "main": [{
                    "className": ".main.l1",
                    "data": data['refinance'],
                    legend: 'Refinance'
                }, {
                    "className": ".main.l2",
                    "data": data['purchase'],
                    legend: 'Purchase'
                }]
            };
            var options = {
                "tickFormatY": function (y) {
                    return y + '%';

                },
                "tickFormatX": function (x) {
                    return x == '999999' ? '$250,000+' : '$' + x + ',000';
                }
            };
            var myChart = new xChart('bar', chart_data, '#purpose_income_chart', options);
            draw_legend(chart_data.main, $('#purpose_income_legend'));
        });
    };

    var draw_legend = function (data, container) {
        var ln = data.length - 1;
        for (i = 0; i <= ln; i++) {
            var legend_block = $('<div>').addClass('media legend_block');
            var color_block = $('<div>').addClass('color_block ' + 'color' + i);
            var img_block = $('<div>').addClass('img').append(color_block);
            var bd_block = $('<div>').html(data[i]['legend']).addClass('bd');
            legend_block.append(img_block).append(bd_block);
            container.append(legend_block);
        }
    };

    var activateSketchPad = function () {
        $(function () {
            $.each(['#f00', '#ff0', '#0f0', '#0ff', '#00f', '#f0f', '#000', '#fff'], function () {
                $('#sketch_pad .tools').append("<a href='#colors_sketch' data-color='" + this + "' style='width: 10px; background: " + this + ";'></a> ");
            });
            $.each([3, 5, 10, 15], function () {
                $('#sketch_pad .tools').append("<a href='#colors_sketch' data-size='" + this + "' style='background: #ccc'>" + this + "</a> ");
            });
            $('#colors_sketch').sketch();
        });
    };

    window.updateDenialRates = updateDenialRates;
    window.updateDenialRatesByIncome = updateDenialRatesByIncome;
    window.updateHalGovBackedByIncome = updateHalGovBackedByIncome;
    window.updateHalGovBackedByRace = updateHalGovBackedByRace;
    window.updateGovBackedByRacePurpose = updateGovBackedByRacePurpose;
    window.updateGovBackedByIncomePurpose = updateGovBackedByIncomePurpose;
    window.activateSketchPad = activateSketchPad;

    $(document).ready(function () {
        $('.chosen-select').chosen();

        $('#metro-form').on('submit', function (event) {
            event.preventDefault();
            var msa_md = $('#msa').find(":selected").val();
            var url = "/msa-report/" + msa_md;
            window.location = url;
        });
    });
})(jQuery);
