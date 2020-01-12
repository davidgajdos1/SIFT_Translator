def Detect_Extremes(d_o_gs,np):
    extremy_vrstvy = []
    for d_o_g in d_o_gs:
        extremy_d_o_g = []
        d_o_g_rows = (d_o_g[0]).shape[0]
        d_o_g_cols = (d_o_g[0]).shape[1]
        for dif in range(1,len(d_o_g)-1):
            extremy_d_o_g.append(Extrema_Detection3(d_o_g[dif-1:dif+2], d_o_g_rows, d_o_g_cols, np))
        extremy_vrstvy.append(extremy_d_o_g)
    return extremy_vrstvy

def Extrema_Detection1(trojica_matic,rows,cols,np):
    extremy = []
    
    def rekurzia_row(num1, num2, my_pixel, matica, cur_row, cur_col):
        nonlocal mins_found, max_found;
        if (mins_found == 0 or max_found == 0):
            if (matica[num1,num2] != my_pixel or [num1,num2] == [cur_row,cur_col]):
                rekurzia_col(num1, num2, my_pixel, matica, cur_row, cur_col)
                num = num1+1
                if num < cur_row+2:
                    rekurzia_row(num, num2, my_pixel, matica, cur_row, cur_col)
        
    def rekurzia_col(num1, num2, my_pixel, matica, cur_row, cur_col):
        nonlocal mins_found,max_found
        if matica[num1,num2] > my_pixel: mins_found += 1;
        elif matica[num1,num2] < my_pixel: max_found += 1;
        num = num2+1
        if num < cur_col+2:
            if (mins_found == 0 or max_found == 0):
                if (matica[num1,num] != my_pixel or [num1,num] == [cur_row,cur_col]):
                    rekurzia_col(num1,num, my_pixel, matica, cur_row, cur_col)
    
    'prechadzam vsetky body matice okrem okrajovych'
    for row in range(1,rows-1):
        for col in range(1,cols-1):

            max_found = 0; mins_found = 0;
            my_pixel = trojica_matic[1][row,col]
            if trojica_matic[0][row-1,col-1] != my_pixel:
                rekurzia_row(row-1, col-1, my_pixel, trojica_matic[0], row, col)
                if max_found == 9 or mins_found == 9:
                    rekurzia_row(row-1, col-1, my_pixel, trojica_matic[1], row, col)
                    if max_found == 17 or mins_found == 17:
                        rekurzia_row(row-1, col-1, my_pixel, trojica_matic[2], row, col)
                        if max_found == 26 or mins_found == 26:
                            extremy.append([row,col,trojica_matic[1][row,col]])                                                
    return extremy                                             

def Extrema_Detection2(trojica_matic,rows,cols,np):
    extremy = []
    for row in range(1,rows-1):
        for col in range(1,cols-1):
            my_pixel = trojica_matic[1][row,col]
            if trojica_matic[0][row-1,col-1] != my_pixel:
                uni_matrix = np.concatenate((np.concatenate((trojica_matic[0][row-1:row+2,col-1:col+2],
                                trojica_matic[1][row-1:row+2,col-1:col+2])),
                                trojica_matic[2][row-1:row+2,col-1:col+2]));
                uni_vector = uni_matrix.reshape(uni_matrix.size)
    
                mins_found = 0; max_found = 0; my_pixel = uni_vector[13];
                uni_vector = uni_vector[uni_vector != my_pixel]; 
                uni_vector_size = uni_vector.size;
                if uni_vector_size == 26:
                    for pixel in range(uni_vector_size):
                        if my_pixel > uni_vector[pixel]:
                            max_found += 1;
                        elif my_pixel < uni_vector[pixel]:
                            mins_found += 1;
                        if mins_found > 0 and max_found > 0:
                            break;
                    if max_found == 26 or mins_found == 26:
                        extremy.append([row,col,trojica_matic[1][row,col]])
    return extremy

def Extrema_Detection3(trojica_matic,rows,cols,np):
    extremy = []
    for row in range(1,rows-1):
        for col in range(1,cols-1):
            my_pixel = trojica_matic[1][row,col]
            if trojica_matic[0][row-1,col-1] != my_pixel:
                mins_found = 0; max_found = 0;
                for img_num in range(3):
                    img_matrix = trojica_matic[img_num][row-1:row+2,col-1:col+2].ravel()        

                    for pixel in range(9):
                        if my_pixel > img_matrix[pixel]:
                            max_found += 1;
                        elif my_pixel < img_matrix[pixel]:
                            mins_found += 1;
                        if mins_found > 0 and max_found > 0 or (mins_found+max_found == 0):
                            break;
#                    if img_num == 0 and not (mins_found < 9 or max_found < 9):
#                        break;
#                    elif img_num == 1 and not(mins_found < 17 or max_found < 17):
#                        break;
#                    elif img_num == 2 and not(mins_found < 26 or max_found < 26):
#                        break;
                    if mins_found > 0 and max_found > 0 or not (mins_found < 9 or max_found < 9):
                        break;
                         
                if max_found == 26 or mins_found == 26:
                        extremy.append([row,col,trojica_matic[1][row,col]])
    return extremy

'ZALOHA'

'pomocky'
#(difference_of_gaussians[0][0]).shape[1]
       
#npX = np.asarray(X)
#npY = np.asarray(Y)

#a = np.array([[1,2,3,4,5],[6,7,8]])

'to iste ako ravel alebo reshape # triple nested list comprehension'
#uni_vector = [y for x in [trojica_matic[x][row-1:row+2,col-1:col+2] for x in [0,1,2]] for y in x for y in y] 

'REKURZIA'
#    def rekurzia_row(num1, num2, my_pixel, matica, cur_row, cur_col):
#        nonlocal mins_found, max_found;
#        if (mins_found == 0 or max_found == 0):
#            if (matica[num1,num2] != my_pixel or [num1,num2] == [cur_row,cur_col]):
#                rekurzia_col(num1, num2, my_pixel, matica, cur_row, cur_col)
#                num = num1+1
#                if num < cur_row+2:
#                    rekurzia_row(num, num2, my_pixel, matica, cur_row, cur_col)
#        
#    def rekurzia_col(num1, num2, my_pixel, matica, cur_row, cur_col):
#        nonlocal mins_found,max_found
#        if matica[num1,num2] > my_pixel: mins_found += 1;
#        elif matica[num1,num2] < my_pixel: max_found += 1;
#        num = num2+1
#        if num < cur_col+2:
#            if (mins_found == 0 or max_found == 0):
#                if (matica[num1,num] != my_pixel or [num1,num] == [cur_row,cur_col]):
#                    rekurzia_col(num1,num, my_pixel, matica, cur_row, cur_col)