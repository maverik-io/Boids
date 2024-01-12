# Pygame Boids Implementation

This is a Pygame implementation of the Boids algorithm, which simulates the flocking behavior of birds.

## Usage

Run the `main.py` script to start the simulation. You can add boids or obstacles by clicking on the screen. The behavior
of the click (whether it adds a boid, an obstacle, or a "bad" obstacle) can be toggled by clicking the middle mouse
button. Debug can be accessed by left-clicking the mouse.

## Dependencies

- Pygame library (version 2.5.2 used)

## Project Structure

- `main.py`: The main script to run the simulation.
- `utils/boid.py`: Contains the `Boid` class which implements the behavior of the boids.
- `utils/obstacle.py`: Contains the `Obstacle` class which implements the obstacles that the boids can interact with.

## Resources

For more information on the Boids algorithm, refer to:

- [Craig Reynolds' original paper on the Boids algorithm](http://www.red3d.com/cwr/boids/)

- [Wikipedia article on the Boids algorithm](https://en.wikipedia.org/wiki/Boids)
