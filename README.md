# DLA simulation

---

In this notebook I am simulating [diffusion limited aggregation](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation), and calculate the objects fractal dimension.


### Description of the simulation

Steps:

- start with an aggregate made of one point.
- release particles randomly on a circle outside the bounding box of the aggregate.
- simluate Brownian motion until the particle reaches the aggregate, or it goes outside a larger circle.

I decided to implement the aggregate as a dictionary. The keys are the coordinates, and the values show the indices of the particles (temporal order). I find it more intuitive and flexibe than storing a grid.

### Calculating the objects  fractal dimension

I calculate the objects fractal dimension using the [Correlation dimension](https://en.wikipedia.org/wiki/Correlation_dimension).

---

*Author: Dezso Ribli*