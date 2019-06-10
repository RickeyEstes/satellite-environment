# 2D Wafer-Scale Spacecraft Stabilization Environment
## Overview
This environment simulates the stabilization of a spacecraft along one axis of rotation. The spacecraft receives data
from its ADCS sensors (accelerometer, gyros, etc.) and exerts a torque in response to stabilize itself. In the real
world, achieving a completely fixed state is unrealistic, so instead success is measured by the longest time it can
maintain an oriented state within some tolerance \delta\theta. It also should respond to stochastic disruption by
particles commonly found in LEO.  
