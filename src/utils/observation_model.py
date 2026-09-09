import numpy as np


class ObservationModel(object):
    """
    Observation model assumed of
    """

    @staticmethod
    def sonar_model(xk, point, v):
        return np.sqrt((xk[0] - point[0]) ** 2 + (xk[1] - point[1]) ** 2) + v

    def __init__(self):
        self._matrices = {"H": np.zeros(shape=(2, 3)),
                          "M": np.zeros(shape=(2, 2))}

    @property
    def H(self):
        return self._matrices["H"]

    @H.setter
    def H(self, value):

        if value.shape != (2, 3):
            raise ValueError("Invalid matrix shape")

        self._matrices["H"] = value

    @property
    def M(self):
        return self._matrices["M"]

    @M.setter
    def M(self, value):
        if value.shape != (2, 2):
            raise ValueError("Invalid matrix shape")

        self._matrices["M"] = value

    def value(self, state, obs, verr):
        """
      Compute the value that the observation model
      assumes given the current state, the actual observations
      and the assumed error of the observations

      Parameters
      ----------
      state : np.array(shape=(3,1))
      obs : np.array(shape=???)
      verr : np.array(shape=???)
      Returns
      -------
      None.
      """
        return ObservationModel.sonar_model(xk=state, point=obs, v=verr)

    """
    def sonar_model_jacobian(self, xk, point, w):

        return np.array([[1.0/np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2), 0.0, 0.0],
                         [0.0, 1.0/np.sqrt((xk[0] - point[0])**2 + (xk[1] - point[1])**2), 0.0]])
    """

    """
    def sonar_model_jacobian_wrt_error(self, xk, point, w, shape_diagonal=None):

        if shape_diagonal is None:
            return np.array([1.0, 1.0])

        x = np.zeros(shape=shape_diagonal)
        np.fill_diagonal(x, 1.0)
        return x
    """
