(function ($) {
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
        "type": "bar",
        "main": [
          {
            "className": ".msa",
            "data": data['Home purchase']
          },
          {
            "className": ".msa2",
            "data": data['Refinancing']
          }
        ]
      };

      var tt =
        document.createElement('div'),
        leftOffset = -(~~$('html').css('padding-left').replace('px', '') + ~~$('body').css('margin-left').replace('px', '')),
        topOffset = -32;

      tt.className = 'ex-tooltip';
      document.body.appendChild(tt);
      
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
      
      var firstChart = new xChart('bar',
                                  chartData,
                                  '#first-chart',
                                  options);
    });
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

