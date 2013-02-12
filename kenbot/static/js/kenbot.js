(function ($) {
  var tt = document.createElement('div'),
      leftOffset = -(~~$('html').css('padding-left').replace('px', '') + ~~$('body').css('margin-left').replace('px', '')),
      topOffset = -32;

  tt.className = 'ex-tooltip';
  document.body.appendChild(tt);

  var updateDenialRates = function (msa_md) {    
    $.get('/denial_rates_data/' + msa_md, function (data, textStatus, xhr) {
      data = data.result.map(function (datum) {
        return {
          "x": datum.race,
          "y": datum.denial_rate,
          "loan_purpose": datum.loan_purpose
        };
      }).groupBy(function (datum) {
        return datum.loan_purpose;
      });

      var chartData = {
        "xScale": "ordinal",
        "yScale": "linear",
        "main": [
          {
            "className": ".msa",
            "data": data['Home purchase'],
            "legend": "Purchase"
          },
          {
            "className": ".msa2",
            "data": data['Refinancing'],
            "legend": "Refinancing"
          }
        ]
      };
      
      var options = {
        "tickFormatX": function (d) {
          return d.truncate(25, false);
        },
        "mouseover": function (d, i) {
          var pos = $(this).offset();
          $(tt).text(d.loan_purpose + " - " + d.y.round(2) + "%")
            .css({top: topOffset + pos.top, left: pos.left + leftOffset})
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

  var updateDenialRatesByIncome = function (msa_md) {
    $.get('/denial_by_income/' + msa_md, function (data, textStatus, xhr) {
      data = data.result.map(function (datum) {
        return {
          "x": datum.income_group,
          "y": datum.denial_percent,
          "income_group": datum.income_group,
          "race": datum.race,
          "total_denied": datum.total_denied
        };
      }).filter(function (datum) {
        return datum.income_group !== 999999;
      }).groupBy(function (datum) {
        return datum.race;
      });

      var chartData = {
        "xScale": "linear",
        "yScale": "linear",
        "main": [
          {
            "className": ".white",
            "data": data['White']
          },
          {
            "className": ".asian",
            "data": data['Asian']
          },
          {
            "className": ".black",
            "data": data['Black or African American']
          },
          {
            "className": ".pacific",
            "data": data['Native Hawaiian or Other Pacific Islander']
          },
          {
            "className": ".first-nations",
            "data": data['American Indian or Alaska Native']
          }
        ]
      };

      var options = {
        "xMin": 30,
        "xMax": 150,
        "tickFormatX": function (d) {
          return "$" + (d * 1000).format();
        },
        "mouseover": function (d, i) {
          var pos = $(this).offset();
          $(tt).text(d.race + " - " + d.y.round(2) + "%")
            .css({top: topOffset + pos.top, left: pos.left + leftOffset})
            .show();
        },
        "mouseout": function (x) {
          $(tt).hide();
        }
      };

      var incomeChart = new xChart('line-dotted',
                                  chartData,
                                  '#income-chart',
                                  options);
    });
  };

  var updateHalGovBackedByIncome = function(msa_md) {
      $.get('/hal_gov_backed_by_income/' + msa_md, function(data, textStatus, xhr){
          var hal = [];
          var gov = [];
          data = data.result.each(function (datum) {
              var obj = {x: datum.income_group, y:datum.is_hal_percent};
              hal.push(obj);
              var obj2 = {x: datum.income_group, y:datum.is_gov_backed_percent};
              gov.push(obj2);
          })
          var chart_data = {
              "xScale": "ordinal",
              "yScale": "linear",
              "main": [
                  {"className":".main.l1","data":hal, legend:'hal'},
                  {"className":".main.l2","data":gov, legend:'gov'}
              ]
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

  var updateHalGovBackedByRace = function(msa_md) {
      $.get('/hal_gov_backed_by_race/' + msa_md, function(data, textStatus, xhr){
          var hal = [];
          var gov = [];
          data = data.result.each(function (datum) {
              var obj = {x: datum.race, y:datum.is_hal_percent};
              hal.push(obj);
              var obj2 = {x: datum.race, y:datum.is_gov_backed_percent};
              gov.push(obj2);
          })
          var chart_data = {
              "xScale": "ordinal",
              "yScale": "linear",
              "main": [
                  {"className":".main.l1","data":hal, legend:'hal'},
                  {"className":".main.l2","data":gov, legend:'gov'}
              ]
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

  var updateGovBackedByRacePurpose = function(msa_md){
      $.get('/gov_backed_by_race_purpose/' + msa_md, function(data, textStatus, xhr){
          var data = data.result.map(
              function(datum){return({
                  x:datum.race,
                  y:datum.is_gov_backed_percent,
                  loan_purpose_name:datum.loan_purpose_name
              });
              }).groupBy(function(d){
                  return d.loan_purpose_name;
              });
          var chart_data = {
              "xScale": "ordinal",
              "yScale": "linear",
              "main": [
                  {"className":".main.l1","data":data['refinance'], legend:'Refinance'},
                  {"className":".main.l2","data":data['purchase'], legend:'Purchase'}
              ]
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

  var updateGovBackedByIncomePurpose = function(msa_md){
      $.get('/gov_backed_by_income_purpose/' + msa_md, function(data, textStatus, xhr){
          var data = data.result.map(
              function(datum){return({
                  x:datum.income_group,
                  y:datum.is_gov_backed_percent,
                  loan_purpose_name:datum.loan_purpose_name
              });
              }).groupBy(function(d){
                  return d.loan_purpose_name;
              });
          var chart_data = {
              "xScale": "ordinal",
              "yScale": "linear",
              "main": [
                  {"className":".main.l1","data":data['refinance'], legend:'Refinance'},
                  {"className":".main.l2","data":data['purchase'], legend:'Purchase'}
              ]
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

  var draw_legend = function(data, container){
    var ln = data.length - 1;
    for (i = 0; i<= ln; i++){
        var legend_block = $('<div>').addClass('media legend_block');
        var color_block = $('<div>').addClass('color_block ' + 'color' + i);
        var img_block = $('<div>').addClass('img').append(color_block);
        var bd_block = $('<div>').html(data[i]['legend']).addClass('bd')
        legend_block.append(img_block).append(bd_block);
        container.append(legend_block);
    }
  };

  var activateSketchPad = function(){
      $(function() {
          $.each(['#f00', '#ff0', '#0f0', '#0ff', '#00f', '#f0f', '#000', '#fff'], function() {
              $('#sketch_pad .tools').append("<a href='#colors_sketch' data-color='" + this + "' style='width: 10px; background: " + this + ";'></a> ");
          });
          $.each([3, 5, 10, 15], function() {
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

