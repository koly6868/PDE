import ImgController as conv
import numpy as np
import D2DimEquation as eq
import os
import PlotConroller as pc
import PaperGenerator as pg

def main():
    images_path = r"solution/"
    isCalck = False

    if isCalck:
        sol = Calc()
        np.save("result",sol)
        SavaeSolutionAsGif(sol,images_path)
    else:
        sol = np.load("result.npy")
    SavaeSolutionAsGif(sol,images_path)
    ShowSolution(sol)
    print("ok")


def SavaeSolutionAsGif(sol,images_path):
    #iverse values
    for t in range(0,sol.shape[0]):
        data = np.vectorize(lambda p: 255 if p > 255 else p)(sol[t])
        data = np.vectorize(lambda p: 255 - p)(data)
        conv.SaveArrayAsImage(images_path + str(t) + ".bmp",data)

    #clear reuslt folder
    gif_path = r"gif"
    if not os.path.exists(gif_path):
        os.mkdir(gif_path)
    else:
        for the_file in os.listdir(gif_path):
            file_path = os.path.join(images_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
    paths = list(map(lambda p: images_path+p,os.listdir(images_path)))
    conv.ImagesToGif(paths,"gif")

def ShowSolution(sol):
    p = pc.Plot3D(sol)
    p.Draw()

def Calc():
    init_cond = conv.ImageToNdarray("input.jpg")
    init_cond =  np.vectorize(lambda p: 255 - p)(init_cond)
    D = 2.0
    C = 0.9
    step_x = 0.5
    step_y = 0.5
    step_t = 0.4
    size_t = 100
    size_x, size_y = init_cond.shape
    param = D / pg.Generate(size_x,size_y,C,0.05)

    border_cond = []   
    border_cond.append(np.zeros(( size_t, init_cond.shape[0])))
    border_cond.append(np.zeros(( size_t, init_cond.shape[0])))
    border_cond.append(np.zeros(( size_t, init_cond.shape[1])))
    border_cond.append(np.zeros(( size_t, init_cond.shape[1])))

    infl_func = np.zeros((size_t, size_x, size_y))
    time = int(1/step_t)
    infl_func[0:time + 1] = init_cond
    infl_func[0: 3 * time,10:20,10:20] = 200


    return eq.Solve(param,step_x,step_y,step_t,init_cond,border_cond, infl_func)


main()