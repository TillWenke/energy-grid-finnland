# For the Junction 2022 Hackathon in Espoo. For the challenges proposed by Aalto University and McKinsey.

"The focus on this project is utilizing a graph theoretical approach coupled with public geospatial information to inform power systems engineers
and in turn policy makers, on how the power distribution system can be improved."

# Main contribution:
Building a representation of the Finnish power grid as a graph including power lines and producers (power plants) and consumers (municipalities) with their annular energy production/ consumption data >>> graph_preparation/grid.json

Contraction/ Collapsing this graph to only include producer/ consumer nodes and no intermediate nodes (links between power lines) and modify it to run "max flow min cut" algorithm on it to identify bottlenecks in the power grid >>> graph_preparation/grid_contracted_units.json

# View the results - suggestions for new power lines
* having nodejs and angular installed
* in frontend/opgrid run "npm i"
* in frontend/opgrid run "ng serve"
