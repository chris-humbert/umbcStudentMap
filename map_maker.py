
# DO THIS NEXT
import mapSearch
import numpy as np; np.random.seed(42) #42
import pandas as pd
# from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def showMap():

    # Changes the location of points
    # df = pd.DataFrame({"lon1" : np.random.randint(-15,30,10),
    #                    "lat1" : np.random.randint(33,66,10),
    #                    "lon2" : np.random.randint(-15,30,10),
    #                    "lat2" : np.random.randint(33,66,10)})

    # https://matplotlib.org/basemap/stable/api/basemap_api.html#mpl_toolkits.basemap.Basemap

    # 39.250961890177166, -76.71811748114376 LLC
    # 39.25980046061478, -76.70451444706288 URC
    # 39.25555078560786, -76.71131596401352 Center

    # 39.21434889767328, -76.65212723183939 LLC TEST
    # 39.41895772879715, -76.39741595859792 URC TEST


    img = plt.imread("umbc_map_small.jpg")
    fig, ax = plt.subplots()
    # UMBC
    # ax = Basemap(llcrnrlon=39.250961890177166,llcrnrlat=-76.71811748114376,urcrnrlon=39.25980046061478,urcrnrlat=-76.70451444706288,
    #               resolution='i', projection='tmerc', lat_0 = -76.71131596401352, lon_0 = 39.25555078560786) #tmerc


    #                 use cyl to make map on coords
    # 'tmerc', lat_0 = -76.71131596401352, lon_0 = 39.25555078560786


    # https://stackoverflow.com/questions/54488720/how-to-plot-lines-between-multiple-x-y-points-in-matplotlib-basemap
    # https: // stackoverflow.com / questions / 34458251 / plot - over - an - image - background - in -python
    # https://matplotlib.org/basemap/stable/api/basemap_api.html#mpl_toolkits.basemap.Basemap
    # arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=400, ypixels=None, dpi=96, cachedir=None, verbose=False, **kwargs)
    # m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=400, ypixels=400)

    # ax.drawmapboundary(color='k',linewidth=1.0, fill_color="red",zorder=None,ax = None)

    # Need to make smaller
    # img = plt.imread("umbc_map.jpg")
    # fig, ax = plt.subplots()

    x = range(300)
    # adjusts the zoom
    ax.imshow(img, extent=[0,1524,0,1516])
    # Might need to manually add plot points for all graphs or find a way to automatically add points using long and lat
    ax.plot(x,x,'--',linewidth=5,color='firebrick')
    ax.plot(450, 500, 'bo',markersize=1)
    ax.plot(410, 215, 'bo',markersize=1)
    

    ax.plot
    # possibly convert coords to points by getting long and lat and converting to x and y for the coordinate plane
    # ax.imshow(img)
    '''
    m = Basemap(llcrnrlon=-12,llcrnrlat=30,urcrnrlon=50,urcrnrlat=69.,
                 resolution='h', projection='tmerc', lat_0 = 48.9, lon_0 = 15.3)
    
    m.drawcoastlines(linewidth=0.72, color='gray')
    m.drawcountries(zorder=0, color='gray')
    '''

    # lon1, lat1 = m(df.lon1.values, df.lat1.values)
    # lon2, lat2 = m(df.lon2.values, df.lat2.values)

    # pts = np.c_[lon1, lat1, lon2, lat2].reshape(len(lon1), 2, 2)
    # plt.gca().add_collection(LineCollection(pts, color="crimson", label="Lines"))

    # m.plot(lon1, lat1, marker="o", ls="", label="Start")
    # m.plot(lon2, lat2, marker="o", ls="", label="Fin")

    # plt.legend()
    plt.show()