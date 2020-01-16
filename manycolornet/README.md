This implementation is optimized for calculating the color-avoiding largest component when there are many colors. 
It does so by using the standard BFS algorithm and when it goes through the colors, it restricts later searches to nodes which are still connectable based on avoiding the colors already seen.
Because this algorithm is better suited for many colors, it is used for the AS calculations and loads real data.

