// import { Component, OnInit } from '@angular/core';
import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, OnDestroy } from '@angular/core';
import { Map } from 'maplibre-gl';

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

  // marker = {
  //   "type": "geojson",
  //   "data": {
  //       "type": "Feature",
  //       "geometry": {
  //           "type": "Point",
  //           "coordinates": [27.1, 64.3]
  //       },
  //       "properties": {
  //           "title": "Mapbox DC",
  //           "marker-symbol": "monument"
  //       }
  //   }
  // }

  // geometries = [
  //   {
  //     'type': 'Point',
  //     'coordinates': [25.699977, 62.872534]
  //   },
  //   {
  //     'type': 'Point',
  //     'coordinates': [24.699977, 63.872534]
  //   },
  //   {
  //     'type': 'Point',
  //     'coordinates': [26.699977, 61.872534]
  //   }
  // ]

  // geometries = [
  //   {
  //     'type': 'Feature',
  //     'geometry': {
  //       'type': 'Point',
  //       'coordinates': [25.699977, 62.872534]
  //     },
  //   },
  //   {
  //     'type': 'Feature',
  //     'geometry': {
  //       'type': 'Point',
  //       'coordinates': [24.699977, 63.872534]
  //     },
  //   },
  //   {
  //     'type': 'Feature',
  //     'geometry': {
  //       'type': 'Point',
  //       'coordinates': [26.699977, 61.872534]
  //     }
  //   },
  // ]


  constructor() { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    // this.map?.remove();
  }

  ngAfterViewInit() {
    // this.showMap();
  }

  async showMap() {
    const map = await this.initMap();
    await setTimeout(()=> {
      this.setupMap(map);
    }, 3000);
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
    const result: Map = map.addSource('national-park', {
      'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': [
          {
            'type': 'Feature',
            'geometry': {
              'type': 'Polygon',
              'coordinates': [
                [
                  [25.699977, 62.872534],
                  [24.699977, 63.872534],
                  [26.699977, 61.872534]
                ]
              ]
            }
          },
          {
            'type': 'Feature',
            'geometry': {
              'type': 'Point',
              'coordinates': [25.699977, 62.872534]
            }
          },
          {
            'type': 'Feature',
            'geometry': {
              'type': 'Point',
              'coordinates': [24.699977, 63.872534]
            }
          },
          {
            'type': 'Feature',
            'geometry': {
              'type': 'Point',
              'coordinates': [26.699977, 61.872534]
            }
          }
        ]
      }
    });

  }
}
