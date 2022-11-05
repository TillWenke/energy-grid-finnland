// import { Component, OnInit } from '@angular/core';
import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, OnDestroy } from '@angular/core';
import { Map, GeoJSONSource } from 'maplibre-gl';
import { data } from '../../data/grid'; 

console.log(data.nodes);
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

  nodes = [
    {
      "id": 12345,
      "lat": 62.872534,
      "lon": 25.699977,
      "power": 1380
    },
    {
      "id": 98765,
      "lat": 63.872534,
      "lon": 24.699977,
      "power": -240
    },
    {
      "id": 24680,
      "lat": 61.872534,
      "lon": 26.699977,
      "power": -590
    }
  ]

  edges = [
    {
      "id_a": 12345,
      "id_b": 98765,
      "capacity": 1200
    },
    {
      "id_a": 24680,
      "id_b": 98765,
      "capacity": 800
    }
  ]

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
      this.setupMap(map);
      this.addLine(map);
    }, 100);
  }

  async initMap() {
    const initialState = { lng: 27.1, lat: 64.3, zoom: 5 };

    this.map = await new Map({
      container: this.mapContainer.nativeElement,
      style: `https://demotiles.maplibre.org/style.json`,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom
    });
    return this.map;
  }

  setupMap(map: Map) {
    let features = data.nodes.forEach(node => {
      return {
        "type": "Feature",
          "properties": { "name": "First Island" },
          "geometry": {
            "type": "Point",
            "coordinates": [node.lon, node.lat]
          }
      }
    });
    console.log(features)

    map.addSource(SOURCE_ID, {
      type: 'geojson',
      data: 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_ports.geojson'
    });

    (map.getSource(SOURCE_ID) as GeoJSONSource).setData({
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": { "name": "First Island" },
          "geometry": {
            "type": "Point",
            "coordinates": [27.1, 64.3]
          }
        },
        {
          "type": "Feature",
          "properties": { "name": "Second Island" },
          "geometry": {
            "type": "Point",
            "coordinates": [24.699977, 63.872534]
          }
        },
        {
          "type": "Feature",
          "properties": { "name": "Thirde Island" },
          "geometry": {
            "type": "Point",
            "coordinates": [26.699977, 61.872534]
          }
        }
      ]
    });

    map.addLayer({
      'id': 'red-circle',
      'type': 'circle',
      'source': SOURCE_ID,
      'paint': {
        'circle-radius': 6,
        'circle-color': '#B42222'
      },
      'filter': ['==', '$type', 'Point']
    });
  }

  addLine(map: Map) {
    map.addSource('route', {
      'type': 'geojson',
      'data': {
        'type': 'Feature',
        'properties': {},
        'geometry': {
          'type': 'LineString',
          'coordinates': [
            [27.1, 64.3],
            [24.699977, 63.872534]
          ]
        }
      }
    });
    map.addLayer({
      'id': 'route',
      'type': 'line',
      'source': 'route',
      'layout': {
        'line-join': 'round',
        'line-cap': 'round'
      },
      'paint': {
        'line-color': '#888',
        'line-width': 2
      }
    });

  }

}