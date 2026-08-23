import numpy as np


class MotionModel(object):

    def __init__(self, dt, tol, init_state=np.array([0.0, 0.0, 0.0])):
        self._state = init_state
        self._Dt = dt
        self._tol = tol
        self._matrices = {"F": np.zeros(shape=(3, 3)),
                          "L": np.zeros(shape=(3, 2))}

    @property
    def F(self):
        return self._matrices["F"]

    @property
    def L(self):
        return self._matrices["L"]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def act(self, u, werr):
        self.step(u=u, werr=werr)

    def step(self, u, werr):
        """
        Computes Odisseus next state dynamics
        The model adopted is a simple kinematic model for
        a differential drive system

        :param u: control input if length 2
        :type  u: array

        :param werr: array of length 2 represents unpredictable process noise
        :type  werr: array

        :return: np.array
        """

        # update the matrix description of the model
        self.update_matrix_description(u, werr)

        # the angular velocity
        w = u[1]
        theta = self._state[2]

        if np.fabs(w) < self._tol:
            # the orientation has not chenged

            self._state[0] += (u[0] * self._Dt + werr[0]) * np.cos(theta + werr[1])
            self._state[1] += (u[0] * self._Dt + werr[0]) * np.sin(theta + werr[1])
        else:

            self._state[2] += w * self._Dt + werr[1]
            self._state[0] += (u[0] / (2 * w) + werr[0]) * (np.sin(self._state[2]) - np.sin(theta))
            self._state[1] -= (u[0] / (2 * w) + werr[0]) * (np.cos(self._state[2]) - np.cos(theta))

        return self._state

    def update_matrix_description(self, u, werr):

        distance = 0.5 * u[0] * self._Dt
        orientation = u[1] * self._Dt
        values = self._state

        if np.fabs(u[1]) < self._tol:

            F = self._matrices["F"]

            F[0, 0] = 1.0
            F[0, 1] = 0.0
            F[0, 2] = (distance + werr[0]) * np.sin(values[2] + orientation + werr[1])

            F[1, 0] = 0.0
            F[1, 1] = 1.0
            F[1, 2] = -(distance + werr[0]) * np.cos(values[2] + orientation + werr[1])

            F[2, 0] = 0.0
            F[2, 1] = 0.0
            F[2, 2] = 1.0

            L = self._matrices["L"]

            L[0, 0] = np.cos(values[2] + orientation + werr[1])
            L[0, 1] = (distance + werr[0]) * np.sin(values[2] + orientation + werr[1])

            L[1, 0] = np.sin(values[2] + orientation + werr[1]);
            L[1, 1] = -(distance + werr[0]) * np.cos(values[2] + orientation + werr[1])

            L[2, 0] = 0.0
            L[2, 1] = 1.0

        else:

            F = self._matrices["F"]

            F[0, 0] = 1.0
            F[0, 1] = 0.0
            F[0, 2] = -(distance + werr[0]) * np.cos(values[2] + orientation + werr[1])(distance + werr[0]) * np.cos(values[2])

            F[1, 0] = 0.0
            F[1, 1] = 1.0
            F[1, 2] = -(distance + errors[0]) * np.sin(values[2] + orientation + werr[1]) + (distance + errors[0]) * np.sin(values[2])

            F[2, 0] = 0.0
            F[2, 1] = 0.0
            F[2, 2] = 1.0

            L = self._matrices["L"]

            L[0, 0] = np.sin(values[2] + orientation + werr[1]) - np.sin(values[2])

            L[0, 1] = -((v / 2.0 * w) + werr[0]) * np.cos(values[2] + orientation + werr[1]) * np.sin(values[2] + orientation + werr[1])

            L[1, 0] = -np.cos(values[2] + orientation + werr[1]) + np.cos(values[2])
            L[1, 1] = ((v / 2.0 * w) + werr[0]) * np.sin(values[2] + orientation + werr[1])

            L[2, 0] = 0.0
            L[2, 1] = 1.0
