import matplotlib.pyplot as plt
import pandas as pd
from prince import PCA
import matplotlib.pyplot as pyplot

class AprendizajePCA:
    def __init__(self, datos, n_componentes = 5):
        self.__datos = datos
        self.__modelo = PCA(n_components = n_componentes).fit(self.__datos)
        self.__correlacion_var = self.__modelo.column_correlations(datos)
        self.__coordenadas_ind = self.__modelo.row_coordinates(datos)
        self.__contribucion_ind = self.__modelo.row_contributions(datos)
        self.__cos2_ind = self.__modelo.row_cosine_similarities(datos)
        self.__var_explicada = [x * 100 for x in self.__modelo.explained_inertia_]
    @property
    def datos(self):
        return self.__datos
    @datos.setter
    def datos(self, datos):
        self.__datos = datos
    @property
    def modelo(self):
        return self.__modelo
    @property
    def correlacion_var(self):
        return self.__correlacion_var
    @property
    def coordenadas_ind(self):
        return self.__coordenadas_ind
    @property
    def contribucion_ind(self):
        return self.__contribucion_ind
    @property
    def cos2_ind(self):
        return self.__cos2_ind
    @property
    def var_explicada(self):
        return self.__var_explicada
        self.__var_explicada = var_explicada
    def plot_plano_principal(self, ejes = [0, 1], ind_labels = True, titulo = 'Temporadas de ventas de autos'):
        x = self.coordenadas_ind[ejes[0]].values
        y = self.coordenadas_ind[ejes[1]].values
        plt.style.use('seaborn-whitegrid')
        plt.scatter(x, y, color = 'yellow')
        plt.title(titulo)
        plt.axhline(y = 0, color = 'dimgrey', linestyle = '-')
        plt.axvline(x = 0, color = 'dimgrey', linestyle = '-')
        inercia_x = round(self.var_explicada[ejes[0]], 2)
        inercia_y = round(self.var_explicada[ejes[1]], 2)
        plt.xlabel('Eje X.' +'(' + str(ejes[0]) + ')'+' (' + str(inercia_x) + '%)')
        plt.ylabel('Eje Y.' +'(' + str(ejes[1]) + ')'+' (' + str(inercia_y) + '%)')
        if ind_labels:
            for i, txt in enumerate(self.coordenadas_ind.index):
                plt.annotate(txt, (x[i], y[i]))
    def plot_circulo(self, ejes = [0, 1], var_labels = True, titulo = 'Círculo de Correlación Marcas de vehiculos'):
        cor = self.correlacion_var.iloc[:, ejes].values
        plt.style.use('seaborn-whitegrid')
        c = plt.Circle((0, 0), radius = 1, color = 'gray', fill = False)
        plt.gca().add_patch(c)
        plt.axis('equal')
        plt.title(titulo)
        plt.axhline(y = 0, color = 'gray', linestyle = 'solid')
        plt.axvline(x = 0, color = 'gray', linestyle = '-')
        inercia_x = round(self.var_explicada[ejes[0]], 2)
        inercia_y = round(self.var_explicada[ejes[1]], 2)
        plt.xlabel('Eje X.' +'(' + str(ejes[0]) + ')'+' (' + str(inercia_x) + '%)')
        plt.ylabel('Eje Y.' +'(' + str(ejes[1]) + ')'+' (' + str(inercia_y) + '%)')
        for i in range(cor.shape[0]):
            plt.arrow(0, 0, cor[i, 0] * 0.95, cor[i, 1] * 0.95, color = 'grey',
                      alpha = 0.5, head_width = 0.05, head_length = 0.05)
            if var_labels:
                plt.text(cor[i, 0] * 1.05, cor[i, 1] * 1.05, self.correlacion_var.index[i],
                         color = 'green', ha = 'center', va = 'center')
    def plot_sobreposicion(self, ejes = [0, 1], ind_labels = True,
                      var_labels = True, titulo = 'Superposicion Ventas po temporada'):
        x = self.coordenadas_ind[ejes[0]].values
        y = self.coordenadas_ind[ejes[1]].values
        cor = self.correlacion_var.iloc[:, ejes]
        scale = min((max(x) - min(x)/(max(cor[ejes[0]]) - min(cor[ejes[0]]))),
                    (max(y) - min(y)/(max(cor[ejes[1]]) - min(cor[ejes[1]])))) * 0.8
        cor = self.correlacion_var.iloc[:, ejes].values
        plt.style.use('seaborn-whitegrid')
        plt.axhline(y = 0, color = 'dimgrey', linestyle = '-')
        plt.axvline(x = 0, color = 'dimgrey', linestyle = '-')
        plt.title(titulo)

        inercia_x = round(self.var_explicada[ejes[0]], 2)
        inercia_y = round(self.var_explicada[ejes[1]], 2)
        plt.xlabel('Eje X.' +'(' + str(ejes[0]) + ')'+' (' + str(inercia_x) + '%)')
        plt.ylabel('Eje Y.' +'(' + str(ejes[1]) + ')'+' (' + str(inercia_y) + '%)')
        plt.scatter(x, y, color = 'yellow')
        if ind_labels:
            for i, txt in enumerate(self.coordenadas_ind.index):
                plt.annotate(txt, (x[i], y[i]))
        for i in range(cor.shape[0]):
            plt.arrow(0, 0, cor[i, 0] * scale, cor[i, 1] * scale, color = 'gray',
                      alpha = 0.5, head_width = 0.05, head_length = 0.05)
            if var_labels:
                plt.text(cor[i, 0] * scale * 0.9, cor[i, 1] * scale * 0.9,
                         self.correlacion_var.index[i],
                         color = 'green', ha = 'center', va = 'top')


dato = pd.read_csv('Ventas.csv', delimiter = ';', decimal = ",",
                        header = 0, index_col = 0)
V=AprendizajePCA(dato)
V.plot_sobreposicion()

pyplot.savefig('GraficaGeneral.png')
pyplot.savefig('GraficaGeneral.png')
pyplot.savefig('Graficasuper.png')






