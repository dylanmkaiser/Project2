function counter(route, crimeFrequency) {
    d3.json(route).then(function (data) {

        for (var i = 0; i < data.length; i++) {
            var currentCrime = data[i].dist_from_venue;
            // If the crime has been seen before...
            if (currentCrime in crimeFrequency) {
                // Add one to the counter
                crimeFrequency[currentCrime] += 1;
            }
            else {
                // Set the counter at 1
                crimeFrequency[currentCrime] = 1;
            }
        }
    })
}

var staples_crime_frequency = {};
var coliseum_crime_frequency = {};
var dodger_crime_frequency = {};

counter("/staples_crimes", staples_crime_frequency);
counter("/coliseum_crimes", coliseum_crime_frequency);
counter("/dodger_crimes", dodger_crime_frequency);

console.log(staples_crime_frequency);
console.log(coliseum_crime_frequency);
console.log(dodger_crime_frequency);


var x = [];
var y = [];
Object.entries(staples_crime_frequency).forEach(([key, value]) => {
    x.push(key);
    y.push(value);
});

console.log(x);
console.log(y); 



