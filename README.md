# MetroKit Python MVP

A personal project to build aesthetically pleasing graph structures with a Metro graphic design theme.

This version (the Python MVP) uses `svgwrite` to render the graph; however, I'm planning to port this to Swift using either AppKit or a SwiftUI canvas. I might also port this to React.js, but we'll see.

## Notes

- [ ] Revise line population to ensure lines don't branch
- [ ] Add cost to edges that intersect other edges on the same line
- [ ] Connect subgraphs to each other (direct and indirectly)
  - Connect graph with closest average position of each vertex (?)
  - Ignore connected subgraphs
- [ ] Add line beveling

## Most Recent Graph Rendering

Only part of the graph may displayed on GitHub. Download the svg from the svgs dir if you want to view the whole thing!

<img src="svgs/cluster_mst.svg" alt="most recently rendered SVG of metro themed graph" width="2048" height="2048">