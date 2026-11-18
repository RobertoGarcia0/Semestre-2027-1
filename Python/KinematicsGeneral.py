from sympy import *
import matplotlib.pyplot as plt
class Robot():
  def __init__(self, dof:int=3, 
               xyz:tuple[tuple[float]]=((0, 0, 0), (0.3, 0, 0), (0.3, 0, 0), (0.3, 0, 0)), 
               rpy:tuple[tuple[float]]=((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))):
    print("Inicializando robot")
    print("Definiendo variables")
    # ---Espacio de las juntas ---
    # Variables de posición
    th = []
    for i in range(dof):
      th.append(Symbol("theta_" + str(i+1)))
    # Variables de velocidad
    th_dot = []
    for i in range(dof):
      th_dot.append(Symbol("theta_" + str(i+1) + "_dot"))
    # Variables de aceleración
    th_dot_dot = []
    for i in range(dof):
      th_dot_dot.append(Symbol("theta_" + str(i+1) + "_dot_dot"))
    self.th, self.th_dot, self.th_dot_dot = th, th_dot, th_dot_dot
    # --- Espacio del robot ---
    # Variables de posición
    x = []
    for i in range(6):
      x.append(Symbol("x_" + str(i+1)))
    # Variables de velocidad
    x_dot = []
    for i in range(6):
      x_dot.append(Symbol("x_" + str(i+1) + "_dot"))
    # Variables de aceleración
    x_dot_dot = []
    for i in range(6):
      x_dot_dot.append(Symbol("x_" + str(i+1) + "_dot_dot"))
    self.x, self.x_dot, self.x_dot_dot = x, x_dot, x_dot_dot

    # --------- Cinemática directa ---------
    print("Generando transformación y Jacobiano")
    # Vectores de posición
    pos = []
    for i in range(dof + 1):
      pos.append(self._pos(xyz[i][0], xyz[i][1], xyz[i][2]))
    # Matrices de rotación
    rot = []
    for i in range(dof):
      rot.append(self._rot(rpy[i][0], rpy[i][1], rpy[i][2], th[i]))
    rot.append(self._rot(rpy[dof][0], rpy[dof][1], rpy[dof][2])) 
    # Matrices de transformación
    T = []
    for i in range(dof + 1):
      # T_i_i+1
      T.append(self._tr(pos[i], rot[i]))
    # Transformación del efector final
    T_0_p = T[0] # Agrega t_0_1
    for i in range(1, dof + 1):
      # Agrega t_i_i+1
      T_0_p = T_0_p * T[i]
    T_0_p = simplify(T_0_p)
    # Postura (dependiendo de las variables a controlar)
    x_0_p = T_0_p[0, 3]
    y_0_p = T_0_p[1, 3]
    z_0_p = T_0_p[2, 3]
    beta_0_p = trigsimp(asin(-T_0_p[2, 0])) # -pi/2 < beta < pi/2
    gamma_0_p = trigsimp(atan2(T_0_p[2, 1]/cos(beta_0_p), T_0_p[2, 2]/cos(beta_0_p)))
    alpha_0_p = trigsimp(atan2(T_0_p[1, 0]/cos(beta_0_p), T_0_p[0, 0]/cos(beta_0_p)))
    xi_0_p = Matrix([x_0_p, y_0_p, alpha_0_p])
    # Jacobiano
    J = diff(xi_0_p, th[0])
    for i in range(1, dof):
      J = Matrix.hstack(J, diff(xi_0_p, th[i]))
    # --------- Cinemática inversa ---------
    print("Generando cinemática inversa")
    J_inv = J.inv()
    # Vector de velocidad del efector final como variables (dependiendo de las variables a controlar)
    xi_0_p_dot = Matrix([x_dot[0], x_dot[1], x_dot[5]]) # x, y, alpha
    # Vector de velocidad de las juntas como variables
    theta_0_p_dot=[]
    for i in range(dof):
      theta_0_p_dot.append(th_dot[i])
    # Velocidad de las juntas en términos de la velocidad del efector final (Cinemática inversa)
    theta_dot = J_inv * xi_0_p_dot
    #Guardar variables
    self.xi_0_p = xi_0_p
    self.xi_0_p_dot = xi_0_p_dot
    self.theta_dot = theta_dot
    self.J = J
    self.J_inv = J_inv
    # Polinomio lambda
    print("Generando polinomio lambda")
    t = symbols("t")
    self.t = t
    a_0, a_1, a_2, a_3, a_4, a_5 = symbols("a_0, a_1, a_2, a_3, a_4, a_5")
    self.a_0, self.a_1, self.a_2, self.a_3, self.a_4, self.a_5 = a_0, a_1, a_2, a_3, a_4, a_5
    self.lam = a_0 + a_1 * t + a_2 * t**2 + a_3 * t**3 + a_4 * t**4 + a_5 * t**5
    # derivadas del polinomio
    self.lam_dot = diff(self.lam, t)
    self.lam_dot_dot = diff(self.lam_dot, t)

  def def_trayectoria(self, t_i=0, t_f=4, frec=10, th_i=(0.1, 0.1, 0.1), xi_f=(0.7, 0.1, 0)):
    print("Definiendo trayectoria hacia {}".format(xi_f))
    t = symbols("t")
    # Posición inicial del efector final
    xi_i = self.xi_0_p
    for i in range(len(self.th)):
      xi_i = xi_i.subs({self.th[i]: th_i[i]})
    # Muestreo y dt
    self.dt = 1.0/frec
    self.muestras = t_f * frec + 1
    # Ecuaciones de restricción para trayectoria
    eq1 = self.lam.subs(t, t_i)     # = 0
    eq2 = self.lam.subs(t, t_f) - 1 # = 0
    eq3 = self.lam_dot.subs(t, t_i)
    eq4 = self.lam_dot.subs(t, t_f)
    eq5 = self.lam_dot_dot.subs(t, t_i)
    eq6 = self.lam_dot_dot.subs(t, t_f)
    solutions = solve((eq1, eq2, eq3, eq4, eq5, eq6),
                    (self.a_0, self.a_1, self.a_2, self.a_3, self.a_4, self.a_5))
    # Sustituyendo solución en polinimio lambda
    lam_s         = self.lam.subs(solutions)
    lam_dot_s     = self.lam_dot.subs(solutions)
    lam_dot_dot_s = self.lam_dot_dot.subs(solutions)
    
    # Ecuaciones de posiciones, velocidades y aceleraciones
    xi_f = Matrix([xi_f[0], xi_f[1], xi_f[2]])
    xi_eq         = xi_i + (xi_f - xi_i) * lam_s
    xi_dot_eq     = (xi_f - xi_i) * lam_dot_s
    xi_dot_dot_eq = (xi_f - xi_i) * lam_dot_dot_s

    # Generar arreglos para guardar muestreo
    # Tiempo
    t_m = Matrix.zeros(1, self.muestras)
    for i in range(self.muestras):
      t_m[i] = self.dt * i

    # Arreglos para posición, velocidad y aceleración del E.F.
    xi_m         = Matrix.zeros(len(xi_i), self.muestras)
    xi_dot_m     = Matrix.zeros(len(xi_i), self.muestras)
    xi_dot_dot_m = Matrix.zeros(len(xi_i), self.muestras)

    print("Muestreando trayectoria del efector final")
    # Muestreo del efector final
    for i in range(self.muestras):
      xi_m[:, i]         = xi_eq.        subs({self.t: t_m[i]})
      xi_dot_m[:, i]     = xi_dot_eq.    subs({self.t: t_m[i]})
      xi_dot_dot_m[:, i] = xi_dot_dot_eq.subs({self.t: t_m[i]})
      pass

    # ---- Cinemática inversa ----
    # Velocidades de las juntas como ecuación
    th_dot_eq = self.theta_dot # self.theta_dot = J_inv * xi_0_p_dot
    # Posición, velocidad y aceleración de las juntas
    th_m         = Matrix.zeros(3, self.muestras)
    th_dot_m     = Matrix.zeros(3, self.muestras)
    th_dot_dot_m = Matrix.zeros(3, self.muestras)
    # Agregar valor conocido
    for i in range(len(th_i)):
      th_m[i, 0] = th_i[i]
    # Lambdificar ecuaciones de velocidad
    variables = list(self.th) + list(self.xi_0_p_dot)
    th_dot_func = lambdify(variables, th_dot_eq, modules='sympy')
    #Muestreo de las juntas
    print("Muestreando trayectoria de las juntas con cinemática inversa")
    for i in range(self.muestras):
      # Velocidades
      valores = list(th_m[:, i]) + list(xi_dot_m[:, i])
      th_dot_m[:, i] = th_dot_func(*valores)
      # print("Iteración: {}".format(i))
      if i < self.muestras - 1:
        # Posiciones
        th_m[:, i+1] = th_m[:, i] + th_dot_m[:, i] * self.dt
      if not (i == 0):
        # Aceleración
        th_dot_dot_m[:, i-1] = (th_dot_m[:, i] - th_dot_m[:, i-1]) / self.dt

    self.th_m = th_m
    self.xi_m = xi_m
    self.t_m = t_m

    print("Posición final de las juntas:")
    for th, valor in zip(self.th, th_m[:, -1]):
      print("{} = {}".format(th, valor))
    self.graficar_xi()
    self.graficar_th()

  def graficar_xi(self):
    # Gráficas
    fig, x_g = plt.subplots(nrows=1, ncols=len(self.xi_m[:, 0]), squeeze=False)
    x_g = x_g.flatten()
    fig.suptitle("Posiciones del efector final")
    for i in range(len(x_g)):
      x_g[i].set_title("x_" + str(i+1))
      x_g[i].plot(self.t_m.T, self.xi_m[i, :].T, color="RED")
    plt.show()

  def graficar_th(self):
    # Gráficas
    fig, th_g = plt.subplots(nrows=1, ncols=len(self.th_m[:, 0]), squeeze=False)
    th_g = th_g.flatten()
    fig.suptitle("Posiciones de las articulaciones")
    for i in range(len(th_g)):
      th_g[i].set_title("th_" + str(i+1))
      th_g[i].plot(self.t_m.T, self.th_m[i, :].T, color="BLUE")
    plt.show()

  def _pos(self, x=0, y=0, z=0):
    pos = Matrix([[x],
                  [y],
                  [z]])
    
    return pos
  def _rot(self, gamma:float=0, beta:float=0, alpha:float=0, act:Symbol=0):
        R_x = Matrix([[1,          0,           0],
                      [0, cos(gamma), -sin(gamma)],
                      [0, sin(gamma),  cos(gamma)]])
        R_y = Matrix([[cos(beta),  0, sin(beta)],
                      [        0,  1,         0],
                      [-sin(beta), 0, cos(beta)]])
        R_z = Matrix([[cos(alpha), -sin(alpha), 0], 
                      [sin(alpha),  cos(alpha), 0],
                      [         0,           0, 1]])
        R_act = Matrix([[cos(act), -sin(act), 0], 
                      [sin(act),  cos(act), 0],
                      [         0,           0, 1]])
        # URDF maneja las rotaciones como zyx, y al final rotación de la junta
        return R_z * R_y * R_x * R_act
  def _tr(self, pos:Matrix, rot:Matrix):
    tr = Matrix.vstack(Matrix.hstack(rot, pos), Matrix([0, 0, 0, 1]).T)
    return tr
  def _tr_h(self, x=0, y=0, z=0, gamma=0, beta=0, alpha=0):
      T_x = Matrix([[1,          0,           0, x],
                    [0, cos(gamma), -sin(gamma), 0],
                    [0, sin(gamma),  cos(gamma), 0],
                    [0,          0,           0, 1],])
      T_y = Matrix([[cos(beta),  0, sin(beta), 0],
                    [        0,  1,         0, y],
                    [-sin(beta), 0, cos(beta), 0],
                    [0, 0, 0, 1]])
      T_z = Matrix([[cos(alpha), -sin(alpha), 0, 0], 
                    [sin(alpha),  cos(alpha), 0, 0],
                    [         0,           0, 1, z], 
                    [         0,           0, 0, 1]])
      return T_x * T_y * T_z
    
def main():
  robot = Robot()
  robot.def_trayectoria()
  pass
if __name__ == "__main__":
  main()