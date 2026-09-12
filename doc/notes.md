# Odiseus Robot

This set of notes describes the design of Odysseus.

## Hardware

- Arduino board
- Raspberry Pi
- L298 H-bridge


## Motor control

The two DC brushed motors are controlled via an Arduino board and an L298 H-bridge. 
In addition, the motors are equipped with encoders.
The Arduino board accepts commands from the Raspberry Pi board via the Serial port. 
A ```MotorCMD``` has the following structure

```commandline
cmd_type: string
left: int
right: int
```

The ```cmd_type``` is an enumeration with the following values:

- SET l, r
- STOP
- LEFT 0, r
- RIGHT l, 0

In fact, the MotorCMD class reads from the Serial port.

----
**Remark**

The Raspberry Pi board sends MotorCMDs for both motors.

----

## Sensor Modeling

\begin{equation}
\mathbf{h} = \begin{pmatrix}
h_{sonar} \\
h_{camera} \\
h_{ir}
\end{pmatrix}
\end{equation}


Odysseus is equipped with the following three types of sensors

\begin{itemize}
	\item Ultrasound sensor
	\item Camera sensor
	\item infrared sensor
\end{itemize}

### Ultrasound Sensor Model

As mentioned previously $\mathbf{h}$ represents a vector valued function and $h_{sonar}$ is the modeled measurement from the
sonar sensor. Odysseus is using the following model

\begin{equation}
h_{sonar}(\mathbf{x}, \mathbf{v}_{sonar}) = \sqrt{(x - x_o)^2 + (y - y_o)^2} +  \mathbf{v}_{sonar}
\label{sonar_h}
\end{equation} 

where $\mathbf{v}_{sonar}$ is the error vector associated with the sonar. $x_o, y_o$ are the coordinates of the
obstacle detected by the sensor.

## Kinematics Model

The Extended Kalman Filter discussed in section \ref{extended_kalman_filter}, requires
as motion model as input in order to make a predictions about the
pose of the robot. This section discusses the kinematics model used by Odysseus.

### Unicycle model


Odysseus is using the following unicycle model in order to capture the kinematics
of the robot motion 

\begin{eqnarray}
\frac{dx}{dt} = v cos(\theta) \\
\frac{dy}{dt} = v sin(\theta) \\
\frac{d\theta}{dt} = \omega
\label{continuous_kinematic_model} 
\end{eqnarray}

where $x,y$ are are the coordinates of the reference point, $\theta$ is the yaw angle, $v$ is the input velocity and $\omega$ is the input angular velocity of the robotic platform.

The state vector $\mathbf{x}$ has three components; the $x, y$ components of the 
reference point and the orientation or yaw angle $\theta$. Mathematically, this is written as

\begin{equation}
\mathbf{x} = (x, y, \theta)
\label{state_vector}
\end{equation}

As mentioned previously, the velocity $v$ is one of the inputs that is given to the system. Namely, it is calculated according to

\begin{equation}
v = \frac{v_l + v_r}{2}
\label{odysseus_velocity}
\end{equation}

where $R$ is the wheels radius and $v_r,v_l$ are the right and left wheels velocities respectively. Both are related to the angular wheel velocities $\omega_r,$ and  $\omega_l$ respectively and the wheel radius $R$ according to equation \ref{wheel_velocity}

\begin{equation}
v_i = \omega_iR, ~~ i = r, l
\label{wheel_velocity}
\end{equation}
Similarly the second input to the system is the angular velocity of 
the robot $\omega$. This is related to $v_l$ and $v_r$ according to equation \ref{odysseus_angular_velocity}

\begin{equation}
\omega = \frac{v_l - v_r}{2L}
\label{odysseus_angular_velocity}
\end{equation}

### Discrete kinematic model

Equation \ref{continuous_kinematic_model} represents a continuous model. Odysseus, instead uses a discrete
counterpart of the model given by the equations below. 

#### Case $\omega=0$
This case translates to the situation where the heading of the robot remains the same.
In this case the model will simply update the $x$ and $y$ coordinates of the reference point 
according to the equations \ref{equ1} and \ref{equ2} respectively.

\begin{eqnarray}
x_k = x_{k-1} + (\Delta t v_k + \mathbf{w}_{1,k})cos(\theta_{k-1} + \mathbf{w}_{2,k}) \label{equ1} \\
y_k = y_{k-1} + (\Delta t v_k + \mathbf{w}_{1,k})sin(\theta_{k-1} + \mathbf{w}_{2,k}) \label{equ2}
\end{eqnarray} 

\subsubsection{Case $\omega \neq 0$}
When the $\omega$ is deemed to be non zero, then the following equations are used
in order to estimate the pose of the robot.

\begin{eqnarray}
\theta_k = \theta_{k -1} + \Delta t \omega_k + \mathbf{w}_{2,k} \\
\label{equ3}
x_k = x_{k-1} + (\frac{v_k}{2w_k} + \mathbf{w}_{1,k})(sin(\theta_k) - sin(\theta_{k-1})) \label{equ4} \\
y_k = y_{k-1} - (\frac{v_k}{2w_k} + \mathbf{w}_{1,k})(cos(\theta_{k}) - cos(\theta_{k-1})) \label{equ5}
\end{eqnarray}

Note that we first update the heading of the robot and then the $x$ and $y$ coordinates
of the reference point.

Both scenarios incorporate the error by assuming that this is additive. The error is accounted for
the linear and angular velocities. $\Delta t$ is the sampling rate. 


## State Estimation

This section discusses the state estimation algorithms 
implemented in Odysseus. 

### Extended Kalman Filter

The Extended Kalman Filter is a state estimation technique for non-linear systems. 
It is an extension of the very popular Kalman Filter (see \url{https://en.wikipedia.org/wiki/Kalman_filter}).
Just like the original Kalman Filter algorithm, the EKF has also two steps namely predict and update. 
The main difference of EKF over Kalman Filter is that it introduces a linearization of the non-linear system. 
Overall the algorithm is as follows

#### Predict

At this step an estimate of both the state vector $\mathbf{x}$ and the covariance matrix $\mathbf{P}$ is made.
This is done according to

\begin{equation}
\bar{\mathbf{x}}_k = \mathbf{f}(\hat{\mathbf{x}}_{k-1}, \mathbf{u}_k, \mathbf{w}_k)
\end{equation}

where $\mathbf{f}$ is described by equations \ref{equ1},  \ref{equ2} and \ref{equ3}. $\hat{\mathbf{x}}_{k-1}$ is the state at the previous
time step. $\mathbf{u}_k, \mathbf{w}$ are the input vector and error vector associated with the process. The covariance matrix is estimated via 

\begin{equation}
\bar{\mathbf{P}}_k = \mathbf{F}_k \mathbf{P}_{k-1} \mathbf{F}_{k}^T + \mathbf{L}_k\mathbf{Q}_k\mathbf{L}_{k}^T
\end{equation}

where $\mathbf{F}$ is the Jacobian matrix of $\mathbf{f}$ with respect to the state variables. 
$\mathbf{Q}_k$ is the covariance matrix of the error and $\mathbf{L}_k$ is the Jacobian matrix of the motion
model, i.e. $\mathbf{f}$, with respect to $\mathbf{w}$.

#### Update

The update step established the predicted state vector and covariance matrix. Overall this step is summarized by
the equations below

\begin{equation}
\mathbf{S}_k = \mathbf{H}_k \bar{\mathbf{P}}_k \mathbf{H}_{k}^T + \mathbf{M}_k\mathbf{R}_k\mathbf{M}_{k}^T
\end{equation}

\begin{equation}
\mathbf{K}_k = \bar{\mathbf{P}}_k \mathbf{H}_{k}^T\mathbf{S}_{k}^{-1}
\label{gain_matrix} 
\end{equation} 

\begin{equation}
\mathbf{x}_{k} = \bar{\mathbf{x}}_{k} + \mathbf{K}(\mathbf{z}_k - \mathbf{h}(\bar{\mathbf{x}}_k, \mathbf{v}_k))
\end{equation}

\begin{equation}
\mathbf{P}_k = (\mathbf{I} - \mathbf{K}_k\mathbf{H}_k)\bar{\mathbf{P}}_k
\end{equation}

where $\mathbf{H}$ is the Jacobian matrix of the observation model $\mathbf{h}$. $\mathbf{M}$ is the Jacobian matrix of 
the observation model with respect to the error vector $\mathbf{v}$.  $\mathbf{K}$ is the
gain matrix and $\mathbf{R}$ is the covariance matrix related to the error vector $\mathbf{v}$.
 



## Simulation Verification


\subsection{EKF Verification}
This section presents some simulation results that verify the EKF implementation on Odysseus

\subsubsection{Test 1}

In this test the following input data was used

\begin{equation}
R = 
\begin{pmatrix}
 1.0 & 0.0 \\
0.0 & 1.0 
\end{pmatrix}
\end{equation}

\begin{equation}
Q = 
\begin{pmatrix}
0.001 & 0.0 \\
0.0 & 0.001 
\end{pmatrix}
\end{equation}

The motion model $\mathbf{f}$ is according to equation \ref{odysseus_discrete} where the error vector $\mathbf{w}$ was set to zero.

The observation model function $\mathbf{h}$ was simply the identity function meaning returning the passed state vector

\begin{equation}
\mathbf{h}(\mathbf{x}, \mathbf{v}) = \mathbf{x}
\end{equation}

The error vector $\mathbf{v}$ was set to

\begin{equation}
\mathbf{v} = (0.0, 0.0)
\end{equation}

Finally, the following data was used

\begin{enumerate}
	\item $\Delta t = 0.5$
	\item $R = 2.5 cm$
	\item $v_L = v_R = 50 RPM$
	\item $L= 15 cm$ 
\end{enumerate}


\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.480]{imgs/ekf_straight_motion_1.png}
	\end{center}
	\caption{ Straight motion test 1.}
	\label{ekf_straight_motion_1}
\end{figure}

\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.480]{imgs/ekf_change_direction_1.png}
	\end{center}
	\caption{ Change direction test 1.}
	\label{ekf_change_direction_1}
\end{figure}

\subsubsection{Test 2}

The second simulation test uses equation \ref{sonar_h} to model the sonar measurement

\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.480]{imgs/ekf_straight_motion_2.png}
	\end{center}
	\caption{ Straight motion test 2.}
	\label{ekf_straight_motion_2}
\end{figure}


## Software Architecture & Design

Odysseus is a multiprocess application. All its sensors as well as its motors run on a separate process.
These processes are

\begin{itemize}
	\item \mintinline{c++}{MasterProcess}
	\item \mintinline{c++}{WebAppProcess}
	\item \mintinline{c++}{CameraProcess}
	\item \mintinline{c++}{IRProcess}
	\item \mintinline{c++}{UltrasoundSensorProcess}
	\item \mintinline{c++}{PropulsionProcess}
	\item \mintinline{c++}{DecisionMakerProcess}
\end{itemize}

\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.380]{imgs/design_1.png}
	\end{center}
	\caption{ Process inheritance diagram.}
	\label{design_1}
\end{figure}

\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.480]{imgs/design_2.png}
	\end{center}
	\caption{ \mintinline{c++}{MasterProcess}.}
	\label{design_2}
\end{figure}

\begin{figure}[!htb]
	\begin{center}
		\includegraphics[scale=0.380]{imgs/design_3.png}
	\end{center}
	\caption{ Process messaging.}
	\label{design_3}
\end{figure}



