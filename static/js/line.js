function group_by_distance(data) {
    var output = {};
    for (var i = 0; i < data.length; i++) {
        var currentCrime = data[i].dist_from_venue;
        // If the crime has been seen before...
        if (currentCrime in output) {
            // Add one to the counter
            output[currentCrime] += 1;
        }
        else {
            // Set the counter at 1
            output[currentCrime] = 1;
        }
    }

    return output;
}

function split_key_values(obj) {
    var output = {
        x: [],
        y: []
    };

    Object.entries(obj).forEach(([key, value]) => {
        output.x.push(key);
        output.y.push(value);
    });
    //output.x.sort();
    return output;
}

d3.json("/staples_crimes").then(function (data) {
    var staples_data = split_key_values(group_by_distance(data));
    console.log(staples_data);
    var trace1 = {
        x: staples_data.x,
        y: staples_data.y,
        type: "scatter",
        line: {
            color: "#DC143C"
          },
        name: "Staples Center"
       };
    d3.json("/coliseum_crimes").then(function (data) {
        var coliseum_data = split_key_values(group_by_distance(data));
        console.log(coliseum_data);
        var trace2 = {
            x: coliseum_data.x,
            y: coliseum_data.y,
            type: "scatter",
            line: {
                color: "#FFD700"
              },
            name: "Coliseum"
           };
        d3.json("/dodger_crimes").then(function (data) {
            var dodger_data = split_key_values(group_by_distance(data));
            console.log(dodger_data);
            var trace3 = {
                x: dodger_data.x,
                y: dodger_data.y,
                type: "scatter",
                line: {
                    color: "#0000FF"
                  },
                name: "Dodger Stadium"
               };

    var layout = {
        title: "Crime Count vs. Distance, by Venue",
        xaxis: { title: "Distance (mi)"},
        yaxis: { title: "Number of Crimes"}
    };

    var line_data = [trace1,trace2,trace3];

    Plotly.newPlot("plot", line_data, layout);
        });
    });
});

