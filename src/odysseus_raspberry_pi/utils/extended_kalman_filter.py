
import numpy as np
from odysseus_raspberry_pi.utils.matrix_descriptor import MatrixDescriptor

__all__ = ["ExtendedKalmanFilter",
           "EKFMatrixDescription"]

# Holds the names of the matrices used in the Kalman Filter class
NAMES = ["P", "K", "Q", "R"]

class EKFMatrixDescription(MatrixDescriptor):
    """
    Matrix description for Kalman Filter class
    """

    def __init__(self):
        MatrixDescriptor.__init__(self, names=NAMES)

    def set_matrix(self, name, item):
        """
        Set the Matrix with the given name to the given value
        """
        self._matrices[name] = item

    def get_matrix(self, name):
        return self._matrices[name]


class ExtendedKalmanFilter(object):

    """
    Extended Kalman Filter implementation
    """

    def __init__(self, motion_model, observation_model,
                 matrix_description, odysseus_config):

        # configuration of odysseus
        self._config = odysseus_config

        # the motion model used
        self._motion_model = motion_model

        # the observation model used
        self._observation_model = observation_model

        # the matrix descriptor
        self._mat_desc = matrix_description

    @property
    def state(self):
      return self._motion_model.state

    def set_matrix(self, name, mat):
        """
        Set the matrix with name
        :param name: The name of the matrix to set
        :param mat: The matrix
        :return:
        """
        self._mat_desc.set_matrix(name=name, mat=mat)

    def iterate(self, u, z, w, v, **kwargs):

        self.predict(u=u, w=w)
        self.update(z=z, v=v)

    def predict(self, u, w):
        """
        Performs the prediction step for Kalman Filter
        """

        state = self._motion_model.value(u, w)

        F = self._motion_model.F
        F_T = F.T

        L = self._motion_model.L
        L_T = L.T

        P = self._mat_desc["P"]
        Q = self._mat_desc["Q"]

        P = F * P * F_T + np.dot(L, np.dot(Q, L_T))
        self._mat_desc["P"] = P

    def update(self, z, v):

        """
        Performs the update step of the Extended Kalman Filter
        :param z: the sensor measurements
        :type  z:
        :param v: error vector associated with the meansuremnt
        """

        P = self._mat_desc["P"]
        R = self._mat_desc["R"]
        state = self._motion_model.state

        # get the value predicted by the observation model
        # z is actually a vector that includes all the measurements
        # done by the sensoring system
        zpred = self._observation_model.value(measurement=z, measurement_error=v)

        # if the predicted measurement is None
        # then set it to zero in order to proceed
        # if the measurement z is None then the model
        # is expected to handle this
        if zpred is None:
            zpred = np.array([0.0 for i in range(len(z))])

        H = self._observation_model.H
        H_T = H.T

        M = self._observation_model.M

        try:
            # S = H*P*H^T + M*R*M^T
            S_inv = np.linalg.inv(np.dot(H, np.dot(P, H_T)) + np.dot(M, np.dot(R, M.T)))

            # compute the gain matrix
            K = np.dot(P, np.dot(H_T, S_inv))

            # compute gain matrix
            self._mat_desc["K"] = K

            innovation = self._calculate_innovation(z=z, zpred=zpred)
            state += np.dot(self._mat_desc["K"], innovation)

            #I = np.zeros(shape=(len(state), len(state)))
            #np.fill_diagonal(I, 1.0)
            I = np.eye(len(state))

            # update covariance matrix
            P = (I - np.dot(self._mat_desc["K"], H)) * P
            self._mat_desc["P"] = P

        except np.linalg.linalg.LinAlgError as exception:

            if str(exception) == 'Singular matrix':
                # this is a singular matrix what
                # should we do? Simply use the predicted
                # values and log the fact that there was a singular matrix
                raise

    def _calculate_innovation(self, z, zpred):

        innovation = np.array([0.0 for i in range(len(z))])

        for i in range(len(z)):
            if z[i] != self._config["INVALID_SIGNAL"]:
                innovation[i] = z[i] - zpred[i]
        return innovation
