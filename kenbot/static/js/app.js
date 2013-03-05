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

  var numToPercent = function (n) {
    return (n / 100.0).round(4)
  };

  var incomeGroup = function (n) {
    if (n < 300) {
      return "$" + d3.format(',r')(n * 1000);
    } else {
      return "$300,000+";
    }
  }

  var setupChart = function (chart, container, data, fn) {
    nv.addGraph(function() {  
      chart.color(d3.scale.category10().range());

      fn(chart);

      d3.select(container)
        .datum(data)
        .transition().duration(500)
        .call(chart);
 
      nv.utils.windowResize(chart.update);
        
      return chart;
    });   
  }
  
  var raceLabels = function (race) {
    var raceMap = {
      'Black or African American': 'Black',
      'Native Hawaiian or Other Pacific Islander': 'Pacific Islander',
      'American Indian or Alaska Native': 'Native American'
    };
    return raceMap[race] || race;
  }

  var createChartData = function (data, keys) {
    return keys.map(function (key) {
      return {"key": key, "values": data[key]};
    });
  }

  var racesToShow = ['White', 'Black', 'Asian', 'Pacific Islander', 'Native American'];

  var updateDenialRates = function (msa_md, container) {
    container = container || "#race-chart";
    
    $.get('/denial_rates_data/' + msa_md, function (data, textStatus, xhr) {
      data = data.result.map(function (datum) {
        return {
          "x": raceLabels(datum.race),
          "y": numToPercent(datum.denial_rate),
          "race": raceLabels(datum.race),
          "loan_purpose": datum.loan_purpose
        };
      }).filter(function (datum) {
        return racesToShow.some(datum.race);
      }).groupBy(function (datum) {
        return datum.loan_purpose;
      });

      setupChart(nv.models.multiBarChart(),
                 container,
                 createChartData(data, ["Home purchase", "Refinancing"]),
                 function (chart) {
                   chart.yAxis
                     .axisLabel('Denial Rate')
                     .tickFormat(d3.format('4.2p'));
                 });                   
    });
  };

  var updateDenialRatesByIncome = function (msa_md, container) {
    container = container || "#income-chart";

    $.get('/denial_by_income/' + msa_md, function (data, textStatus, xhr) {
      data = data.result.map(function (datum) {
        return {
          "x": datum.income_group,
          "y": numToPercent(datum.denial_percent),
          "income_group": datum.income_group,
          "race": raceLabels(datum.race),
          "total_denied": datum.total_denied
        };
      }).groupBy(function (datum) {
        return datum.race;
      });

      console.log(data);
      
      setupChart(nv.models.lineChart(),
                 container,
                 createChartData(data, racesToShow),
                 function (chart) {
                   chart.xAxis
                     .axisLabel('Income')
                     .tickFormat(incomeGroup);
 
                   chart.yAxis
                     .axisLabel('Denial Rate')
                     .tickFormat(d3.format('4.2p'));
                 });
    });
  }

  var updateHalGovBackedByIncome = function(msa_md, container) {
    container = container || "#hal-income-chart";

    $.get('/hal_gov_backed_by_income/' + msa_md, function(data, textStatus, xhr){
      data = data.result.map(function (datum) {
        return [
          { "x": datum.income_group,
            "y": numToPercent(datum.is_hal_percent),
            "loan_type": "HAL",
            "income_group": datum.income_group
          },
          {
            "x": datum.income_group,
            "y": numToPercent(datum.is_gov_backed_percent),
            "loan_type": "Government-backed",
            "income_group": datum.income_group            
          }
        ];
      }).flatten().groupBy(function (datum) {
        return datum.loan_type;
      });

      setupChart(nv.models.multiBarChart(),
                 container,
                 createChartData(data, ["HAL", "Government-backed"]),
                 function (chart) {
                   chart.xAxis
                     .axisLabel('Income')
                     .tickFormat(incomeGroup);
        
                   chart.yAxis
                     .tickFormat(d3.format('4.2p'));
                 });                   
    });
  };

  var updateHalGovBackedByRace = function (msa_md, container) {
    container = container || '#hal-race-chart';
    $.get('/hal_gov_backed_by_race/' + msa_md, function(data, textStatus, xhr){
      data = data.result.map(function (datum) {
        return [
          { "x": raceLabels(datum.race),
            "y": numToPercent(datum.is_hal_percent),
            "loan_type": "HAL",
            "race": raceLabels(datum.race)
          },
          { "x": raceLabels(datum.race),            
            "y": numToPercent(datum.is_gov_backed_percent),
            "loan_type": "Government-backed",
            "race": raceLabels(datum.race)              
          }
        ];
      }).flatten().filter(function (datum) {
        return racesToShow.some(datum.race);          
      }).groupBy(function (datum) {
        return datum.loan_type;
      });

      setupChart(nv.models.multiBarChart(),
                 container,
                 createChartData(data, ["HAL", "Government-backed"]),
                 function (chart) {    
                   chart.yAxis
                     .tickFormat(d3.format('4.2p')); 
                 });
    });
  };

  var updateGovBackedByRacePurpose = function (msa_md, container) {
    container = container || '#purpose-race-chart';
    
    $.get('/gov_backed_by_race_purpose/' + msa_md, function(data, textStatus, xhr){
      var data = data.result.map(function (datum) {
        return {
          "x": raceLabels(datum.race),
          "y": numToPercent(datum.is_gov_backed_percent),
          "race": raceLabels(datum.race),
          "loan_purpose_name": datum.loan_purpose_name
        };
     }).filter(function (datum) {
        return racesToShow.some(datum.race);        
      }).groupBy(function(d){
        return d.loan_purpose_name;
      });

      setupChart(nv.models.multiBarChart(),
                 container,
                 createChartData(data, ["Home purchase", "Refinancing"]),
                 function (chart) {    
                   chart.yAxis
                     .tickFormat(d3.format('4.2p')); 
                 });
    });
  };

  var updateGovBackedByIncomePurpose = function (msa_md, container) {
    container = container || '#purpose-income-chart';
    
    $.get('/gov_backed_by_income_purpose/' + msa_md, function (data, textStatus, xhr) {
      var data = data.result.map(
        function (datum) {
          return {
            'x': datum.income_group,
            'y': numToPercent(datum.is_gov_backed_percent),
            'loan_purpose_name': datum.loan_purpose_name,
            'income_group': datum.income_group
          };
        }).groupBy(function(d){
          return d.loan_purpose_name;
        });

      setupChart(nv.models.multiBarChart(),
                 container,
                 createChartData(data, ["Home purchase", "Refinancing"]),
                 function (chart) {
                   chart.xAxis
                     .axisLabel('Income')
                     .tickFormat(incomeGroup);

                   chart.yAxis
                     .tickFormat(d3.format('4.2p')); 
                 });      
    });
  };

  window.updateDenialRates = updateDenialRates;
  window.updateDenialRatesByIncome = updateDenialRatesByIncome;
  window.updateHalGovBackedByIncome = updateHalGovBackedByIncome;
  window.updateHalGovBackedByRace = updateHalGovBackedByRace;
  window.updateGovBackedByRacePurpose = updateGovBackedByRacePurpose;
  window.updateGovBackedByIncomePurpose = updateGovBackedByIncomePurpose;

  $(document).ready(function () {
    $('.chosen-select').chosen();

    $('#metro-form').on('submit', function (event) {
      event.preventDefault();
      var msa_md = $('#msa').find(":selected").val();
      var url = "/metro/" + msa_md;
      window.location = url;
    });

    $('#metro-comparison-form').on('submit', function (event) {
      event.preventDefault();
      var msa_md1 = $('#msa1').find(":selected").val();
      var msa_md2 = $('#msa2').find(":selected").val();
      var url = "/compare/" + msa_md1 + "/" + msa_md2;
      window.location = url;
    });

    $('.tabs').foundationTabs({
      callback: function () {
        $(window).trigger('resize');
      }
    });
  });
})(jQuery);

