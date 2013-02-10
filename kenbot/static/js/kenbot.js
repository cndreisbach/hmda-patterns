(function ($) {
  $(document).ready(function () {
    $('.chosen-select').chosen();

    $('#metro-form').on('submit', function (event) {
      event.preventDefault();

      var msa_md = $('#msa').find(":selected").val();
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

        console.log(data);

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

        var options = {
          "tickFormatX": function (d) {
            return d.truncate(25, false);
          }
        };
          
        var firstChart = new xChart('bar',
                                    chartData,
                                    '#first-chart',
                                    options);
      });
    });

   if(true){
       $(function() {
           $.each(['#f00', '#ff0', '#0f0', '#0ff', '#00f', '#f0f', '#000', '#fff'], function() {
               $('#sketch_pad .tools').append("<a href='#colors_sketch' data-color='" + this + "' style='width: 10px; background: " + this + ";'></a> ");
           });
           $.each([3, 5, 10, 15], function() {
               $('#sketch_pad .tools').append("<a href='#colors_sketch' data-size='" + this + "' style='background: #ccc'>" + this + "</a> ");
           });
           $('#colors_sketch').sketch();
       });
   }


  });
})(jQuery);

