def skew_matrix_torch(vector):  # vector to skewsym. matrix

    ss_matrix = torch.zeros((3,3))
    ss_matrix[0, 1] = -vector[2]
    ss_matrix[0, 2] = vector[1]
    ss_matrix[1, 0] = vector[2]
    ss_matrix[1, 2] = -vector[0]
    ss_matrix[2, 0] = -vector[1]
    ss_matrix[2, 1] = vector[0]

    return ss_matrix


def rotation_matrix(angles):
    ct = torch.cos(angles[0])
    cp = torch.cos(angles[1])
    cg = torch.cos(angles[2])
    st = torch.sin(angles[0])
    sp = torch.sin(angles[1])
    sg = torch.sin(angles[2])

    #Create rotation matrices
    R_x = torch.zeros((3, 3))
    R_x[0, 0] = 1.
    R_x[1, 1] = ct
    R_x[1, 2] = -st
    R_x[2, 1] = st
    R_x[2, 2] = ct

    R_y = torch.zeros((3, 3))
    R_y[0, 0] = cp
    R_y[0, 2] = sp
    R_y[1, 1] = 1.
    R_y[2, 0] = -sp
    R_y[2, 2] = cp

    R_z = torch.zeros((3, 3))
    R_z[0, 0] = cg
    R_z[0, 1] = -sg
    R_z[1, 0] = sg
    R_z[1, 1] = cg
    R_z[2, 2] = 1.

    #R_x = torch.tensor([[1,0,0],[0,ct,-st],[0,st,ct]])
    #R_y = torch.tensor([[cp,0,sp],[0,1,0],[-sp,0,cp]])
    #R_z = torch.tensor([[cg,-sg,0],[sg,cg,0],[0,0,1]])
    R = R_z @ R_y @ R_x
    return R

def wrap_angle(val):
    pi = torch.tensor(np.pi)
    return torch.remainder(val + pi, (2 * pi)) - pi

def torch_dynamics(self, state, action):
    next_state = torch.zeros(12)

    L = 1
    b = 0.0245
    I = torch.tensor([[1., 0., 0.], [0., 2., 0.], [0., 0., 3.]])
    invI = torch.inverse(I)

    #Define state vector
    pos = state[0:3]
    v   = state[3:6]
    euler_vector = state[6:9]
    omega = state[9:12]

    # The acceleration
    sum_action = torch.zeros(3)
    sum_action[2] = torch.sum(action)

    dv = (torch.tensor([0,0,-self.mass*self.g]) + rotation_matrix(euler_vector) @ sum_action)/self.mass

    # The angular accelerations
    tau = torch.zeros(3)
    tau[0] = L*(action[0] - action[2])
    tau[1] = L*(action[1] - action[3])
    tau[2] =  b*(action[0] - action[1] + action[2] - action[3])

    #These two are equivalent forms
    #domega = invI @ (tau - skew_matrix_torch(omega) @ I @ omega)
    domega = invI @ (tau - torch.cross(omega, I @ omega))

    next_state[0:3] = pos + v * self.dt
    next_state[3:6] = v + dv * self.dt
    next_state[6:9] = wrap_angle(euler_vector + omega*self.dt)
    next_state[9:12] = omega + domega * self.dt

    return next_state