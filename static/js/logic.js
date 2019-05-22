// var heat_array = [];

// function read_route(route) {
 
//   d3.json(route).then(function(data){
//     for (var i = 0; i < data.length; i++) {
//       heat_array.push(data[i]);
//     }
//   })
// };

// read_route("/staples_info");
// read_route("/coliseum_info");
// read_route("/dodger_info");


function read_route(route, arr) {
 
  d3.json(route).then(function(data){
    for (var i = 0; i < data.length; i++) {
      arr.push(data[i]);
    }
  })
};

var sc = [];
var col = [];
var ds = [];

read_route("/staples_info", sc);
read_route("/coliseum_info", col);
read_route("/dodger_info", ds);

var sc_map = L.heatLayer(sc, {
  radius: 20,
  blur: 35
});

var col_map = L.heatLayer(col, {
  radius: 20,
  blur: 35
});

var ds_map = L.heatLayer(ds, {
  radius: 20,
  blur: 35
});



var arenas = [
  {name: "Staples Center",
  coordinates: [34.043018, -118.267258]
  },
  {name: "LA Memorial Coliseum",
  coordinates: [34.014053, -118.287872]
  },
  {name: "Dodger Stadium",
  coordinates: [34.073853, -118.239960]
  }
]

arena_markers = [];

for(var i=0; i <arenas.length; i++) {
  arena_markers.push(L.marker(arenas[i].coordinates, {
    draggable: false,
  }).bindPopup("<h4>" + arenas[i].name + "</h4>"));
}

var arena_layer = L.layerGroup(arena_markers);

// var heat = L.heatLayer(heat_array, {
//   radius: 20,
//   blur: 35
// });


var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
});

var outdoors = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.outdoors",
  accessToken: API_KEY
});

var satellite = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets-satellite",
  accessToken: API_KEY
});

var baseMaps = {
  Light: light,
  Outdoors: outdoors,
  Satellite: satellite
};

var overlayMaps = {
  Arenas: arena_layer,
  StaplesCenter: sc_map,
  Coliseum: col_map,
  DodgerStadium: ds_map
  // HeatMap: heat
};

// Create map object and set default layers
var myMap = L.map("map", {
  center: [34.0469, -118.2468],
  zoom: 13,
  layers: [outdoors, sc_map, arena_layer]
});

L.control.layers(baseMaps, overlayMaps).addTo(myMap);