import matplotlib.pyplot as plt
import numpy as np
from acados_template import latexify_plot
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from tqdm import tqdm

def piecewise_constant(setpoints, setpoints_duration, Ts):

    '''
    Defines the sampled version with sample time Ts of a piecewise constant reference,
    
                 _
                | setpoints(0)      0   <= t < T_1
                | setpoints(1)      T_1 <= t < T_1 + T_2
      ref(t) = <
                | ...
                | setpoints(n-1)    T_1 + ... T_(n-1) <= t <= T_1 + ... + T_n
                 _
    
    where T_1, ..., T_n are the duration of each setpoint, i.e. the entries of setpoints_duration
    
    '''
    # compute the number of samples for each setpoint 
    n_samples = np.rint(setpoints_duration/Ts).astype(int)

    # compute the reference for each setpoint
    ref = setpoints[0]*np.ones((n_samples[0],))

    for i in range(1, len(setpoints)):
        ref = np.append(ref, setpoints[i]*np.ones((n_samples[i],)))

    # add one sample to account for the non-strict inequality on both sides
    # in the definition of the last setpoint 
    ref = np.append(ref, ref[-1])

    # compute final time instant
    Tf = np.round(np.sum(n_samples)*Ts, 3)
    
    return (ref, Tf)
    
def plot_results(time, time_dt, state, control):

    latexify_plot()

    # plot state
    plt.subplots(2, 2)

    # - plot cart position
    plt.subplot(2, 2, 1)
    plt.plot(time, state[:, 0])
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$p$ [m]')
    plt.grid(True)

    # - plot pendulum angle
    plt.subplot(2, 2, 2)
    plt.plot(time, np.rad2deg(state[:, 1]))
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$\\theta$ [deg]')
    plt.gca().grid(True)

    # - plot cart velocity
    plt.subplot(2, 2, 3)
    plt.plot(time, state[:, 2])
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$v$ [m/s]')
    plt.grid(True)

    # - plot pendulum angular velocity
    plt.subplot(2, 2, 4)
    plt.plot(time, np.rad2deg(state[:, 3]))
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$\omega$ [deg/s]')
    plt.grid(True)

    plt.tight_layout()

    # plot control input
    plt.figure()
    delta_t = np.diff(time_dt)[-1]
    plt.step(time_dt, control, where='post')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$F$ [N]')
    plt.grid(True)

def plot_pred_traj(time, time_dt, state, control, x_opt, u_opt, k, shooting_nodes=None):
    
    latexify_plot()
    
    plt.subplots(2, 2)

    # get number of shooting time intervals 
    N = x_opt.shape[0]

    # construct the time vector for prediction
    if shooting_nodes is None:
        # if the shooting nodes are not provided, assume uniform grid
        Ts = np.diff(time_dt)[-1]
        time_pred = time_dt[k].item()+np.arange(0, N)*Ts
    else:
        time_pred = time_dt[k].item()+shooting_nodes
        
    plt.subplot(2, 2, 1)
    plt.plot(time, state[:, 0])
    plt.step(time_pred, x_opt[:, 0, k].reshape(-1,1), where='post', color='red')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$p$ [m]')
    plt.grid(True)

    plt.subplot(2, 2, 2)

    plt.plot(time, np.rad2deg(state[:, 1]))
    plt.step(time_pred, np.rad2deg(x_opt[:, 1, k].reshape(-1,1)), where='post', color='red')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$\\theta$ [deg]')
    plt.gca().grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(time, state[:, 2])
    plt.step(time_pred, x_opt[:, 2, k].reshape(-1,1), where='post', color='red')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$v$ [m/s]')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(time, np.rad2deg(state[:, 3]))
    plt.step(time_pred, np.rad2deg(x_opt[:, 3, k].reshape(-1,1)), where='post', color='red')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$\omega$ [deg/s]')
    plt.grid(True)

    plt.tight_layout()

    plt.figure()    
    plt.step(time_dt, control, where='post')
    plt.step(time_pred, np.append(u_opt[:, 0, k], u_opt[-1, 0, k]).reshape(-1,1), where='post', color='red')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('$F$ [N]')
    plt.grid(True)

def plot_cpt(t, cpt, Ts=None):

    latexify_plot()

    plt.figure()
    plt.step(t, cpt*1000, where='post')
    plt.gca().set_xlabel('time [s]')
    plt.gca().set_ylabel('cpt [ms]')
    plt.grid(True) 
    
    if(Ts is not None):
        plt.hlines(Ts*1000, t[0], t[-1], linestyles="dashed", alpha=0.7)


def plot_grid(grid, title=None):

    latexify_plot()
    
    plt.figure()
    
    for t in grid:
        plt.axvline(t)
    
    plt.gca().set_xlabel('time [s]')

    if title is not None:
        plt.title("\\bfseries " + title)
    

def inverted_pendulum_animation(p, theta, ts, filename=None):

    latexify_plot()

    # define colors
    cart_color     = [0.6549, 0.7804, 0.9059]
    pendulum_color = [0.2549, 0.4118, 0.8824]
    mass_color     = [0.2510, 0.8784, 0.8157] 

    # initialize plot
    fig, ax = plt.subplots()
    plot, = ax.plot([], [], color=pendulum_color, linewidth=2, zorder=3)

    # set plot style
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    
    ax.set_xlim([-3, 3])
    ax.set_ylim(ymin = -1, ymax =1)
    ax.set_aspect('equal')
    ax.set_title('\\bfseries Inverted Pendulum simulation')
    ax.grid(True)
    

    # set number of frames per second
    fps = 20
    # create FFMpegWriter object
    animation_writer = FFMpegWriter(fps)

    # compute decimation factor
    df = int(1 / (ts * fps))
    
    # define parameters 
    cart_width  = 1  
    cart_height = 0.5
    l = 0.8

    # draw cart
    r = Rectangle((p[0] - cart_width/2, -cart_height/2) , cart_width, cart_height, color=cart_color, zorder=2) 
    ax.add_patch(r)  
    
    # draw line for base 
    ax.hlines(-cart_height/2, -2.5, 2.5, colors='black')

    # compute x,y coordinates of the end of the pendulum
    x_pendulum = p - l*np.sin(theta)
    y_pendulum = l*np.cos(theta)

    # draw pendulum mass
    mass = Circle((y_pendulum[0], y_pendulum[0]), 0.1, color=mass_color, zorder=4)
    ax.add_patch(mass)
    
    
    with animation_writer.saving(fig, filename if filename is not None else "simulation.mp4", dpi=300):
        for i in tqdm(range(0, len(p), df), desc="Generating Animation", ascii=False, ncols=75, colour='green'):
            
            # update cart, pendulum and mass position
            r.set(xy=(p[i] - cart_width/2,  -cart_height/2))
            plot.set_data([p[i], x_pendulum[i]], [0, y_pendulum[i]])
            mass.set(center=(x_pendulum[i], y_pendulum[i]))

            # update figure
            fig.canvas.draw()
            
            # save figure as video frame
            animation_writer.grab_frame()
            
    plt.close(fig)
