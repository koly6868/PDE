import numpy as np


def Solve(param: float,
          step_x,
          step_y,
          step_t,
          init_cond: np.ndarray,
          border_cond,
          infl_func: np.ndarray):
        x_size, y_size = init_cond.shape
        t_size = border_cond[0].shape[0]
        
        # iniitialization grid of solution
        res = np.zeros((t_size, x_size, y_size))
        res[0] = init_cond
        res[:, :, 0] = border_cond[0]
        res[:, :, y_size-1] = border_cond[1]
        res[:, 0, :] = border_cond[2]
        res[:, x_size-1, :] = border_cond[3]
        
        #computing coefficients
        cInfl = -(step_x ** 2)
        #solving
        for t in range(0,t_size - 1):
            # first half step of computing
            slice = np.zeros((x_size-2,y_size-2))
            for y in range(0,y_size - 2):
                c1 = param*step_t
                c2= -(2*step_t*param + step_x ** 2)
                invA = np.linalg.inv(Create3DiagMatrix((x_size-2,y_size-2),c2[:,y+1],c1[:,y+1],c1[:,y+1]))
                b = cInfl*res[t,1:-1,y + 1]
                # linear interpolation
                b[0] -= c1[0,y+1] * Average(res[t,0,y + 1],res[t+1,0,y + 1])
                b[-1] -= c1[-1,y+1] * Average(res[t,-1,y + 1],res[t+1,-1,y + 1])
                slice[:,y] = np.dot(
                    invA,
                    b)
            # second half step of computing
            for x in range(0,x_size - 2):
                invA = np.linalg.inv(Create3DiagMatrix((x_size-2,y_size-2),c2[x+1,:],c1[x+1,:],c1[x+1,:]))
                b = -((step_y ** 2) * slice[x,:]) - (step_t * (step_y ** 2)) * infl_func[t,x + 1,1:-1]
                b[0] -= c1[x+1,0] * Average(res[t,x + 1,0],res[t+1,x + 1,0])
                b[-1] -= c1[x+1,-1] * Average(res[t,x + 1,-1],res[t+1,x + 1,-1])
                
                res[t+1,x+1,1:-1] = np.dot(invA,b)
        
        return res
         

def Create3DiagMatrix(
    shape : tuple,
    main_val,
    up_val,
    down_val):
        mtr = np.zeros(shape)
        mtr[0,0] = main_val[0]
        mtr[0,1] = up_val[0]
        mtr[-1,-1] = main_val[-1]
        mtr[-1,-2] = down_val[-1]
        for i in range(1,shape[0] - 1):
            mtr[i,i-1:i+2] = np.array([down_val[i],main_val[i],up_val[i]])
    
        return mtr

def Average(a, b):
    return (a+b)/2