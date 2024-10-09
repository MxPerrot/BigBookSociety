#######################################
# biplot
# version 12/11/2021
#######################################

import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.cm as cm
import seaborn as sns
from sklearn.decomposition import PCA


def biplot(pca=[], x=None, y=None, components=[0,1], score=None, coeff=None, coeff_labels=None, score_labels=None, circle='T', bigdata=1000, cat=None, cmap="viridis", density=True, title="Correlation circle", show_graph=False, save_path="./biplot.png"):
    """
    Create a biplot visualization of PCA results or other data.

    This function generates a biplot, which can be used to visualize the results of a Principal Component Analysis (PCA) or to plot general data with additional features like convex hulls for big data sets.

    Parameters:
    pca (PCA object, optional): A fitted sklearn PCA object. If provided, it will be used to extract components and scores.
    x (array-like, optional): The input data for the x-axis. If score is None, this will be used as the score data.
    y (array-like, optional): The input data for the y-axis. Only used if x is one-dimensional.
    components (list, optional): The PCA components to use for the plot. Default is [0, 1] (first two components).
    score (array-like, optional): The PCA scores. If None and pca is provided, it will be calculated from pca and x.
    coeff (array-like, optional): The PCA coefficients (loadings). If None and pca is provided, it will be extracted from pca.
    coeff_labels (list, optional): Labels for the coefficient arrows.
    score_labels (list, optional): Labels for the score points.
    circle (str, optional): If 'T', a unit circle will be drawn. Default is 'T'.
    bigdata (int, optional): Threshold for switching to big data mode. Default is 1000.
    cat (array-like, optional): Categories for coloring the points.
    cmap (str, optional): Colormap to use for categorical coloring. Default is "viridis".
    density (bool, optional): If True, show density plot for big data. Default is True.
    title (str, optional): Title of the plot. Default is "Correlation circle".
    show_graph (bool, optional): If True, display the plot. Default is False.
    save_path (str, optional): Path to save the plot. Default is "./biplot.png".

    Returns:
    None: This function does not return any value. It creates and optionally saves and/or displays a plot.

    Note:
    - The function scales and centers the input data for display purposes.
    - For large datasets (determined by 'bigdata' parameter), it switches to a convex hull representation.
    - If PCA object is provided, it takes precedence over manually provided scores and coefficients.
    """
    
    # If a PCA object is provided, use it to extract components and scores
    if isinstance(pca,PCA)==True :
        coeff = np.transpose(pca.components_[components, :])
        score=  pca.fit_transform(x)[:,components]
        if isinstance(x,pd.DataFrame)==True :
            coeff_labels = list(x.columns)

    # If score is provided, use it as the score data
    if score is not None : x = score
    
    # Extract x and y coordinates from input data
    if x.shape[1]>1 :
        xs = x[:,0]
        ys = x[:,1]
    else :
        xs = x
        ys = y
    
    # Check if x and y have the same length
    if (len(xs) != len(ys)) : print("Warning ! x et y n'ont pas la même taille !")
    
    # Calculate scaling factors for x and y
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    
    # Center and scale the data to range [-1, 1]
    temp = (xs - xs.min())
    x_c = temp / temp.max() * 2 - 1
    temp = (ys - ys.min())
    y_c = temp / temp.max() * 2 - 1
    
    # Create a DataFrame with centered data
    data = pd.DataFrame({"x_c":x_c,"y_c":y_c})
    #print("Attention : pour des facilités d'affichage, les données sont centrées-réduites")
    
    # Handle categories for coloring
    if cat is None : cat = [0]*len(xs)
    elif len(pd.Series(cat)) == 1 : cat = list(pd.Series(cat))*len(xs)
    elif len(pd.Series(cat)) != len(xs) : print("Warning ! Nombre anormal de catégories !")
    cat = pd.Series(cat).astype("category")
    
    # Create the plot
    fig = plt.figure(figsize=(6,6),facecolor='w') 
    ax = fig.add_subplot(111)
    
    # Display points if data size is less than bigdata threshold
    if (len(xs) < bigdata) :   
        ax.scatter(x_c,y_c, c = cat.cat.codes,cmap=cmap)
        if density==True : print("Warning ! Le mode density actif n'apparait que si BigData est paramétré.")
    # Display convex hulls for big data
    else :
        # Set up color mapping
        norm = mpl.colors.Normalize(vmin=0, vmax=(len(np.unique(cat.cat.codes))))
        cmap = cmap
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        
        # Plot density if enabled
        if density==True :
            sns.set_style("white")
            sns.kdeplot(x="x_c",y="y_c",data=data)
            if len(np.unique(cat)) <= 1 :
                sns.kdeplot(x="x_c", y="y_c", data=data, cmap="Blues", fill=True, thresh=0)
            else :
                for i in np.unique(cat) :
                    color_temp = m.to_rgba(i)
                    sns.kdeplot(x="x_c",y="y_c",data=data[cat==i], color=color_temp,
                                shade=True, thresh=0.25, alpha=0.25)     
        
        # Plot convex hulls for each category
        for cat_temp in cat.cat.codes.unique() :
            x_c_temp = [x_c[i] for i in range(len(x_c)) if (cat.cat.codes[i] == cat_temp)]
            y_c_temp = [y_c[i] for i in range(len(y_c)) if (cat.cat.codes[i] == cat_temp)]
            points = [ [ None ] * len(x_c_temp) ] * 2
            points = np.array(points)
            points = points.reshape(len(x_c_temp),2)
            points[:,0] = x_c_temp
            points[:,1] = y_c_temp
            hull = ConvexHull(points)
            temp = 0
            for simplex in hull.simplices:
                color_temp = m.to_rgba(cat_temp)
                plt.plot(points[simplex, 0], points[simplex, 1],color=color_temp)
                if (temp == 0) :
                    plt.xlim(-1,1)
                    plt.ylim(-1,1)
                    temp = temp+1
    
    # Plot coefficients (loadings) if provided
    if coeff is not None :
        # Draw unit circle if requested
        if (circle == 'T') :
            x_circle = np.linspace(-1, 1, 100)
            y_circle = np.linspace(-1, 1, 100)
            X, Y = np.meshgrid(x_circle,y_circle)
            F = X**2 + Y**2 - 1.0
            plt.contour(X,Y,F,[0])
        
        # Plot arrows and labels for each coefficient
        n = coeff.shape[0]
        for i in range(n):
            plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5,
                      head_width=0.05, head_length=0.05)
            if coeff_labels is None:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
            else:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, coeff_labels[i], color = 'g', ha = 'center', va = 'center')
        
        # Add score labels if provided
        if score_labels is not None :
            for i in range(len(score_labels)) :
                temp_x = xs[i] * scalex
                temp_y = ys[i] * scaley
                plt.text(temp_x,temp_y,list(score_labels)[i])
    
    # Set plot properties
    plt.axis('scaled')
    plt.xlim(-1.2,1.2)
    plt.ylim(-1.2,1.2)
    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid(linestyle='--')
    plt.title(title)
    
    # Save the figure
    plt.savefig(save_path,bbox_inches='tight')
    plt.clf()
    
    # Show the plot if requested
    if show_graph: plt.show()