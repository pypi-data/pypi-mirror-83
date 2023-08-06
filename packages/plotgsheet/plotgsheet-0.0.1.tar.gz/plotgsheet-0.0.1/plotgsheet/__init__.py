import gspread
import matplotlib.pyplot as plt
import pandas as pd

def plotgs(credentialspath,drivepath,Gtype='Line',Gtitle='Google-Sheet-Graph',Xaxis=1,Yaxis=2,AxisLabel=[1,1],PlotColor='b',savefilename='Google_Sheet_Graph'):

    # paste your credentails file name in service account filename
    gc = gspread.service_account(filename=credentialspath)

    # paste your Google Sheet Link in open_by_url 
    sh = gc.open_by_url(drivepath)
    worksheet = sh.sheet1

    # Please Enter Your Valid X--Axis 
    row_name = worksheet.row_values(1)
    '''print('Enter Your X Axis From The List of Columns\n')
    print(row_name,'\n')
    print('1 For Frist Column 2 For Second Column And So On .......\n')
    X=int(input())

    # Please Enter Your Valid Y--Axis
    print('Enter Your Y Axis From The List of Columns\n')
    print(row_name,'\n')
    print('1 For Frist Column 2 For Second Column And So On .......\n')
    Y=int(input())'''
    X=Xaxis
    Y=Yaxis

    # This line handling that user is giving right X and Y Axis or Not 

    if X<=len(row_name) and Y<=len(row_name):

        # Getting All Columns After 1st Row For X--Axis
        
        X_values_list = worksheet.col_values(X)
        values_of_X=[]
        for i in X_values_list[1:]:
            values_of_X.append(int(i))

        print('Values On X Axis:- ',values_of_X)

        # Getting All Columns After 1st Row For Y--Axis
        
        Y_values_list = worksheet.col_values(Y)
        values_of_Y=[]
        for i in Y_values_list[1:]:
            values_of_Y.append(int(i))
        print('\nValues On Y Axis:- ',values_of_Y)
        
        # Here We are going to plot the Graph of data with X and Y Axis
        fig = plt.figure(figsize=(15,8))
        fig = plt.gcf()
        
        if AxisLabel[0]==0 and AxisLabel[1]==0:
            plt.gca().axes.yaxis.set_ticklabels([])
            plt.gca().axes.xaxis.set_ticklabels([])

        elif AxisLabel[0]==1 and AxisLabel[1]==0:
            plt.gca().axes.yaxis.set_ticklabels([])
            
        elif AxisLabel[0]==0 and AxisLabel[1]==1:
            plt.gca().axes.xaxis.set_ticklabels([])
            
        if Gtype=='Line':
            plt.plot(X_values_list,Y_values_list,color = PlotColor)

        elif Gtype=='Bar':
            plt.bar(X_values_list,Y_values_list,color = PlotColor)

        elif Gtype=='Scatter':
            plt.scatter(X_values_list,Y_values_list,color = PlotColor)

        plt.xlabel(row_name[X-1]+' - X-Axis') 
        plt.ylabel(row_name[Y-1]+' - Y-Axis') 
        plt.title(Gtitle)
        plt.savefig(savefilename+'.jpg', dpi=100)
        plt.show()
        print('\nGraph Has Been Saved in Your File Directory')
    else:
        print('\nPlease Enter a Valid Number and Run Again')
