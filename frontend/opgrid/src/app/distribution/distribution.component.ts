// import { Component, OnInit } from '@angular/core';
import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, OnDestroy } from '@angular/core';
import { Map, GeoJSONSource } from 'maplibre-gl';
import { data } from '../../data/grid'; 
import { GeoJSON, Feature } from 'geojson';

const baseLineWidth = 0.0000002;
const baseRadius = 0.1;
const baseZoom = 10;

const proposals = {"0":{"source":1147151748,"target":3536595671},"1":{"source":824065452,"target":4447358451},"2":{"source":634989945,"target":2636358023},"3":{"source":2408331411,"target":2408331526},"4":{"source":2647668116,"target":1568817948},"5":{"source":2156877608,"target":4011659942},"6":{"source":2278030269,"target":2759244272},"7":{"source":7833850369,"target":7833827236},"8":{"source":246529612,"target":294854486},"9":{"source":6175259891,"target":288465276},"10":{"source":1092860862,"target":5048354290},"11":{"source":1224394666,"target":1425122020},"12":{"source":1802301146,"target":5931192731},"13":{"source":2408331345,"target":2408331223},"14":{"source":2376430694,"target":1019905622},"15":{"source":1224394666,"target":2090571394},"16":{"source":8661578399,"target":8661598578},"17":{"source":3943008213,"target":3943008240}};

const metersPerPixel = function(latitude: any, zoomLevel: any) { 
  const EARTH_RADIUS = 6378137; const TILESIZE = 512; 
  const EARTH_CIRCUMFERENCE = 2 * Math.PI * EARTH_RADIUS; 
  const scale = Math.pow(2,zoomLevel); 
  const worldSize = TILESIZE * scale; 
  var latitudeRadians = latitude * (Math.PI/180); 
  return EARTH_CIRCUMFERENCE * Math.cos(latitudeRadians) / worldSize; 
};

var pixelValue = function(latitude: any, meters: any, zoomLevel: any) {
  return meters / metersPerPixel(latitude, zoomLevel);
};


var nodes: any = []
data.nodes.forEach(function(node){
  nodes[node.id] = node;
});
const SOURCE_ID = 'finnish-grid';

@Component({
  selector: 'app-distribution',
  templateUrl: './distribution.component.html',
  styleUrls: ['./distribution.component.scss']
})
export class DistributionComponent implements OnInit, AfterViewInit, OnDestroy {

  map: Map | undefined;

  @ViewChild('map')
  private mapContainer!: ElementRef<HTMLElement>;

  constructor() { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.map?.remove();
  }

  ngAfterViewInit() {
    this.showMap();
  }

  async showMap() {
    const map = await this.initMap();

    // initMap needs to load style.json from the internet, wait for it to complete
    await setTimeout(() => {
      //this.setupMap(map);
      this.addPowerLines(map);
      this.addTowns(map);
      this.addPowerPlants(map);
      this.addProposedLines(map)
    }, 1000);
  }

  async initMap() {
    const initialState = { lng: 27.1, lat: 64.3, zoom: 4 };

    this.map = await new Map({
      container: this.mapContainer.nativeElement,
      style: `https://demotiles.maplibre.org/style.json`,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom,
      minZoom: 0,
      maxZoom: 24
    });
    return this.map;
  }

  setupMap(map: Map) {
    map.addSource(SOURCE_ID, {
      type: 'geojson',
      data: 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_ports.geojson'
    });

    const points: GeoJSON = { "type": "FeatureCollection",
    "features": data.nodes.map(function(node){
        const f: Feature = {
          "type": "Feature",
          "properties": { "name": "Second Island" },
          "geometry": {
            "type": "Point",
            "coordinates": [node.lon, node.lat]
          }
        };
        return f;
      })
    };
    
    (map.getSource(SOURCE_ID) as GeoJSONSource).setData(points);

    map.addLayer({
      'id': 'map',
      'type': 'circle',
      'source': SOURCE_ID,
      'filter': ['==', '$type', 'Point']
    });
  }

  addPowerLines(map: Map) {
    map.addSource('lines', { 'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': data.links.map(function(link){
          const f: Feature = {
            "type": "Feature",
            "properties": { 
              "capacity":  link.capacity*baseLineWidth
            },
            "geometry": {
              "type": "LineString",
              "coordinates": [
                [nodes[link.source].lon, nodes[link.source].lat],
                [nodes[link.target].lon, nodes[link.target].lat]
              ]
            }
          }; return f;
        })
      }, tolerance: 0.00001
    });
    map.addLayer({
      'id': 'lines',
      'type': 'line',
      'source': 'lines',
      'layout': {
        'line-join': 'round',
        'line-cap': 'round',
        'visibility': 'visible',
      },
      "minzoom": 0,
      "maxzoom": 24,
      'paint': {
        'line-color': '#888',
        "line-width": [
          'interpolate', 
          ['exponential', 2],
          ['zoom'],
          0, ["*", ["get", "capacity"], ["^", 2, -baseZoom]],
          24, ["*", ["get", "capacity"], ["^", 2, 24-baseZoom]]
      ]
      }
    })
  }

  addTowns(map: Map) {
    map.addSource('towns', { 'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': data.nodes.filter(function(node){
          return node.power < 0;
        }).map(function(node){
          const f: Feature = {
            "type": "Feature",
            "properties": { 
              'color': '#33C9EB', // blue 
              'radius': -node.power/(1/baseRadius)
            },
            "geometry": {
              "type": "Point",
              "coordinates": [node.lon, node.lat]
            }
          };
          return f;
        })
      }
    });
    map.addLayer({
      'id': 'towns',
      'type': 'circle',
      'source': 'towns',
      'paint': {
        'circle-radius': [
          'interpolate', 
          ['exponential', 2],
          ['zoom'],
          0, ["*", ["get", "radius"], ["^", 2, -baseZoom]],
          24, ["*", ["get", "radius"], ["^", 2, 24-baseZoom]]
      ],
        'circle-color': ['get', 'color']
      }
    });
  };

  addPowerPlants(map: Map) {
    map.addSource('powerplants', { 'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': data.nodes.filter(function(node){
          return node.power > 0;
        }).map(function(node){
          const f: Feature = {
            "type": "Feature",
            'properties': {
              'color': '#F7455D', // red
              'radius': node.power/(1/baseRadius),
            },
            "geometry": {
              "type": "Point",
              "coordinates": [node.lon, node.lat]
            }
          };
          return f;
        })
      }
    });
    map.addLayer({
      'id': 'powerplants',
      'type': 'circle',
      'source': 'powerplants',
      paint: {
        'circle-radius': [
          'interpolate', 
          ['exponential', 2],
          ['zoom'],
          0, ["*", ["get", "radius"], ["^", 2, -baseZoom]],
          24, ["*", ["get", "radius"], ["^", 2, 24-baseZoom]]
      ],
        'circle-color': ['get', 'color']
      }
    });
  };

  addProposedLines(map: Map) {
    map.addSource('proposals', { 'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': Object.values(proposals).map(function(coord){
          const f: Feature = {
            "type": "Feature",
            "properties": { 
              "capacity":  1000000000*baseLineWidth
            },
            "geometry": {
              "type": "LineString",
              "coordinates": [
                [nodes[coord.source].lon, nodes[coord.source].lat],
                [nodes[coord.target].lon, nodes[coord.target].lat]
              ]
            }
          }; return f;
        })
      }, tolerance: 0.00001
    });
    map.addLayer({
      'id': 'proposals',
      'type': 'line',
      'source': 'proposals',
      'layout': {
        'line-join': 'round',
        'line-cap': 'round',
        'visibility': 'visible',
      },
      "minzoom": 0,
      "maxzoom": 24,
      'paint': {
        'line-opacity': 0.5,
        'line-color': '#25F75D',
        "line-width": [
          'interpolate', 
          ['exponential', 2],
          ['zoom'],
          0, ["*", ["get", "capacity"], ["^", 2, -baseZoom]],
          24, ["*", ["get", "capacity"], ["^", 2, 24-baseZoom]]
      ]
      }
    })
  }
}